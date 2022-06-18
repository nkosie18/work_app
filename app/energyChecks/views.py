from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app.energyChecks.models import Pdd_data_photons, Pdd_data_electrons

energyChecks_bp= Blueprint('energyChecks',__name__, static_folder='static', template_folder='templates')

@energyChecks_bp.route('/energyChecks', methods = ['GET'])
@login_required
def energyChecks():
    photon_energies = Pdd_data_photons.query.all()
    electron_energies = Pdd_data_electrons.query.all()
    return render_template(energyChecks.htnl, photons = photon_energies, electrons = electron_energies)

