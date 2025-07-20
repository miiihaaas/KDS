import unittest
from flask import url_for
from app import create_app, db
from app.models.client import PravnoLice, RadnaJedinica, Objekat, Prostorija
from app.models.user import User
from bs4 import BeautifulSoup

class DebugBreadcrumbsTest(unittest.TestCase):
    """Test klasa za detaljan debug breadcrumbs navigacije."""
    
    @classmethod
    def setUpClass(cls):
        """Setup koji se izvršava jednom pre svih testova u klasi."""
        print("\nPostavljanje test klase...")
        cls.app = create_app('testing')
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        
    def setUp(self):
        """Priprema test okruženja pre svakog testa."""
        self.app = self.__class__.app
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Čišćenje baze pre svakog testa
        db.drop_all()
        db.create_all()
        print(f"\nPriprema testa: {self._testMethodName}")
        
        # Kreiranje test korisnika (administratora)
        self.test_user = User(
            ime='Test',
            prezime='Administrator',
            email='test@example.com',
            tip='administrator'
        )
        self.test_user.set_password('password123')
        db.session.add(self.test_user)
        
        # Kreiranje test podataka u hijerarhiji
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
        
        self.client = self.app.test_client()

    def tearDown(self):
        """Čišćenje nakon svakog testa."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def login(self):
        """Helper metoda za prijavljivanje test korisnika."""
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        print(f"Login status: {response.status_code}")
        return response
    
    def test_debug_breadcrumbs_radna_jedinica(self):
        """Test za detaljni debug breadcrumbs navigacije na stranici radne jedinice."""
        self.login()
        
        # Prvo proverimo pravno lice (roditelj radne jedinice)
        print("\n--- DEBUG PRAVNO LICE ---")
        pravno_lice_response = self.client.get(f'/klijenti/{self.pravno_lice.id}', follow_redirects=True)
        print(f"Pravno lice response status: {pravno_lice_response.status_code}")
        print(f"Pravno lice URL: {pravno_lice_response.request.path}")
        
        # Zatim radnu jedinicu
        print("\n--- DEBUG RADNA JEDINICA ---")
        response = self.client.get(f'/klijenti/radna-jedinica/{self.radna_jedinica.id}', follow_redirects=True)
        print(f"Radna jedinica response status: {response.status_code}")
        print(f"Radna jedinica URL: {response.request.path}")
        
        # Analiziramo HTML
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Pronađi breadcrumbs
        breadcrumbs = soup.find('nav', {'aria-label': 'breadcrumb'})
        if not breadcrumbs:
            print("GREŠKA: Breadcrumb navigacija nije pronađena!")
            breadcrumbs = soup.find_all(['nav', 'ol', 'ul'])
            print(f"Pronađeno navigacijskih elemenata: {len(breadcrumbs)}")
            for i, nav in enumerate(breadcrumbs[:3]):
                print(f"Nav {i}: {nav.name}, klase: {nav.get('class')}, tekst: {nav.text.strip()[:50]}...")
        else:
            print("Breadcrumb navigacija pronađena!")
            
            # Proverimo stavke breadcrumbs-a
            items = breadcrumbs.find_all('li')
            print(f"Broj breadcrumb elemenata: {len(items)}")
            
            # Detaljni ispis svih breadcrumb elemenata
            for i, item in enumerate(items):
                print(f"\n-- Item {i}: --")
                print(f"HTML: {item}")
                print(f"Tekst: '{item.text.strip()}'")
                print(f"Klase: {item.get('class')}")
                
                # Proveri da li item ima link
                link = item.find('a')
                if link:
                    print(f"Link: {link.get('href')}")
                    print(f"Link tekst: '{link.text.strip()}'")
                else:
                    print("Nema linka u ovom breadcrumb elementu.")
        
        # Provera linka za povratak na pravno lice
        print("\n--- PROVERA LINKOVA ZA NAVIGACIJU ---")
        all_links = soup.find_all('a')
        print(f"Ukupan broj linkova na stranici: {len(all_links)}")
        
        # Ispiši prvih 10 linkova
        for i, link in enumerate(all_links[:10]):
            href = link.get('href', '')
            print(f"Link {i}: href='{href}', text='{link.text.strip()}'")
            if '/klijenti/' in href or self.pravno_lice.naziv in link.text or 'nazad' in link.text.lower():
                print(f"  --> Potencijalni link ka pravnom licu!")
        
        # Provera sadržaja stranice
        page_content = response.data.decode('utf-8')[:500]  # Prvih 500 karaktera
        print(f"\nPrvih 500 karaktera HTML stranice:\n{page_content}")

if __name__ == '__main__':
    unittest.main()
