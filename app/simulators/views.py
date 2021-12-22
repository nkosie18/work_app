from flask import render_template, Blueprint

simulators_bp = Blueprint('simulators',__name__, template_folder='templates', static_folder='static')

@simulators_bp.route('/simulators')
def simulators():
    return render_template('simulators.html')


