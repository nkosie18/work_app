from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.trs398.models import Pdd_data_photons, Pdd_data_electrons
from app.energyChecks import readmcc
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from app.linac.models import Machine, Electron_energy, Photon_energy
from sqlalchemy import and_, asc, desc
from app import db
from uuid import uuid4 


energyChecks_bp= Blueprint('energyChecks',__name__, static_folder='static', template_folder='templates')

@energyChecks_bp.route('/energyChecks', methods = ['GET'])
@login_required
def energyChecks():
    photon_energies = Pdd_data_photons.query.all()
    electron_energies = Pdd_data_electrons.query.all()
    return   'hello world' #render_template(energyChecks.htnl, photons = photon_energies, electrons = electron_energies)

class energy_check_p():
    def __init__(self, machine, beam, pdd10_curr, pdd10_prev, pdd_comm, tpr2010_curr, tpr2010_prev, tpr2010_comm, dmax_curr, dmax_prev, dmax_comm):
        self.machine = machine
        self.beam = beam
        self.pdd10_curr = pdd10_curr
        self.pdd10_prev = pdd10_prev
        self.pdd_comm = pdd_comm
        self.dmax_curr = dmax_curr
        self.dmax_prev = dmax_prev
        self.dmax_comm = dmax_comm
        self.tpr2010_curr = tpr2010_curr
        self.tpr2010_prev = tpr2010_prev
        self.tpr2010_comm = tpr2010_comm

class energy_checks_e():
    def __init__(self, machine, beam, R50_curr, R50_prev, R50_comm, Rp_curr, Rp_prev, Rp_comm, mean_e_curr, mean_e_prev, mean_e_comm):
        self.machine = machine
        self.beam = beam
        self.R50_curr = R50_curr
        self.R50_prev = R50_prev
        self.R50_comm = R50_comm
        self.Rp_curr = Rp_curr
        self.Rp_prev = Rp_prev
        self.Rp_comm = Rp_comm
        self.mean_e_curr = mean_e_curr
        self.mean_e_prev = mean_e_prev
        self.mean_e_comm = mean_e_comm


@energyChecks_bp.route('/energyChecks/upload_status', methods = ['GET'])
@login_required
def upload_status():
    uid_from_session = request.args.get('uid_new')
    new_photon_data = Pdd_data_photons.query.filter_by(uid_new_p = uid_from_session).all()
    new_electron_data = Pdd_data_electrons.query.filter_by(uid_new_e = uid_from_session).all()
    results_p = []
    results_e = []

    ###########
    # Photon data
    #############
    for each_p_beam in new_photon_data:
        machine_id = each_p_beam.machine_scaned_p
        beam_id = each_p_beam.beam_energy_p
        machine_obj = Machine.query.filter_by(id = machine_id).first()
        beam_obj = Photon_energy.query.filter_by(id = beam_id).first()   # this is the commissioning data
        name_combined = '{}_{}'.format(machine_obj.n_name, beam_obj.energy)
        #comm_data = Photon_energy.query.filter(and_(Photon_energy.machine_id_p == machine_id, Photon_energy.id == beam_id)).first()
        previous_data_p = Pdd_data_photons.query.filter(and_(Pdd_data_photons.machine_scaned_p == machine_id, Pdd_data_photons.beam_energy_p == beam_id, Pdd_data_photons.uid_new_p != uid_from_session)).order_by(desc(Pdd_data_photons.date)).first()
        if previous_data_p is not None:
            print("dmax: %s" %each_p_beam.dose_dmax)
            json_obj_p = energy_check_p(machine_obj.n_name, beam_obj.energy, each_p_beam.pdd10, previous_data_p.pdd10, beam_obj.com_pdd10, each_p_beam.tpr2010, previous_data_p.tpr2010, beam_obj.com_tpr, each_p_beam.dose_dmax, previous_data_p.dose_dmax, beam_obj.com_dose_dmax)
            results_p.append(json_obj_p)
        if previous_data_p is None:
            json_obj_p = energy_check_p(machine_obj.n_name, beam_obj.energy, each_p_beam.pdd10, beam_obj.com_pdd10, beam_obj.com_pdd10, each_p_beam.tpr2010, beam_obj.com_tpr, beam_obj.com_tpr, each_p_beam.dose_dmax, beam_obj.com_dose_dmax, beam_obj.com_dose_dmax)
            results_p.append(json_obj_p)

    for each_e_beam in new_electron_data:
        machine_id_e = each_e_beam.machine_scaned_e
        beam_id_e = each_e_beam
        machine_obje = Machine.query.filter_by(id = machine_id_e).first()
        beam_obje = Electron_energy.query.filter_by(id = beam_id_e).first()  # This is the commissioning data for the electrns.
        previous_data_e = Pdd_data_electrons.query.filter(and_(Pdd_data_electrons.machine_scaned_e == machine_id_e, Pdd_data_electrons.beam_energy_e == beam_id_e, Pdd_data_electrons.uid_new_e != uid_from_session)).order_by(desc(Pdd_data_electrons.date)).first()
        if not previous_data_e is None:
            json_obj_e = 


    return render_template('energyChecks/upload_status.html',round = round, results_p = results_p, abs = abs, float = float )

        
            

        
    
    new_electron_data = Pdd_data_electrons.query.filter_by(uid_new_e = uid_from_session).all()


    return render_template('energyChecks/upload_status.html')


