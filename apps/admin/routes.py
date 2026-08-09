from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from apps.utils.helpers import admin_required
from apps import db
from apps.models import User

admin = Blueprint('admin',__name__)




@admin.route('/users')
@admin_required
def users():
    users = User.query.all()
    return render_template('users.html',title='Users',users=users)



@admin.route('/user/<int:user_id>/role', methods=['POST'])
@admin_required
def change_role(user_id):

    user = User.query.get_or_404(user_id)

    if user.role == 'admin':

        admin_count = User.query.filter_by(role='admin').count()

        if admin_count == 1:
            flash('You cannot remove the last admin.', 'danger')
            return redirect(url_for('admin.users'))

        user.role = 'employee'

    else:
        user.role = 'admin'

    db.session.commit()

    flash('User role has been updated successfully!', 'success')

    return redirect(url_for('admin.users'))
