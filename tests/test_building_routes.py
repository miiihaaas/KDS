import unittest
from flask import url_for
from app import create_app, db
from app.models.client import PravnoLice, RadnaJedinica, Objekat, Prostorija
from app.models.user import User

class BuildingRoutesTestCase(unittest.TestCase):
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
        
        # Kreiranje test pravnog lica
        self.pravno_lice = PravnoLice(
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
        db.session.add(self.pravno_lice)
        
        # Kreiranje test radne jedinice
        self.radna_jedinica = RadnaJedinica(
            naziv='Centrala',
            adresa='Test adresa 123',
            mesto='Beograd',
            postanski_broj='11000',
            drzava='Srbija',
            telefon='+381 11 123-4567',
            email='centrala@testkompanija.rs',
            pravno_lice_id=1  # ID će biti 1 nakon commit-a
        )
        db.session.add(self.radna_jedinica)
        
        db.session.commit()
        
        # Kreiranje test objekta
        self.objekat = Objekat(
            naziv='Glavna zgrada',
            opis='Sedište kompanije',
            radna_jedinica_id=self.radna_jedinica.id
        )
        db.session.add(self.objekat)
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
    
    def test_radna_jedinica_list(self):
        """Test prikaza liste radnih jedinica za pravno lice."""
        self.login()
        response = self.client.get(f'/klijenti/pravno-lice/{self.pravno_lice.id}/radne-jedinice', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Centrala', response.data)  # Naziv radne jedinice
    
    def test_radna_jedinica_details(self):
        """Test prikaza detalja radne jedinice."""
        self.login()
        response = self.client.get(f'/klijenti/radna-jedinica/{self.radna_jedinica.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Centrala', response.data)  # Naziv radne jedinice
        self.assertIn(b'Test Kompanija', response.data)  # Naziv pravnog lica
    
    def test_create_radna_jedinica(self):
        """Test kreiranje nove radne jedinice."""
        self.login()
        response = self.client.post(f'/klijenti/pravno-lice/{self.pravno_lice.id}/radne-jedinice/novi', data={
            'naziv': 'Nova radna jedinica',
            'adresa': 'Nova adresa 456',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'kontakt_osoba': 'Marko Marković',
            'telefon': '+381 21 456-7890',
            'email': 'nova@testkompanija.rs',
            'napomena': 'Test napomena'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nova radna jedinica je uspe', response.data)  # Deo flash poruke
        
        # Proveravamo da li je radna jedinica stvarno kreirana u bazi
        rj = RadnaJedinica.query.filter_by(naziv='Nova radna jedinica').first()
        self.assertIsNotNone(rj)
        self.assertEqual(rj.naziv, 'Nova radna jedinica')
        self.assertEqual(rj.pravno_lice_id, self.pravno_lice.id)
    
    def test_edit_radna_jedinica(self):
        """Test izmene postojeće radne jedinice."""
        self.login()
        response = self.client.post(f'/klijenti/radna-jedinica/{self.radna_jedinica.id}/izmeni', data={
            'naziv': 'Centrala (izmenjeno)',
            'adresa': 'Test adresa 123',
            'mesto': 'Beograd',
            'postanski_broj': '11000',
            'drzava': 'Srbija',
            'kontakt_osoba': 'Novi kontakt',
            'telefon': '+381 11 123-4567',
            'email': 'centrala@testkompanija.rs',
            'napomena': 'Izmenjena napomena'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'uspe', response.data)  # Deo flash poruke o uspešnoj izmeni
        
        # Proveravamo da li su podaci stvarno promenjeni u bazi
        rj = RadnaJedinica.query.get(self.radna_jedinica.id)
        self.assertEqual(rj.naziv, 'Centrala (izmenjeno)')
        self.assertEqual(rj.kontakt_osoba, 'Novi kontakt')
    
    def test_objekat_list(self):
        """Test prikaza liste objekata za radnu jedinicu."""
        self.login()
        response = self.client.get(f'/klijenti/radna-jedinica/{self.radna_jedinica.id}/objekti', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Glavna zgrada', response.data)  # Naziv objekta
    
    def test_objekat_details(self):
        """Test prikaza detalja objekta."""
        self.login()
        response = self.client.get(f'/klijenti/objekat/{self.objekat.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Glavna zgrada', response.data)  # Naziv objekta
        self.assertIn(b'Centrala', response.data)  # Naziv radne jedinice
    
    def test_create_objekat(self):
        """Test kreiranje novog objekta."""
        self.login()
        response = self.client.post(f'/klijenti/radna-jedinica/{self.radna_jedinica.id}/objekti/novi', data={
            'naziv': 'Novi objekat',
            'opis': 'Opis novog objekta'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Novi objekat je uspe', response.data)  # Deo flash poruke
        
        # Proveravamo da li je objekat stvarno kreiran u bazi
        obj = Objekat.query.filter_by(naziv='Novi objekat').first()
        self.assertIsNotNone(obj)
        self.assertEqual(obj.naziv, 'Novi objekat')
        self.assertEqual(obj.opis, 'Opis novog objekta')
        self.assertEqual(obj.radna_jedinica_id, self.radna_jedinica.id)
    
    def test_edit_objekat(self):
        """Test izmene postojećeg objekta."""
        self.login()
        response = self.client.post(f'/klijenti/objekat/{self.objekat.id}/izmeni', data={
            'naziv': 'Glavna zgrada (izmenjeno)',
            'opis': 'Izmenjeni opis sedišta kompanije'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Objekat je uspe', response.data)  # Deo flash poruke
        
        # Proveravamo da li su podaci stvarno promenjeni u bazi
        obj = Objekat.query.get(self.objekat.id)
        self.assertEqual(obj.naziv, 'Glavna zgrada (izmenjeno)')
        self.assertEqual(obj.opis, 'Izmenjeni opis sedišta kompanije')
    
    def test_delete_objekat(self):
        """Test brisanja objekta."""
        self.login()
        response = self.client.post(f'/klijenti/objekat/{self.objekat.id}/obrisi', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'uspe', response.data)  # Deo flash poruke o uspešnom brisanju
        
        # Proveravamo da li je objekat stvarno obrisan iz baze
        obj = Objekat.query.get(self.objekat.id)
        self.assertIsNone(obj)
    
    def test_prostorija_crud(self):
        """Test CRUD operacija za prostoriju."""
        self.login()
        
        # Kreiranje prostorije
        response = self.client.post(f'/klijenti/objekat/{self.objekat.id}/prostorije/nova', data={
            'naziv': 'Test prostorija',
            'sprat': '1',
            'broj': '101',
            'namena': 'Kancelarija'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nova prostorija je uspe', response.data)  # Deo flash poruke
        
        # Pronalaženje kreirane prostorije
        prostorija = Prostorija.query.filter_by(naziv='Test prostorija').first()
        self.assertIsNotNone(prostorija)
        
        # Pregled detalja prostorije
        response = self.client.get(f'/klijenti/prostorija/{prostorija.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test prostorija', response.data)
        self.assertIn(b'101', response.data)  # Broj prostorije
        
        # Izmena prostorije
        response = self.client.post(f'/klijenti/prostorija/{prostorija.id}/izmeni', data={
            'naziv': 'Test prostorija (izmenjeno)',
            'sprat': '1',
            'broj': '101A',
            'namena': 'Kancelarija direktora'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prostorija je uspe', response.data)  # Deo flash poruke
        
        # Provera izmenjenih podataka u bazi
        prostorija = Prostorija.query.get(prostorija.id)
        self.assertEqual(prostorija.naziv, 'Test prostorija (izmenjeno)')
        self.assertEqual(prostorija.broj, '101A')
        
        # Brisanje prostorije
        response = self.client.post(f'/klijenti/prostorija/{prostorija.id}/obrisi', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'uspe', response.data)  # Deo flash poruke o uspešnom brisanju
        
        # Provera da li je prostorija obrisana
        prostorija = Prostorija.query.get(prostorija.id)
        self.assertIsNone(prostorija)
    
    def test_hierarchy_navigation(self):
        """Test navigacije kroz hijerarhiju entiteta."""
        self.login()
        
        # Kreiranje prostorije za testiranje hijerarhije
        prostorija = Prostorija(
            naziv='Test prostorija',
            sprat='1',
            broj='101',
            namena='Kancelarija',
            objekat_id=self.objekat.id
        )
        db.session.add(prostorija)
        db.session.commit()
        
        # Test navigacije do detalja prostorije
        response = self.client.get(f'/klijenti/prostorija/{prostorija.id}', follow_redirects=True)
        
        # Provera da li su svi elementi hijerarhije vidljivi na stranici
        self.assertIn(b'Test Kompanija', response.data)  # Pravno lice
        self.assertIn(b'Centrala', response.data)  # Radna jedinica
        self.assertIn(b'Glavna zgrada', response.data)  # Objekat
        self.assertIn(b'Test prostorija', response.data)  # Prostorija

if __name__ == '__main__':
    unittest.main()