@energyChecks_bp.route('/energyChecks/update_pdd', methods = ['GET','POST'])
@login_required
def update_pdd():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('file[]')
        uid_new = str(uuid4())
        for file in uploaded_files:
            if file.filename =='':
                flash('No file selected!, Please select at least one file to upload.')
                return redirect(url_for('energyChecks.update_pdd'))

            if not file.filename =='':
                file_name = secure_filename(file.filename)
                file_ext = os.path.splitext (file.filename)[1]
                if file_ext in current_app.config['ALLOWED_EXTENSIONS']:
                    file.save(os.path.join(current_app.config['UPLOAD_PATH'], file_name))
                    savedFilePath = 'Uploads/%s' %file_name
                    mymcc = readmcc.read_file(savedFilePath)
                    mcc_dict = {}
                    scan_number = 0
                    for each_scan in mymcc:
                        scan_number += 1
                        mcc_dict['Scan_%s' %scan_number] = each_scan.calc_results()
                        if each_scan.calc_results()['Type'] == 'PDD':
                            if each_scan.calc_results()['modality'] == 'X':
                                date_today = datetime.now().date()
                                machine = Machine.query.filter_by(n_name = each_scan.calc_results()['machine']).first_or_404()
                                beamEnergy = each_scan.calc_results()['Energy']
                                print('the dose at depth max is: %s' %each_scan.calc_results()['D max'])
                                if not beamEnergy in ['16X','110X']:
                                    machine_energy = Photon_energy.query.filter(and_(Photon_energy.energy == '%sX-WFF' %beamEnergy[0:-1], Photon_energy.machine_id_p == machine.id)).first_or_404()
                                if beamEnergy == '16X':
                                    machine_energy = Photon_energy.query.filter(and_(Photon_energy.energy == '6X-FFF', Photon_energy.machine_id_p == machine.id)).first_or_404()
                                
                                if beamEnergy == '110X':
                                    machine_energy = Photon_energy.query.filter(and_(Photon_energy.energy == '10X-FFF', Photon_energy.machine_id_p == machine.id)).first_or_404()
                                pdd_data = Pdd_data_photons(uid_new_p = uid_new, date = date_today, pdd10 = float(each_scan.calc_results()['D100']), tpr2010 = float(each_scan.calc_results()['Q Index']), dose_dmax = each_scan.calc_results()['D max'] , machine_scaned_p = machine.id, beam_energy_p = machine_energy.id,  user_added_by_p = current_user.id)
                                
                                checkDuplicate = Pdd_data_photons.query.filter(and_(Pdd_data_photons.date == date_today, Pdd_data_photons.machine_scaned_p == machine.id, Pdd_data_photons.beam_energy_p == machine_energy.id)).first()
                                if not checkDuplicate is None:
                                    flash(' %s : This PDD data already exists!  (Machine: %s, Energy: %s)' %(file_name, machine.n_name, machine_energy.energy))
                                    
                                if checkDuplicate is None:
                                    db.session.add(pdd_data)
                                    db.session.commit()
                                    flash('%s : PDD data added for %s %s' %(file_name, machine.n_name, machine_energy.energy))
########################################################################################
####         ELECTRONS PDD HANDLER #####################################################
########################################################################################
                            if each_scan.calc_results()['modality'] == 'EL':
                                date_today = datetime.now().date()
                                machine = Machine.query.filter_by(n_name = each_scan.calc_results()['machine']).first_or_404()
                                beamEnergy = each_scan.calc_results()['Energy']
                                r50 = each_scan.calc_results()['R50']['R50']
                                Rp = each_scan.calc_results()['Rp']
                                E_not = round(float(each_scan.calc_results()['R50']['R50']) * 2.33, 2)
                                machine_energy = Electron_energy.query.filter(and_(Electron_energy.energy == beamEnergy[0:-1], Electron_energy.machine_id_e == machine.id)).first_or_404()
                                pdd_data = Pdd_data_electrons(uid_new_e = uid_new ,date = date_today, R50 = float(r50), E_not = E_not, Rp = float(Rp), machine_scaned_e = machine.id, beam_energy_e = machine_energy.id,  user_added_by_e = current_user.id)
                                check_duplicates = Pdd_data_electrons.query,filter(and_(Pdd_data_electrons.date == date_today, Pdd_data_electrons.machine_scaned_e == machine.id, Pdd_data_electrons.beam_energy_e == machine_energy.id)).first()
                                if not check_duplicates is None:
                                    flash(' %s : This PDD data already exists!  (Machine: %s, Energy: %s)' %(file_name, machine.n_name, machine_energy.energy))
                                    
                                if checkDuplicate is None:
                                    db.session.add(pdd_data)
                                    db.session.commit()
                                    flash('%s : PDD data added for %s %s' %(file_name, machine.n_name, machine_energy.energy))
                        if not each_scan.calc_results()['Type'] == 'PDD':
                            flash('%s : This is not a PDD scan, please select a PDD scan to upload.' %file_name)
                if not file_ext in current_app.config['ALLOWED_EXTENSIONS']:
                    flash('%s : The selected file has an extension that is currently not supported.' %file_name)
                    flash('Please select a file with the following extensions: %s' %current_app.config['ALLOWED_EXTENSIONS'])


        return redirect(url_for('energyChecks.upload_status', uid_new = uid_new))


                   
    '''        
        n = 0
        for file in uploaded_files:
            n += 1
            m = 0
            mcc_dict = {}
            my_mcc = readmcc.read_file(file)
            for i in my_mcc:
                m += 1
                mcc_dict['SCAN_' + str(m)] = i.calc_result()
                print(i.calc_results())
'''

    return render_template('energyChecks/update_pdd.html')
