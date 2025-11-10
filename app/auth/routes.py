from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from ..models import db, User, UserProfile, PasswordReset
import secrets


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Credenciales inválidas", "error")
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "estudiante")
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()

        errors = []
        if not username:
            errors.append("Usuario es obligatorio")
        if not password or len(password) < 6:
            errors.append("Contraseña mínima de 6 caracteres")
        if role not in ["admin", "docente", "estudiante"]:
            errors.append("Rol inválido")
        if User.query.filter_by(username=username).first():
            errors.append("Usuario ya existe")
        if email and UserProfile.query.filter_by(email=email).first():
            errors.append("Email ya registrado")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("register.html")

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        profile = UserProfile(user_id=user.id, full_name=full_name or None, email=email or None)
        db.session.add(profile)
        db.session.commit()
        flash("Registro exitoso. Inicia sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Usuario no encontrado", "error")
            return render_template("forgot.html")
        token = secrets.token_urlsafe(32)
        PasswordReset.create_for_user(user, token, minutes_valid=30)
        reset_link = url_for("auth.reset", token=token, _external=True)
        flash(f"Enlace de restablecimiento: {reset_link}", "success")
        return redirect(url_for("auth.login"))
    return render_template("forgot.html")


@auth_bp.route("/reset/<token>", methods=["GET", "POST"])
def reset(token):
    pr = PasswordReset.query.filter_by(token=token).first()
    if not pr or pr.used:
        flash("Token inválido", "error")
        return redirect(url_for("auth.forgot"))
    from datetime import datetime
    if pr.expires_at < datetime.utcnow():
        flash("Token expirado", "error")
        return redirect(url_for("auth.forgot"))
    if request.method == "POST":
        password = request.form.get("password", "").strip()
        if not password or len(password) < 6:
            flash("Contraseña mínima de 6 caracteres", "error")
            return render_template("reset.html")
        user = pr.user
        user.set_password(password)
        pr.used = True
        db.session.commit()
        flash("Contraseña actualizada. Inicia sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("reset.html")