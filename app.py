#!/usr/bin/env python3
"""
KDS - Sistem za digitalizaciju servisa HVAC uređaja
Glavna aplikacija
"""

import os
from dotenv import load_dotenv

# Učitaj environment varijable iz .env fajla
load_dotenv()

from app import create_app, db
from app.models.user import User

# Kreiranje Flask aplikacije
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Dodaje objekte u Flask shell kontekst."""
    return {
        'db': db,
        'User': User
    }

@app.cli.command()
def init_db():
    """Inicijalizuje bazu podataka."""
    try:
        db.create_all()
        print("Baza podataka je uspešno inicijalizovana.")
    except Exception as e:
        print(f"Greška pri inicijalizaciji baze: {str(e)}")

@app.cli.command('create-admin')
def create_admin():
    """Kreira administratorski nalog."""
    try:
        # Proveri da li već postoji administrator
        admin = User.query.filter_by(tip='administrator').first()
        if admin:
            print(f"Administrator već postoji: {admin.email}")
            return
        
        # Kreiraj novog administratora
        admin_user = User(
            ime='Admin',
            prezime='KDS',
            email='admin@kds.rs',
            tip='administrator',
            aktivan=True
        )
        admin_user.set_password('admin123')
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("Administratorski nalog je kreiran:")
        print(f"Email: admin@kds.rs")
        print(f"Lozinka: admin123")
        print("VAŽNO: Promenite lozinku nakon prve prijave!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Greška pri kreiranju administratora: {str(e)}")

@app.cli.command()
def test_db():
    """Testira konekciju sa bazom podataka."""
    try:
        # Test osnovne konekcije
        db.engine.execute('SELECT 1')
        print("✓ Konekcija sa bazom je uspešna.")
        
        # Test kreiranja tabela
        db.create_all()
        print("✓ Tabele su uspešno kreirane/ažurirane.")
        
        # Test osnovnih operacija
        user_count = User.query.count()
        print(f"✓ Broj korisnika u bazi: {user_count}")
        
    except Exception as e:
        print(f"✗ Greška pri testiranju baze: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
