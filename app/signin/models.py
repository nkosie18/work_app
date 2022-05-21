#from enum import unique
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.hospitals.models import Institution




class User(UserMixin, db.Model):
    __tablename__:'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(300))
    role = db.Column(db.String(20), index=True)
    remember_me = db.Column(db.String(12))
    status = db.Column(db.String(15))
    institution_id = db.Column(db.Integer,  db.ForeignKey("institution.id", ondelete='CASCADE'))
    b_trs398_photons = db.relationship('Trs398_photons', backref='physicist_phot', lazy='dynamic', passive_deletes=True)
    b_trs398_electrons = db.relationship('Trs398_electrons', backref='physicist_elec', lazy='dynamic', passive_deletes=True)
    b_pdd_photons = db.relationship('Pdd_data_photons', backref='added_by_p', lazy = 'dynamic', passive_deletes=True)
    b_pdd_electrons = db.relationship('Pdd_data_electrons', backref='added_by_e', lazy = 'dynamic', passive_deletes=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
