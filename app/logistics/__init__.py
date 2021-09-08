from flask import Blueprint

bp = Blueprint('logistics', __name__)

from app.logistics import models