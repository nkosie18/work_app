
from app import app
from flask import render_template
from flask_login import current_user, login_required



@app.route('/')
@login_required
def home():
    inst3 = current_user.institution.inst_name
    print(inst3)
    return render_template('home.html', inst3 = inst3)


