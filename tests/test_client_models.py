import unittest
from app import create_app, db
from app.models.client import PravnoLice, FizickoLice, RadnaJedinica, LokacijaKuce
from datetime import datetime

class ClientModelTestCase(unittest.TestCase):
    def setUp(self):
        """Priprema test okruženja pre svakog testa."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        """Čišćenje nakon svakog testa."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_pravno_lice_creation(self):
        """Test kreiranje pravnog lica."""
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
        
        retrieved = PravnoLice.query.get(pravno_lice.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.naziv, 'Test Kompanija')
        self.assertEqual(retrieved.pib, '123456789')
        self.assertEqual(retrieved.mb, '12345678')
        self.assertEqual(retrieved.adresa, 'Test adresa 123')
        self.assertEqual(retrieved.mesto, 'Beograd')
        
    def test_fizicko_lice_creation(self):
        """Test kreiranje fizičkog lica."""
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
        
        retrieved = FizickoLice.query.get(fizicko_lice.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.ime, 'Petar')
        self.assertEqual(retrieved.prezime, 'Petrović')
        self.assertEqual(retrieved.get_full_name(), 'Petar Petrović')
        self.assertEqual(retrieved.adresa, 'Ulica lipa 45')
        
    def test_radna_jedinica_creation(self):
        """Test kreiranje radne jedinice za pravno lice."""
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
        
        radna_jedinica = RadnaJedinica(
            naziv='Ogranak Novi Beograd',
            adresa='Bulevar Mihajla Pupina 10',
            mesto='Beograd',
            postanski_broj='11070',
            telefon='+381 11 222-3333',
            kontakt_osoba='Jovan Jovanović',
            pravno_lice_id=pravno_lice.id
        )
        
        db.session.add(radna_jedinica)
        db.session.commit()
        
        # Provera da li je radna jedinica kreirana i povezana sa pravnim licem
        self.assertEqual(radna_jedinica.pravno_lice_id, pravno_lice.id)
        self.assertEqual(pravno_lice.radne_jedinice.count(), 1)
        self.assertEqual(pravno_lice.radne_jedinice.first().naziv, 'Ogranak Novi Beograd')
        
    def test_lokacija_kuce_creation(self):
        """Test kreiranje lokacije za fizičko lice."""
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
            naziv='Vikendica',
            adresa='Fruškogorska 22',
            mesto='Sremski Karlovci',
            postanski_broj='21205',
            napomena='Vikendica na Fruškoj gori',
            fizicko_lice_id=fizicko_lice.id
        )
        
        db.session.add(lokacija)
        db.session.commit()
        
        # Provera da li je lokacija kreirana i povezana sa fizičkim licem
        self.assertEqual(lokacija.fizicko_lice_id, fizicko_lice.id)
        self.assertEqual(fizicko_lice.lokacije.count(), 1)
        self.assertEqual(fizicko_lice.lokacije.first().naziv, 'Vikendica')
        
    def test_timestamps(self):
        """Test da li se automatski postavljaju vremenske oznake."""
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
        
        before_create = datetime.utcnow()
        db.session.add(pravno_lice)
        db.session.commit()
        after_create = datetime.utcnow()
        
        # Provera da li je created_at postavljen automatski
        self.assertIsNotNone(pravno_lice.created_at)
        self.assertIsNotNone(pravno_lice.updated_at)
        
        # Provera da li je created_at između vremena pre i posle kreiranja
        self.assertTrue(before_create <= pravno_lice.created_at <= after_create)
        self.assertTrue(before_create <= pravno_lice.updated_at <= after_create)

if __name__ == '__main__':
    unittest.main()
