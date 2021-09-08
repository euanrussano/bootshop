from flask import Blueprint

bp = Blueprint('offers', __name__)

from app.offers import models