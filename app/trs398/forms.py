from datetime import datetime
from flask_wtf import FlaskForm
from  wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, FloatField
from wtforms import validators
from app.linac.models import Machine
from app.ionization_chambers.models import Ionization_chambers, Chamber_calfactor
from app.linac.models import Photon_energy, Electron_energy
import wtforms
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user


class TRS398_photonsForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    temp = FloatField('Temperature 0C', validators=[DataRequired()])
    press = FloatField('Pressure (hPa)', validators=[DataRequired()])
    m_list = Machine.query.filter_by(hospital_id = current_user.institution_id).all()
    machine = SelectField('Machine', choices = m_list)
    beam = SelectField('Beam Type', choices=['Photon Beam', 'Electron Beam'])
    if beam == 'Photon Beam':
        energies =  Photon_energy.query.filter_by(machine_id = machine.id ).all()
    else:
        energies = Electron_energy.query.filter_by(machine_id = machine.id).all()
    energy_sel = SelectField('Energy', choices= energies)
    chamberss = Ionization_chambers.query.filter_by(institution_id = current_user.institution_id).all()
    ion_chember = SelectField('Ionization Chambers', choices = chamberss)
    pdd10_def = SelectField('PDD10', choices=['Use Measured Data', 'Use Commissioning Data'])
    tpr2010 = SelectField('Beam Quality (TPR20,10)', choices=['Use Measured Data', 'Use Commisioning Data'])
    


