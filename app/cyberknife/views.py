from flask import render_template, Blueprint

cyberknife_bp = Blueprint('cyberknife',__name__, template_folder='templates', static_folder='static')

@cyberknife_bp.route('/cyberknife')
def cyberknife():
    return render_template('cyberknife.html')


