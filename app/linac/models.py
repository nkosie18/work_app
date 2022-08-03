from operator import index
from app import db
#from app.hospitals.models import Institution
#from app.trs398.models import Trs398_photons, Trs398_electrons

# We still need to add information about the Institution and 
# the institution needs to add information about the physicist and therapist if need be, contact details ect.
class Machine(db.Model):
    __tablename__ = 'machine'
    id = db.Column(db.Integer, primary_key = True)
    make = db.Column(db.String(120), index= True)
    n_name = db.Column(db.String(4), index=True)
    com_date = db.Column(db.Date)
    com_technique = db.Column(db.String(10), index=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey("institution.id", ondelete='CASCADE'))
    photon_en = db.relationship('Photon_energy', backref='machine_en_ph', lazy='dynamic', passive_deletes=True)
    electron_en = db.relationship('Electron_energy', backref='machine_en_el', lazy='dynamic', passive_deletes=True) 
    m_trs398_photons = db.relationship('Trs398_photons', backref='machine_trs_ph', lazy='dynamic', passive_deletes=True)
    m_trs398_electrons = db.relationship('Trs398_electrons', backref='machine_trs_el', lazy='dynamic', passive_deletes=True)
    m_pdd_data_photons = db.relationship('Pdd_data_photons', backref='machine_pdd_ph', lazy='dynamic', passive_deletes=True)
    m_pdd_data_electrons = db.relationship('Pdd_data_electrons', backref='machine_pdd_el', lazy='dynamic', passive_deletes=True)


    def __repr__(self):
        return "<{}>".format(self.n_name)

class Photon_energy(db.Model):
    __tablename__= 'photon_energy'
    id = db.Column(db.Integer, primary_key =True)
    energy = db.Column(db.String(10), index = True)
    dose_dmax = db.Column(db.Float)
    com_pdd10 = db.Column(db.Float)
    com_tpr = db.Column(db.Float) 
    machine_id_p = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete='CASCADE'), nullable=True)
    trs398_readings = db.relationship('Trs398_photons', backref='trs398_cal_energy', lazy='dynamic', passive_deletes=True)
    pdd_energy_checks_p = db.relationship('Pdd_data_photons', backref='linac_energy_photon', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return "<{}>".format(self.energy)



#Electron beams trs-398 data.
class Electron_energy(db.Model):
    __tablename__= 'electron_energy'
    id = db.Column(db.Integer, primary_key = True)
    energy = db.Column(db.String(10), index = True)
    com_r50ion = db.Column(db.Float)
    com_r80ion = db.Column(db.Float)
    mean_energy = db.Column(db.Float)
    machine_id_e = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete='CASCADE'), nullable=True)
    trs398_readings = db.relationship('Trs398_electrons', backref='ion_chamber_elen', lazy='dynamic', passive_deletes=True)
    pdd_energy_checks_e = db.relationship('Pdd_data_electrons', backref='linac_energy_electron', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return "<{}>".format(self.energy)

'''
#Tracking linac faults.

class Linac_fault(db.Model):
    __tablename__ = 'linac_fault'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date)
    comment = db.Column(db.String(300))
    machine21 = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete='CASCADE'), nullable=False)
    physicist21 = db.Column(db.Integer, db.ForeignKey("user.id",ondelete='CASCADE'), nullable=False)
'''  







"""class Photon_pdd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    energy = db.Column(db.Integer, db.ForeignKey("photon_energy.id", ondelete='CASCADE'))
    depth = db.Column(db.Float)
    pdd = db. Column(db.Float)

    def __repr__(self):
        return "<PDD: {}>".format(self.energy)


class Electron_pdd(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    energy = db.Column(db.Integer, db.ForeignKey("electron_energy.id", ondelete='CASCADE'))
    depth = db.Column(db.Float)
    pdd = db.Column(db.Float)

    def __repr__(self):
        return "<PDD: {}>".format(self.energy) """
