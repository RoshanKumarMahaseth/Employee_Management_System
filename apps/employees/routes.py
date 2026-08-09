from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from apps import db
from apps.models import Employee
from apps.utils.helpers import log_activity, admin_required
from .forms import EmployeeForm

employees = Blueprint('employees', __name__)


@employees.route('/employee',methods=['GET','POST'])
@admin_required
def employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            position=form.position.data,
            salary=form.salary.data,
            joining_date=form.joining_date.data,
            status=form.status.data
        )
        db.session.add(employee)
        db.session.commit()
        log_activity(f'Added employee: {employee.first_name} {employee.last_name}')
        flash('Employee has been added successfully!','success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_employee.html',title='Employee',form=form)

@employees.route('/employees')
@login_required
def employee_list():

    search = request.args.get('search', '').strip()

    if search:
        employee_records= Employee.query.filter(
            db.or_(
                Employee.first_name.ilike(f'%{search}%'),
                Employee.last_name.ilike(f'%{search}%'),
                Employee.email.ilike(f'%{search}%'),
                Employee.position.ilike(f'%{search}%')
            )
        ).all()
    else:
        employee_records = Employee.query.all()

    return render_template('employees.html',title='Employees',employees=employee_records,search=search)

@employees.route('/employee/<int:employee_id>')
@login_required
def employee_details(employee_id):

    employee = Employee.query.get_or_404(employee_id)

    return render_template(
        'employee_details.html',
        title='Employee Details',
        employee=employee
    )

@employees.route('/employee/<int:employee_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_employee(employee_id):

    employee = db.session.get(Employee, employee_id)

    if employee is None:
        flash('Employee not found.', 'danger')
        return redirect(url_for('employees.employee_list'))

    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():

        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.email = form.email.data
        employee.phone = form.phone.data
        employee.position = form.position.data
        employee.salary = form.salary.data
        employee.joining_date = form.joining_date.data
        employee.status = form.status.data

        db.session.commit()

        flash('Employee has been updated successfully!', 'success')

        return redirect(url_for('employees.employee_list'))

    return render_template('edit_employee.html',title='Edit Employee',form=form)


@employees.route('/employee/<int:employee_id>/delete',methods=['GET','POST'])
@admin_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee_name = f'{employee.first_name} {employee.last_name}'
    db.session.delete(employee)
    db.session.commit()
    log_activity( f'Deleted employee: {employee_name}')
    flash('Employee has been deleted successfully!','success')
    return redirect(url_for('employees.employee_list'))



