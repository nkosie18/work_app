from datetime import datetime
from flask_wtf import FlaskForm
from  wtforms import StringField, SelectField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired, ValidationError

#long trs-398. This does not use any previouse data. all the data used in the calculations are measured data

class TRS398_photonsForm(FlaskForm):
    date = DateField('Date', default = datetime.now().date())
    chamber = SelectField('Ionization Chamber', choices=['PTW 30013-0391','PTW 30013-0390', 'PTW 30013-011795', 'PTW 30013-011794'])
    electrometer = SelectField('Electrometer', choices=['Unidose-11126', 'BEAM-SCAN','OTHER'])
    bias_voltage1 = SelectField('Voltage(V1)', choices=[-400, -300, -200, -150, -100, 0, +400, +300, +200, +150, +100])
    m11_reading = FloatField('M1 (nC)', validators=[DataRequired()])
    m12_reading = FloatField('M2 (nC)', validators=[DataRequired()])
    m13_reading = FloatField('M3 (nC)', validators=[DataRequired()])
    bias_voltage2 = SelectField('Reduced voltage(V2)', choices=[-200, -150, -100, +200, +150, +100])
    #change voltage for calculation of the recombination correction
    m21_reading = FloatField('M1 (nC)')
    m22_reading = FloatField('M2 (nC)')
    submit = SubmitField('Next Beam')


class TRS398_electronForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], default = datetime.now().date())
    chamber = SelectField('Ionization Chamber', choices=['PTW 30013-0391', 'PTW 30013-011795', 'PTW 30013-011794', 'PTW 30013-0390', 'Other'])
    electrometer = SelectField('Electrometer', choices=['Unidose-11126', 'BEAM-SCAN','OTHER'])
    bias_voltage1 = SelectField('V1', choices=[-400, -300, -200, -150, -100, 0, +400, +300, +200, +150, +100])
    m11_reading = FloatField('M1 (nC)', validators=[DataRequired()])
    m12_reading = FloatField('M2 (nC)', validators=[DataRequired()])
    m13_reading = FloatField('M3 (nC)', validators=[DataRequired()])
    bias_voltage2 = SelectField('V2', choices=[-200, -150, -100, +200, +150, +100])
    #change voltage for calculation of the recombination correction
    m21_reading = FloatField('M1 (nC)')
    m22_reading = FloatField('M2 (nC)')

    submit = SubmitField('Submit')

    '''
        def validate_r50(self, R50ion):
        if not R50ion is None:
            if not isinstance(R50ion, float):
                raise ValidationError(message='This field expact number')

    def validate_r80(self, R80ion):
        if not R80ion is None:
            if not isinstance(R80ion, float):
                raise ValidationError(message='This field expact number')
    '''
    def validate_chamber(self, chamber, other_name, other_calf):
        chamb_list = ['PTW 30013-0391', 'PTW 30013-011795', 'PTW 30013-011794', 'PTW 30013-0390']
        if not chamber in chamb_list:
            if not chamber == 'Other':
                raise ValidationError(message= 'Please select a chamber in the list provided. If your chamber is not in the list, please select other')

            elif chamber == 'Other':
                if not other_name or not other_calf:
                    raise ValidationError(message=' Please provide your chamber type and serial number in the field provided. This entry is used in the calculations.')
        






   








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


