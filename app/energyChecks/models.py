from app import db

'''
class Pdd_data_photons(db.Model):
    __tablename__='pdd_data_photons'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date)
    pdd10 = db.Column(db.Float)
    tpr2010 = db.Column(db.Float)
    user_added_by_p = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))  #added_by_p
    beam_energy_p = db.Column(db.Integer, db.ForeignKey("photon_energy.id", ondelete='CASCADE')) #linac_energy_photon
    machine_scaned_p = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete = 'CASCADE'))   #machine_pdd_ph
    

    def __repr__(self):
        return '<%s>' %self.date

class Pdd_data_electrons(db.Model):
    __tablename__= 'pdd_data_electrons'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date)
    r50ion = db.Column(db.Float)
    e_not = db.Column(db.String(10))
    r80ion = db.Column(db.Float)
    user_added_by_e = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))  #added_by_e
    beam_energy_e = db.Column(db.Integer, db.ForeignKey("electron_energy.id", ondelete='CASCADE')) #linac_energy_electron
    machine_scaned_e = db.Column(db.Integer, db.ForeignKey("machine.id", ondelete = 'CASCADE'))   #machine_pdd_el
    
    def __repr__(self):
        return '<%s>' %self.date

        [<6X-WFF>, <10X-WFF>, <18X-WFF>, <6X-FFF>, <10X-FFF>]

        [<4E>, <6E>, <9E>, <12E>, <15E>]
        
        LINAC 1 ELEKTA

        L1 ELEKTA VERSA

        L1 ELEKTA VERSA

        ELEKTA LINAC 2
        ELEKTA LINAC 2

        L3 ELEKTA SYNERGY
        L3 ELEKTA SYNERGY
        L3 ELEKTA SYNERGY

'''