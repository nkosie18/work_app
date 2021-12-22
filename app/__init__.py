from flask import Flask, render_template
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

@app.route('/test2')
def test2():
    a = "nkosie"
    return render_template('test2.html', name = a)

from app.signin.views import login_bp, logout_bp, register_bp
from app.machines.views import machines_bp
from app.linac.views import linac_bp
from app.ct.views import ct_bp

app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)
app.register_blueprint(machines_bp)
app.register_blueprint(linac_bp)
app.register_blueprint(ct_bp)

login.login_view = 'login.login'

from app import views
from app.error import errors