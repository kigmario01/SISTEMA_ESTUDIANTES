from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import users_bp
from ..models import db, User, UserProfile


def require_role(*roles):
    return current_user.is_authenticated and current_user.role in roles


@users_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user
    profile = UserProfile.query.filter_by(user_id=user.id).first()
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        # email único si se establece
        if email:
            existing = UserProfile.query.filter(UserProfile.email == email, UserProfile.user_id != user.id).first()
            if existing:
                flash("Email ya registrado por otro usuario", "error")
                return render_template("users/profile.html", profile=profile)
        if not profile:
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)
        profile.full_name = full_name or None
        profile.email = email or None
        profile.phone = phone or None
        db.session.commit()
        flash("Perfil actualizado", "success")
        return redirect(url_for("users.profile"))
    return render_template("users/profile.html", profile=profile)


@users_bp.route("/manage")
@login_required
def manage_users():
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("index"))
    q = request.args.get("q", "")
    query = User.query
    if q:
        query = query.filter(User.username.ilike(f"%{q}%"))
    users = query.order_by(User.username).all()
    # map profiles
    profiles = {p.user_id: p for p in UserProfile.query.filter(UserProfile.user_id.in_([u.id for u in users])).all()}
    return render_template("users/list.html", users=users, profiles=profiles, q=q)


@users_bp.route("/<int:user_id>/role", methods=["GET", "POST"])
@login_required
def edit_role(user_id):
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("users.manage_users"))
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        role = request.form.get("role")
        if role not in ["admin", "docente", "estudiante"]:
            flash("Rol inválido", "error")
        else:
            user.role = role
            db.session.commit()
            flash("Rol actualizado", "success")
            return redirect(url_for("users.manage_users"))
    return render_template("users/role_form.html", user=user)