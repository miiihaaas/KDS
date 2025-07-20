import unittest
from flask import url_for
from app import create_app, db
from app.models.client import PravnoLice, FizickoLice
from app.models.user import User
import json
from flask_login import login_user

class ClientRoutesTestCase(unittest.TestCase):
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
    
    def test_klijenti_lista_page(self):
        """Test pristupa strani sa listom klijenata."""
        # Prvo se prijavljujemo
        self.login()
        
        # Zatim pristupamo listi klijenata
        response = self.client.get('/klijenti/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lista klijenata', response.data)
        
    def test_novi_klijent_page(self):
        """Test pristupa strani za kreiranje novog klijenta."""
        self.login()
        response = self.client.get('/klijenti/novi', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Izaberite tip klijenta', response.data)
    
    def test_create_pravno_lice(self):
        """Test kreiranje novog pravnog lica kroz formu."""
        self.login()
        
        # Prvo biramo tip klijenta
        response = self.client.post('/klijenti/novi', data={
            'tip_klijenta': 'pravno_lice',
            'submit': 'Nastavi'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Podaci o pravnom licu', response.data)
        
        # Zatim popunjavamo formu za pravno lice
        response = self.client.post('/klijenti/novi/pravno_lice', data={
            'naziv': 'Test Kompanija d.o.o.',
            'pib': '123456789',
            'mb': '12345678',
            'adresa': 'Test adresa 123',
            'mesto': 'Beograd',
            'postanski_broj': '11000',
            'drzava': 'Srbija',
            'telefon': '+381 11 123-4567',
            'email': 'info@testkompanija.rs',
            'submit': 'Sačuvaj'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Klijent je uspe', response.data)  # Deo flash poruke
        
        # Proveravamo da li je klijent stvarno kreiran u bazi
        pravno_lice = PravnoLice.query.filter_by(pib='123456789').first()
        self.assertIsNotNone(pravno_lice)
        self.assertEqual(pravno_lice.naziv, 'Test Kompanija d.o.o.')
    
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
        self.assertIn(b'Klijent je uspe', response.data)  # Deo flash poruke
        
        # Proveravamo da li je klijent stvarno kreiran u bazi
        fizicko_lice = FizickoLice.query.filter_by(email='marko@example.com').first()
        self.assertIsNotNone(fizicko_lice)
        self.assertEqual(fizicko_lice.ime, 'Marko')
        self.assertEqual(fizicko_lice.prezime, 'Marković')
    
    def test_view_client_details(self):
        """Test prikaza detalja klijenta."""
        # Prvo kreiramo klijenta direktno u bazi
        pravno_lice = PravnoLice(
            tip='pravno_lice',
            naziv='Test Kompanija',
            pib='123456789',
            mb='12345678',
            adresa='Test adresa 123',
            mesto='Beograd',
            postanski_broj='11000',
            drzava='Srbija',
            telefon='+381 11 123-4567',
            email='info@testkompanija.rs'
        )
        
        db.session.add(pravno_lice)
        db.session.commit()
        
        # Prijavljujemo se i pristupamo detaljima
        self.login()
        response = self.client.get(f'/klijenti/{pravno_lice.id}', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Kompanija', response.data)
        self.assertIn(b'123456789', response.data)  # PIB
    
    def test_edit_client(self):
        """Test izmene postojećeg klijenta."""
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
        self.assertIn(b'Izmena podataka', response.data)
        
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
        self.assertIn(b'uspe', response.data)  # Deo poruke o uspešnom ažuriranju
        
        # Proveravamo da li su podaci stvarno promenjeni u bazi
        updated = FizickoLice.query.get(fizicko_lice.id)
        self.assertEqual(updated.prezime, 'Petrović-Njegoš')
    
    def test_ajax_search(self):
        """Test AJAX pretrage klijenata."""
        # Kreiramo nekoliko klijenata
        pravno_lice1 = PravnoLice(
            tip='pravno_lice',
            naziv='Telekom Srbija',
            pib='100001111',
            mb='10001111',
            adresa='Takovska 2',
            mesto='Beograd',
            postanski_broj='11000',
            drzava='Srbija',
            telefon='+381 11 111-1111',
            email='office@telekom.rs'
        )
        
        pravno_lice2 = PravnoLice(
            tip='pravno_lice',
            naziv='Informatika AD',
            pib='100002222',
            mb='10002222',
            adresa='Jevrejska 32',
            mesto='Beograd',
            postanski_broj='11000',
            drzava='Srbija',
            telefon='+381 11 222-2222',
            email='office@informatika.rs'
        )
        
        db.session.add_all([pravno_lice1, pravno_lice2])
        db.session.commit()
        
        # Prijavljujemo se i testiramo AJAX pretragu
        self.login()
        
        # Testiramo AJAX endpoint za pretragu
        response = self.client.get('/klijenti/pretraga?term=telekom', 
                                  headers={'X-Requested-With': 'XMLHttpRequest'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['naziv'], 'Telekom Srbija')
        
        # Testiramo pretragu koja vraća više rezultata
        response = self.client.get('/klijenti/pretraga?term=beograd', 
                              headers={'X-Requested-With': 'XMLHttpRequest'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        print(f"DEBUGING AJAX TEST: Odgovor za pretragu 'beograd': {data}")
        
        self.assertEqual(len(data), 2)  # Oba klijenta su iz Beograda

if __name__ == '__main__':
    unittest.main()
