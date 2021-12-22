from flask import render_template, Blueprint

brachy_bp = Blueprint('brachy',__name__, template_folder='templates', static_folder='static')

@brachy_bp.route('/brachy')
def brachy():
    return render_template('brachy.html')


