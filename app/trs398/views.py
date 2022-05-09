from flask import Blueprint, render_template, request
from app.trs398.models import Trs398_electrons, Trs398_photons
from app.ionization_chambers.models import Ionization_chambers, Chamber_calfactor
from app.trs398.forms import TRS398_photonsForm
from flask_login import current_user, login_required
from sqlalchemy import and_, asc
import numpy as np
from app.trs398.energyCorrections import Kq_photons

def k_recomb(volt_ratio, charge_ratio):
    voltage_ratio = [2, 2.5, 3, 3.5, 4, 5]
    k_recomb_table = {'a_0': [2.337, 1.474, 1.198, 1.080, 1.022, 0.975],
    'a_1': [-3.636, -1.587, -0.875, -0.542, -0.363, -0.188],
    'a_2': [2.299, 1.114, 0.677, 0.463, 0.341, 0.214]}
    a0_r = np.interp(volt_ratio, voltage_ratio, k_recomb_table['a_0'])
    a1_r = np.interp(volt_ratio,voltage_ratio, k_recomb_table['a_1'])
    a2_r = np.interp(volt_ratio, voltage_ratio, k_recomb_table['a_2'])
    k_rec = a0_r + a1_r*charge_ratio + a2_r*(charge_ratio**2)
    return k_rec

def k_poll(m1, m2):
    return((np.abs(m1) + np.abs(m2))/2*np.abs(m1))



trs_398_bp = Blueprint('trs_398', __name__, template_folder='templates', static_folder='static')
@trs_398_bp.route('/trs_398/photons', methods=['GET','POST'])
@login_required
def trs_398_photons():
    form = TRS398_photonsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            date_1 = form.date.data
            reading1 = form.m11_reading.data
            reading2 = form.m12_reading.data
            #check if the data has not already been added to the database, this will prevent duplication
            check_entry = Trs398_photons.query.filter(and_(Trs398_photons.date == date_1, Trs398_photons.m_reading21 == reading1, Trs398_photons.m_reading22 == reading2)).first()
            if check_entry is None:
                m_v1_avrg = (form.m11_reading.data + form.m12_reading.data + form.m13_reading.data)/3 #M1 reading
                m_v2_avrg = (form.m21_reading.data + form.m22_reading.data)/2   # Half voltage M2 corresponding to V2
                m_v_1_avrg = (form.m31_reading.data + form.m32_reading.data)/2  #reverse polarity -M1
                v_ratio = np.abs(form.bias_voltage1.data/form.bias_voltage2.data)   #V1/V2
                m_ratio = m_v1_avrg/m_v2_avrg                                       # M1/M2
                k_s = round(k_recomb(v_ratio, m_ratio),3)
                k_pol = round(k_poll(m_v1_avrg, m_v_1_avrg),3)

                if form.chamber[0:3] == 'PTW':
                    chamber_ndw = Chamber_calfactor.query.join(Ionization_chambers.query.filter_by(sn = form.chamber.split('-')[1])).order_by(asc(Chamber_calfactor.date_loaded)).first()


                




    
    return render_template('trs398.html', form=form)