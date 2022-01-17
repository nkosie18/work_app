from flask import render_template, Blueprint

petct_bp = Blueprint('petct',__name__, template_folder='templates', static_folder='static')

@petct_bp.route('/petct')
def petct():
    return render_template('petct.html')


