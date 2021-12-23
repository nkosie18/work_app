from flask import render_template, Blueprint

mri_bp = Blueprint('mri',__name__, template_folder='templates', static_folder='static')

@mri_bp.route('/mri')
def mri():
    return render_template('mri.html')


