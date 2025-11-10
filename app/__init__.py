import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
from .config import Config
from .models import db, User
from werkzeug.security import generate_password_hash


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        # Crear admin por defecto si no existe
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", role="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

    # Blueprints
    from .auth.routes import auth_bp
    from .users.routes import users_bp
    from .students.routes import students_bp
    from .courses.routes import courses_bp
    from .teachers.routes import teachers_bp
    from .grades.routes import grades_bp
    from .reports.routes import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(grades_bp)
    app.register_blueprint(reports_bp)

    @app.route("/")
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        # Dashboard statistics
        from .models import Student, Course, Teacher, Enrollment
        
        stats = {
            'students_count': Student.query.count(),
            'courses_count': Course.query.count(),
            'teachers_count': Teacher.query.count(),
            'grades_count': Enrollment.query.count()
        }
        
        return render_template("index.html", **stats)

    return app