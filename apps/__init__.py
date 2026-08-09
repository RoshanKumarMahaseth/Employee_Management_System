import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message='Please log in to access this page.'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from apps.models import User 
from apps.auth import auth
from apps.employees import employees
from apps.admin import admin
from apps.main import main
app.register_blueprint(auth)
app.register_blueprint(employees)
app.register_blueprint(admin)
app.register_blueprint(main)