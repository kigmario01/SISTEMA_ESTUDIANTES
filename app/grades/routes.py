from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import grades_bp
from ..models import db, Enrollment, Student, Course, Teacher


def require_role(*roles):
    return current_user.is_authenticated and current_user.role in roles


@grades_bp.route("/")
@login_required
def list_grades():
    course_id = request.args.get("course_id")
    teacher_id = request.args.get("teacher_id")
    query = Enrollment.query
    if course_id:
        query = query.filter(Enrollment.course_id == int(course_id))
    if teacher_id:
        query = query.filter(Enrollment.teacher_id == int(teacher_id))
    enrollments = query.all()
    courses = Course.query.order_by(Course.name).all()
    teachers = Teacher.query.order_by(Teacher.name).all()
    return render_template(
        "grades/list.html",
        enrollments=enrollments,
        courses=courses,
        teachers=teachers,
        selected_course_id=course_id,
        selected_teacher_id=teacher_id,
    )


@grades_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_grade():
    if not require_role("admin", "docente"):
        flash("Acceso restringido a administradores y docentes", "error")
        return redirect(url_for("grades.list_grades"))
    students = Student.query.order_by(Student.name).all()
    courses = Course.query.order_by(Course.name).all()
    teachers = Teacher.query.order_by(Teacher.name).all()
    if request.method == "POST":
        student_id = int(request.form.get("student_id"))
        course_id = int(request.form.get("course_id"))
        teacher_id = int(request.form.get("teacher_id"))
        grade = request.form.get("grade")
        grade_val = float(grade) if grade else None
        e = Enrollment(student_id=student_id, course_id=course_id, teacher_id=teacher_id, grade=grade_val)
        db.session.add(e)
        db.session.commit()
        return redirect(url_for("grades.list_grades"))
    return render_template("grades/form.html", students=students, courses=courses, teachers=teachers, action="create")


@grades_bp.route("/<int:enrollment_id>/edit", methods=["GET", "POST"])
@login_required
def edit_grade(enrollment_id):
    if not require_role("admin", "docente"):
        flash("Acceso restringido a administradores y docentes", "error")
        return redirect(url_for("grades.list_grades"))
    e = Enrollment.query.get_or_404(enrollment_id)
    students = Student.query.order_by(Student.name).all()
    courses = Course.query.order_by(Course.name).all()
    teachers = Teacher.query.order_by(Teacher.name).all()
    if request.method == "POST":
        e.student_id = int(request.form.get("student_id"))
        e.course_id = int(request.form.get("course_id"))
        e.teacher_id = int(request.form.get("teacher_id"))
        grade = request.form.get("grade")
        e.grade = float(grade) if grade else None
        db.session.commit()
        return redirect(url_for("grades.list_grades"))
    return render_template("grades/form.html", enrollment=e, students=students, courses=courses, teachers=teachers, action="edit")


@grades_bp.route("/<int:enrollment_id>/delete", methods=["POST"])
@login_required
def delete_grade(enrollment_id):
    if not require_role("admin", "docente"):
        flash("Acceso restringido a administradores y docentes", "error")
        return redirect(url_for("grades.list_grades"))
    e = Enrollment.query.get_or_404(enrollment_id)
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for("grades.list_grades"))