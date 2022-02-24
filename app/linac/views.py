from flask import render_template, Blueprint, request, flash, redirect, url_for
from app.hospitals.models import Institution
from app import db
from app.linac.models import Machine, Photon_energy, Electron_energy
from app.linac.forms import AddMachineForm, AddBeamsPhotons, AddBeamsElectrons
from flask_login import current_user
from sqlalchemy import and_

linac_bp = Blueprint('linac',__name__, template_folder='templates', static_folder='static')

@linac_bp.route('/add linac', methods=['GET', 'POST'])
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
def linacs():
    return render_template('linac2.html')

