from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user, login_required
from apps import db
from apps.models import ActivityLog

def log_activity(action):
    activity = ActivityLog(
        action=action,
        user_id=current_user.id
    )

    db.session.add(activity)
    db.session.commit()



# admin checker

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args,**kwargs):
        if current_user.role != 'admin':
            flash('You do not have permission to access this page.','danger')
            return redirect(url_for('main.dashboard'))
        return f(*args,**kwargs)
    return decorated_function