from flask import render_template, Blueprint

tps_bp = Blueprint('tps',__name__, template_folder='templates', static_folder='static')

@tps_bp.route('/tps')
def tps():
    return render_template('tps.html')


