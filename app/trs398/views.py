from flask import Blueprint, render_template
from app.trs398.models import Trs398_electrons, Trs398_photons
from app.trs398.forms import TRS398_photonsForm
from flask_login import current_user, login_required


trs_398_bp = Blueprint('trs_398', __name__, template_folder='templates', static_folder='static')
@trs_398_bp.route('/trs_398')
@login_required
def trs_398():
    all_p = Trs398_photons.query.all()
    all_e = Trs398_electrons.query.all()
    form = TRS398_photonsForm()
    return render_template('trs398.html', form=form)