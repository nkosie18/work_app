import time
from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify, abort
from flask_login import login_required, current_user
from app.ionization_chambers.models import Ionization_chambers, Sr_checks, Chamber_calfactor, Temp_press
from app.ionization_chambers.forms import CheckSourceForm, NewChamberForm, CalibrationCertForm, TempPressForm
from flask_login import current_user
from app import db
from datetime import datetime, timedelta
import math
import numpy as np
from sqlalchemy import and_, asc, desc
from app.ionization_chambers.unidos import Unidos


e = Unidos()

def selector(abc :str):
    while True:
        e.telegram("U")
        if e.telegram("?W") == abc:
            break

ion_chamber_bp = Blueprint('ion_chamber',__name__, template_folder= 'templates', static_folder='static')
reg_chamber_bp = Blueprint('reg_chamber',__name__, template_folder= 'templates', static_folder='static')



@ion_chamber_bp.route('/ionization chambers')
@login_required
def ion_chamber():
    chambers = Ionization_chambers.query.all()

    #cals = Chamber_calfactor
    return render_template('chambers.html', chambers=chambers, datetime = datetime)

@ion_chamber_bp.route('/Add calibration certificate Data', methods=['GET', 'POST'])
@login_required
def Cal_certs():
    if not current_user.role == 'Guest':
        form = CalibrationCertForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                check = Chamber_calfactor.query.filter(and_(Chamber_calfactor.date_cal == form.cal_date.data, Chamber_calfactor.ndw == form.calfactor.data)).first()
                if check is None:
                    chamb = form.chambers.data
                    sn1 = chamb[10:]
                    chamb_obj = Ionization_chambers.query.filter_by(sn = sn1).first()
                    newCert = Chamber_calfactor(added_by = current_user.username, date_cal = form.cal_date.data, cal_lab = form.cal_lab.data, cal_electrometer = form.electrometer.data, calfact_electrometer = form.electrometerCalFactor.data, elec_voltage = form.calVoltage.data, ndw = form.calfactor.data, cal_energy = form.beamQuality.data, cal_machine = form.calMachine.data, ion_chamb = chamb_obj)
                    db.session.add(newCert)
                    db.session.commit()
                    flash('Everything works fine, the chamber certificate has been added to the database')
                    return redirect(url_for('ion_chamber.ion_chamber'))
                else:
                    flash('The cirtificate you are trying to add already exist in the database.')
                    return redirect(url_for('ion_chamber.ion_chamber'))
                    
        return render_template('calCetificate.html', form = form)
    else:
        abort(403)

@ion_chamber_bp.route('/sr-90_measurements', methods=['GET','POST'])
@login_required
def select_measurements_method():
    checkTempPress = Temp_press.query.order_by(desc(Temp_press.date_time)).first()
    if not checkTempPress == None:
        if (checkTempPress.date_time + timedelta(minutes = 30)) < datetime.now():
            form1 = TempPressForm()
            if request.method == 'POST':
                if form1.validate_on_submit():
                    new_tp_data = Temp_press(date_time = datetime.now(), temp = form1.temp.data, press = form1.press.data)
                    db.session.add(new_tp_data)
                    db.session.commit()
                    return redirect(url_for('ion_chamber.select_measurements_method'))
            return render_template('tempPress.html', form = form1)
        else:
            return render_template('sr_90_method.html')
##########################################################################
#################################################################
##################################################################

@ion_chamber_bp.route('/sr_90_automated')
@login_required
def auto_measure_sr_checks():
    
    chamber_used_today = Ionization_chambers.query.join(Sr_checks.query.filter(Sr_checks.date == datetime.now().date()).subquery()).all()
    chambers = Ionization_chambers.query.all()
    list_chambers = []
    for each in chambers:
        if not each in chamber_used_today:
            list_chambers.append(each)
    temp_press_obj = Temp_press.query.order_by(desc(Temp_press.date_time)).first()

    return render_template('auto_Sr_90_measurement.html', chambers = list_chambers, temp_press_obj = temp_press_obj )
