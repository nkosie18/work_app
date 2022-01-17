from datetime import datetime
from flask_wtf import FlaskForm
from  wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, FloatField
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user




class NewChamberForm(FlaskForm):
    date_add = DateField('Date', validators=[DataRequired()], default= datetime.today().date())
    make = StringField('Make and Model', validators=[DataRequired()])
    sn = StringField('Serial N0', validators=[DataRequired()])
    chamber_type = SelectField('Chamber Type', choices=['Reference (TRS-398)', 'Field (TRS-398)', 'Field (scanning)', 'Reference (scanning)'])
    submit = SubmitField('Register')


class CalibrationCertForm(FlaskForm):
    #remember to query the database for the chamber to be used.
    electrometer = StringField('Electrometer-S/N')
    electrometerCalFactor = FloatField('Electrometer Calibration Factor', validators=[DataRequired()])
    calVoltage = StringField('calibration Voltage', validators=[DataRequired()])
    calfactor = FloatField('Calibration Factor (Gy/nC)', validators=[DataRequired()])
    cal_date = DateField('Date Callibrated', validators=[DataRequired()])
    cal_lab = StringField('Calibration Lab', validators=[DataRequired()])
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

    




