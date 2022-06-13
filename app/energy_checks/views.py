from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from config import Config
from app.trs398 import readmcc

energy_bp = Blueprint('energy',__name__,template_folder= 'templates', static_folder='static')
@energy_bp.route('/energy_checks', methods=['GET','POST'])
@login_required
def energy_check():
    machine = request.args.get('machine')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part was found')
            return redirect(url_for('energy.energy_check'))
        for file in request.files.getlist('file'):
            if file.filename !='':
                filename = secure_filename(file.filename)
                file_ext = os.path.splitext(filename)[1]
                if file_ext in Config['ALLOWED_EXTENSIONS']:
                    file_data = readmcc.read_file(filename)
                    mcc_dict = {}
                    scan =0
                    for i in file_data:
                        scan +=1
                        mcc_dict['SCAN_' + str(scan)] = i.calc_results()
                        if i.calc_results()['Type'] == 'PDD':
                            energy = i.calc_results()['Energy']
                            if energy[::-1][0] == 'X':
                                


        return redirect(url_for('energy.energy_check'))
    return render_template('energy_check.html') 


