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

#long trs-398. This does not use any previouse data. all the data used in the calculations are measured data

class TRS398_photonsForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], default = datetime.now().date())
    temp = FloatField('Temperature (<sup>0</sup>C)', validators=[DataRequired()])
    press = FloatField('Pressure (hPa)', validators=[DataRequired()])
    pdd10 = FloatField('PDD<sub>10</sub>', validators=[DataRequired()])
    tpr_2010 = FloatField('TPR<sub>20,10</sub>', validators=[DataRequired()])
    chamber = SelectField('Ionization Chamber', choices=['PTW 30013-0391', 'PTW 30013-011795', 'PTW 30013-011794', 'PTW 30013-0390'])
    electrometer = SelectField('Electrometer', choices=['Unidose-11126', 'BEAM-SCAN','OTHER'])
    electrometer_other = StringField('Electrometer (name and SN)')
    bias_voltage1 = SelectField('V1', choices=['-400V','-300V', '-200V', '-150', '-100V', '0V', '+400V','+300V', '+200V', '+150', '+100V'])
    m11_reading = FloatField('M<sub>1</sub> (nC)', validators=[DataRequired()])
    m12_reading = FloatField('M<sub>2</sub> (nC)', validators=[DataRequired()])
    m13_reading = FloatField('M<sub>3</sub> (nC)', validators=[DataRequired()])
    bias_voltage2 = SelectField('V2', choices=['-200V', '-150', '-100V','+200V', '+150', '+100V'])
    #change voltage for calculation of the recombination correction
    m21_reading = FloatField('M<sub>1</sub> (nC)')
    m22_reading = FloatField('M<sub>2</sub> (nC)')
    #reversed polarity for calculation of polarity correction
    m31_reading = FloatField('M<sub>1</sub> (nC)')
    m32_reading = FloatField('M<sub>1</sub> (nC)')
    submit = SelectField('Submit')



   








    '''
    m_list = Machine.query.filter_by(hospital_id = 1).all()
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
    submit = SubmitField('Submit')
''' 


