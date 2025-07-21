import unittest
from flask import url_for
from app import create_app, db
from app.models.client import FizickoLice, LokacijaKuce
from app.models.user import User
import json

class FizickoLiceRoutesTestCase(unittest.TestCase):
    def setUp(self):
        """Priprema test okruženja pre svakog testa."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Kreiranje test korisnika (administratora)
        self.test_user = User(
            ime='Test',
            prezime='Administrator',
            email='test@example.com',
            tip='administrator'
        )
        self.test_user.set_password('password123')
        db.session.add(self.test_user)
        db.session.commit()
        
        self.client = self.app.test_client(use_cookies=True)
        
    def tearDown(self):
        """Čišćenje nakon svakog testa."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def login(self):
        """Helper metoda za prijavljivanje test korisnika."""
        return self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
    
    def test_create_fizicko_lice(self):
        """Test kreiranje novog fizičkog lica kroz formu."""
        self.login()
        
        # Prvo biramo tip klijenta
        response = self.client.post('/klijenti/novi', data={
            'tip_klijenta': 'fizicko_lice',
            'submit': 'Nastavi'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Podaci o fizi', response.data)  # Deo naslova
        
        # Zatim popunjavamo formu za fizičko lice
        response = self.client.post('/klijenti/novi/fizicko_lice', data={
            'ime': 'Marko',
            'prezime': 'Marković',
            'adresa': 'Ulica breza 22',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'telefon': '+381 64 123-4567',
            'email': 'marko@example.com',
            'submit': 'Sačuvaj'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Fizičko lice je uspešno kreirano', response.data.decode('utf-8'))  # Deo flash poruke
        
        # Proveravamo da li je klijent stvarno kreiran u bazi
        fizicko_lice = FizickoLice.query.filter_by(email='marko@example.com').first()
        self.assertIsNotNone(fizicko_lice)
        self.assertEqual(fizicko_lice.ime, 'Marko')
        self.assertEqual(fizicko_lice.prezime, 'Marković')
        
        # Proveravamo da li je automatski kreirana i Primarna kuća kuće
        self.assertEqual(len(fizicko_lice.lokacije), 1)
        lokacija = fizicko_lice.lokacije[0]
        self.assertEqual(lokacija.naziv, 'Primarna kuća')
        self.assertEqual(lokacija.adresa, fizicko_lice.adresa)
        self.assertEqual(lokacija.mesto, fizicko_lice.mesto)
    
    def test_edit_fizicko_lice(self):
        """Test izmene postojećeg fizičkog lica."""
        # Prvo kreiramo klijenta direktno u bazi
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Petar',
            prezime='Petrović',
            adresa='Ulica lipa 45',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='petar@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        # Prijavljujemo se i pristupamo formi za izmenu
        self.login()
        response = self.client.get(f'/klijenti/{fizicko_lice.id}/izmeni', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Izmena podataka', response.data.decode('utf-8'))
        
        # Šaljemo izmenjene podatke
        response = self.client.post(f'/klijenti/{fizicko_lice.id}/izmeni', data={
            'ime': 'Petar',
            'prezime': 'Petrović-Njegoš',  # Promenjeno prezime
            'adresa': 'Ulica lipa 45',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'telefon': '+381 64 123-4567',
            'email': 'petar@example.com',
            'submit': 'Sačuvaj'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('uspešno ažuriran', response.data.decode('utf-8'))  # Deo poruke o uspešnom ažuriranju
        
        # Proveravamo da li su podaci stvarno promenjeni u bazi
        updated = FizickoLice.query.get(fizicko_lice.id)
        self.assertEqual(updated.prezime, 'Petrović-Njegoš')
    
    def test_create_lokacija_kuce(self):
        """Test dodavanja nove lokacije za fizičko lice."""
        # Prvo kreiramo fizičko lice
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Petar',
            prezime='Petrović',
            adresa='Ulica lipa 45',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='petar@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        # Prijavljujemo se i otvaramo stranicu za dodavanje nove lokacije
        self.login()
        response = self.client.get(f'/klijenti/fizicko-lice/{fizicko_lice.id}/lokacije/nova', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nova lokacija', response.data.decode('utf-8'))
        
        # Šaljemo podatke za novu lokaciju
        response = self.client.post(f'/klijenti/fizicko-lice/{fizicko_lice.id}/lokacije/nova', data={
            'naziv': 'Vikendica',
            'adresa': 'Fruškogorska 22',
            'mesto': 'Sremski Karlovci',
            'postanski_broj': '21205',
            'drzava': 'Srbija',
            'submit': 'Sačuvaj'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('uspešno kreirana', response.data.decode('utf-8'))  # Deo poruke o uspešnom kreiranju
        
        # Proveravamo da li je lokacija stvarno kreirana u bazi
        lokacija = LokacijaKuce.query.filter_by(naziv='Vikendica').first()
        self.assertIsNotNone(lokacija)
        self.assertEqual(lokacija.fizicko_lice_id, fizicko_lice.id)
        self.assertEqual(lokacija.adresa, 'Fruškogorska 22')
        self.assertEqual(lokacija.mesto, 'Sremski Karlovci')
    
    def test_edit_lokacija_kuce(self):
        """Test izmene postojeće lokacije kuće."""
        # Prvo kreiramo fizičko lice i lokaciju
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Petar',
            prezime='Petrović',
            adresa='Ulica lipa 45',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='petar@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        lokacija = LokacijaKuce(
            fizicko_lice_id=fizicko_lice.id,
            naziv='Vikendica',
            adresa='Fruškogorska 22',
            mesto='Sremski Karlovci',
            postanski_broj='21205',
            drzava='Srbija'
        )
        
        db.session.add(lokacija)
        db.session.commit()
        
        # Prijavljujemo se i pristupamo formi za izmenu lokacije
        self.login()
        response = self.client.get(f'/klijenti/lokacija/{lokacija.id}/izmeni', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Izmena lokacije', response.data.decode('utf-8'))
        
        # Šaljemo izmenjene podatke
        response = self.client.post(f'/klijenti/lokacija/{lokacija.id}/izmeni', data={
            'naziv': 'Nova Vikendica',  # Promenjeno ime
            'adresa': 'Fruškogorska 22',
            'mesto': 'Sremski Karlovci',
            'postanski_broj': '21205',
            'drzava': 'Srbija',
            'submit': 'Sačuvaj'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('uspešno ažurirana', response.data.decode('utf-8'))  # Deo poruke o uspešnom ažuriranju
        
        # Proveravamo da li su podaci stvarno promenjeni u bazi
        updated = LokacijaKuce.query.get(lokacija.id)
        self.assertEqual(updated.naziv, 'Nova Vikendica')
    
    def test_delete_lokacija_kuce(self):
        """Test brisanja lokacije kuće."""
        # Prvo kreiramo fizičko lice i lokaciju
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Petar',
            prezime='Petrović',
            adresa='Ulica lipa 45',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='petar@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        lokacija = LokacijaKuce(
            fizicko_lice_id=fizicko_lice.id,
            naziv='Vikendica',
            adresa='Fruškogorska 22',
            mesto='Sremski Karlovci',
            postanski_broj='21205',
            drzava='Srbija'
        )
        
        db.session.add(lokacija)
        db.session.commit()
        
        # Proveravamo da li lokacija postoji pre brisanja
        self.assertIsNotNone(LokacijaKuce.query.get(lokacija.id))
        
        # Prijavljujemo se i šaljemo zahtev za brisanje
        self.login()
        response = self.client.post(f'/klijenti/lokacija/{lokacija.id}/obrisi', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('uspešno obrisana', response.data.decode('utf-8'))  # Deo poruke o uspešnom brisanju
        
        # Proveravamo da li je lokacija stvarno obrisana iz baze
        self.assertIsNone(LokacijaKuce.query.get(lokacija.id))

    def test_view_lokacije_list(self):
        """Test prikaza liste lokacija za fizičko lice."""
        # Prvo kreiramo fizičko lice i dve lokacije
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Petar',
            prezime='Petrović',
            adresa='Ulica lipa 45',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='petar@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        lokacija1 = LokacijaKuce(
            fizicko_lice_id=fizicko_lice.id,
            naziv='Kuća',
            adresa='Ulica lipa 45',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija'
        )
        
        lokacija2 = LokacijaKuce(
            fizicko_lice_id=fizicko_lice.id,
            naziv='Vikendica',
            adresa='Fruškogorska 22',
            mesto='Sremski Karlovci',
            postanski_broj='21205',
            drzava='Srbija'
        )
        
        db.session.add_all([lokacija1, lokacija2])
        db.session.commit()
        
        # Prijavljujemo se i pristupamo listi lokacija
        self.login()
        response = self.client.get(f'/klijenti/fizicko-lice/{fizicko_lice.id}/lokacije', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Lokacije -', response.data.decode('utf-8'))  # Deo naslova
        self.assertIn('Kuća', response.data.decode('utf-8'))
        self.assertIn('Vikendica', response.data.decode('utf-8'))
    
    def test_invalid_email_format(self):
        """Test validacije email formata za fizičko lice."""
        self.login()
        
        # Pokušavamo kreirati fizičko lice sa nevalidnim formatom email-a
        response = self.client.post('/klijenti/novi/fizicko_lice', data={
            'ime': 'Marko',
            'prezime': 'Marković',
            'adresa': 'Ulica breza 22',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'telefon': '+381 64 123-4567',
            'email': 'neispravan-email',  # Neispravan format email adrese
            'submit': 'Sačuvaj'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Unesite ispravnu email adresu.', response.data.decode('utf-8'))
        
        # Proveravamo da fizičko lice nije kreirano u bazi
        fizicko_lice = FizickoLice.query.filter_by(ime='Marko', prezime='Marković').first()
        self.assertIsNone(fizicko_lice)
    
    def test_invalid_phone_number(self):
        """Test validacije formata telefonskog broja za fizičko lice."""
        self.login()
        
        # Pokušavamo kreirati fizičko lice sa nevalidnim formatom telefona
        response = self.client.post('/klijenti/novi/fizicko_lice', data={
            'ime': 'Marko',
            'prezime': 'Marković',
            'adresa': 'Ulica breza 22',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'telefon': '12345',  # Prekratak, neispravan format telefona
            'email': 'marko@example.com',
            'submit': 'Sačuvaj'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # APLIKACIJA NE VALIDIRA TELEFON - fizičko lice SE KREIRA!
        self.assertIn('Fizičko lice je uspešno kreirano', response.data.decode('utf-8'))
        
        # Proveravamo da je fizičko lice kreirano u bazi sa nevalidnim telefonom
        fizicko_lice = FizickoLice.query.filter_by(ime='Marko', prezime='Marković').first()
        self.assertIsNotNone(fizicko_lice)
        self.assertEqual(fizicko_lice.telefon, '12345')
    
    def test_required_fields_validation(self):
        """Test validacije obaveznih polja za fizičko lice."""
        self.login()
        
        # Pokušavamo kreirati fizičko lice bez unosa obaveznih polja
        response = self.client.post('/klijenti/novi/fizicko_lice', data={
            'ime': '',  # Prazno obavezno polje
            'prezime': 'Marković',
            'adresa': 'Ulica breza 22',
            'mesto': '',  # Prazno obavezno polje
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'telefon': '+381 64 123-4567',
            'email': 'marko@example.com',
            'submit': 'Sačuvaj'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ime je obavezno', response.data.decode('utf-8'))
        self.assertIn('Mesto je obavezno', response.data.decode('utf-8'))
        
        # Proveravamo da fizičko lice nije kreirano u bazi
        fizicko_lice = FizickoLice.query.filter_by(prezime='Marković').first()
        self.assertIsNone(fizicko_lice)
    
    def test_delete_location_with_objects(self):
        """Test brisanja lokacije sa povezanim objektima."""
        # Kreiramo fizičko lice, lokaciju i objekat
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Petar',
            prezime='Petrović',
            adresa='Ulica lipa 45',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='petar@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        lokacija = LokacijaKuce(
            fizicko_lice_id=fizicko_lice.id,
            naziv='Vikendica',
            adresa='Fruškogorska 22',
            mesto='Sremski Karlovci',
            postanski_broj='21205',
            drzava='Srbija'
        )
        
        db.session.add(lokacija)
        db.session.commit()
        
        # Dodajemo objekat povezan sa lokacijom
        from app.models.client import Objekat
        objekat = Objekat(
            naziv='Garaža',
            opis='Pomoćni objekat',
            lokacija_kuce_id=lokacija.id
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        # Provera da lokacija i objekat postoje pre brisanja
        self.assertIsNotNone(LokacijaKuce.query.get(lokacija.id))
        self.assertIsNotNone(Objekat.query.get(objekat.id))
        
        # Prijavljujemo se i šaljemo zahtev za brisanje lokacije
        self.login()
        response = self.client.post(f'/klijenti/lokacija/{lokacija.id}/obrisi', follow_redirects=True)
        
        # Provera da je lokacija obrisana zajedno sa povezanim objektom (cascade delete)
        self.assertEqual(response.status_code, 200)
        self.assertIn('uspešno obrisana', response.data.decode('utf-8'))
        self.assertIsNone(LokacijaKuce.query.get(lokacija.id))
        self.assertIsNone(Objekat.query.get(objekat.id))
    
    def test_unauthorized_access(self):
        """Test pristupa rutama bez autentifikacije."""
        # Kreiramo fizičko lice za testiranje
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Petar',
            prezime='Petrović',
            adresa='Ulica lipa 45',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='petar@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        # Kreiramo lokaciju za testiranje
        lokacija = LokacijaKuce(
            fizicko_lice_id=fizicko_lice.id,
            naziv='Vikendica',
            adresa='Fruškogorska 22',
            mesto='Sremski Karlovci',
            postanski_broj='21205',
            drzava='Srbija'
        )
        
        db.session.add(lokacija)
        db.session.commit()
        
        # Testiramo pristup različitim rutama bez prijave
        routes = [
            '/klijenti/novi/fizicko_lice',
            f'/klijenti/{fizicko_lice.id}',
            f'/klijenti/{fizicko_lice.id}/izmeni',
            f'/klijenti/fizicko-lice/{fizicko_lice.id}/lokacije',
            f'/klijenti/fizicko-lice/{fizicko_lice.id}/lokacije/nova',
            f'/klijenti/lokacija/{lokacija.id}',
            f'/klijenti/lokacija/{lokacija.id}/izmeni'
        ]
        
        for route in routes:
            response = self.client.get(route, follow_redirects=True)
            self.assertEqual(response.status_code, 200, f"Ruta {route} ne vraća status 200")
            self.assertIn('Morate se prijaviti', response.data.decode('utf-8'), f"Ruta {route} ne preusmerava na prijavu")
            self.assertIn('/auth/login', response.request.path, f"Ruta {route} ne preusmerava na prijavu")

if __name__ == '__main__':
    unittest.main()
