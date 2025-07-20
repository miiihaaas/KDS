from datetime import datetime
from app import db

class Material(db.Model):
    """Model potrošnog materijala u sistemu."""
    
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False, unique=True, index=True)
    jedinica_mere = db.Column(db.String(20), nullable=False, index=True)
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Material {self.naziv}, {self.jedinica_mere}>'
    
    def get_material_info(self):
        """Vraća osnovne informacije o materijalu."""
        return f"{self.naziv} ({self.jedinica_mere})"
    
    @classmethod
    def get_active_materials(cls):
        """Vraća samo aktivne materijale, sortirane po nazivu."""
        return cls.query.filter_by(active=True).order_by(cls.naziv).all()
    
    def toggle_status(self):
        """Menja status materijala između aktivnog i neaktivnog."""
        self.active = not self.active
        return self.active
