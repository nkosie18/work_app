from datetime import datetime
from types import new_class
from flask import flash, jsonify
from app import db
from flask import Blueprint, render_template, request, redirect, url_for
from app.linac.models import Machine, Photon_energy, Electron_energy
from app.trs398.models import Pdd_data_electrons, Pdd_data_photons, Trs398_electrons, Trs398_photons
from app.ionization_chambers.models import Ionization_chambers, Chamber_calfactor, Temp_press
from app.trs398.forms import TRS398_photonsForm, TRS398_electronForm
from flask_login import current_user, login_required
from sqlalchemy import and_, asc, desc
import numpy as np
from app.trs398.energyCorrections import Kq_photons, Kq_electrons
from app.trs398.pdd_zref import Pdd_data
from app.signin.models import User

def k_recomb(volt_ratio: float, charge_ratio: float) -> float:
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

def k_tp(temp:float, press:float) -> float:
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

@trs_398_bp.route('/trs_398/check_beam_data', methods=['POST'])
@login_required
def update_beam_data():
    machine = request.form['machine']
    beam = request.form['beam']
    chamber = request.form['chamber'].split("-")[0]
    chamber_obj = Ionization_chambers.query.filter_by(sn = request.form['chamber'].split("-")[1]).first()
    chamber_cal_cert = Chamber_calfactor.query.filter_by(chamber_id1 = chamber_obj.id).order_by(desc(Chamber_calfactor.date_cal)).first()
    machine_obj = Machine.query.filter_by(n_name = machine).first()
    beam_obj = Photon_energy.query.filter(and_(Photon_energy.energy == beam, Photon_energy.machine_id_p == machine_obj.id )).first()
    pdd_data = Pdd_data_photons.query.filter(and_(Pdd_data_photons.beam_energy_p == beam_obj.id, Pdd_data_photons.machine_scaned_p == machine_obj.id)).order_by(desc(Pdd_data_photons.date)).first()
    if not pdd_data is None:
        kq_corr = Kq_photons(pdd_data.tpr2010, chamber).kq_value()
        date_m  = datetime.strftime( pdd_data.date, "%d %b %Y")
        beam_data = {'date': date_m, 'tpr2010': pdd_data.tpr2010, 'pdd10': pdd_data.pdd10, 'k_corr': kq_corr}
        chamber_data = {'date': datetime.strftime(chamber_cal_cert.date_cal, "%d %b %Y"), 'lab': chamber_cal_cert.cal_lab, 'energy': chamber_cal_cert.cal_energy, 'ndw': chamber_cal_cert.ndw }
        return jsonify({'success': True, 'beam_data':beam_data, 'chamber_data': chamber_data })
    else:
        return jsonify({'success': False, 'message': 'No PDD Data was Found in the Database!!'})

@trs_398_bp.route('/trs398/photons/correctionFactors', methods=["POST"])
@login_required
def correctionFactors():
    avrg_m1 = float(request.form['avrg_reading'])
    avrg_m2 = float(request.form['avrg_reading2'])
    v1 = int(request.form['v1'])
    v2 = int(request.form['v2'])
    k_s = k_recomb((v1/v2), (avrg_m1/avrg_m2))

    return jsonify({'success' : True, 'k_s' : k_s})

