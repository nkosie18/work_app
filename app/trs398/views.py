from flask import Blueprint
from app.trs398.models import Trs398_electrons, Trs398_photons


trs_398_bp = Blueprint('trs_398', __name__, template_folder='templates', static_folder='static')
@trs_398_bp.route('/trs_398')
def trs_398():
    all_p = Trs398_photons.query.all()
    all_e = Trs398_electrons.query.all()
    return "work for trs 398 is still requirered here"