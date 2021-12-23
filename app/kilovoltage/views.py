from flask import render_template, Blueprint

kilovoltage_bp = Blueprint('kilovoltage',__name__, template_folder='templates', static_folder='static')

@kilovoltage_bp.route('/kilovoltage')
def kilovoltage():
    return render_template('kilovoltage.html')


