from flask import render_template
from app import app


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden_access(error):
    return render_template('errors/403.html'), 403

