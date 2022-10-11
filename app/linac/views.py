from app.signin.models import User
from flask import jsonify, render_template, Blueprint, request, flash, redirect, url_for
from app.hospitals.models import Institution
from app import db
from app.trs398.models import Pdd_data_electrons, Pdd_data_photons, Trs398_photons, Trs398_electrons
from app.linac.models import Machine, Photon_energy, Electron_energy
from app.linac.forms import AddMachineForm, AddBeamsPhotons, AddBeamsElectrons
from flask_login import current_user, login_required
from sqlalchemy import and_ , desc
from datetime import datetime

linac_bp = Blueprint('linac',__name__, template_folder='templates', static_folder='static')


@linac_bp.route('/add linac', methods=['GET', 'POST'])
@login_required
def new_linac():
    
    form = AddMachineForm()
    if request.method =='POST':
        if form.validate_on_submit():
            make = form.make.data
            n_name = form.n_name.data
            com_date = form.com_date.data
            hospital_mach = Institution.query.filter_by(id = current_user.institution_id).first()
            
            check = Machine.query.filter(and_(Machine.make == make, Machine.n_name == n_name, Machine.com_date == com_date)).first()
            if check is None:
                new_machine =  Machine(make = make, n_name = n_name, com_date = com_date, hospital_mach = hospital_mach)
                db.session.add( new_machine)
                db.session.commit()
                flash('A new machine has been added to the database!!')
                return  "I still need to add html page here tha will show all the hospital machines" #redirect(url_for('linac.new_linac'))
            
            else:
                flash('The machine that you are trying to add has already been added, Please verify tha data and try again.')
                
                return redirect(url_for('linac.new_linac'))
                
                
    return render_template('new_linac.html', form = form)

@linac_bp.route('/linacs')
@login_required
def linacs():
    linacs = Machine.query.all()
    return render_template('linac2.html', linacs=linacs)

@linac_bp.route('/linac/status')
@login_required
def linac_status():
    arg_data = request.args.get('machine_selected')
    striped_arg = arg_data.strip()[1]
    linac_selected = Machine.query.filter_by(n_name = "L"+striped_arg).first()
    print(linac_selected.make)

@linac_bp.route('/EnergyChecks', methods = ['POST'])
@login_required
def energychecks():
    selected_machine_name = request.form['machine_id'].strip(" ")
    machine_obj = Machine.query.filter_by(n_name = selected_machine_name).first()
    energy_checks_data_photons = Pdd_data_photons.query.filter_by(machine_scaned_p = machine_obj.id).all()
    energy_checks_data_electrons = Pdd_data_electrons.query.filter_by(machine_scaned_e = machine_obj.id).all()
    data_electrons = []
    data_photons = []
    if energy_checks_data_photons:
        for item in energy_checks_data_photons:

            energ_obj_p = item.linac_energy_photon.energy
            uid_p = item.uid_new_p
            mdate = datetime.strftime(item.date, "%Y-%m-%d")
            dmax_p = item.dose_dmax
            pdd_10 = item.pdd10
            tpr = item.tpr2010
            user_obj_p = User.query.filter_by(id = item.user_added_by_p).first()
            added_by_p = user_obj_p.username

            data_photons.append({'uid': uid_p, 'date': mdate, 'energy': energ_obj_p, 'dose_dmax': dmax_p, 'pdd10':pdd_10, 'tpr': tpr, 'added_by': added_by_p})


    if energy_checks_data_electrons:
        for items in energy_checks_data_electrons:
            energ_obj_e = items.linac_energy_electron.energy
            uid_e = items.uid_new_e
            mdate_e = datetime.strftime(items.date, "%Y-%m-%d")
            R50 = items.R50
            E_not = items.E_not
            Rp = items.Rp
            user_obj_e = User.query.filter_by(id = items.user_added_by_e).first()
            added_by_e = user_obj_e.username

            data_electrons.append({'uid':uid_e, 'date': mdate_e, 'energy': energ_obj_e, 'r50': R50, 'e_not': E_not, 'r_p' : Rp, 'added_by': added_by_e })

    if not energy_checks_data_electrons:
        return jsonify({'results': 'success', 'data_p': data_photons})
    elif not energy_checks_data_photons:
        return jsonify({'results': 'success', 'data_e': data_electrons})
    elif energy_checks_data_electrons and energy_checks_data_photons:
        return jsonify({'results': 'success', 'data_p': data_photons, 'data_e': data_electrons}) 
    else:
            return jsonify({'result':'502','data':'The code exacuted fine, but there is no data in your database'}) 



@linac_bp.route('/linacViewProcess', methods=['POST'])
@login_required
def linacViewProcess():
    selected_machine_name = request.form['machine_id'].strip(" ")
    selected_qc = request.form['test_name'].strip(" ")
    print(selected_qc)
    if selected_qc == 'trs398':
        measured_data_photons = Machine.query.filter(Machine.n_name == selected_machine_name).join(Trs398_photons).all()
        measured_data_electrons = Machine.query.filter(Machine.n_name == selected_machine_name).join(Trs398_electrons).all()
        qcdata_trs398_photons = []
        qcdata_trs398_electrons = []
        if measured_data_photons:
            for item in measured_data_photons:
                mDate = datetime.strftime(item.date, "%Y-%m-%d")
                mTemp = item.temp
                mPress = item.press
                mChamber = '{}-{}'.format(item.ion_chamber_trs_ph.make, item.ion_chamber_trs_ph.sn)
                mBiasvoltage = item.m_biasVoltage
                mDoseMax = item.m_dose_max
                mPdiff = item.m_pdiff

                qcdata_trs398_photons.append({
                    'date': mDate,
                    'temp' : mTemp,
                    'press' : mPress,
                    'chamber': mChamber,
                    'biase_voltay' : mBiasvoltage,
                    'dose_dmax': mDoseMax,
                    'percent_diff': mPdiff    
                })

        if measured_data_electrons:
            for item in measured_data_electrons:
                bDate = datetime.strftime(item.date, "%Y-%m-%d")
                bTemp = item.temp
                bPress = item.press
                bChamber = '{}-{}'.format(item.ion_chamber_trs_el.make, item.ion_chamber_trs_el.sn)
                bBiasvoltage = item.m_biasVoltage
                bDoseMax = item.b_dose_max
                bPdiff = item.b_pdiff

                qcdata_trs398_electrons.append({
                    'date': bDate,
                    'temp' : bTemp,
                    'press' : bPress,
                    'chamber': bChamber,
                    'biase_voltay' : bBiasvoltage,
                    'dose_dmax': bDoseMax,
                    'percent_diff': bPdiff    
                })

        if measured_data_electrons and measured_data_photons:       
            return jsonify({'result': 'success', 'data_p':qcdata_trs398_photons, 'data_e': qcdata_trs398_electrons})

        else:
            return jsonify({'result':'502','data':'The code exacuted fine, but there is no data in your database'})
    



    

