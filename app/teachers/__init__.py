from flask import Blueprint

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")

from . import routes  # noqa