from itsdangerous import URLSafeSerializer as Serializer
from datetime import date
from apps import db,login_manager
from flask_login import UserMixin,current_user
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    email = db.Column(db.String(120),nullable=False,unique=True)
    password = db.Column(db.String(60),nullable=False)
    role = db.Column(db.String(20),nullable=False,default='employee')

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token,max_age=1800)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

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