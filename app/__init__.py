from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.debug=True
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch =True)
login = LoginManager(app)

from app.signin.views import login_bp, logout_bp, register_bp
from app.machines.views import machines_bp

app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)
app.register_blueprint(machines_bp)



login.login_view = 'login.login'

from app import views
from app.error import errors