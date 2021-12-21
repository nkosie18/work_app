from flask import render_template, Blueprint

sasqart_bp = Blueprint('sasqart',__name__, template_folder='templates', static_folder='static')

@sasqart_bp.route('/brachy')
def brachy():
    return render_template('brachy.html')

@sasqart_bp.route('/linacMonthlyChecks')
def linac():
    return render_template('linac.html')