from flask import render_template, Blueprint

cbct_bp = Blueprint('cbct',__name__, template_folder='templates', static_folder='static')
cbct_form_bp = Blueprint('cbct_form',__name__, template_folder='templates', static_folder='static')

@cbct_bp.route('/cbct')
def cbct():
    return render_template('cbct.html')

@cbct_form_bp.route('/cbct_form')
def cbct_form():
    return render_template('cbct_form.html')