@trs_398_bp.route('/trs398/photons_2', methods=["POST"])
@login_required
def trs398_photons():
    date_measured = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    voltage_v1 = int(request.form['v1'])
    reading1 = float(request.form['m1_reading'])
    reading2 = float(request.form['m2_reading'])
    reading3 = float(request.form['m3_reading'])
    # Recombination Correction Readings
    voltage_v2 = int(request.form['v2'])
    reading4 = float(request.form['m21_reading'])
    reading5 = float(request.form['m22_reading'])
    #electrometer
    electrometer = request.form['electrometer']
    avrg_readings1 = (reading1 + reading2 + reading3)/3
    avrg_reading2 = (reading4 + reading5)/2
    k_s = k_recomb((voltage_v1/voltage_v2),(avrg_readings1/ avrg_reading2))
    ndw_cor = float(request.form['ndw'])

    temp = float(request.form['temp'].split(' ')[0])
    press = float(request.form['press'].split(' ')[0])
    ktp_corr = k_tp(temp,press)
    machine_obj = Machine.query.filter_by(n_name = request.form['machine']).first()
    energy_obj = Photon_energy.query.filter(and_(Photon_energy.energy == request.form['energy'], Photon_energy.machine_id_p == machine_obj.id )).first()

    beam_data_date = datetime.strptime(request.form['beam_data_date'], '%d %b %Y').date()
    beam_data = Pdd_data_photons.query.filter(and_(Pdd_data_photons.date == beam_data_date, Pdd_data_photons.beam_energy_p == energy_obj.id)).first()
    chamber_obj = Ionization_chambers.query.filter_by(sn = request.form['chamber'].split("-")[1] ).first()
    kqq_corr = Kq_photons(beam_data.tpr2010, request.form['chamber'].split("-")[0]).kq_value()

    
    check_duplicates = Trs398_photons.query.filter(and_(Trs398_photons.date == date_measured, Trs398_photons.m_reading21 == reading1, Trs398_photons.m_reading22 == reading2, Trs398_photons.machine_id == machine_obj.id, Trs398_photons.beam_id == energy_obj.id)).first()
    if not check_duplicates:
        new_data = Trs398_photons(date = date_measured, temp = temp, press = press, m_reading21 = reading1, m_reading22 = reading2, m_reading23 = reading3, m_pdd10 = beam_data.pdd10, m_tpr = beam_data.tpr2010, m_ks = k_s, m_kqq = kqq_corr, m_dose_ref = request.form['dose_ref'], m_electrometer = electrometer, m_biasVoltage = voltage_v1, m_user_id = current_user.id, ion_chamber_id = chamber_obj.id, machine_id = machine_obj.id, beam_id = energy_obj.id) 
        db.session.add(new_data)
        db.session.commit()
        return jsonify({'success':True})    
    else:
        return jsonify({'success': False})

@trs_398_bp.route('/trs_398/photons', methods=['GET','POST'])
@login_required
def trs_398_photons():
    form = TRS398_photonsForm()
    machine = Machine.query.filter_by(n_name = request.args.get('machine')).first()
    temp_press = Temp_press.query.order_by(desc(Temp_press.date_time)).first()
    


    beam_energies = machine.photon_en.all()  #list of all the energies oblects
    beamEnergy_used_today = Photon_energy.query.join(Trs398_photons.query.filter(and_(Trs398_photons.date == datetime.now().date(), Trs398_photons.machine_id == machine.id)).subquery()).all()
    
    list_beams = []
    for each in beam_energies:
        if not each in beamEnergy_used_today:
            list_beams.append(each)

    if request.method == 'POST':
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
            v_ratio = np.abs(float(form.bias_voltage1.data) / float(form.bias_voltage2.data))   #V1/V2
            m_ratio = m_v1_avrg/m_v2_avrg
                                                   # M1/M2
            ktp = k_tp(temp_press.temp, temp_press.press)
            k_s = round(k_recomb(v_ratio, m_ratio),3)
            print(form.chamber.data)
            chamber_selected = Ionization_chambers.query.filter_by(sn = form.chamber.data.split('-')[1]).subquery()
            chamber_certificate = Chamber_calfactor.query.join(chamber_selected).order_by(desc(Chamber_calfactor.date_cal)).first()
            selected_chamber = Ionization_chambers.query.filter_by(id = chamber_certificate.chamber_id1).first_or_404()
            beam_energy = Photon_energy.query.filter(and_(Photon_energy.machine_id_p == machine.id, Photon_energy.energy == form.photon_energy.data)).first_or_404()
            scan_data = Pdd_data_photons.query.filter(and_(Pdd_data_photons.beam_energy_p == beam_energy.id, Pdd_data_photons.machine_scaned_p == machine.id )).order_by(desc(Pdd_data_photons.date)).first_or_404()
            kqq = Kq_photons(scan_data.tpr2010, selected_chamber.make.replace('-', ' ')).kq_value()
            bias_voltage = form.bias_voltage1
            electrometer = form.electrometer.data
            dose_refDepth = (m_v1_avrg * ktp) * chamber_certificate.ndw * kqq * k_s
            return redirect(url_for('trs_398.trs_398_photons')) 

        else:
            flash('The data you want to add to the database already exist!')
            redirect(url_for('trs_398.trs_398_photons'))
    return render_template('trs398.html', form=form, linac_obj = machine, environ = temp_press, beams = list_beams, round = round, k_s = k_recomb)

