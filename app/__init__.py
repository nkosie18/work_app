from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)



from app.signin.views import login_bp, logout_bp, register_bp
from app.linac.views import linac_bp
from app.ct.views import ct_bp
from app.hospitals.views import hospitals_bp
from app.ionization_chambers.views import ion_chamber_bp, reg_chamber_bp
from app.trs398.views import trs_398_bp
from app.brachytherapy.views import brachy_bp
from app.simulators.views import simulators_bp
from app.qcchecks.views import qcchecks_bp
from app.kilovoltage.views import kilovoltage_bp
from app.tps.views import tps_bp
from app.gammaknife.views import gammaknife_bp
from app.cyberknife.views import cyberknife_bp
from app.cbct.views import cbct_bp
from app.mri.views import mri_bp
from app.petct.views import petct_bp
from app.cbct.views import cbct_form_bp
from app.energyChecks.views import energyChecks_bp




app.register_blueprint(trs_398_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)
app.register_blueprint(linac_bp)

app.register_blueprint(ct_bp)
app.register_blueprint(ion_chamber_bp)
app.register_blueprint(reg_chamber_bp)
app.register_blueprint(brachy_bp)
app.register_blueprint(simulators_bp)
app.register_blueprint(qcchecks_bp)
app.register_blueprint(kilovoltage_bp)
app.register_blueprint(tps_bp)
app.register_blueprint(gammaknife_bp)
app.register_blueprint(cyberknife_bp)
app.register_blueprint(cbct_bp)
app.register_blueprint(mri_bp)
app.register_blueprint(petct_bp)
app.register_blueprint(cbct_form_bp)
app.register_blueprint(energyChecks_bp)
app.register_blueprint(hospitals_bp)



login.login_view = 'login.login'

from app import views
from app.error import errors
