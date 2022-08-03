from flask_wtf import FlaskForm
from  wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.hospitals.models import Institution
from app.signin.models import User 

class LoginForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

def hospital_list():
    hospital_list = []
    hospitals = Institution.query.all()
    for each in hospitals:
        hospital_list.append(each.inst_name)
    return hospital_list


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    hospitals = SelectField('Institution', choices= hospital_list())
    role = SelectField('Role', choices=['Admin', 'Physicist','Therapist', 'Guest'])
    status = SelectField('status', choices=['Active', 'Suspended'])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='The two passwords are not matching!!')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('User already exist, Please select a different username')