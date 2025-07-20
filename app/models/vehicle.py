from datetime import datetime
from app import db

class Vehicle(db.Model):
    """Model vozila u sistemu."""
    
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(100), nullable=False, index=True)
    model = db.Column(db.String(100), nullable=False, index=True)
    registracija = db.Column(db.String(20), unique=True, nullable=False, index=True)
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Vehicle {self.marka} {self.model}, {self.registracija}>'
    
    def get_vehicle_info(self):
        """Vraća osnovne informacije o vozilu."""
        return f"{self.marka} {self.model} ({self.registracija})"
    
    @classmethod
    def get_active_vehicles(cls):
        """Vraća samo aktivna vozila, sortirana po registarskoj oznaci."""
        return cls.query.filter_by(active=True).order_by(cls.registracija).all()
    
    def toggle_status(self):
        """Menja status vozila između aktivnog i neaktivnog."""
        self.active = not self.active
        return self.active