@ion_chamber_bp.route('/sr_checks/null')
@login_required
def null_electrometer():
    if e.telegram("N") == 'N':
        while True:
            time.sleep(1)
            if e.telegram("?S") in ['RES', 'E14']:
                break
        if e.telegram("?S") =='E14':
            e.telegram("E")
            return jsonify({'status': 'failor', 'message':'Nulling of electrometer not possible.'})
        if e.telegram('?S') == 'RES':
            return jsonify({'status':'success', 'message':'Electrometer nulling completed successfully.'})


##Get the list of chambers from the database
@ion_chamber_bp.route('/sr_checks/auto_measure', methods=['POST'])
@login_required
def auto_measure():
    selected_chamb = request.form['selected_chamber'].strip()
    selected_elect = request.form['selected_electrometer'].strip()
    selected_source = request.form['selected_source'].strip()
    selected_chamb_sn = selected_chamb.split('-')[2]
    if len(selected_chamb_sn)< 5:
        new_sn = selected_chamb_sn[1:]
    elif len(selected_chamb_sn) > 4:
        new_sn = selected_chamb_sn[2:]
    e.get_to_home()
    e.change_mode_dose()
    time.sleep(1)
    e.select_chamber(new_sn)
    
    e.change_range(1)
    measurement_list = []
    for x in range (0,3):
        e.telegram("R")
        if e.telegram("I") == 'I':
            time.sleep(2)
            while True:
                if e.telegram("?S") == 'HLD':
                    time.sleep(0.5)
                    break
                time.sleep(1)
            ms = e.telegram("V").split('s')[1]
            m1 = ms.lstrip().split(' ')[0]
            m2 = float(m1)*1000
            measurement_list.append(m2)
            
    if len(measurement_list) == 3:
        chamber_in_use = Ionization_chambers.query.filter_by(sn = selected_chamb_sn).first()
        electrometer1 = '{} {}'.format(selected_elect.split(' ')[0], e.telegram("SER"))
        date1 = datetime.now().date()
        temp_press1 = Temp_press.query.order_by(desc(Temp_press.date_time)).first()
        new_record = Sr_checks(date = date1, sr_source = selected_source, m_electrometer = electrometer1, elect_voltage = '+ 400V', m_reading1 = measurement_list[0], m_reading2 =measurement_list[1], m_reading3 = measurement_list[2], m_temp = temp_press1.temp, m_press = temp_press1.press, ion_chamber_id = chamber_in_use.id, hospitals_id = chamber_in_use.institution_id)
        db.session.add(new_record)
        db.session.commit()
    return jsonify({'status':'success'})




@ion_chamber_bp.route('/sr_checks/disconnect electrometer')
@login_required
def disconnect_electrometer():
    try:
        e.disconnect()
        return jsonify({'status':'success', 'message':'Electrometer disconnected successfully'})
    except:
        return jsonify({'status':'failor', 'message': 'I dont know what the problem is'})

@ion_chamber_bp.route('/sr_checks/checkConnection')
@login_required
def check_connections():
    try:
        elect = e.telegram('PTW')[0:6]
        if  elect == "UNIDOS":
            serial_number = e.telegram("SER")
            return jsonify({'status':'success', 'message':'Electrometer already connected', 'electrometer': 'UNIDOS-'+serial_number})
        elif e.telegram('PTW') == "NULL SERIAL":
            return jsonify({'status':'failor', 'message': 'No electrometer is connected'})
    except:
        print('There is something wrong')
        return jsonify({'status':'failor', 'message': 'An Unexpected error has occured'})


@ion_chamber_bp.route('/sr_checks/connect electrometer')
@login_required
def connect_electrometer():
    try:
        if e.telegram('PTW')[0:6] == 'UNIDOS':
            serial_number = e.telegram("SER")
            return jsonify({'status':'success', 'message':'Electrometer already connected', 'electrometer': 'UNIDOS-'+serial_number})
        else:
            raise Exception('Unidose not found!')
            
    except:
        if e.connect():
            if e.telegram('PTW')[0:6] == "UNIDOS":
                serial_number = e.telegram("SER")
                return jsonify({'status':'success', 'message': 'Electrometer found', 'electrometer': 'UNIDOS-'+serial_number})
        else:
            return jsonify({'status':'failor', 'message': 'No electrometer was found'})


