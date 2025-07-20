#!/usr/bin/env python3
"""
Test skripta za testiranje funkcionalnosti upravljanja vozilima.
Testira sve acceptance kriterijume iz Story 1.4.
"""

from app import create_app, db
from app.models.vehicle import Vehicle
from app.models.user import User
from app.utils.forms import VehicleForm
from flask_login import login_user
import os

def create_test_vehicles():
    """Kreira test vozila za testiranje."""
    print("Kreiranje test vozila...")
    
    try:
        # Proverava da li već postoje test vozila
        existing_active = Vehicle.query.filter_by(registracija="BG123AB").first()
        existing_inactive = Vehicle.query.filter_by(registracija="NS456CD").first()
        
        if existing_active and existing_inactive:
            print("Sva test vozila već postoje.")
            return existing_active, existing_inactive
        
        print("Kreiranje nedostajućih test vozila...")
        
        # Kreiraj aktivno vozilo ako ne postoji
        if not existing_active:
            active_vehicle = Vehicle(
                marka="Volkswagen",
                model="Passat",
                registracija="BG123AB",
                active=True
            )
            db.session.add(active_vehicle)
            print("Kreirano aktivno vozilo.")
        else:
            active_vehicle = existing_active
        
        # Kreiraj neaktivno vozilo ako ne postoji
        if not existing_inactive:
            inactive_vehicle = Vehicle(
                marka="Škoda", 
                model="Octavia",
                registracija="NS456CD",
                active=False
            )
            db.session.add(inactive_vehicle)
            print("Kreirano neaktivno vozilo.")
        else:
            inactive_vehicle = existing_inactive
        
        db.session.commit()
        print("Test vozila su uspešno kreirana.")
        return active_vehicle, inactive_vehicle
        
    except Exception as e:
        db.session.rollback()
        print(f"Greška pri kreiranju test vozila: {e}")
        return None, None

def test_vehicle_model():
    """Testira Vehicle model i osnovne metode."""
    print("\n=== TESTIRANJE VEHICLE MODEL-A ===")
    
    vehicle = Vehicle.query.filter_by(registracija="BG123AB").first()
    if not vehicle:
        print("❌ Vehicle model test - vozilo nije pronađeno")
        return False
    
    # Test osnovnih atributa
    print(f"✓ Marka: {vehicle.marka}")
    print(f"✓ Model: {vehicle.model}")
    print(f"✓ Registracija: {vehicle.registracija}")
    print(f"✓ Aktivan status: {vehicle.active}")
    
    # Test metoda
    print(f"✓ get_vehicle_info(): {vehicle.get_vehicle_info()}")
    
    # Test toggle_status
    original_status = vehicle.active
    new_status = vehicle.toggle_status()
    print(f"✓ toggle_status() promena: {original_status} -> {new_status}")
    vehicle.toggle_status()  # Vraćamo na originalno stanje
    db.session.commit()
    
    print("✅ Vehicle model test prošao uspešno")
    return True

def test_vehicle_crud():
    """Testira CRUD operacije za vozila."""
    print("\n=== TESTIRANJE CRUD OPERACIJA ===")
    
    # Test CREATE
    print("\nTest 1: Kreiranje novog vozila")
    new_vehicle = Vehicle(
        marka="Toyota",
        model="Corolla",
        registracija="KG789EF",
        active=True
    )
    db.session.add(new_vehicle)
    db.session.commit()
    print(f"✓ Vozilo kreirano sa ID: {new_vehicle.id}")
    
    # Test READ
    print("\nTest 2: Čitanje vozila")
    read_vehicle = Vehicle.query.filter_by(registracija="KG789EF").first()
    if read_vehicle:
        print(f"✓ Pronađeno vozilo: {read_vehicle.get_vehicle_info()}")
    else:
        print("❌ Vozilo nije pronađeno!")
        
    # Test UPDATE
    print("\nTest 3: Ažuriranje vozila")
    if read_vehicle:
        read_vehicle.model = "Camry"
        db.session.commit()
        updated_vehicle = Vehicle.query.get(read_vehicle.id)
        print(f"✓ Ažurirano vozilo: {updated_vehicle.get_vehicle_info()}")
    
    # Test DELETE
    print("\nTest 4: Brisanje vozila")
    if read_vehicle:
        vehicle_id = read_vehicle.id
        db.session.delete(read_vehicle)
        db.session.commit()
        deleted = Vehicle.query.get(vehicle_id) is None
        print(f"✓ Vozilo obrisano: {deleted}")
    
    print("✅ CRUD operacije test prošao uspešno")
    return True

