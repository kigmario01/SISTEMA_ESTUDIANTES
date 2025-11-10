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
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()

        if not name or not email:
            flash("Nombre y correo son obligatorios", "error")
            student = Student(name=name, email=email)
            return render_template("students/form.html", action="create", student=student)

        if Student.query.filter_by(email=email).first():
            flash("Ya existe un estudiante con ese correo", "error")
            student = Student(name=name, email=email)
            return render_template("students/form.html", action="create", student=student)

        s = Student(name=name, email=email)
        db.session.add(s)
        db.session.commit()
        flash("Estudiante creado correctamente", "success")
        return redirect(url_for("students.list_students"))

    return render_template("students/form.html", action="create", student=None)


@students_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    if not require_role("admin"):
        flash("Acceso restringido a administradores", "error")
        return redirect(url_for("students.list_students"))
    s = Student.query.get_or_404(student_id)
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()

        if not name or not email:
            flash("Nombre y correo son obligatorios", "error")
            return render_template("students/form.html", action="edit", student=s)

        existing = Student.query.filter(Student.email == email, Student.id != s.id).first()
        if existing:
            flash("Ya existe otro estudiante con ese correo", "error")
            return render_template("students/form.html", action="edit", student=s)

        s.name = name
        s.email = email
        db.session.commit()
        flash("Estudiante actualizado", "success")
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
    flash("Estudiante eliminado", "success")
    return redirect(url_for("students.list_students"))