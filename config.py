import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://yjeatzelisegcu:87661ce9f0f0a318216a7ff906f2ce4aa499d397fe8af3e1918199a08a72ebe0@ec2-3-228-78-158.compute-1.amazonaws.com:5432/dfaa8g4sstjpen'
    SQLALCHEMY_MIGRATION_REPO= os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRETE_KEY') or 'ThiS-iS-a-VeRY-seCRET-kEY'
    LDAP_LOGIN_VIEW = 'login.login'
    UPLOAD_PATH = 'Uploads'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)