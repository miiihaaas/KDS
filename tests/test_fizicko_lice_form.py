import unittest
from app import create_app
from app.utils.client_forms import FizickoLiceForm, LokacijaKuceForm

class FizickoLiceFormTestCase(unittest.TestCase):
    def setUp(self):
        """Priprema test okruženja pre svakog testa."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        """Čišćenje nakon svakog testa."""
        self.app_context.pop()
    
    def test_fizicko_lice_form_validation(self):
        """Test validacije forme za fizičko lice."""
        # Test sa validnim podacima
        form = FizickoLiceForm(data={
            'ime': 'Petar',
            'prezime': 'Petrović',
            'adresa': 'Ulica lipa 45',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'telefon': '+381 64 123-4567',
            'email': 'petar@example.com'
        })
        
        # Forma bi trebalo da bude validna
        self.assertTrue(form.validate())
        
        # Test sa nedostajućim imenom (obavezno polje)
        form = FizickoLiceForm(data={
            'prezime': 'Petrović',
            'adresa': 'Ulica lipa 45',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'telefon': '+381 64 123-4567',
            'email': 'petar@example.com'
        })
        
        # Forma ne bi trebalo da bude validna
        self.assertFalse(form.validate())
        self.assertIn('ime', form.errors)
        
        # Test sa nedostajućim prezimenom (obavezno polje)
        form = FizickoLiceForm(data={
            'ime': 'Petar',
            'adresa': 'Ulica lipa 45',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'telefon': '+381 64 123-4567',
            'email': 'petar@example.com'
        })
        
        # Forma ne bi trebalo da bude validna
        self.assertFalse(form.validate())
        self.assertIn('prezime', form.errors)
        
        # Test sa nevalidnim email formatom
        form = FizickoLiceForm(data={
            'ime': 'Petar',
            'prezime': 'Petrović',
            'adresa': 'Ulica lipa 45',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000',
            'drzava': 'Srbija',
            'telefon': '+381 64 123-4567',
            'email': 'petar.example.com'  # nevalidan email format
        })
        
        # Forma ne bi trebalo da bude validna zbog email-a
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)
        
        # Test sa nevalidnim poštanskim brojem
        form = FizickoLiceForm(data={
            'ime': 'Petar',
            'prezime': 'Petrović',
            'adresa': 'Ulica lipa 45',
            'mesto': 'Novi Sad',
            'postanski_broj': '21000a',  # sadrži slovo
            'drzava': 'Srbija',
            'telefon': '+381 64 123-4567',
            'email': 'petar@example.com'
        })
        
        # Forma ne bi trebalo da bude validna zbog poštanskog broja
        self.assertFalse(form.validate())
        self.assertIn('postanski_broj', form.errors)
    
    def test_lokacija_kuce_form_validation(self):
        """Test validacije forme za lokaciju kuće."""
        # Test sa validnim podacima
        form = LokacijaKuceForm(data={
            'naziv': 'Vikendica',
            'adresa': 'Fruškogorska 22',
            'mesto': 'Sremski Karlovci',
            'postanski_broj': '21205',
            'drzava': 'Srbija'
        })
        
        # Forma bi trebalo da bude validna
        self.assertTrue(form.validate())
        
        # Test sa nedostajućim nazivom (obavezno polje)
        form = LokacijaKuceForm(data={
            'adresa': 'Fruškogorska 22',
            'mesto': 'Sremski Karlovci',
            'postanski_broj': '21205',
            'drzava': 'Srbija'
        })
        
        # Forma ne bi trebalo da bude validna
        self.assertFalse(form.validate())
        self.assertIn('naziv', form.errors)
        
        # Test sa nedostajućom adresom (obavezno polje)
        form = LokacijaKuceForm(data={
            'naziv': 'Vikendica',
            'mesto': 'Sremski Karlovci',
            'postanski_broj': '21205',
            'drzava': 'Srbija'
        })
        
        # Forma ne bi trebalo da bude validna
        self.assertFalse(form.validate())
        self.assertIn('adresa', form.errors)
        
        # Test sa previše dugačkim nazivom
        form = LokacijaKuceForm(data={
            'naziv': 'X' * 256,  # predugačak naziv
            'adresa': 'Fruškogorska 22',
            'mesto': 'Sremski Karlovci',
            'postanski_broj': '21205',
            'drzava': 'Srbija'
        })
        
        # Forma ne bi trebalo da bude validna
        self.assertFalse(form.validate())
        self.assertIn('naziv', form.errors)

if __name__ == '__main__':
    unittest.main()