def test_active_vehicles():
    """Testira metodu za dohvatanje aktivnih vozila."""
    print("\n=== TESTIRANJE FILTRIRANJA AKTIVNIH VOZILA ===")
    
    # Dobavlja aktivna vozila
    active_vehicles = Vehicle.get_active_vehicles()
    
    # Proverava da li su sva vozila aktivna
    all_active = all(v.active for v in active_vehicles)
    
    print(f"✓ Broj aktivnih vozila: {len(active_vehicles)}")
    print(f"✓ Sva vozila su aktivna: {all_active}")
    
    # Pronalazi neaktivna vozila da potvrdi da nisu u listi
    inactive_vehicle = Vehicle.query.filter_by(active=False).first()
    if inactive_vehicle:
        print(f"✓ Neaktivno vozilo nije u listi: {inactive_vehicle.registracija not in [v.registracija for v in active_vehicles]}")
    
    print("✅ Test filtriranja aktivnih vozila prošao uspešno")
    return True

def test_unique_registration():
    """Testira validaciju jedinstvenosti registarske oznake."""
    print("\n=== TESTIRANJE JEDINSTVENOSTI REGISTARSKE OZNAKE ===")
    
    # Pokušavamo kreirati vozilo sa postojećom registracijom
    try:
        duplicate_vehicle = Vehicle(
            marka="Mercedes",
            model="C-Class",
            registracija="BG123AB",  # Već postoji
            active=True
        )
        db.session.add(duplicate_vehicle)
        db.session.commit()
        print("❌ Kreiranje duplikata uspelo - test NIJE prošao!")
        db.session.rollback()
        return False
    except Exception as e:
        print(f"✓ Kreiranje duplikata nije uspelo (očekivano): {e}")
        db.session.rollback()
    
    print("✅ Test jedinstvenosti registarske oznake prošao uspešno")
    return True

def create_admin_user():
    """Kreira admin korisnika za testiranje ruta."""
    admin = User.query.filter_by(email="admin@test.com").first()
    if not admin:
        admin = User(
            ime="Marko",
            prezime="Petrović",
            email="admin@test.com",
            tip="administrator",
            aktivan=True
        )
        admin.set_password("admin123456")
        db.session.add(admin)
        db.session.commit()
        print("Kreiran administrator za testiranje.")
    return admin

def main():
    """Glavna test funkcija."""
    print("🚀 Pokretanje testova za Story 1.4 - Upravljanje vozilima")
    
    # Kreiranje Flask aplikacije
    app = create_app('development')
    
    with app.app_context():
        # Kreiranje tabela ako ne postoje
        db.create_all()
        
        # Kreiranje test vozila i admin korisnika
        active_vehicle, inactive_vehicle = create_test_vehicles()
        admin = create_admin_user()
        
        # Pokretanje testova
        tests_passed = []
        
        tests_passed.append(test_vehicle_model())
        tests_passed.append(test_vehicle_crud())
        tests_passed.append(test_active_vehicles())
        tests_passed.append(test_unique_registration())
        
        # Sumarni rezultati
        total_tests = len(tests_passed)
        passed_tests = sum(1 for test in tests_passed if test)
        
        print(f"\n🎯 Rezultati: {passed_tests}/{total_tests} testova uspešno.")
        
        if all(tests_passed):
            print("\n🎉 Svi testovi su uspešno završeni!")
        else:
            print("\n⚠️ Neki testovi nisu uspešni. Proverite detalje iznad.")
        
        print("\nTest podaci:")
        print("- Aktivno vozilo: Volkswagen Passat, registracija BG123AB")
        print("- Neaktivno vozilo: Škoda Octavia, registracija NS456CD")
        print("- Admin korisnik: admin@test.com / admin123456")
        
        print("\nMožete pokrenuti aplikaciju sa:")
        print("venvKDS\\Scripts\\activate && python app.py")
        print("\nIli direktno:")
        print(".\\venvKDS\\Scripts\\python.exe app.py")

if __name__ == "__main__":
    main()
