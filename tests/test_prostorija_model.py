import unittest
from app import create_app, db
from app.models.client import Objekat, Prostorija
from datetime import datetime

class ProstorijaModelTestCase(unittest.TestCase):
    def setUp(self):
        """Priprema test okruženja pre svakog testa."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Kreiranje objekta za testove
        self.objekat = Objekat(
            naziv='Test objekat',
            opis='Test opis'
        )
        
        db.session.add(self.objekat)
        db.session.commit()
        
    def tearDown(self):
        """Čišćenje nakon svakog testa."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_prostorija_sa_nazivom_i_oznakom(self):
        """Test kreiranje prostorije sa nazivom i numeričkom oznakom."""
        prostorija = Prostorija(
            naziv='Kancelarija direktora',
            numericka_oznaka='A-101',
            sprat='1',
            namena='Kancelarija',
            objekat_id=self.objekat.id
        )
        
        db.session.add(prostorija)
        db.session.commit()
        
        retrieved = Prostorija.query.get(prostorija.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.naziv, 'Kancelarija direktora')
        self.assertEqual(retrieved.numericka_oznaka, 'A-101')
        self.assertEqual(retrieved.sprat, '1')
        self.assertEqual(retrieved.namena, 'Kancelarija')
        self.assertEqual(retrieved.objekat_id, self.objekat.id)
        self.assertEqual(retrieved.get_display_name(), 'Kancelarija direktora (A-101)')
        
    def test_prostorija_samo_sa_nazivom(self):
        """Test kreiranje prostorije samo sa nazivom."""
        prostorija = Prostorija(
            naziv='Sala za sastanke',
            sprat='2',
            namena='Sastanci',
            objekat_id=self.objekat.id
        )
        
        db.session.add(prostorija)
        db.session.commit()
        
        retrieved = Prostorija.query.get(prostorija.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.naziv, 'Sala za sastanke')
        self.assertIsNone(retrieved.numericka_oznaka)
        self.assertEqual(retrieved.get_display_name(), 'Sala za sastanke')
        
    def test_prostorija_samo_sa_oznakom(self):
        """Test kreiranje prostorije samo sa numeričkom oznakom."""
        prostorija = Prostorija(
            numericka_oznaka='B-202',
            sprat='2',
            namena='Skladište',
            objekat_id=self.objekat.id
        )
        
        db.session.add(prostorija)
        db.session.commit()
        
        retrieved = Prostorija.query.get(prostorija.id)
        
        self.assertIsNotNone(retrieved)
        self.assertIsNone(retrieved.naziv)
        self.assertEqual(retrieved.numericka_oznaka, 'B-202')
        self.assertEqual(retrieved.get_display_name(), 'B-202')

    def test_prostorija_timestamps(self):
        """Test da li se automatski postavljaju vremenske oznake za prostoriju."""
        prostorija = Prostorija(
            naziv='Test prostorija',
            objekat_id=self.objekat.id
        )
        
        before_create = datetime.utcnow()
        db.session.add(prostorija)
        db.session.commit()
        after_create = datetime.utcnow()
        
        self.assertIsNotNone(prostorija.created_at)
        self.assertIsNotNone(prostorija.updated_at)
        self.assertTrue(before_create <= prostorija.created_at <= after_create)
        self.assertTrue(before_create <= prostorija.updated_at <= after_create)

    def test_cascade_delete_from_objekat(self):
        """Test da li se automatski brišu prostorije kada se obriše objekat."""
        prostorija = Prostorija(
            naziv='Test prostorija',
            objekat_id=self.objekat.id
        )
        
        db.session.add(prostorija)
        db.session.commit()
        
        # Provera da li je prostorija kreirana
        self.assertEqual(Prostorija.query.count(), 1)
        
        # Brisanje objekta
        db.session.delete(self.objekat)
        db.session.commit()
        
        # Provera da li je prostorija takođe obrisana
        self.assertEqual(Prostorija.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
