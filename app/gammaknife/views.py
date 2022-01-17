from flask import render_template, Blueprint

gammaknife_bp = Blueprint('gammaknife',__name__, template_folder='templates', static_folder='static')

@gammaknife_bp.route('/gammaknife')
def gammaknife():
    return render_template('gammaknife.html')


