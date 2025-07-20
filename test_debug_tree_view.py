import unittest
from flask import url_for
from app import create_app, db
from app.models.client import PravnoLice, RadnaJedinica, Objekat, Prostorija
from app.models.user import User
from bs4 import BeautifulSoup

class DebugTreeViewTest(unittest.TestCase):
    """Test klasa za detaljan debug tree-view strukture."""
    
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
        
        self.radna_jedinica2 = RadnaJedinica(
            naziv='Podružnica',
            adresa='Druga adresa 456',
            mesto='Novi Sad',
            postanski_broj='21000',
            drzava='Srbija',
            telefon='+381 21 123-4567',
            email='podruznica@testkompanija.rs',
            pravno_lice_id=self.pravno_lice.id
        )
        db.session.add(self.radna_jedinica2)
        db.session.commit()
        
        self.objekat = Objekat(
            naziv='Glavna zgrada',
            opis='Sedište kompanije',
            radna_jedinica_id=self.radna_jedinica.id
        )
        db.session.add(self.objekat)
        
        self.objekat2 = Objekat(
            naziv='Druga zgrada',
            opis='Druga zgrada u centrali',
            radna_jedinica_id=self.radna_jedinica.id
        )
        db.session.add(self.objekat2)
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
    
    def test_debug_tree_view_structure(self):
        """Test za detaljni debug strukture stabla na stranici pravnog lica."""
        self.login()
        
        # Prvo pogledajmo pravno lice
        print("\n--- DEBUG TREE VIEW NA PRAVNOM LICU ---")
        response = self.client.get(f'/klijenti/{self.pravno_lice.id}', follow_redirects=True)
        print(f"Response status: {response.status_code}")
        print(f"URL: {response.request.path}")
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Sačuvajmo HTML u fajl za detaljnu analizu
        with open('debug_pravno_lice.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("HTML sačuvan u fajl 'debug_pravno_lice.html'")
        
        # Takođe ispišemo prvih 1000 karaktera HTML-a
        html_content = str(soup)[:1000]
        print(f"Prvih 1000 karaktera HTML-a:\n{html_content}\n...")
        
        # Traženje potencijalnih tree-view elemenata
        print("\n--- PRETRAGA TREE-VIEW ELEMENATA ---")
        
        # Tražimo ul elemente
        ul_elements = soup.find_all('ul')
        print(f"Ukupno ul elemenata: {len(ul_elements)}")
        for i, ul in enumerate(ul_elements[:5]):  # Prikaz samo prvih 5
            print(f"\nUL {i}:")
            print(f"Klase: {ul.get('class')}")
            print(f"ID: {ul.get('id')}")
            print(f"Tekst: {ul.text.strip()[:50]}...")
            
            # Ako ul sadrži nazive radnih jedinica, to je verovatno tree-view
            if 'Centrala' in ul.text and 'Podružnica' in ul.text:
                print("=== OVAJ UL SADRŽI RADNE JEDINICE! ===")
        
        # Tražimo div elemente sa potencijalnim tree-view klasama
        tree_divs = soup.find_all('div', {'class': lambda c: c and any(
            tree_term in c.lower() for tree_term in ['tree', 'struktur', 'hirarhij', 'nav'])})
        print(f"\nUkupno div elemenata sa mogućim tree klasama: {len(tree_divs)}")
        for i, div in enumerate(tree_divs[:3]):
            print(f"\nDIV {i}:")
            print(f"Klase: {div.get('class')}")
            print(f"ID: {div.get('id')}")
            print(f"Tekst: {div.text.strip()[:50]}...")
            
        # Tražimo elemente koji sadrže radne jedinice
        elements_with_rj = [el for el in soup.find_all(['div', 'ul', 'ol', 'span', 'table']) 
                          if 'Centrala' in el.text and 'Podružnica' in el.text]
        
        print(f"\nUkupno elemenata koji sadrže radne jedinice: {len(elements_with_rj)}")
        for i, el in enumerate(elements_with_rj[:3]):
            print(f"\nElement {i} ({el.name}):")
            print(f"Klase: {el.get('class')}")
            print(f"ID: {el.get('id')}")
            print(f"Tekst: {el.text.strip()[:50]}...")
        
        # Opcionalno, prikažimo sve HTML elemente koji sadrže nazive radnih jedinica
        all_elements_with_rj = []
        for rj_naziv in [self.radna_jedinica.naziv, self.radna_jedinica2.naziv]:
            # Tražimo elemente koji sadrže naziv
            elements = soup.find_all(lambda tag: rj_naziv in tag.text and not tag.name == 'html')
            all_elements_with_rj.extend(elements)
        
        print(f"\nSvi elementi sa radnim jedinicama: {len(all_elements_with_rj)}")
        for i, el in enumerate(all_elements_with_rj[:5]):
            print(f"\nRJ Element {i} ({el.name}):")
            print(f"Sadržaj: {el.text.strip()}")
            # Roditelj elementa
            if el.parent:
                print(f"Roditelj: {el.parent.name}, klase: {el.parent.get('class')}")

        # Hajde da ispitamo i radnu jedinicu
        print("\n--- DEBUG TREE VIEW NA RADNOJ JEDINICI ---")
        rj_response = self.client.get(f'/klijenti/radna-jedinica/{self.radna_jedinica.id}', follow_redirects=True)
        print(f"Response status: {rj_response.status_code}")
        print(f"URL: {rj_response.request.path}")
        
        rj_soup = BeautifulSoup(rj_response.data, 'html.parser')
        
        # Sačuvajmo HTML u fajl za detaljnu analizu
        with open('debug_radna_jedinica.html', 'w', encoding='utf-8') as f:
            f.write(rj_soup.prettify())
        print("HTML sačuvan u fajl 'debug_radna_jedinica.html'")
        
        # Tražimo elemente koji sadrže objekte
        elements_with_obj = [el for el in rj_soup.find_all(['div', 'ul', 'ol', 'span', 'table']) 
                           if 'Glavna zgrada' in el.text and 'Druga zgrada' in el.text]
        
        print(f"\nUkupno elemenata koji sadrže objekte: {len(elements_with_obj)}")
        for i, el in enumerate(elements_with_obj[:3]):
            print(f"\nElement {i} ({el.name}):")
            print(f"Klase: {el.get('class')}")
            print(f"ID: {el.get('id')}")
            print(f"Tekst: {el.text.strip()[:50]}...")

if __name__ == '__main__':
    unittest.main()
