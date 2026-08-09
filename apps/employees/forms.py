from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,DateField,SelectField
from wtforms.validators import DataRequired,Email,Length


class EmployeeForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired(),Length(min=3,max=20)])
    last_name = StringField('Last Name',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    phone = StringField('Phone',validators=[DataRequired(),Length(min=10,max=15)])
    position = StringField('Position',validators=[DataRequired(),Length(min=2,max=50)])
    salary = IntegerField('Salary',validators=[DataRequired()])
    joining_date = DateField('Joining Date',validators=[DataRequired()])
    status = SelectField('Status',choices=[('Active','Active'),('Inactive','Inactive')],validators=[DataRequired()])
    submit = SubmitField('Submit')
