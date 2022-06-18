from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.trs398.models import Pdd_data_photons, Pdd_data_electrons
from app.energyChecks import readmcc
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from app.linac.models import Machine, Electron_energy, Photon_energy
from sqlalchemy import and_, asc, desc 


energyChecks_bp= Blueprint('energyChecks',__name__, static_folder='static', template_folder='templates')

@energyChecks_bp.route('/energyChecks', methods = ['GET'])
@login_required
def energyChecks():
    photon_energies = Pdd_data_photons.query.all()
    electron_energies = Pdd_data_electrons.query.all()
    return   'hello world' #render_template(energyChecks.htnl, photons = photon_energies, electrons = electron_energies)


@energyChecks_bp.route('/energyChecks/update_pdd', methods = ['GET','POST'])
@login_required
def update_pdd():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('file[]')
        for file in uploaded_files:
            if file.filename =='':
                flash('No file selected!, Please select a file to upload.')
                return redirect(url_for('energyChecks.update_pdd'))

            else:
                file_name = secure_filename(file.filename)
                print(file_name)
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
                        print(each_scan.calc_results())
                        if each_scan.calc_results()['Type'] == 'PDD':
                            if each_scan.calc_results()['modality'] == 'X':
                                date_today = datetime.now().date()
                                machine = Machine.query.filter_by(n_name = each_scan.calc_results()['machine']).first_or_404()
                                beamEnergy = each_scan.calc_results()['Energy']
                                if not beamEnergy in ['16X','110X']:
                                    machine_energy = Photon_energy.query.filter(and_(Photon_energy.energy == '%sX-WFF' %beamEnergy[0:-1], Photon_energy.machine_id_p == machine.id)).first_or_404()
                                if beamEnergy == '16X':
                                    machine_energy = Photon_energy.query.filter(and_(Photon_energy.energy == '6X-FFF', Photon_energy.machine_id_p == machine.id)).first_or_404()
                                
                                if beamEnergy == '110X':
                                    machine_energy = Photon_energy.query.filter(and_(Photon_energy.energy == '10X-FFF', Photon_energy.machine_id_p == machine.id)).first_or_404()
                                pdd_data = Pdd_data_photons(date = date_today, pdd10 = each_scan.calc_results()['D100'], tpr2010 = each_scan.calc_results()['Q Index'], machine_scaned_p = machine.id, beam_energy_p = machine_energy.id,  user_added_by_p = current_user.id)
                                print(pdd_data)
                                print( 'we going to do photon things here')
                            else:
                                print( 'we going to do electron things here')

                        else:
                            flash('we going to do profile things here')
                else:
                    flash('The selected file has an extension that is currently not supported.')
                    flash('Please select a file with the following extensions: %s' %current_app.config['ALLOWED_EXTENSIONS'])
                    return redirect(url_for('energyChecks.update_pdd'))



                   
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
