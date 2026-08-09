from flask import render_template,redirect,url_for,request,flash
from apps import app,db,bcrypt
from apps.forms import RegisterForm,LoginForm,EmployeeForm,RequestResetForm,ResetPasswordForm
from apps.models import User,Employee,ActivityLog
from flask_login import login_user,current_user,logout_user,login_required
from functools import wraps
from flask_mail import Message

# admin checker

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args,**kwargs):
        if current_user.role != 'admin':
            flash('You do not have permission to access this page.','danger')
            return redirect(url_for('dashboard'))
        return f(*args,**kwargs)
    return decorated_function



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully! You can now log in','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.','danger')
    return render_template('login.html',title='Login',form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    total_employees = Employee.query.all()
    active_employees = Employee.query.filter_by(status='Active').count()
    total_users = User.query.count()
    return render_template('dashboard.html',title='Dashboard',total_employees=total_employees,active_employees=active_employees,total_users=total_users)



def log_activity(action):
    activity = ActivityLog(
        action=action,
        user_id=current_user.id
    )
    db.session.add(activity)
    db.session.commit()



@app.route('/employee',methods=['GET','POST'])
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
        return redirect(url_for('dashboard'))
    return render_template('add_employee.html',title='Employee',form=form)

@app.route('/employees')
@login_required
def employees():

    search = request.args.get('search', '')

    if search:
        employees = Employee.query.filter(
            db.or_(
                Employee.first_name.ilike(f'%{search}%'),
                Employee.last_name.ilike(f'%{search}%'),
                Employee.email.ilike(f'%{search}%'),
                Employee.position.ilike(f'%{search}%')
            )
        ).all()
    else:
        employees = Employee.query.all()

    return render_template(
        'employees.html',
        title='Employees',
        employees=employees,
        search=search
    )


@app.route('/employee/<int:employee_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_employee(employee_id):

    employee = db.session.get(Employee, employee_id)

    if employee is None:
        flash('Employee not found.', 'danger')
        return redirect(url_for('employees'))

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

        return redirect(url_for('employees'))

    return render_template('edit_employee.html',title='Edit Employee',form=form)


@app.route('/employee/<int:employee_id>/delete',methods=['GET','POST'])
@admin_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    db.session.delete(employee)
    db.session.commit()
    flash('Employee has been deleted successfully!','success')
    return redirect(url_for('employees'))

@app.route('/users')
@admin_required
def users():
    users = User.query.all()
    return render_template('users.html',title='Users',users=users)



@app.route('/user/<int:user_id>/role', methods=['POST'])
@admin_required
def change_role(user_id):

    user = User.query.get_or_404(user_id)

    if user.role == 'admin':

        admin_count = User.query.filter_by(role='admin').count()

        if admin_count == 1:
            flash('You cannot remove the last admin.', 'danger')
            return redirect(url_for('users'))

        user.role = 'employee'

    else:
        user.role = 'admin'

    db.session.commit()

    flash('User role has been updated successfully!', 'success')

    return redirect(url_for('users'))

def send_reset_email(user):
    token = user.get_reset_token()

    reset_link = url_for(
        'reset_token',
        token=token,
        _external=True
    )

    print("\n====================================")
    print("PASSWORD RESET LINK:")
    print(reset_link)
    print("====================================\n")


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        send_reset_email(user)

        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title='Reset Password',form=form )


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user.password = hashed_password
        db.session.commit()

        flash('Your password has been updated! You are now able to log in.','success')
        return redirect(url_for('login'))

    return render_template('reset_token.html',title='Reset Password',form=form)


@app.route('/employee/<int:employee_id>')
@login_required
def employee_details(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    return render_template('employee_details.html',title='Employee Details',employee=employee)

