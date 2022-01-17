from app import db
from app.ionization_chambers.models import Ionization_chambers


#TRS-398 table for photon beams

class Trs398_photons(db.Model):
    __tablename__= 'trs398_photons'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    temp = db.Column(db.Float, nullable=False)
    press = db.Column(db.Float, nullable=False)
    m_avrg = db.Column(db.Float, nullable=False)
    m_pdd10 = db.Column(db.Float)
    m_tpr = db.Column(db.Float)
    m_dose = db.Column(db.Float)
    m_electrometer = db.Column(db.String(128))                          # The electrometer make and model should be added here.
    ion_chamber_id = db.Column(db.Integer, db.ForeignKey("ionization_chambers.id", ondelete='CASCADE'), nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete='CASCADE'), nullable=False)
    beam_id = db.Column(db.Integer, db.ForeignKey("photon_energy.id", ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return "<{}>".format(self.date)


class Trs398_electrons(db.Model):
    __tablename__= 'trs398_electrons'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    temp = db.Column(db.Float, nullable=False)
    press = db.Column(db.Float, nullable=False)
    m_avrg = db.Column(db.Float, nullable=False)
    m_pdd10 = db.Column(db.Float)
    m_tpr = db.Column(db.Float)
    m_dose = db.Column(db.Float)
    ion_chamber_id = db.Column(db.Integer, db.ForeignKey("ionization_chambers.id", ondelete='CASCADE'), nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete='CASCADE'), nullable=False)
    beam_id = db.Column(db.Integer, db.ForeignKey("electron_energy.id", ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return "<{}>".format(self.date)