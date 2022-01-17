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
    hospital_id = db.Column(db.Integer, db.ForeignKey("institution.id", ondelete='CASCADE'))
    photon_en = db.relationship('Photon_energy', backref='machine_en_ph', lazy='dynamic', passive_deletes=True)
    electron_en = db.relationship('Electron_energy', backref='machine_en_el', lazy='dynamic', passive_deletes=True)
    m_trs398_photons = db.relationship('Trs398_photons', backref='machine_trs_ph', lazy='dynamic', passive_deletes=True)
    m_trs398_electrons = db.relationship('Trs398_electrons', backref='machine_trs_el', lazy='dynamic', passive_deletes=True)


    def __repr__(self):
        return "<{}>".format(self.n_name)

class Photon_energy(db.Model):
    __tablename__= 'photon_energy'
    id = db.Column(db.Integer, primary_key =True)
    energy = db.Column(db.String(6), index = True)
    com_pdd10 = db.Column(db.Float)
    com_tpr = db.Column(db.Float)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete='CASCADE'), nullable=False)
    trs398_readings = db.relationship('Trs398_photons', backref='ion_chamber_phen', lazy='dynamic', passive_deletes=True)


    def __repr__(self):
        return "<{}>".format(self.energy)



#Electron beams trs-398 data.
class Electron_energy(db.Model):
    __tablename__= 'electron_energy'
    id = db.Column(db.Integer, primary_key = True)
    energy = db.Column(db.String(6), index = True)
    com_r50ion = db.Column(db.Float)
    com_r80ion = db.Column(db.Float)
    mean_energy = db.Column(db.Float)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete='CASCADE'), nullable=False)
    trs398_readings = db.relationship('Trs398_electrons', backref='ion_chamber_elen', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return "<{}>".format(self.energy)





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
