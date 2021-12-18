from flask import render_template, Blueprint
from app.machines.models import Machine, Photon_energy


machines_bp = Blueprint("machines", __name__, template_folder= "templates", static_folder="static")

@machines_bp.route('/machines')
def machines():
    return "hello world from Machines"


