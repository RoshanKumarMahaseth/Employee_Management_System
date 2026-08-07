from datetime import date
from apps import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    email = db.Column(db.String(120),nullable=False,unique=True)
    password = db.Column(db.String(60),nullable=False)
    role = db.Column(db.String(20),nullable=False,default='employee')

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Employee(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    phone = db.Column(db.String(15),unique=True,nullable=False)
    position = db.Column(db.String(50),nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    joining_date = db.Column(db.Date,nullable=False,default=date.today)
    status = db.Column(db.String(20),nullable=False,default='Active')

    def __repr__(self):
        return f"Employee('{self.first_name}','{self.last_name}')"