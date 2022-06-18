from datetime import datetime
from flask import jsonify
from app import db
from flask import Blueprint, render_template, request
from app.linac.models import Machine, Photon_energy, Electron_energy
from app.trs398.models import Pdd_data_photons, Trs398_electrons, Trs398_photons
from app.ionization_chambers.models import Ionization_chambers, Chamber_calfactor, Temp_press
from app.trs398.forms import TRS398_photonsForm
from flask_login import current_user, login_required
from sqlalchemy import and_, asc, desc
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

def k_tp(temp, press):
    return((101.32/press) * ((273.2 + temp)/293.2))



trs_398_bp = Blueprint('trs_398', __name__, template_folder='templates', static_folder='static')

@trs_398_bp.route('/trs398/update_tp', methods=['POST'])
@login_required
def update_tp():
    temp = request.form['temp']
    press = round(float(request.form['press'].strip())/1.333224,2)  # convert to mmHg
    temp_press_obj = Temp_press(date_time= datetime.now() ,temp=temp, press=press)
    db.session.add(temp_press_obj)
    db.session.commit()
    return jsonify({'success': True})



@trs_398_bp.route('/trs_398/photons', methods=['GET','POST'])
@login_required
def trs_398_photons():
    form = TRS398_photonsForm()
    print(request.args.get('linac'))
    machine = Machine.query.filter_by(n_name = request.args.get('machine')).first()
    temp_press = Temp_press.query.order_by(desc(Temp_press.date_time)).first()
    chambers = Ionization_chambers.query.all()


    beam_energies = machine.photon_en.all()  #list of all the energies oblects
    beamEnergy_used_today = Photon_energy.query.join(Trs398_photons.query.filter(and_(Trs398_photons.date == datetime.now().date(), Trs398_photons.machine_id == machine.id)).subquery()).all()
    
    list_beams = []
    for each in beam_energies:
        if not each in beamEnergy_used_today:
            list_beams.append(each)

    if request.method == 'POST':
        if form.validate_on_submit():
            date_1 = form.date.data
            reading1 = form.m11_reading.data
            reading2 = form.m12_reading.data
            #check if the data has not already been added to the database, this will prevent duplication
            check_entry = Trs398_photons.query.filter(and_(Trs398_photons.date == date_1, Trs398_photons.m_reading21 == reading1, Trs398_photons.m_reading22 == reading2)).first()
            if check_entry is None:
                m1 = form.m11_reading.data 
                m2 = form.m12_reading.data 
                m3 = form.m13_reading.data
                m_v1_avrg = np.average([m1, m2, m3])
                m_v2_avrg = np.average([form.m21_reading.data, form.m22_reading.data])   # Half voltage M2 corresponding to V2
                m_v_1_avrg = np.average([form.m31_reading.data, form.m32_reading.data])  #reverse polarity -M1
                v_ratio = np.abs(form.bias_voltage1.data/form.bias_voltage2.data)   #V1/V2
                m_ratio = m_v1_avrg/m_v2_avrg                                       # M1/M2
                ktp = k_tp(form.temp.data, form.press.data)
                k_s = round(k_recomb(v_ratio, m_ratio),3)
                k_pol = round(k_poll(m_v1_avrg, m_v_1_avrg),3)
                chamber_selected = Ionization_chambers.query.filter_by(sn = form.chamber.data.split('-')[1]).subquery()
                chamber_certificate = Chamber_calfactor.query.join(chamber_selected).order_by(desc(Chamber_calfactor.date_loaded)).first()
                selected_chamber = Ionization_chambers.query.filter_by(id = chamber_certificate.chamber_id1).first_or_404()
                beam_energy = Photon_energy.query.filter(and_(Photon_energy.machine_id_p == machine.id, Photon_energy.energy == form.photon_energy.data)).first_or_404()
                scan_data = Pdd_data_photons.query.filter(and_(Pdd_data_photons.beam_energy_p == beam_energy.id, Pdd_data_photons.machine_scaned_p == machine.id )).order_by(desc(Pdd_data_photons.date)).first_or_404()
                kqq = Kq_photons(scan_data.tpr2010, selected_chamber.make.replace('-', ' ')).kq_value()
                bias_voltage = form.bias_voltage1
                electrometer = form.electrometer.data
                dose_refDepth = (m_v1_avrg * ktp) * chamber_certificate.ndw * kqq * k_s * k_pol
 
    return render_template('trs398.html', form=form, linac_obj = machine, environ = temp_press, beams = list_beams, round = round)