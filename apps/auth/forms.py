from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
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


class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email,You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired(),Length(min=4)])
    confirm_password = PasswordField('Confirm_password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')