@trs_398_bp.route('/trs_398/photons/view_data', methods=['GET'])
@login_required
def check_trs_data_p():
    machine_used = Machine.query.filter_by(n_name = request.args.get('machine')).first()
    date_of_measurement = datetime.strptime(request.args.get('date'), '%Y-%m-%d').date()
    energy_used = Photon_energy.query.filter(and_(Photon_energy.energy == request.args.get('energy'), Photon_energy.machine_id_p == machine_used.id)).first()

    trs_data = Trs398_photons.query.filter(and_(Trs398_photons.date == date_of_measurement, Trs398_photons.machine_id == machine_used.id, Trs398_photons.beam_id == energy_used.id)).first()
    chamber = Ionization_chambers.query.filter_by(id= trs_data.ion_chamber_id).first()
    physicist = User.query.filter_by(id = trs_data.m_user_id).first()
    return  render_template('trs_398_vew_data.html', trs_data = trs_data, physicist = physicist, round = round, chamber = chamber)  #"Machine: %s, date measured: %s, energy: %s" %(trs_data.press, date_of_measurement, energy_used)

###############################################
## ELECTRONS  TRS-398 ##################
#########################################

@trs_398_bp.route('/trs_398/electrons', methods = ['GET' , 'POST'])
@login_required
def trs_398_electrons():
    form = TRS398_electronForm()
    machine_selected = Machine.query.filter_by(n_name = request.args.get('machine')).first()
    temp_press = Temp_press.query.order_by(desc(Temp_press.date_time)).first()

    electron_beams = machine_selected.electron_en.all()
    electronBeams_used_today = Electron_energy.query.join(Trs398_electrons.query.filter(and_(Trs398_electrons.date == datetime.now().date(), Trs398_electrons.machine_id == machine_selected.id)).subquery()).all()
    newElectronBEamsList = []

    for each in electron_beams:
        if not each in electronBeams_used_today:
            newElectronBEamsList.append(each)

    if request.method == 'POST':
        print("Work still needs to be done")

    return render_template('trs398e.html',form=form, linac_obj = machine_selected, environ = temp_press, beams = newElectronBEamsList, round = round)


###############################################
## ELECTRONS  TRS-398 Beam Data ############### 
###############################################

