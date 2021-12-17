from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_heroku import Heroku

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
heroku = Heroku(app)
migrate =Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html')
