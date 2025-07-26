from app import db
from datetime import datetime
from flask import current_app
from sqlalchemy import Enum, Table, ForeignKey, Column, Integer, DateTime

# Tabela asocijacije između uređaja i prostorija (many-to-many)
uredjaji_prostorije = db.Table('uredjaji_prostorije',
    db.Column('uredjaj_id', db.Integer, db.ForeignKey('uredjaji.id'), primary_key=True),
    db.Column('prostorija_id', db.Integer, db.ForeignKey('prostorije.id'), primary_key=True),
    db.Column('dodeljen_at', db.DateTime, default=datetime.utcnow),
    db.Column('dodelio_korisnik_id', db.Integer, db.ForeignKey('users.id'))
)

class Uredjaj(db.Model):
    __tablename__ = 'uredjaji'
    
    # Tipovi i podtipovi uređaja
    TIPOVI = {
        'rashladna_tehnika': [
            'split_sistem', 'cileri', 'centralna_klima', 'toplotne_pumpe', 
            'kanalska_klima', 'klima_komora', 'pokretna_klima', 'klima_ormar', 
            'prozorska_klima', 'vrf_sistemi', 'frizideri'
        ],
        'grejna_tehnika': [
            'ta_pec', 'grejalice', 'kotlovi', 'panelni_radijatori', 'radijatori'
        ],
        'ventilacioni_sistemi': []
    }
    
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.Enum('rashladna_tehnika', 'grejna_tehnika', 'ventilacioni_sistemi', name='tip_uredjaja'), nullable=False)
    podtip = db.Column(db.Enum(
        # Rashladna tehnika
        'split_sistem', 'cileri', 'centralna_klima', 'toplotne_pumpe', 
        'kanalska_klima', 'klima_komora', 'pokretna_klima', 'klima_ormar', 
        'prozorska_klima', 'vrf_sistemi', 'frizideri',
        # Grejna tehnika
        'ta_pec', 'grejalice', 'kotlovi', 'panelni_radijatori', 'radijatori',
        name='podtip_uredjaja'
    ), nullable=True)
    proizvodjac = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    serijski_broj = db.Column(db.String(100), unique=True, nullable=False)
    inventarski_broj = db.Column(db.String(100))
    godina_proizvodnje = db.Column(db.Integer, nullable=False)
    
    # Many-to-many veza sa prostorijama
    prostorije = db.relationship(
        'Prostorija', 
        secondary='uredjaji_prostorije',
        backref=db.backref('uredjaji', lazy='dynamic'),
        lazy='dynamic'
    )
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Uredjaj {self.id}: {self.proizvodjac} {self.model}>"
        
    def get_display_name(self):
        """Vraća formatiran naziv uređaja za prikaz."""
        return f"{self.proizvodjac} {self.model} (SN: {self.serijski_broj})"
    
    def dodeli_prostoriju(self, prostorija, korisnik_id=None):
        """Dodeljuje uređaj prostoriji."""
        if prostorija not in self.prostorije:
            # Ako uređaj već nije dodeljen prostoriji, dodeli ga
            stmt = uredjaji_prostorije.insert().values(
                uredjaj_id=self.id,
                prostorija_id=prostorija.id,
                dodeljen_at=datetime.utcnow(),
                dodelio_korisnik_id=korisnik_id
            )
            db.session.execute(stmt)
            return True
        return False
        
    def ukloni_iz_prostorije(self, prostorija):
        """Uklanja uređaj iz prostorije."""
        if prostorija in self.prostorije:
            stmt = uredjaji_prostorije.delete().where(
                (uredjaji_prostorije.c.uredjaj_id == self.id) & 
                (uredjaji_prostorije.c.prostorija_id == prostorija.id)
            )
            db.session.execute(stmt)
            return True
        return False
