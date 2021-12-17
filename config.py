import os
import psycopg2
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRETE_KEY') or 'ThiS-iS-a-VeRY-seCRET-kEY'
    LDAP_LOGIN_VIEW = 'login.login'
    UPLOAD_PATH = 'Uploads'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)