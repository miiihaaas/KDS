import unittest
from app.utils.helpers import sanitize_search_term
from app import create_app, db
from app.models.client import Client, PravnoLice, FizickoLice
from app.utils.client_forms import ClientBaseForm
from wtforms import Form, StringField
from wtforms.validators import ValidationError
from flask_wtf.form import FlaskForm

class SecurityFunctionsTestCase(unittest.TestCase):
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
        
    def test_sanitize_search_term_empty_input(self):
        """Test da li funkcija za sanitizaciju pravilno obrađuje prazan unos."""
        self.assertEqual(sanitize_search_term(None), None)
        self.assertEqual(sanitize_search_term(''), '')
    
    def test_sanitize_search_term_normal_input(self):
        """Test da li funkcija za sanitizaciju zadržava normalan tekst."""
        # Normalan tekst bi trebalo da ostane nepromenjen
        self.assertEqual(sanitize_search_term('Testiranje'), 'Testiranje')
        self.assertEqual(sanitize_search_term('Novi Beograd'), 'Novi Beograd')
        self.assertEqual(sanitize_search_term('12345'), '12345')
    
    def test_sanitize_search_term_dangerous_input(self):
        """Test da li funkcija za sanitizaciju pravilno čisti opasne karaktere."""
        # SQL injection pokušaji
        self.assertEqual(sanitize_search_term("'; DROP TABLE users;--"), " DROP TABLE users")
        self.assertEqual(sanitize_search_term("Marko' OR '1'='1"), "Marko OR 11")
        
        # SQL wildcards
        self.assertEqual(sanitize_search_term("Test%"), "Test")
        self.assertEqual(sanitize_search_term("Test_user"), "Testuser")
        
        # Specijalni karakteri
        self.assertEqual(sanitize_search_term("Test(123)"), "Test123")
        self.assertEqual(sanitize_search_term("Ime{Prezime}"), "ImePrezime")
        self.assertEqual(sanitize_search_term('Test\\string"with\'quotes'), "Teststringwithquotes")
    
    def test_email_uniqueness_validation(self):
        """Test da li validacija jedinstvenog email-a radi pravilno."""
        # Kreiranje prvog klijenta sa email-om
        pravno_lice = PravnoLice(
            tip='pravno_lice',
            naziv='Test Firma',
            pib='111222333',
            mb='12345678',
            adresa='Test adresa 1',
            mesto='Beograd',
            postanski_broj='11000',
            drzava='Srbija',
            telefon='+381 11 123-4567',
            email='test@firma.rs'
        )
        
        db.session.add(pravno_lice)
        db.session.commit()
        
        # Kreiramo test formu za validaciju
        with self.app.test_request_context():
            class TestForm(ClientBaseForm):
                pass
            
            form = TestForm()
            form.email.data = 'test@firma.rs'
            
            # Test da validacija prijavljuje grešku zbog duplikata
            with self.assertRaises(ValidationError):
                form.validate_email(form.email)
            
            # Test sa drugačijim email-om prolazi validaciju
            form.email.data = 'drugi@firma.rs'
            try:
                form.validate_email(form.email)
                validation_passed = True
            except ValidationError:
                validation_passed = False
            
            self.assertTrue(validation_passed)
    
    def test_email_uniqueness_validation_edit_mode(self):
        """Test da validacija dozvoljava izmenu klijenta sa istim email-om."""
        # Kreiranje klijenta sa email-om
        pravno_lice = PravnoLice(
            tip='pravno_lice',
            naziv='Test Firma',
            pib='111222333',
            mb='12345678',
            adresa='Test adresa 1',
            mesto='Beograd',
            postanski_broj='11000',
            drzava='Srbija',
            telefon='+381 11 123-4567',
            email='test@firma.rs'
        )
        
        db.session.add(pravno_lice)
        db.session.commit()
        
        # Kreiramo test formu za validaciju sa original_email
        with self.app.test_request_context():
            class TestForm(ClientBaseForm):
                pass
            
            # Simuliramo edit mode postavljanjem original_email na isti email
            form = TestForm(original_email='test@firma.rs')
            form.email.data = 'test@firma.rs'
            
            # Test da validacija dozvoljava isti email kod izmene
            try:
                form.validate_email(form.email)
                validation_passed = True
            except ValidationError:
                validation_passed = False
            
            self.assertTrue(validation_passed)

if __name__ == '__main__':
    unittest.main()
