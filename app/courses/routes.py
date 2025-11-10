from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
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
        query = query.filter(Course.name.ilike(f"%{q}%"))
    courses = query.order_by(Course.name).all()
    return render_template("courses/list.html", courses=courses, q=q)


@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_course():
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("courses.list_courses"))
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        if not name:
            flash("Nombre del curso es obligatorio", "error")
        else:
            c = Course(name=name, description=description)
            db.session.add(c)
            db.session.commit()
            return redirect(url_for("courses.list_courses"))
    return render_template("courses/form.html", action="create")


@courses_bp.route("/<int:course_id>/edit", methods=["GET", "POST"])
@login_required
def edit_course(course_id):
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("courses.list_courses"))
    c = Course.query.get_or_404(course_id)
    if request.method == "POST":
        c.name = request.form.get("name")
        c.description = request.form.get("description")
        db.session.commit()
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
    return redirect(url_for("courses.list_courses"))