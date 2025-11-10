from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import teachers_bp
from ..models import db, Teacher


def require_role(*roles):
    return current_user.is_authenticated and current_user.role in roles


@teachers_bp.route("/")
@login_required
def list_teachers():
    q = request.args.get("q", "")
    query = Teacher.query
    if q:
        query = query.filter(Teacher.name.ilike(f"%{q}%"))
    teachers = query.order_by(Teacher.name).all()
    return render_template("teachers/list.html", teachers=teachers, q=q)


@teachers_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_teacher():
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("teachers.list_teachers"))
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()

        if not name or not email:
            flash("Nombre y correo son obligatorios", "error")
            teacher = Teacher(name=name, email=email)
            return render_template("teachers/form.html", action="create", teacher=teacher)

        if Teacher.query.filter_by(email=email).first():
            flash("Ya existe un profesor con ese correo", "error")
            teacher = Teacher(name=name, email=email)
            return render_template("teachers/form.html", action="create", teacher=teacher)

        t = Teacher(name=name, email=email)
        db.session.add(t)
        db.session.commit()
        flash("Profesor creado correctamente", "success")
        return redirect(url_for("teachers.list_teachers"))
    return render_template("teachers/form.html", action="create", teacher=None)


@teachers_bp.route("/<int:teacher_id>/edit", methods=["GET", "POST"])
@login_required
def edit_teacher(teacher_id):
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("teachers.list_teachers"))
    t = Teacher.query.get_or_404(teacher_id)
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()

        if not name or not email:
            flash("Nombre y correo son obligatorios", "error")
            return render_template("teachers/form.html", action="edit", teacher=t)

        existing = Teacher.query.filter(Teacher.email == email, Teacher.id != t.id).first()
        if existing:
            flash("Ya existe otro profesor con ese correo", "error")
            return render_template("teachers/form.html", action="edit", teacher=t)

        t.name = name
        t.email = email
        db.session.commit()
        flash("Profesor actualizado", "success")
        return redirect(url_for("teachers.list_teachers"))
    return render_template("teachers/form.html", action="edit", teacher=t)


@teachers_bp.route("/<int:teacher_id>/delete", methods=["POST"])
@login_required
def delete_teacher(teacher_id):
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("teachers.list_teachers"))
    t = Teacher.query.get_or_404(teacher_id)
    db.session.delete(t)
    db.session.commit()
    flash("Profesor eliminado", "success")
    return redirect(url_for("teachers.list_teachers"))