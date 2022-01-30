from email import message
from flask_wtf import FlaskForm
from  wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, FloatField
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
#from flask_login import current_user
#from app.hospitals.models import Institution


#this ios the form that will be used to add the machines.
#This, if I was just writing a code that I will use in my hospital I would have have added the machines on the terminal because we only have three machines.

class AddMachineForm(FlaskForm):
    make = StringField('Make and Model', validators=[DataRequired()])
    n_name = StringField('Machine Name  e.g. L 1', validators=[DataRequired()])
    com_date = DateField('Date Commissioned', validators=[DataRequired()])  
    submit = SubmitField('Add Machine')
    
    
    
    
class AddBeamsPhotons(FlaskForm):
    energy = StringField('Energy', validators=[DataRequired()])
    com_pdd10 = FloatField('Commissioning Data (PDD10)')
    com_tpr = FloatField('Commissioning Data (TPR20,10)')
    submit = SubmitField('Add Photon Beam')
    
    def validate_data(self, com_pdd10):    
        if isinstance(com_pdd10, float):
            if com_pdd10 > 1:
                raise ValidationError(message='This field is used in calculations and only accept values less then 1 (This is the ratio of measurements at referent depth and depth maximum)')
        
        elif not isinstance(com_pdd10, float):
            raise ValidationError(message='This field is used in calculations and only takes numbers, Pleas enter the ratio of measurements at referent depth and depth maximum.')
    
    
    
    
class AddBeamsElectrons(FlaskForm):
    energy = StringField('Energy', validators=[DataRequired()])
    comp_r50ion = FloatField('Commissioning Data (R50ion)',validators=[DataRequired()])
    com_r80ion = FloatField('Commissioning Data (R80ion)',validators=[DataRequired()])
    mean_energy = FloatField('Commissioning Data (Mean Energy)', validators=[DataRequired()])
    submit = SubmitField('Add Electron Beam')
    
