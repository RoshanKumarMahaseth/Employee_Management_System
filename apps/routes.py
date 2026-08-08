from flask import render_template,redirect,url_for,request,flash
from apps import app,db,bcrypt
from apps.forms import RegisterForm,LoginForm,EmployeeForm
from apps.models import User,Employee
from flask_login import login_user,current_user,logout_user,login_required




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
    return render_template('dashboard.html',title='Dashboard')


@app.route('/employee',methods=['GET','POST'])
@login_required
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
            joining_date=form.joining_date.data
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee has been added successfully!','success')
        return redirect(url_for('dashboard'))
    return render_template('add_employee.html',title='Employee',form=form)

@app.route('/employees')
@login_required
def employees():
    employees = Employee.query.all()
    return render_template('employees.html',title='Employees',employees=employees)

