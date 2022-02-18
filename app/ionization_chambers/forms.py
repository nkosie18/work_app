from datetime import datetime
from flask_wtf import FlaskForm
from  wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, FloatField
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user
from app.ionization_chambers.models import Ionization_chambers




class NewChamberForm(FlaskForm):
    date_add = DateField('Date', validators=[DataRequired()], default= datetime.today().date())
    make = StringField('Make and Model', validators=[DataRequired()])
    sn = StringField('Serial N0', validators=[DataRequired()])
    chamber_type = SelectField('Chamber Type', choices=['Reference (TRS-398)', 'Field (TRS-398)', 'Field (scanning)', 'Reference (scanning)'])
    submit = SubmitField('Register')

chambers = []
all_chambs = Ionization_chambers.query.all()
for each in all_chambs:
    name12 = '{}-{}'.format(each.make, each.sn)
    chambers.append(name12)

class CalibrationCertForm(FlaskForm):
    #remember to query the database for the chamber to be used.
    electrometer = StringField('Electrometer-S/N')
    electrometerCalFactor = FloatField('Electrometer Calibration Factor', validators=[DataRequired()], default = 1.0)
    calVoltage = StringField('Calibration Voltage', validators=[DataRequired()])
    calfactor = FloatField('Calibration Factor (Gy/nC)', validators=[DataRequired()])
    cal_date = DateField('Date Callibrated', validators=[DataRequired()])
    cal_lab = StringField('Calibration Lab', validators=[DataRequired()])
    beamQuality = SelectField('Beam Quality', choices=['Co-60', 'Sr-90', '6 MV', 'Other'])
    calMachine = SelectField('Calibration Unit', choices=['Standards Lab', 'Sr-90 check source', ' L1 (Internaly)', ' L2 (Internaly)', ' L3 (Internaly)'])
    chambers = SelectField('Chember', choices= chambers)
    submit = SubmitField('Capture')


class CheckSourceForm(FlaskForm):
    date = DateField('Measurement Date', validators=[DataRequired()])
    chamber = SelectField('Chamber', choices=['PTW-30013-0390','PTW-30013-0391', 'PTW-30013-011795','PTW-30013-011794' ])
    source = SelectField('Source Used', validators=[DataRequired()],choices=['Sr-90 48002-0762', 'Sr-90 8921-1732'])
    electrometer = StringField('Electrometer (make/model)', validators=[DataRequired()], default='UNIDOS 11126')
    elect_voltage = StringField('Applied Voltage', validators=[DataRequired()], default='+ 400V')
    temp_reading = FloatField('Temperature', validators=[DataRequired()])
    press_reading = FloatField('Pressure', validators=[DataRequired()])
    reading1 = FloatField('Reading 1', validators=[DataRequired()])
    reading2 = FloatField('Reading 2', validators=[DataRequired()])
    reading3 = FloatField('Reading 3', validators=[DataRequired()])
    submit = SubmitField('Accept and Capture') 

    