@ion_chamber_bp.route('/Sr-90 check source measurement', methods=['GET', 'POST'])
@login_required
def sr_checks_m():
    if not current_user.role == 'Guest':
        checkTempPress = Temp_press.query.order_by(desc(Temp_press.date_time)).first()
        if not checkTempPress == None:
            if (checkTempPress.date_time + timedelta(minutes = 30)) < datetime.now():
                form1 = TempPressForm()
                if request.method == 'POST':
                    if form1.validate_on_submit():
                        new_tp_data = Temp_press(date_time = datetime.now(), temp = form1.temp.data, press = form1.press.data)
                        db.session.add(new_tp_data)
                        db.session.commit()
                        return redirect(url_for('ion_chamber.sr_checks_m'))
                        
                        
            
                return render_template('tempPress.html', form = form1)
            else:
                form = CheckSourceForm()  
                if request.method == 'POST':
                    if form.validate_on_submit():
                        chamber = form.chamber.data
                        print(chamber[10:])
                        chamb_obj = Ionization_chambers.query.filter_by(sn = chamber[10:]).first()
                        check1 = Sr_checks.query.filter(and_(Sr_checks.date == form.date.data, Sr_checks.ion_chamber_id == chamb_obj.id)).first()
                        if check1 is None:
                            #chamber = form.chamber.data
                            #chamb_obj = Ionization_chambers.query.filter_by(sn = chamber[10:]).first()
                            entry1 = Sr_checks(hospital_source = current_user.institution, ion_chamber = chamb_obj, date = form.date.data, sr_source = form.source.data, m_electrometer = form.electrometer.data, elect_voltage = form. elect_voltage.data, m_temp = checkTempPress.temp, m_press = checkTempPress.press, m_reading1= form.reading1.data, m_reading2 = form.reading2.data, m_reading3=form.reading3.data)
                            db.session.add(entry1)
                            db.session.commit()

                            flash('The measurement has been added to the database!!')
                            return redirect(url_for('ion_chamber.ion_chamber'))
                        else:
                            flash('Data with the same date for the same chamber has already been added onto the data base!! \n Please make sure the chamber and date that have been selected are correct.')
                            return redirect(url_for('ion_chamber.ion_chamber'))

                return render_template('sr_chechs_do.html', form=form, temp = checkTempPress.temp, press = checkTempPress.press)
    else:
        abort(403)
 

@ion_chamber_bp.route('/chamberCalStatus', methods = ['GET'])
@login_required
def daysAfterCheck():
    chamber_list = Ionization_chambers.query.filter_by(institution_id = current_user.institution_id).all()
    
    chambers_data = []
    today = datetime.now().date()
    for each in chamber_list:
        chamber_dict = {}
        last_measurement = Sr_checks.query.filter(Sr_checks.ion_chamber == each).order_by(desc(Sr_checks.date)).first()
        days_gone = today - last_measurement.date
        chamber_dict['chamber'] = '{}-{}'.format(each.make, each.sn)
        chamber_dict['chamb_sn'] = each.sn
        chamber_dict['cal_date'] = str(days_gone).split(" ")[0]
        chambers_data.append(chamber_dict)
    return jsonify({'status':'success','chamb_dates': chambers_data })

