from flask import Blueprint, render_template
from flask_login import login_required
from apps import db
from apps.models import Employee, User

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html',title='About')



@main.route('/dashboard')
@login_required
def dashboard():
    total_employees = Employee.query.count()
    active_employees = Employee.query.filter_by(status='Active').count()
    total_users = User.query.count()
    return render_template('dashboard.html',title='Dashboard',total_employees=total_employees,active_employees=active_employees,total_users=total_users)

