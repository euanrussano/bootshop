from functools import wraps
from flask import (_request_ctx_stack, current_app, request, session, url_for,
                   has_request_context, redirect)
from flask_login import current_user, login_required

def staff_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_staff:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function