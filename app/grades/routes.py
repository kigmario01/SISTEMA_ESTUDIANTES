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
        try:
            student_id = int(request.form.get("student_id"))
            course_id = int(request.form.get("course_id"))
            teacher_id = int(request.form.get("teacher_id"))
        except (TypeError, ValueError):
            flash("Los identificadores proporcionados no son válidos", "error")
            return render_template(
                "grades/form.html",
                students=students,
                courses=courses,
                teachers=teachers,
                action="create",
                enrollment=None,
            )

        grade = (request.form.get("grade") or "").strip()
        grade_val = None
        if grade:
            try:
                grade_val = float(grade)
            except ValueError:
                flash("La nota debe ser un número válido", "error")
                return render_template(
                    "grades/form.html",
                    students=students,
                    courses=courses,
                    teachers=teachers,
                    action="create",
                    enrollment=Enrollment(student_id=student_id, course_id=course_id, teacher_id=teacher_id, grade=None),
                )
            if grade_val < 0 or grade_val > 100:
                flash("La nota debe estar entre 0 y 100", "error")
                return render_template(
                    "grades/form.html",
                    students=students,
                    courses=courses,
                    teachers=teachers,
                    action="create",
                    enrollment=Enrollment(student_id=student_id, course_id=course_id, teacher_id=teacher_id, grade=grade_val),
                )

        existing = Enrollment.query.filter_by(
            student_id=student_id,
            course_id=course_id,
            teacher_id=teacher_id,
        ).first()
        if existing:
            flash("Ya existe una calificación registrada para este estudiante en el curso seleccionado", "error")
            return render_template(
                "grades/form.html",
                students=students,
                courses=courses,
                teachers=teachers,
                action="create",
                enrollment=Enrollment(
                    student_id=student_id,
                    course_id=course_id,
                    teacher_id=teacher_id,
                    grade=grade_val,
                ),
            )

        e = Enrollment(student_id=student_id, course_id=course_id, teacher_id=teacher_id, grade=grade_val)
        db.session.add(e)
        db.session.commit()
        flash("Calificación registrada", "success")
        return redirect(url_for("grades.list_grades"))
    return render_template("grades/form.html", students=students, courses=courses, teachers=teachers, action="create", enrollment=None)


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
        try:
            student_id = int(request.form.get("student_id"))
            course_id = int(request.form.get("course_id"))
            teacher_id = int(request.form.get("teacher_id"))
        except (TypeError, ValueError):
            flash("Los identificadores proporcionados no son válidos", "error")
            return render_template("grades/form.html", enrollment=e, students=students, courses=courses, teachers=teachers, action="edit")

        grade = (request.form.get("grade") or "").strip()
        grade_val = None
        if grade:
            try:
                grade_val = float(grade)
            except ValueError:
                flash("La nota debe ser un número válido", "error")
                return render_template("grades/form.html", enrollment=e, students=students, courses=courses, teachers=teachers, action="edit")
            if grade_val < 0 or grade_val > 100:
                flash("La nota debe estar entre 0 y 100", "error")
                return render_template("grades/form.html", enrollment=e, students=students, courses=courses, teachers=teachers, action="edit")

        existing = (
            Enrollment.query.filter_by(student_id=student_id, course_id=course_id, teacher_id=teacher_id)
            .filter(Enrollment.id != e.id)
            .first()
        )
        if existing:
            flash("Ya existe otra calificación para este estudiante en el curso seleccionado", "error")
            return render_template("grades/form.html", enrollment=e, students=students, courses=courses, teachers=teachers, action="edit")

        e.student_id = student_id
        e.course_id = course_id
        e.teacher_id = teacher_id
        e.grade = grade_val
        db.session.commit()
        flash("Calificación actualizada", "success")
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
    flash("Calificación eliminada", "success")
    return redirect(url_for("grades.list_grades"))