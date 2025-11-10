from flask import Blueprint

grades_bp = Blueprint("grades", __name__, url_prefix="/grades")

from . import routes  # noqa