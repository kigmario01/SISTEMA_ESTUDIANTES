from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func, or_

from . import courses_bp
from ..models import db, Course


def require_role(*roles):
    return current_user.is_authenticated and current_user.role in roles


@courses_bp.route("/")
@login_required
def list_courses():
    q = request.args.get("q", "")
    query = Course.query
    if q:
        term = f"%{q}%"
        query = query.filter(or_(Course.name.ilike(term), Course.description.ilike(term)))
    courses = query.order_by(Course.name).all()
    return render_template("courses/list.html", courses=courses, q=q)


@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_course():
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("courses.list_courses"))
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()

        if not name:
            flash("El nombre del curso es obligatorio", "error")
            course = Course(name=name, description=description)
            return render_template("courses/form.html", action="create", course=course)

        if Course.query.filter(func.lower(Course.name) == name.lower()).first():
            flash("Ya existe un curso con ese nombre", "error")
            course = Course(name=name, description=description)
            return render_template("courses/form.html", action="create", course=course)

        c = Course(name=name, description=description or None)
        db.session.add(c)
        db.session.commit()
        flash("Curso creado correctamente", "success")
        return redirect(url_for("courses.list_courses"))
    return render_template("courses/form.html", action="create", course=None)


@courses_bp.route("/<int:course_id>/edit", methods=["GET", "POST"])
@login_required
def edit_course(course_id):
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("courses.list_courses"))
    c = Course.query.get_or_404(course_id)
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()

        if not name:
            flash("El nombre del curso es obligatorio", "error")
            return render_template("courses/form.html", action="edit", course=c)

        existing = Course.query.filter(func.lower(Course.name) == name.lower(), Course.id != c.id).first()
        if existing:
            flash("Ya existe otro curso con ese nombre", "error")
            return render_template("courses/form.html", action="edit", course=c)

        c.name = name
        c.description = description or None
        db.session.commit()
        flash("Curso actualizado", "success")
        return redirect(url_for("courses.list_courses"))
    return render_template("courses/form.html", action="edit", course=c)


@courses_bp.route("/<int:course_id>/delete", methods=["POST"])
@login_required
def delete_course(course_id):
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("courses.list_courses"))
    c = Course.query.get_or_404(course_id)
    db.session.delete(c)
    db.session.commit()
    flash("Curso eliminado", "success")
    return redirect(url_for("courses.list_courses"))