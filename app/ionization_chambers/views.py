from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from flask_login import login_required
from sqlalchemy.sql.expression import asc
from app.ionization_chambers.models import Ionization_chambers, Sr_checks #Sr_checksSchema, Chamber_calfactor'''
from app.ionization_chambers.forms import CheckSourceForm, NewChamberForm
from flask_login import current_user
from app import db
from datetime import datetime
import math
import numpy as np
from sqlalchemy import and_, asc, desc



ion_chamber_bp = Blueprint('ion_chamber',__name__, template_folder= 'templates', static_folder='static')
reg_chamber_bp = Blueprint('reg_chamber',__name__, template_folder= 'templates', static_folder='static')



@ion_chamber_bp.route('/ionization chambers')
@login_required
def ion_chamber():
    chambers = Ionization_chambers.query.all()
    #cals = Chamber_calfactor
    return render_template('chambers.html', chambers=chambers, datetime = datetime)

@ion_chamber_bp.route('/Sr-90 check source measurement', methods=['GET', 'POST'])
@login_required
def sr_checks_m():
    form = CheckSourceForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            chamber = form.chamber.data
            chamb_obj = Ionization_chambers.query.filter_by(sn = chamber[10:]).first()
            check1 = Sr_checks.query.filter(and_(Sr_checks.date == form.date.data, Sr_checks.ion_chamber_id == chamb_obj.id)).first()
            if check1 is None:
                #chamber = form.chamber.data
                #chamb_obj = Ionization_chambers.query.filter_by(sn = chamber[10:]).first()
                entry1 = Sr_checks(hospital_source = current_user.institution, ion_chamber = chamb_obj, date = form.date.data, sr_source = form.source.data, m_electrometer = form.electrometer.data, elect_voltage = form. elect_voltage.data, m_temp = form.temp_reading.data, m_press = form.press_reading.data, m_reading1= form.reading1.data, m_reading2 = form.reading2.data, m_reading3=form.reading3.data)
                db.session.add(entry1)
                db.session.commit()

                flash('The measurement has been added to the database!!')
                return redirect(url_for('ion_chamber.ion_chamber'))
            else:
                flash('Data with the same date for the same chamber has already been added onto the data base!! \n Please make sure the chamber and date that have been selected are correct.')
                return redirect(url_for('ion_chamber.ion_chamber'))

    return render_template('sr_chechs_do.html', form=form)


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



    sr_checks = Sr_checks.query.filter(and_(Sr_checks.ion_chamber_id == chamb.id, Sr_checks.base_line != True)).order_by(desc(Sr_checks.date))
    jata = []
    if sr_checks !="":
        for each in sr_checks:
            days = abs(each.date - sr_checks_baseLine.date).days
            decay = math.exp(-(math.log(2)/28.7)*(days)/365.25)

            date1 = datetime.strftime(each.date, "%d %b %Y")
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


        return jsonify({'results':'success', 'data':jata, 'chamb_name':name1, 'date_ref':date_ref, 'electrometer_ref':electrometer_ref, 'elect_voltage_ref' : elect_voltage_ref, 'source_ref' : source_ref, 'decay_ref' : decay_ref, 'exposure_ref' :exposure_ref   })

    else:
        return jsonify({'results':'success', 'chamb_name':name1, 'ref_only': 'true', 'date_ref':date_ref, 'electrometer_ref':electrometer_ref, 'elect_voltage_ref' : elect_voltage_ref, 'source_ref' : source_ref, 'decay_ref' : decay_ref, 'exposure_ref' : exposure_ref   })


@reg_chamber_bp.route('/chamber registration', methods=['GET', 'POST'])
@login_required
def reg_chamber():

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









