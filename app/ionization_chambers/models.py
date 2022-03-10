from datetime import datetime
from app import db
from app.trs398.models import Trs398_electrons, Trs398_photons
from flask_login import current_user





# catalogue of chambers in thee department

class Ionization_chambers(db.Model):
    __tablename__= 'ionization_chambers'
    id = db.Column(db.Integer, primary_key= True)
    date_add = db.Column(db.Date, default = datetime.now())
    make = db.Column(db.String(128), index=True)
    sn = db.Column(db.String(128))
    chamber_type = db.Column(db.String(100), index=True)                    # field or reference chamber
    institution_id = db.Column(db.Integer, db.ForeignKey("institution.id", ondelete='CASCADE'))  #backref inst_chambers
    chamber_cal = db.relationship('Chamber_calfactor', backref = 'ion_chamb', lazy= 'dynamic', passive_deletes=True)
    sr_checks = db.relationship('Sr_checks', backref='ion_chamber', lazy='dynamic', passive_deletes=True)   #Strontium-90 check source measurements
    m_trs398_photons = db.relationship('Trs398_photons', backref='ion_chamber_trs_ph', lazy='dynamic', passive_deletes=True)
    m_trs398_electrons = db.relationship('Trs398_electrons', backref='ion_chamber_trs_el', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return "<{}>".format(self.make) 
'''
class Ionization_chambersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ionization_chambers
        load_instance = True
        '''

#chamber calibration either from the promary/secondary laboratory or through cross calibration.

class Chamber_calfactor(db.Model):
    __tablename__ = 'chamber_calfactor'
    id = db.Column(db.Integer, primary_key=True)
    date_loaded = db.Column(db.Date, default = datetime.now())
    added_by = db.Column(db.String(128))
    date_cal = db.Column(db.Date)
    cal_lab = db.Column(db.String(128))
    cal_electrometer = db.Column(db.String(120))          # Electrometer make and serial number should be entered here
    calfact_electrometer = db.Column(db.Float)
    elec_voltage = db.Column(db.String(30))
    ndw = db.Column(db.Float)                   # Gy/nC
    cal_energy = db.Column(db.String(30))
    cal_machine = db.Column(db.String(30))
    chamber_id1 = db.Column(db.Integer, db.ForeignKey("ionization_chambers.id", ondelete='CASCADE'))   # back referenced to ion_chamb


    def __repr__(self):
        return '<{}>'.format(self.ion_chamb.make)


'''
class Chamber_calfactorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chamber_calfactor
        load_instance = True
#Strontium 90 check source measurements 
'''

class Sr_checks(db.Model):
    __tablename__ = 'sr_checks'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    base_line =db.Column(db.Boolean, default=False)
    sr_source = db.Column(db.String(80))                                #The check source name and serial number should be added here.
    m_electrometer = db.Column(db.String(128))                          #The electrometer make and serial number should be entered here.
    elect_voltage = db.Column(db.String(6))                            
    m_reading1 = db.Column(db.Float)
    m_reading2 = db.Column(db.Float)
    m_reading3 = db.Column(db.Float)
    m_temp = db.Column(db.Float)
    m_press = db.Column(db.Float)
    ion_chamber_id = db.Column(db.Integer, db.ForeignKey("ionization_chambers.id", ondelete='CASCADE'), nullable=False)        #back referenced to ion_chamber
    hospitals_id = db.Column(db.Integer, db.ForeignKey("institution.id", ondelete='CASCADE'), nullable=False)                   #Back referenced to hospital_source

    def __repr__(self):
        return "<{}>".format(self.date)

class Temp_press(db.Model):
    __tablename__='temp_press'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    temp = db.Column(db.Float)
    press = db.Column(db.Float)

    def __repr__(self):
        return "<{}>".format(self.date_time)



'''
class Sr_checksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sr_checks       
        load_instance = True
'''