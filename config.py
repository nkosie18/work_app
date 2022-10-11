import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')         #'postgresql://ioxvqelthnyokf:3545b047d1d750e9fdbc66f1f2b2b11f7ba4e22131e3aaf669f8d736ad1025cc@ec2-3-213-76-170.compute-1.amazonaws.com:5432/db904phg1qatdh'
    SQLALCHEMY_MIGRATION_REPO= os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRETE_KEY') or 'ThiS-iS-a-VeRY-seCRET-kEY'
    LDAP_LOGIN_VIEW = 'login.login'
    UPLOAD_PATH = 'Uploads'
    MAX_CONTENT_LENGTH = 1024 * 1024
    ALLOWED_EXTENSIONS = ['.mcc','.txt']
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
