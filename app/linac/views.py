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


@linac_bp.route('/linacViewProcess', methods=['POST'])
@login_required
def linacViewProcess():
    selected_machine_name = request.form['machine_id'].strip()
    selected_machine = Machine.query.filter_by(n_name = selected_machine_name).first()
    selected_qc = request.form['test_name'].strip()
   

    selected_machine = Machine.query.filter_by(n_name = selected_machine_id).first()
    qcdata = []
    if selected_qc == 'trs398':
        measured_data = Trs398_photons.query.filter_by(machine_id = selected_machine.id).order_by(desc(Trs398_photons.date)).all()
    return jsonify({'result': 'success'})

