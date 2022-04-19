from app import db


#TRS-398 table for photon beams

class Trs398_photons(db.Model):
    __tablename__= 'trs398_photons'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    temp = db.Column(db.Float, nullable=False)    #degrees celcius
    press = db.Column(db.Float, nullable=False)     #hPa
    m_reading21 = db.Column(db.Float)   #nC
    m_reading22 = db.Column(db.Float)   #nC
    m_reading23 = db.Column(db.Float)   #nC
    m_pdd10 = db.Column(db.Float)
    m_tpr = db.Column(db.Float)
    m_kpol = db.Column(db.Float)
    m_ks = db.Column(db.Float)
    m_kqq = db.Column(db.Float)
    m_dose_ref = db.Column(db.Float)
    m_dose_max = db.Column(db.Float)
    m_pdiff = db.Column(db.Float)
    m_electrometer = db.Column(db.String(128))
    m_biasVoltage = db.Column(db.String(10))                      # The electrometer make and model should be added here.
    m_user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable = False)
    ion_chamber_id = db.Column(db.Integer, db.ForeignKey("ionization_chambers.id", ondelete='CASCADE'), nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete='CASCADE'), nullable=False)
    beam_id = db.Column(db.Integer, db.ForeignKey("photon_energy.id", ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return "<{}>".format(self.date)


class Trs398_electrons(db.Model):
    __tablename__= 'trs398_electrons'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    temp = db.Column(db.Float, nullable=False)      #degrees celcius
    press = db.Column(db.Float, nullable=False)     #hPa
    m_reading31 = db.Column(db.Float)   #nC
    m_reading32 = db.Column(db.Float)   #nC
    m_R50 = db.Column(db.Float)
    m_Rp = db.Column(db.Float)
    b_kpol = db.Column(db.Float)
    b_ks = db.Column(db.Float)
    b_kqq = db.Column(db.Float)
    b_dose_ref = db.Column(db.Float)
    b_dose_max = db.Column(db.Float)
    b_pdiff = db.Column(db.Float)
    b_electrometer = db.Column(db.String(128))
    b_biasVoltage = db.Column(db.String(10))
    b_user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable = False)
    ion_chamber_id = db.Column(db.Integer, db.ForeignKey("ionization_chambers.id", ondelete='CASCADE'), nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete='CASCADE'), nullable=False)
    beam_id = db.Column(db.Integer, db.ForeignKey("electron_energy.id", ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return "<{}>".format(self.date)