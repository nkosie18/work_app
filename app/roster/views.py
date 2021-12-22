from flask import Blueprint
from flask.templating import render_template
from datetime import datetime


roster_bp = Blueprint('roster',__name__, template_folder='templates', static_folder='static' )

@roster_bp.route('/roster')
def roster():
    day = datetime.datetime.now()
    return render_template('roster.html')