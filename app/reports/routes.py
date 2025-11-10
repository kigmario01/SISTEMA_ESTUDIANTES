from datetime import datetime
from io import BytesIO

from flask import flash, redirect, render_template, request, send_file, url_for
from flask_login import login_required
from sqlalchemy import func

from . import reports_bp
from ..models import Course, Enrollment, Student, Teacher

try:
    from fpdf import FPDF
except ModuleNotFoundError:  # pragma: no cover - fallback in case dependency missing during runtime
    FPDF = None


def _filtered_enrollments(teacher_id):
    query = Enrollment.query
    if teacher_id:
        query = query.filter(Enrollment.teacher_id == teacher_id)
    return query


def _build_report_payload(teacher_id):
    teacher = Teacher.query.get(teacher_id) if teacher_id else None
    enrollments = _filtered_enrollments(teacher_id)

    graded = enrollments.filter(Enrollment.grade.isnot(None))

    overall_average = graded.with_entities(func.avg(Enrollment.grade)).scalar()

    course_stats = (
        enrollments.join(Course, Enrollment.course_id == Course.id)
        .with_entities(
            Course.id,
            Course.name,
            func.count(Enrollment.id).label("total"),
            func.avg(Enrollment.grade).label("average"),
            func.min(Enrollment.grade).label("minimum"),
            func.max(Enrollment.grade).label("maximum"),
        )
        .group_by(Course.id, Course.name)
        .order_by(Course.name)
        .all()
    )

    grades = [g[0] for g in graded.with_entities(Enrollment.grade).all()]
    distribution_buckets = [
        ("0-59", lambda value: value < 60),
        ("60-69", lambda value: 60 <= value < 70),
        ("70-79", lambda value: 70 <= value < 80),
        ("80-89", lambda value: 80 <= value < 90),
        ("90-100", lambda value: value >= 90),
    ]
    grade_distribution = [
        {
            "label": label,
            "count": sum(1 for grade in grades if condition(grade)),
        }
        for label, condition in distribution_buckets
    ]

    top_students = (
        graded.join(Student, Enrollment.student_id == Student.id)
        .with_entities(
            Student.id,
            Student.name,
            func.avg(Enrollment.grade).label("average"),
            func.count(Enrollment.course_id).label("courses"),
        )
        .group_by(Student.id, Student.name)
        .order_by(func.avg(Enrollment.grade).desc())
        .limit(5)
        .all()
    )

    report = {
        "teacher": teacher,
        "overall_average": round(overall_average, 2) if overall_average is not None else None,
        "total_records": enrollments.count(),
        "course_stats": [
            {
                "course_name": row.name,
                "count": row.total,
                "average": round(row.average, 2) if row.average is not None else None,
                "min": round(row.minimum, 2) if row.minimum is not None else None,
                "max": round(row.maximum, 2) if row.maximum is not None else None,
            }
            for row in course_stats
        ],
        "grade_distribution": grade_distribution,
        "top_students": [
            {
                "student_name": row.name,
                "average": round(row.average, 2) if row.average is not None else None,
                "courses": int(row.courses or 0),
            }
            for row in top_students
        ],
        "generated_at": datetime.utcnow(),
    }
    return report


def _render_pdf(report):
    if FPDF is None:
        raise RuntimeError("La librería fpdf2 no está instalada")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Reporte de calificaciones", ln=1, align="C")

    pdf.set_font("Helvetica", "", 11)
    generated_at = report["generated_at"].strftime("%d/%m/%Y %H:%M")
    pdf.cell(0, 8, f"Generado: {generated_at}", ln=1)
    if report["teacher"]:
        pdf.cell(0, 6, f"Docente: {report['teacher'].name}", ln=1)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Resumen general", ln=1)
    pdf.set_font("Helvetica", "", 11)
    overall = report["overall_average"]
    pdf.cell(0, 6, f"Promedio general: {overall if overall is not None else 'Sin datos'}", ln=1)
    pdf.cell(0, 6, f"Total de registros: {report['total_records']}", ln=1)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Promedio por curso", ln=1)
    pdf.set_font("Helvetica", "", 11)
    if report["course_stats"]:
        for row in report["course_stats"]:
            pdf.multi_cell(
                0,
                6,
                f"{row['course_name']}: promedio {row['average'] if row['average'] is not None else 'N/D'}"
                f" | registros {row['count']}"
                f" | mínimo {row['min'] if row['min'] is not None else 'N/D'}"
                f" | máximo {row['max'] if row['max'] is not None else 'N/D'}",
            )
            pdf.ln(1)
    else:
        pdf.cell(0, 6, "Sin datos disponibles", ln=1)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Distribución de notas", ln=1)
    pdf.set_font("Helvetica", "", 11)
    for bucket in report["grade_distribution"]:
        pdf.cell(0, 6, f"{bucket['label']}: {bucket['count']} registros", ln=1)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Mejores estudiantes", ln=1)
    pdf.set_font("Helvetica", "", 11)
    if report["top_students"]:
        for student in report["top_students"]:
            pdf.cell(
                0,
                6,
                f"{student['student_name']}: promedio {student['average'] if student['average'] is not None else 'N/D'}"
                f" en {student['courses']} cursos",
                ln=1,
            )
    else:
        pdf.cell(0, 6, "No hay notas registradas", ln=1)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output


@reports_bp.route("/")
@login_required
def reports_home():
    teacher_id = request.args.get("teacher_id", type=int)
    teachers = Teacher.query.order_by(Teacher.name).all()
    report = _build_report_payload(teacher_id)
    return render_template(
        "reports/index.html",
        report=report,
        teachers=teachers,
        selected_teacher_id=teacher_id,
    )


@reports_bp.route("/export")
@login_required
def export_report():
    teacher_id = request.args.get("teacher_id", type=int)
    report = _build_report_payload(teacher_id)
    if FPDF is None:
        flash(
            "No se pudo generar el PDF porque falta la dependencia fpdf2.",
            "error",
        )
        return redirect(url_for("reports.reports_home", teacher_id=teacher_id))

    pdf_stream = _render_pdf(report)
    teacher_slug = (
        report["teacher"].name.replace(" ", "_")
        if report["teacher"]
        else "general"
    )
    filename = f"reporte_calificaciones_{teacher_slug}.pdf"
    return send_file(
        pdf_stream,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf",
    )