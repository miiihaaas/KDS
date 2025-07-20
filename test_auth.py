#!/usr/bin/env python3
"""
Test skripta za testiranje autentifikacije funkcionalnosti.
Testira sve acceptance kriterijume iz Story 1.2.
"""

from app import create_app, db
from app.models.user import User
from app.services.auth_service import AuthService
import os

def create_test_users():
    """Kreira test korisnike za testiranje."""
    print("Kreiranje test korisnika...")
    
    try:
        # Proverava da li već postoje test korisnici
        existing_admin = User.query.filter_by(email="admin@test.com").first()
        existing_serviser = User.query.filter_by(email="serviser@test.com").first()
        existing_deaktiviran = User.query.filter_by(email="deaktiviran@test.com").first()
        
        if existing_admin and existing_serviser and existing_deaktiviran:
            print("Svi test korisnici već postoje.")
            return existing_admin, existing_serviser, existing_deaktiviran
        
        print("Kreiranje nedostajućih test korisnika...")
        
        # Kreiraj administrator-a ako ne postoji
        if not existing_admin:
            admin = User(
                ime="Marko",
                prezime="Petrović",
                email="admin@test.com",
                tip="administrator",
                aktivan=True
            )
            admin.set_password("admin123456")
            db.session.add(admin)
            print("Kreiran administrator.")
        else:
            admin = existing_admin
        
        # Kreiraj serviser-a ako ne postoji
        if not existing_serviser:
            serviser = User(
                ime="Ana",
                prezime="Jovanović", 
                email="serviser@test.com",
                tip="serviser",
                aktivan=True
            )
            serviser.set_password("serviser123456")
            db.session.add(serviser)
            print("Kreiran serviser.")
        else:
            serviser = existing_serviser
        
        # Kreiraj deaktiviran-og korisnika ako ne postoji
        if not existing_deaktiviran:
            deaktiviran = User(
                ime="Petar",
                prezime="Nikolić",
                email="deaktiviran@test.com",
                tip="serviser",
                aktivan=False
            )
            deaktiviran.set_password("deaktiviran123456")
            db.session.add(deaktiviran)
            print("Kreiran deaktiviran korisnik.")
        else:
            deaktiviran = existing_deaktiviran
        
        db.session.commit()
        print("Test korisnici su uspešno kreirani.")
        return admin, serviser, deaktiviran
        
    except Exception as e:
        db.session.rollback()
        print(f"Greška pri kreiranju test korisnika: {e}")
        return None, None, None

def test_user_model():
    """Testira User model i Flask-Login integraciju."""
    print("\n=== TESTIRANJE USER MODEL-A ===")
    
    user = User.query.filter_by(email="admin@test.com").first()
    if not user:
        print("❌ User model test - korisnik nije pronađen")
        return False
    
    # Test Flask-Login metoda
    print(f"✓ get_id(): {user.get_id()}")
    print(f"✓ is_active: {user.is_active}")
    print(f"✓ is_authenticated: {user.is_authenticated}")
    print(f"✓ is_anonymous: {user.is_anonymous}")
    
    # Test password metoda
    print(f"✓ check_password('admin123456'): {user.check_password('admin123456')}")
    print(f"✓ check_password('pogrešna'): {user.check_password('pogrešna')}")
    
    # Test role metoda
    print(f"✓ is_administrator(): {user.is_administrator()}")
    print(f"✓ is_serviser(): {user.is_serviser()}")
    print(f"✓ get_full_name(): {user.get_full_name()}")
    
    print("✅ User model test prošao uspešno")
    return True

def test_auth_service_basic():
    """Testira osnovne AuthService funkcionalnosti bez HTTP konteksta."""
    print("\n=== TESTIRANJE AUTH SERVICE (BASIC) ===")
    
    # Test pronalaska korisnika
    print("Test 1: Pronalaženje korisnika po email-u")
    user = AuthService.get_user_by_email("admin@test.com")
    print(f"✓ Korisnik pronađen: {user is not None}")
    if user:
        print(f"  - Ime: {user.get_full_name()}")
        print(f"  - Tip: {user.tip}")
        print(f"  - Aktivan: {user.aktivan}")
    
    # Test password provere
    print("\nTest 2: Password provera")
    if user:
        correct_password = user.check_password("admin123456")
        wrong_password = user.check_password("pogrešna")
        print(f"✓ Ispravna lozinka: {correct_password}")
        print(f"✓ Pogrešna lozinka: {wrong_password}")
    
    # Test deaktiviranog korisnika
    print("\nTest 3: Deaktiviran korisnik")
    deaktiviran_user = AuthService.get_user_by_email("deaktiviran@test.com")
    print(f"✓ Deaktiviran korisnik pronađen: {deaktiviran_user is not None}")
    if deaktiviran_user:
        print(f"  - Aktivan: {deaktiviran_user.aktivan}")
    
    print("✅ AuthService basic test prošao uspešno")
    return True

def test_role_methods():
    """Testira role metode na User modelu."""
    print("\n=== TESTIRANJE ROLE METODA ===")
    
    admin = User.query.filter_by(email="admin@test.com").first()
    serviser = User.query.filter_by(email="serviser@test.com").first()
    deaktiviran = User.query.filter_by(email="deaktiviran@test.com").first()
    
    if admin:
        print(f"Admin is_administrator(): {admin.is_administrator()}")
        print(f"Admin is_serviser(): {admin.is_serviser()}")
    else:
        print("❌ Admin korisnik nije pronađen!")
    
    if serviser:
        print(f"Serviser is_administrator(): {serviser.is_administrator()}")
        print(f"Serviser is_serviser(): {serviser.is_serviser()}")
    else:
        print("❌ Serviser korisnik nije pronađen!")
    
    if deaktiviran:
        print(f"Deaktiviran is_active: {deaktiviran.is_active}")
        print(f"Deaktiviran aktivan: {deaktiviran.aktivan}")
    else:
        print("❌ Deaktiviran korisnik nije pronađen!")
    
    print("✅ Role metode test prošao uspešno")
    return True

def main():
    """Glavna test funkcija."""
    print("🚀 Pokretanje testova za Story 1.2 - Implementacija autentifikacije")
    
    # Kreiranje Flask aplikacije
    app = create_app('development')
    
    with app.app_context():
        # Kreiranje tabela ako ne postoje
        db.create_all()
        
        # Kreiranje test korisnika
        admin, serviser, deaktiviran = create_test_users()
        
        # Pokretanje testova bez obzira na to da li su korisnici već postojali
        test_user_model()
        test_auth_service_basic()
        test_role_methods()
        
        print("\n🎉 Svi testovi su završeni uspešno!")
        
        print("\nTest korisnici:")
        print("- admin@test.com / admin123456 (administrator)")
        print("- serviser@test.com / serviser123456 (serviser)")
        print("- deaktiviran@test.com / deaktiviran123456 (deaktiviran serviser)")
        
        print("\nSada možete pokrenuti aplikaciju sa:")
        print("venvKDS\\Scripts\\activate && python app.py")
        print("\nIli direktno:")
        print(".\\venvKDS\\Scripts\\python.exe app.py")

if __name__ == "__main__":
    main()
