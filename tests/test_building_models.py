import unittest
from app import create_app, db
from app.models.client import PravnoLice, RadnaJedinica, Objekat, Prostorija
from datetime import datetime

class BuildingModelsTestCase(unittest.TestCase):
    def setUp(self):
        """Priprema test okruženja pre svakog testa."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Kreiranje test podataka koje će koristiti svaki test
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
        db.session.commit()
        
        self.radna_jedinica = RadnaJedinica(
            naziv='Centrala',
            adresa='Test adresa 123',
            mesto='Beograd',
            postanski_broj='11000',
            drzava='Srbija',
            telefon='+381 11 123-4567',
            email='centrala@testkompanija.rs',
            pravno_lice_id=self.pravno_lice.id
        )
        db.session.add(self.radna_jedinica)
        db.session.commit()
        
    def tearDown(self):
        """Čišćenje nakon svakog testa."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_objekat_creation(self):
        """Test kreiranje objekta za radnu jedinicu."""
        objekat = Objekat(
            naziv='Glavna zgrada',
            opis='Sedište kompanije',
            radna_jedinica_id=self.radna_jedinica.id
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        # Provera da li je objekat kreiran i povezan sa radnom jedinicom
        retrieved = Objekat.query.get(objekat.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.naziv, 'Glavna zgrada')
        self.assertEqual(retrieved.opis, 'Sedište kompanije')
        self.assertEqual(retrieved.radna_jedinica_id, self.radna_jedinica.id)
        
        # Provera da li je radna jedinica pravilno povezana sa objektom
        self.assertEqual(len(self.radna_jedinica.objekti), 1)
        self.assertEqual(self.radna_jedinica.objekti[0].naziv, 'Glavna zgrada')
    
    def test_prostorija_creation(self):
        """Test kreiranje prostorije za objekat."""
        objekat = Objekat(
            naziv='Glavna zgrada',
            opis='Sedište kompanije',
            radna_jedinica_id=self.radna_jedinica.id
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        prostorija = Prostorija(
            naziv='Kancelarija direktora',
            sprat='1',
            broj='101',
            namena='Kancelarija',
            objekat_id=objekat.id
        )
        
        db.session.add(prostorija)
        db.session.commit()
        
        # Provera da li je prostorija kreirana i povezana sa objektom
        retrieved = Prostorija.query.get(prostorija.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.naziv, 'Kancelarija direktora')
        self.assertEqual(retrieved.sprat, '1')
        self.assertEqual(retrieved.broj, '101')
        self.assertEqual(retrieved.objekat_id, objekat.id)
        
        # Provera da li je objekat pravilno povezan sa prostorijom
        self.assertEqual(len(objekat.prostorije), 1)
        self.assertEqual(objekat.prostorije[0].naziv, 'Kancelarija direktora')
    
    def test_cascade_delete_objekat(self):
        """Test da li brisanje objekta briše i povezane prostorije (cascade delete)."""
        objekat = Objekat(
            naziv='Glavna zgrada',
            opis='Sedište kompanije',
            radna_jedinica_id=self.radna_jedinica.id
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        prostorija1 = Prostorija(
            naziv='Kancelarija 1',
            sprat='1',
            broj='101',
            namena='Kancelarija',
            objekat_id=objekat.id
        )
        
        prostorija2 = Prostorija(
            naziv='Kancelarija 2',
            sprat='1',
            broj='102',
            namena='Kancelarija',
            objekat_id=objekat.id
        )
        
        db.session.add_all([prostorija1, prostorija2])
        db.session.commit()
        
        # Pamtimo ID-eve za kasnije provere
        prostorija1_id = prostorija1.id
        prostorija2_id = prostorija2.id
        objekat_id = objekat.id
        
        # Proveramo da li su prostorije kreirane
        self.assertEqual(Prostorija.query.count(), 2)
        
        # Brišemo objekat
        db.session.delete(objekat)
        db.session.commit()
        
        # Proveravamo da li je objekat obrisan
        self.assertIsNone(Objekat.query.get(objekat_id))
        
        # Proveravamo da li su prostorije obrisane
        self.assertIsNone(Prostorija.query.get(prostorija1_id))
        self.assertIsNone(Prostorija.query.get(prostorija2_id))
        self.assertEqual(Prostorija.query.count(), 0)
    
    def test_cascade_delete_radna_jedinica(self):
        """Test da li brisanje radne jedinice briše i povezane objekte i prostorije (cascade delete)."""
        objekat = Objekat(
            naziv='Glavna zgrada',
            opis='Sedište kompanije',
            radna_jedinica_id=self.radna_jedinica.id
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        prostorija = Prostorija(
            naziv='Kancelarija direktora',
            sprat='1',
            broj='101',
            namena='Kancelarija',
            objekat_id=objekat.id
        )
        
        db.session.add(prostorija)
        db.session.commit()
        
        # Pamtimo ID-eve za kasnije provere
        prostorija_id = prostorija.id
        objekat_id = objekat.id
        
        # Brišemo radnu jedinicu
        db.session.delete(self.radna_jedinica)
        db.session.commit()
        
        # Proveravamo da li su objekat i prostorija obrisani
        self.assertIsNone(Objekat.query.get(objekat_id))
        self.assertIsNone(Prostorija.query.get(prostorija_id))

if __name__ == '__main__':
    unittest.main()
