from flask import render_template, Blueprint
from app import db
from app.signin.models import User
from app.machines.models import Machine, Photon_energy


qcchecks_bp = Blueprint("qcchecks", __name__, template_folder= "templates", static_folder="static")

@qcchecks_bp.route('/qcchecks')
def qcchecks():
    return render_template("qcchecks.html")


