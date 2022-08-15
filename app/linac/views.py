import re
from unittest import result
from flask import jsonify, render_template, Blueprint, request, flash, redirect, url_for
from app.hospitals.models import Institution
from app import db
from app.trs398.models import Trs398_photons, Trs398_electrons
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

        if measured_data_electrons and measured_data_electrons:       
            return jsonify({'result': 'success', 'data_p':qcdata_trs398_photons, 'data_e': qcdata_trs398_electrons})

        else:
            return jsonify({'result':'502','data':'The code exacuted fine, but there is no data in your database'})
    



    

