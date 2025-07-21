import unittest
from app import create_app, db
from app.models.client import PravnoLice, FizickoLice, RadnaJedinica, LokacijaKuce, Objekat, Prostorija
from datetime import datetime

class ObjekatModelTestCase(unittest.TestCase):
    def setUp(self):
        """Priprema test okruženja pre svakog testa."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Kreiranje pravnog lica za testove
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
        
        # Kreiranje fizičkog lica za testove
        self.fizicko_lice = FizickoLice(
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
        
        db.session.add(self.pravno_lice)
        db.session.add(self.fizicko_lice)
        db.session.commit()
        
        # Kreiranje radne jedinice za testove
        self.radna_jedinica = RadnaJedinica(
            naziv='Ogranak Novi Beograd',
            adresa='Bulevar Mihajla Pupina 10',
            mesto='Beograd',
            postanski_broj='11070',
            telefon='+381 11 222-3333',
            kontakt_osoba='Jovan Jovanović',
            pravno_lice_id=self.pravno_lice.id
        )
        
        # Kreiranje lokacije kuće za testove
        self.lokacija_kuce = LokacijaKuce(
            naziv='Vikendica',
            adresa='Fruškogorska 22',
            mesto='Sremski Karlovci',
            postanski_broj='21205',
            fizicko_lice_id=self.fizicko_lice.id
        )
        
        db.session.add(self.radna_jedinica)
        db.session.add(self.lokacija_kuce)
        db.session.commit()
        
    def tearDown(self):
        """Čišćenje nakon svakog testa."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_objekat_za_radnu_jedinicu(self):
        """Test kreiranje objekta povezanog sa radnom jedinicom."""
        objekat = Objekat(
            naziv='Upravna zgrada',
            opis='Glavna zgrada kompanije',
            radna_jedinica_id=self.radna_jedinica.id
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        retrieved = Objekat.query.get(objekat.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.naziv, 'Upravna zgrada')
        self.assertEqual(retrieved.opis, 'Glavna zgrada kompanije')
        self.assertEqual(retrieved.radna_jedinica_id, self.radna_jedinica.id)
        self.assertIsNone(retrieved.lokacija_kuce_id)
        self.assertEqual(retrieved.get_parent_type(), 'radna_jedinica')
        self.assertEqual(retrieved.get_parent().id, self.radna_jedinica.id)
        
    def test_objekat_za_lokaciju_kuce(self):
        """Test kreiranje objekta povezanog sa lokacijom kuće."""
        objekat = Objekat(
            naziv='Pomoćni objekat',
            opis='Garaža i ostava',
            lokacija_kuce_id=self.lokacija_kuce.id
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        retrieved = Objekat.query.get(objekat.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.naziv, 'Pomoćni objekat')
        self.assertEqual(retrieved.opis, 'Garaža i ostava')
        self.assertEqual(retrieved.lokacija_kuce_id, self.lokacija_kuce.id)
        self.assertIsNone(retrieved.radna_jedinica_id)
        self.assertEqual(retrieved.get_parent_type(), 'lokacija_kuce')
        self.assertEqual(retrieved.get_parent().id, self.lokacija_kuce.id)

    def test_objekat_timestamps(self):
        """Test da li se automatski postavljaju vremenske oznake za objekat."""
        objekat = Objekat(
            naziv='Test Objekat',
            opis='Test opis',
            radna_jedinica_id=self.radna_jedinica.id
        )
        
        before_create = datetime.utcnow()
        db.session.add(objekat)
        db.session.commit()
        after_create = datetime.utcnow()
        
        self.assertIsNotNone(objekat.created_at)
        self.assertIsNotNone(objekat.updated_at)
        self.assertTrue(before_create <= objekat.created_at <= after_create)
        self.assertTrue(before_create <= objekat.updated_at <= after_create)

    def test_cascade_delete_from_radna_jedinica(self):
        """Test da li se automatski brišu objekti kada se obriše radna jedinica."""
        objekat = Objekat(
            naziv='Kancelarijska zgrada',
            opis='Kancelarije',
            radna_jedinica_id=self.radna_jedinica.id
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        # Provera da li je objekat kreiran
        self.assertEqual(Objekat.query.count(), 1)
        
        # Brisanje radne jedinice
        db.session.delete(self.radna_jedinica)
        db.session.commit()
        
        # Provera da li je objekat takođe obrisan
        self.assertEqual(Objekat.query.count(), 0)

    def test_cascade_delete_from_lokacija_kuce(self):
        """Test da li se automatski brišu objekti kada se obriše lokacija kuće."""
        objekat = Objekat(
            naziv='Glavni objekat',
            opis='Kuća',
            lokacija_kuce_id=self.lokacija_kuce.id
        )
        
        db.session.add(objekat)
        db.session.commit()
        
        # Provera da li je objekat kreiran
        self.assertEqual(Objekat.query.count(), 1)
        
        # Brisanje lokacije kuće
        db.session.delete(self.lokacija_kuce)
        db.session.commit()
        
        # Provera da li je objekat takođe obrisan
        self.assertEqual(Objekat.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
