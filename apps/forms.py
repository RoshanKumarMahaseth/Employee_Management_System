from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,ValidationError,IntegerField,DateField
from wtforms.validators import DataRequired,Email,Length,EqualTo
from apps.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=4)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    confirm_password = PasswordField('confirm_password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken. Please choose another.")

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is already registered.")

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EmployeeForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired(),Length(min=3,max=20)])
    last_name = StringField('Last Name',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    phone = StringField('Phone',validators=[DataRequired(),Length(min=10,max=15)])
    position = StringField('Position',validators=[DataRequired(),Length(min=2,max=50)])
    salary = IntegerField('Salary',validators=[DataRequired()])
    joining_date = DateField('Joining Date',validators=[DataRequired()])
    submit = SubmitField('Submit')

