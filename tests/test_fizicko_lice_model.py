import unittest
from app import create_app, db
from app.models.client import FizickoLice, LokacijaKuce, Objekat, Prostorija
from datetime import datetime

class FizickoLiceModelTestCase(unittest.TestCase):
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
    
    def test_fizicko_lice_creation(self):
        """Test kreiranje fizičkog lica."""
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Marko',
            prezime='Marković',
            adresa='Ulica breza 22',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='marko@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        retrieved = FizickoLice.query.get(fizicko_lice.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.ime, 'Marko')
        self.assertEqual(retrieved.prezime, 'Marković')
        self.assertEqual(retrieved.puno_ime, 'Marko Marković')
        self.assertEqual(retrieved.adresa, 'Ulica breza 22')
        self.assertEqual(retrieved.mesto, 'Novi Sad')
        self.assertEqual(retrieved.email, 'marko@example.com')
    
    def test_lokacija_kuce_creation(self):
        """Test kreiranje lokacije za fizičko lice."""
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Marko',
            prezime='Marković',
            adresa='Ulica breza 22',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='marko@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        lokacija = LokacijaKuce(
            fizicko_lice_id=fizicko_lice.id,
            naziv='Vikendica',
            adresa='Fruškogorska 22',
            mesto='Sremski Karlovci',
            postanski_broj='21205',
            drzava='Srbija',
            napomena='Vikendica na Fruškoj gori'
        )
        
        db.session.add(lokacija)
        db.session.commit()
        
        # Provera da li je lokacija kreirana i povezana sa fizičkim licem
        self.assertEqual(lokacija.fizicko_lice_id, fizicko_lice.id)
        self.assertEqual(len(fizicko_lice.lokacije), 1)
        self.assertEqual(fizicko_lice.lokacije[0].naziv, 'Vikendica')
        self.assertEqual(fizicko_lice.lokacije[0].adresa, 'Fruškogorska 22')

    def test_timestamps_lokacija_kuce(self):
        """Test da li se automatski postavljaju vremenske oznake za lokaciju kuće."""
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Marko',
            prezime='Marković',
            adresa='Ulica breza 22',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='marko@example.com'
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
        
        before_create = datetime.utcnow()
        db.session.add(lokacija)
        db.session.commit()
        after_create = datetime.utcnow()
        
        # Provera da li je created_at postavljen automatski
        self.assertIsNotNone(lokacija.created_at)
        self.assertIsNotNone(lokacija.updated_at)
        
        # Provera da li je created_at između vremena pre i posle kreiranja
        self.assertTrue(before_create <= lokacija.created_at <= after_create)
        self.assertTrue(before_create <= lokacija.updated_at <= after_create)

    def test_hijerarhija_fizicko_lice_lokacija_objekat_prostorija(self):
        """Test hijerarhijske strukture: Fizičko lice > Lokacija kuće > Objekat > Prostorija"""
        # Kreiranje fizičkog lica
        fizicko_lice = FizickoLice(
            tip='fizicko_lice',
            ime='Marko',
            prezime='Marković',
            adresa='Ulica breza 22',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 64 123-4567',
            email='marko@example.com'
        )
        
        db.session.add(fizicko_lice)
        db.session.commit()
        
        # Kreiranje lokacije
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
        
        # Kreiranje objekta
        objekat = Objekat(
            lokacija_kuce_id=lokacija.id,
            naziv='Kuća',
            opis='Glavna kuća'
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        # Kreiranje prostorije
        prostorija = Prostorija(
            objekat_id=objekat.id,
            naziv='Dnevna soba',
            sprat='Prizemlje',
            broj='1',
            namena='Boravak'
        )
        
        db.session.add(prostorija)
        db.session.commit()
        
        # Provera relacija
        self.assertEqual(prostorija.objekat_id, objekat.id)
        self.assertEqual(objekat.lokacija_kuce_id, lokacija.id)
        self.assertEqual(lokacija.fizicko_lice_id, fizicko_lice.id)
        
        # Provera navigacije kroz relacije
        self.assertEqual(prostorija.objekat.naziv, 'Kuća')
        self.assertEqual(objekat.lokacija_kuce.naziv, 'Vikendica')
        self.assertEqual(lokacija.fizicko_lice.puno_ime, 'Marko Marković')
        
        # Provera broja objekata u lokaciji
        self.assertEqual(len(lokacija.objekti), 1)
        
        # Provera broja prostorija u objektu
        self.assertEqual(len(objekat.prostorije), 1)
        
if __name__ == '__main__':
    unittest.main()
