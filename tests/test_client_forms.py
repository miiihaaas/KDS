import unittest
from app import create_app
from app.utils.client_forms import RadnaJedinicaForm, ObjekatForm, ProstorijaForm
from app.models.client import PravnoLice, RadnaJedinica, Objekat
from wtforms import StringField
from wtforms.validators import Length, Email, Optional
from wtforms.form import Form

class ClientFormsTestCase(unittest.TestCase):
    def setUp(self):
        """Priprema test okruženja pre svakog testa."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        """Čišćenje nakon svakog testa."""
        self.app_context.pop()
    
    def test_radna_jedinica_form_validation(self):
        """Test validacije forme za radnu jedinicu."""
        # Test sa validnim podacima
        form = RadnaJedinicaForm(data={
            'naziv': 'Test Radna Jedinica',
            'adresa': 'Test adresa 123',
            'mesto': 'Beograd',
            'postanski_broj': '11000',
            'drzava': 'Srbija',
            'kontakt_osoba': 'Petar Petrović',
            'telefon': '+381 11 123-4567',
            'email': 'radna.jedinica@example.com',
            'napomena': 'Test napomena'
        })
        
        # Forma bi trebalo da bude validna
        self.assertTrue(form.validate())
        
        # Test sa invalidnim podacima - nedostaje naziv (obavezno polje)
        form = RadnaJedinicaForm(data={
            'adresa': 'Test adresa 123',
            'mesto': 'Beograd',
            'postanski_broj': '11000',
            'drzava': 'Srbija',
            'kontakt_osoba': 'Petar Petrović',
            'telefon': '+381 11 123-4567',
            'email': 'radna.jedinica@example.com'
        })
        
        # Forma ne bi trebalo da bude validna
        self.assertFalse(form.validate())
        self.assertIn('naziv', form.errors)
        
        # Test sa invalidnim emailom - koristimo poboljšanu formu sa optional_email validatorom
        form = RadnaJedinicaForm(data={
            'naziv': 'Test Radna Jedinica',
            'adresa': 'Test adresa 123',
            'mesto': 'Beograd',
            'postanski_broj': '11000',
            'drzava': 'Srbija',
            'kontakt_osoba': 'Petar Petrović',
            'telefon': '+381 11 123-4567',
            'email': 'nije-validan-email'  # nevalidan email format
        })
        
        # Forma ne bi trebalo da bude validna zbog email-a
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)
        
        # Debug info
        print(f"RadnaJedinicaForm validation errors: {form.errors}")
    
    def test_objekat_form_validation(self):
        """Test validacije forme za objekat."""
        # Test sa validnim podacima
        form = ObjekatForm(data={
            'naziv': 'Test Objekat',
            'opis': 'Test opis objekta'
        })
        
        # Forma bi trebalo da bude validna
        self.assertTrue(form.validate())
        
        # Test sa invalidnim podacima - nedostaje naziv (obavezno polje)
        form = ObjekatForm(data={
            'opis': 'Test opis objekta'
        })
        
        # Forma ne bi trebalo da bude validna
        self.assertFalse(form.validate())
        self.assertIn('naziv', form.errors)
        
        # Test sa previše dugačkim nazivom
        form = ObjekatForm(data={
            'naziv': 'X' * 256,  # Predugačak naziv
            'opis': 'Test opis objekta'
        })
        
        # Forma ne bi trebalo da bude validna
        self.assertFalse(form.validate())
        self.assertIn('naziv', form.errors)
    
    def test_prostorija_form_validation(self):
        """Test validacije forme za prostoriju."""
        # Test sa validnim podacima
        form = ProstorijaForm(data={
            'naziv': 'Kancelarija 101',
            'sprat': '1',
            'broj': '101',
            'namena': 'Kancelarija'
        })
        
        # Forma bi trebalo da bude validna
        self.assertTrue(form.validate())
        
        # Test sa invalidnim podacima - nedostaje naziv (obavezno polje)
        form = ProstorijaForm(data={
            'sprat': '1',
            'broj': '101',
            'namena': 'Kancelarija'
        })
        
        # Forma ne bi trebalo da bude validna
        self.assertFalse(form.validate())
        self.assertIn('naziv', form.errors)
        
        # Test sa previše dugačkim brojem prostorije - koristimo poboljšanu formu sa optional_length validatorom
        form = ProstorijaForm(data={
            'naziv': 'Kancelarija 101',  # Obavezno polje
            'broj': 'X' * 51,  # Predugačak string za broj prostorije
            'sprat': '1',
            'namena': 'Kancelarija'
        })
        
        # Forma ne bi trebala da bude validna zbog predužog broja prostorije
        self.assertFalse(form.validate())
        self.assertIn('broj', form.errors)
        
        # Debug info
        print(f"ProstorijaForm validation errors: {form.errors}")

    def test_email_validator(self):
        """Test direktno za Email validator."""
        # Kreiranje proste test forme sa Email validatorom
        class TestEmailForm(Form):
            email = StringField('Email', validators=[
                Email(message='Unesite ispravnu email adresu.')
            ])
        
        # Test sa nevalidnim emailom
        form = TestEmailForm()
        form.email.data = 'nije-validan-email'
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)
        print(f"Email validator greška: {form.errors['email']}")

    def test_length_validator(self):
        """Test direktno za Length validator."""
        # Kreiranje proste test forme sa Length validatorom
        class TestLengthForm(Form):
            polje = StringField('Polje', validators=[
                Length(max=50, message='Polje ne može biti duže od 50 karaktera.')
            ])
        
        # Test sa predugačkim stringom
        form = TestLengthForm()
        form.polje.data = 'X' * 51
        self.assertFalse(form.validate())
        self.assertIn('polje', form.errors)
        print(f"Length validator greška: {form.errors['polje']}")

    def test_optional_length_custom_validator(self):
        """Test za prilagođeni optional_length validator."""
        from app.utils.validators import optional_length
        
        # Kreiranje test forme sa prilagođenim optional_length validatorom
        class TestCustomOptionalLengthForm(Form):
            polje = StringField('Polje', validators=[
                optional_length(max=50, message='Polje ne može biti duže od 50 karaktera.')
            ])
        
        # Test 1: Predugačak string (51 karakter)
        form = TestCustomOptionalLengthForm()
        form.polje.data = 'X' * 51
        self.assertFalse(form.validate())
        self.assertIn('polje', form.errors)
        print(f"Custom optional_length (predugačko): {form.errors['polje']}")
        
        # Test 2: Prazno polje (treba da prođe validaciju)
        form = TestCustomOptionalLengthForm()
        form.polje.data = ''
        self.assertTrue(form.validate())
        
        # Test 3: Prihvatljiva dužina (50 karaktera)
        form = TestCustomOptionalLengthForm()
        form.polje.data = 'X' * 50
        self.assertTrue(form.validate())

    def test_optional_email_custom_validator(self):
        """Test za prilagođeni optional_email validator."""
        from app.utils.validators import optional_email
        
        # Kreiranje test forme sa prilagođenim optional_email validatorom
        class TestCustomOptionalEmailForm(Form):
            email = StringField('Email', validators=[
                optional_email(message='Unesite ispravnu email adresu.')
            ])
        
        # Test 1: Nevalidan email
        form = TestCustomOptionalEmailForm()
        form.email.data = 'nije-validan-email'
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)
        print(f"Custom optional_email (nevalidan): {form.errors['email']}")
        
        # Test 2: Prazno polje (treba da prođe validaciju)
        form = TestCustomOptionalEmailForm()
        form.email.data = ''
        self.assertTrue(form.validate())
        
        # Test 3: Validan email
        form = TestCustomOptionalEmailForm()
        form.email.data = 'test@example.com'
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
