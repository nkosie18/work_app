from flask import render_template, Blueprint
from app.linac.models import Machine, Photon_energy, Electron_energy

linac_bp = Blueprint('linac',__name__, template_folder='templates', static_folder='static')

@linac_bp.route('/linac')
def linac():
    return render_template('linac.html')


