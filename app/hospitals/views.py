from flask import Blueprint, render_template
from app.hospitals.models import Institution

hospitals_bp = Blueprint('hospitals', __name__, template_folder='templates', static_folder= 'static')

@hospitals_bp.route('/hospitals')
def hospitals():
    return 'work is still needed here!'

