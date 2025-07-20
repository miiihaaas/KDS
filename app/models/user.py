from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """Model korisnika sistema."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    tip = db.Column(db.Enum('administrator', 'serviser', name='user_tip'), nullable=False, index=True)
    aktivan = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        """Postavlja hashovan password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Proverava da li je password ispravan."""
        return check_password_hash(self.password_hash, password)
    
    def is_administrator(self):
        """Proverava da li je korisnik administrator."""
        return self.tip == 'administrator'
    
    def is_serviser(self):
        """Proverava da li je korisnik serviser."""
        return self.tip == 'serviser'
    
    def get_full_name(self):
        """Vraća puno ime korisnika."""
        return f"{self.ime} {self.prezime}"
    
    # Flask-Login zahtevi
    def get_id(self):
        return str(self.id)
    
    @property
    def is_active(self):
        return self.aktivan