@ion_chamber_bp.route('/chambViewProcess', methods=['POST'])
@login_required
def chamberViewProcess():
    selected_chamber = request.form['sn'].strip()
    chamb = Ionization_chambers.query.filter_by(sn = selected_chamber).first()
    name1 = '{}-{}'.format(chamb.make, selected_chamber)

    # baseline query to recall the baseline measurements.
    sr_checks_baseLine = Sr_checks.query.filter(and_(Sr_checks.ion_chamber_id == chamb.id, Sr_checks.base_line == True)).first()

    #reference data
    date_ref = datetime.strftime(sr_checks_baseLine.date, "%d %b %Y")
    electrometer_ref = sr_checks_baseLine.m_electrometer
    elect_voltage_ref = sr_checks_baseLine.elect_voltage
    source_ref = sr_checks_baseLine.sr_source
    temp_ref = sr_checks_baseLine.m_temp
    press_ref = sr_checks_baseLine.m_press
    ktpp_ref = (1013.3/press_ref)*((273.2 + temp_ref)/293.2)
    decay_ref = 1
    
    exposure_ref = ((sr_checks_baseLine.m_reading1 + sr_checks_baseLine.m_reading2 + sr_checks_baseLine.m_reading3)/3)*ktpp_ref

    chamber_cert = Chamber_calfactor.query.filter_by(chamber_id1 = chamb.id).all()

    sr_checks = Sr_checks.query.filter(and_(Sr_checks.ion_chamber_id == chamb.id, Sr_checks.base_line != True)).order_by(desc(Sr_checks.date)).all()
    jata = []
    cert_data = []
    if sr_checks !="":
        for each in sr_checks:
            days = abs(each.date - sr_checks_baseLine.date).days
            decay = math.exp(-(math.log(2)/28.7)*(days)/365.25)

            date1 = datetime.strftime(each.date, "%Y-%m-%d")
            avrg = ((each.m_reading1 + each.m_reading2 + each.m_reading3)/3)

            ktp = (760.004/each.m_press)*((273.2 + each.m_temp)/293.2)

            exposure_corr = ((avrg * ktp)/decay)

            percent_diff = 100*((exposure_ref - exposure_corr)/ exposure_ref)

            jata.append({
                'date': date1,
                'mean_exposure': avrg,
                'm_temp' : each.m_temp,
                'm_press' : each.m_press, 
                'ktp' : ktp,
                'decay': decay,
                'exposure_corr' : exposure_corr,
                'percent_diff' : percent_diff
            })
            #inside the for loop.
        #outside the for loop.
        for each in chamber_cert:
            date2 = datetime.strftime(each.date_cal, "%Y-%m-%d")
            physicist = each.added_by
            date_loaded = datetime.strftime(each.date_loaded, "%Y-%m-%d")
            cal_lab = each.cal_lab
            electrometer = each.cal_electrometer
            bias_voltage = each.elec_voltage
            ndw = each.ndw
            cal_energy = each.cal_energy

            cert_data.append({
                'date_cal': date2,
                'added_by' : physicist,
                'date_loaded': date_loaded,
                'cal_lab': cal_lab,
                'electrometer': electrometer,
                'voltage': bias_voltage,
                'ndw' : ndw,
                'cal_energy' : cal_energy
            })

        return jsonify({'results':'success', 'data':jata, 'cert':cert_data, 'chamb_name':name1, 'date_ref':date_ref, 'electrometer_ref':electrometer_ref, 'elect_voltage_ref' : elect_voltage_ref, 'source_ref' : source_ref, 'decay_ref' : decay_ref, 'exposure_ref' :exposure_ref   })

    else:
        return jsonify({'results':'success', 'chamb_name':name1, 'cert':cert_data, 'ref_only': 'true', 'date_ref':date_ref, 'electrometer_ref':electrometer_ref, 'elect_voltage_ref' : elect_voltage_ref, 'source_ref' : source_ref, 'decay_ref' : decay_ref, 'exposure_ref' : exposure_ref   })


@reg_chamber_bp.route('/chamber registration', methods=['GET', 'POST'])
@login_required
def reg_chamber():
    if not current_user.role == 'Guest':
        form = NewChamberForm()

        if request.method == 'POST':
            if form.validate_on_submit():
                check = Ionization_chambers.query.filter_by(sn = form.sn.data).first()
                if check is None:
                    date_add = form.date_add.data
                    make = form.make.data
                    sn = form.sn.data
                    chamber_type =form.chamber_type.data
                    inst = current_user.institution

                    new_chamber = Ionization_chambers(date_add = date_add, make = make, sn =sn, chamber_type = chamber_type, inst_chambers = inst)

                    db.session.add(new_chamber)
                    db.session.commit()
                    flash('A new chamber has just been added successfuly!!')

                    return redirect(url_for('ion_chamber.ion_chamber'))

                else:
                    return render_template('chamberExist.html', chamber=check)
        
        else:
            return render_template('newChamberRegistration.html',form = form)
    else:
        abort(403)

@ion_chamber_bp.route('/auto_sr_checks', methods=["GET"])
@login_required
def automate():
    return render_template('automate.html')


@ion_chamber_bp.route('/respond/connect', methods=["POST"])
@login_required
def responce_automate():
    e.connect()
    status = e.telegram("PTW")
    if status[0:6]== "UNIDOS":
        return jsonify({"status":"success"})
    
    else:
         return jsonify({"status": "Failed to connect"})
    











 