@trs_398_bp.route('/trs_398e/check_beam_data', methods=['POST'])
@login_required
def checkElectronsBeamData():
    machine_obj = Machine.query.filter_by(n_name = request.form['machine']).first()
    beam_obj = Electron_energy.query.filter(and_(Electron_energy.energy == request.form['beam'], Electron_energy.machine_id_e == machine_obj.id)).first()
    pdd_data = beam_obj.pdd_energy_checks_e.order_by(desc(Pdd_data_electrons.date)).first()
    chamber_obj = Ionization_chambers.query.filter_by(sn = request.form['chamber'].split('-')[1]).first()
    chamber_certificate = chamber_obj.chamber_cal.order_by(desc(Chamber_calfactor.date_loaded)).first()

    if not pdd_data is None:
        r50 = round((pdd_data.R50)/10,2)
        zref = (0.6 * r50 - 0.1)*10
        pdd_zref = Pdd_data(beam_obj.energy, zref, machine_obj.n_name).pdd()
        kqq = Kq_electrons(r50, request.form['chamber'].split('-')[0]).kq_value()
        beam_data = {'date' : datetime.strftime(pdd_data.date, '%d-%m-%Y'),
                'r50' : r50,
                'zref' : round(zref/10,2),
                'pdd_zref' : pdd_zref,
                'kqq' : kqq}

        chamber_data = {'date' : datetime.strftime(chamber_certificate.date_cal, '%d-%m-%Y'),
                    'lab' : chamber_certificate.cal_lab,
                    'energy' : chamber_certificate.cal_energy,
                    'ndw' : chamber_certificate.ndw}

        return jsonify({"success": True, 'beam_data' : beam_data, 'chamber_data' : chamber_data})
    else:
        return jsonify({'success': False, 'message': 'No PDD Data was Found in the Database!!'})


@trs_398_bp.route('/trs398/electrons_2', methods = ['POST'])
@login_required
def commitTrs398Results():
    date_measured = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    voltage_v1 = int(request.form['v1'])
    reading1 = float(request.form['m1_reading'])
    reading2 = float(request.form['m2_reading'])
    reading3 = float(request.form['m3_reading'])
    # Recombination Correction Readings
    voltage_v2 = int(request.form['v2'])
    reading4 = float(request.form['m21_reading'])
    reading5 = float(request.form['m22_reading'])
    #electrometer
    electrometer = request.form['electrometer']
    avrg_readings1 = (reading1 + reading2 + reading3)/3
    avrg_reading2 = (reading4 + reading5)/2
    k_s = k_recomb((voltage_v1/voltage_v2),(avrg_readings1/ avrg_reading2))
    ndw_cor = float(request.form['ndw'])

    temp = float(request.form['temp'].split(' ')[0])
    press = float(request.form['press'].split(' ')[0])
    ktp_corr = k_tp(temp,press)
    pdd_zref = float(request.form['pdd_zref'])

    beam_data_date = datetime.strptime(request.form['beam_data_date'], '%d-%m-%Y').date()
    machine_obj = Machine.query.filter_by(n_name = request.form['machine']).first()
    energy_obj = Electron_energy.query.filter(and_(Electron_energy.energy == request.form['energy'], Electron_energy.machine_id_e == machine_obj.id )).first()
    chamber_obj = Ionization_chambers.query.filter_by(sn = request.form['chamber'].split("-")[1]).first()
    beam_data = Pdd_data_electrons.query.filter(and_(Pdd_data_electrons.date == beam_data_date, Pdd_data_electrons.beam_energy_e == energy_obj.id)).first()
   
    kqq = Kq_electrons(beam_data.R50, request.form['chamber'].split("-")[0]).kq_value()

    check_duplicates = Trs398_electrons.query.filter(and_(Trs398_electrons.date == date_measured, Trs398_electrons.m_reading31 == reading1, Trs398_electrons.m_reading32 == reading2, Trs398_electrons.machine_id == machine_obj.id, Trs398_electrons.beam_id == energy_obj.id)).first()
    if not check_duplicates:
        new_data = Trs398_electrons(date = date_measured, temp = temp, press = press, m_reading31 = reading1, m_reading32 = reading2, m_R50 = beam_data.R50, m_Rp = beam_data.Rp, b_ks = k_s, b_kqq = kqq, b_dose_max = round(float(request.form['dose_zmax']),3), b_electrometer = request.form['electrometer'], b_biasVoltage = request.form['v1'], b_user_id = current_user.id, ion_chamber_id = chamber_obj.id, machine_id = machine_obj.id, beam_id = energy_obj.id)
        db.session.add(new_data)
        db.session.commit()
        return jsonify({'success':True})
    return jsonify({'success':False})