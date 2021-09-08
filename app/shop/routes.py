from flask import render_template, request, redirect, url_for
from flask_login import current_user

from werkzeug.urls import url_parse
from datetime import datetime, timedelta

#from app import dummy_data

from app.shop import bp

@bp.route('/')
@bp.route('/index')
def index():
    return 'index'
