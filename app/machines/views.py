from flask import render_template, Blueprint
from app import db
from app.signin.models import User
from app.machines.models import Machine, Photon_energy


machines_bp = Blueprint("machines", __name__, template_folder= "templates", static_folder="static")

@machines_bp.route('/machines')
def machines():
    name = User.query.filter_by(username = "Itumeleng").first()
    return render_template("test2.html", name = name.username)


