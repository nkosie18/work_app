from app import db
#from app import ma
from app.ionization_chambers.models import Sr_checks
from app.linac.models import Machine

class Institution(db.Model):
    __tablename__= 'institution'
    id = db.Column(db.Integer, primary_key = True)
    inst_name = db.Column(db.String(228), index=True)
    inst_address = db.Column(db.String(400))
    inst_chambers =  db.relationship('Ionization_chambers', backref='inst_chambers', lazy='dynamic', passive_deletes=True)
    inst_users =  db.relationship('User', backref='institution', lazy='dynamic', passive_deletes=True)
    inst_machines = db.relationship('Machine', backref='hospital_mach', lazy='dynamic', passive_deletes=True)
    inst_sources = db.relationship('Sr_checks', backref='hospital_source', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return '<{}>'.format(self.inst_name)

"""class InstitutionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        Deadman1
        model = Institution
        load_instance = True"""