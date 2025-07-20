from app import db
from datetime import datetime

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.String(20), nullable=False)  # 'pravno_lice' ili 'fizicko_lice'
    adresa = db.Column(db.String(255), nullable=False)
    mesto = db.Column(db.String(100), nullable=False)
    postanski_broj = db.Column(db.String(20), nullable=False)
    drzava = db.Column(db.String(100), nullable=False, default='Srbija')
    telefon = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'client',
        'polymorphic_on': tip
    }

# Model za pravno lice
class PravnoLice(Client):
    __tablename__ = 'pravna_lica'
    
    id = db.Column(db.Integer, db.ForeignKey('clients.id'), primary_key=True)
    naziv = db.Column(db.String(255), nullable=False, index=True)
    pib = db.Column(db.String(9), unique=True, nullable=False, index=True)
    mb = db.Column(db.String(8), unique=True, nullable=False)
    
    radne_jedinice = db.relationship('RadnaJedinica', backref='pravno_lice', lazy=True, cascade='all, delete-orphan')
    
    __mapper_args__ = {
        'polymorphic_identity': 'pravno_lice',
    }
    
    def __repr__(self):
        return f'<PravnoLice {self.naziv}, PIB: {self.pib}>'

# Model za fizičko lice
class FizickoLice(Client):
    __tablename__ = 'fizicka_lica'
    
    id = db.Column(db.Integer, db.ForeignKey('clients.id'), primary_key=True)
    ime = db.Column(db.String(100), nullable=False, index=True)
    prezime = db.Column(db.String(100), nullable=False, index=True)
    
    lokacije = db.relationship('LokacijaKuce', backref='fizicko_lice', lazy='dynamic')
    
    __mapper_args__ = {
        'polymorphic_identity': 'fizicko_lice',
    }
    
    def __repr__(self):
        return f'<FizickoLice {self.ime} {self.prezime}>'
    
    def get_full_name(self):
        return f"{self.ime} {self.prezime}"

# Model za radnu jedinicu (za pravna lica)
class RadnaJedinica(db.Model):
    __tablename__ = 'radne_jedinice'
    
    id = db.Column(db.Integer, primary_key=True)
    pravno_lice_id = db.Column(db.Integer, db.ForeignKey('pravna_lica.id'), nullable=False)
    naziv = db.Column(db.String(255), nullable=False)
    adresa = db.Column(db.String(255), nullable=False)
    mesto = db.Column(db.String(100), nullable=False)
    postanski_broj = db.Column(db.String(20), nullable=False)
    drzava = db.Column(db.String(100), nullable=False, default='Srbija')
    telefon = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255))
    kontakt_osoba = db.Column(db.String(255))
    napomena = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    objekti = db.relationship('Objekat', backref='radna_jedinica', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<RadnaJedinica {self.naziv}, {self.adresa}, {self.mesto}>'

# Model za lokaciju kuće (za fizička lica)
class LokacijaKuce(db.Model):
    __tablename__ = 'lokacije_kuce'
    
    id = db.Column(db.Integer, primary_key=True)
    fizicko_lice_id = db.Column(db.Integer, db.ForeignKey('fizicka_lica.id'), nullable=False)
    naziv = db.Column(db.String(255), nullable=False)
    adresa = db.Column(db.String(255), nullable=False)
    mesto = db.Column(db.String(100), nullable=False)
    postanski_broj = db.Column(db.String(20), nullable=False)
    napomena = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<LokacijaKuce {self.naziv}, {self.adresa}, {self.mesto}>'

# Model za objekte (zgrade) radne jedinice
class Objekat(db.Model):
    __tablename__ = 'objekti'
    
    id = db.Column(db.Integer, primary_key=True)
    radna_jedinica_id = db.Column(db.Integer, db.ForeignKey('radne_jedinice.id'), nullable=False)
    naziv = db.Column(db.String(255), nullable=False)
    opis = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    prostorije = db.relationship('Prostorija', backref='objekat', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Objekat {self.naziv}>'

# Model za prostorije objekta
class Prostorija(db.Model):
    __tablename__ = 'prostorije'
    
    id = db.Column(db.Integer, primary_key=True)
    objekat_id = db.Column(db.Integer, db.ForeignKey('objekti.id'), nullable=False)
    naziv = db.Column(db.String(255), nullable=False)
    sprat = db.Column(db.String(50))
    broj = db.Column(db.String(50))
    namena = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Prostorija {self.naziv} - {self.broj}>'
