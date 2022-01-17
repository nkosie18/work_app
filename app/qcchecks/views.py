from flask import render_template, Blueprint


qcchecks_bp = Blueprint("qcchecks", __name__, template_folder= "templates", static_folder="static")

@qcchecks_bp.route('/qcchecks')
def qcchecks():
    return render_template("qcchecks.html")


