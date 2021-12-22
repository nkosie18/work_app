from flask import render_template, Blueprint

ct_bp = Blueprint('ct',__name__, template_folder='templates', static_folder='static')

@ct_bp.route('/ct')
def ct():
    return render_template('ct.html')


