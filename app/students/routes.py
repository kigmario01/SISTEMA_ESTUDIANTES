from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import students_bp
from ..models import db, Student


def require_role(*roles):
    return current_user.is_authenticated and current_user.role in roles


@students_bp.route("/")
@login_required
def list_students():
    q = request.args.get("q", "")
    query = Student.query
    if q:
        query = query.filter(Student.name.ilike(f"%{q}%"))
    students = query.order_by(Student.name).all()
    return render_template("students/list.html", students=students, q=q)


@students_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_student():
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("students.list_students"))
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        if not name or not email:
            flash("Nombre y email son obligatorios", "error")
        else:
            s = Student(name=name, email=email)
            db.session.add(s)
            db.session.commit()
            return redirect(url_for("students.list_students"))
    return render_template("students/form.html", action="create")


@students_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("students.list_students"))
    s = Student.query.get_or_404(student_id)
    if request.method == "POST":
        s.name = request.form.get("name")
        s.email = request.form.get("email")
        db.session.commit()
        return redirect(url_for("students.list_students"))
    return render_template("students/form.html", action="edit", student=s)


@students_bp.route("/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_student(student_id):
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("students.list_students"))
    s = Student.query.get_or_404(student_id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("students.list_students"))