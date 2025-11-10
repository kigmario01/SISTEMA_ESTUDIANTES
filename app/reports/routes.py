from flask import render_template, request
from flask_login import login_required
from . import reports_bp
from ..models import Enrollment, Course, Teacher, Student
from sqlalchemy import func


@reports_bp.route("/")
@login_required
def reports_home():
    # Reporte: promedio por curso (opcionalmente filtrado por docente)
    teacher_id = request.args.get("teacher_id")
    q = Enrollment.query
    if teacher_id:
        q = q.filter(Enrollment.teacher_id == int(teacher_id))
    # Calcula promedio por curso
    data = (
        q.with_entities(
            Enrollment.course_id,
            func.avg(Enrollment.grade)
        )
        .group_by(Enrollment.course_id)
        .all()
    )
    courses = {c.id: c for c in Course.query.all()}
    teachers = Teacher.query.order_by(Teacher.name).all()
    summarized = [
        {
            "course": courses.get(course_id).name if courses.get(course_id) else "",
            "avg": round(avg, 2) if avg is not None else None,
        }
        for course_id, avg in data
    ]
    return render_template("reports/index.html", summarized=summarized, teachers=teachers, selected_teacher_id=teacher_id)