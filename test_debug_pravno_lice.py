from flask import session, current_app, url_for
import unittest
from bs4 import BeautifulSoup
import os
import re
from app import create_app, db
from app.models import User, PravnoLice, RadnaJedinica, Objekat, Prostorija
from werkzeug.security import generate_password_hash
from datetime import datetime

class PravnoLiceDebugTest(unittest.TestCase):
    """Test za debug pravnog lica i linkova na stranici."""
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Kreiranje test korisnika i test podataka
        h = generate_password_hash('test1234')
        self.user = User(username='testuser', password_hash=h)
        db.session.add(self.user)
        
        # Test pravno lice, radna jedinica, objekat i prostorija
        self.pravno_lice = PravnoLice(naziv='Test Pravno Lice', pib='123456789', 
                                     maticni_broj='12345678', adresa='Test Adresa')
        db.session.add(self.pravno_lice)
        
        self.radna_jedinica = RadnaJedinica(naziv='Test Radna Jedinica', 
                                           pravno_lice=self.pravno_lice)
        db.session.add(self.radna_jedinica)
        
        self.objekat = Objekat(naziv='Test Objekat', 
                              adresa='Test Adresa Objekta', 
                              radna_jedinica=self.radna_jedinica)
        db.session.add(self.objekat)
        
        self.prostorija = Prostorija(naziv='Test Prostorija', 
                                    sprat='1', broj='101', namena='Kancelarija',
                                    objekat=self.objekat)
        db.session.add(self.prostorija)
        
        db.session.commit()
        
        self.client = self.app.test_client(use_cookies=True)
        
        print("Postavljanje test klase uspešno završeno")
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        print("Čišćenje test klase...")
        
    def login(self):
        """Helper za prijavu test korisnika."""
        return self.client.post('/auth/login',
                               data={'username': 'testuser', 'password': 'test1234'},
                               follow_redirects=True)
    
    def test_debug_pravno_lice(self):
        """Debug test za analizu linkova na stranici pravnog lica."""
        self.login()
        
        # Pristup stranici pravnog lica
        response = self.client.get(f'/klijenti/{self.pravno_lice.id}', follow_redirects=True)
        print(f"Response status: {response.status_code}")
        print(f"URL: {response.request.path}")
        
        if response.status_code != 200:
            self.fail(f"Neuspešan zahtev za stranicu pravnog lica, status kod: {response.status_code}")
        
        # Parsiranje sadržaja
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Sačuvaj HTML za detaljnu analizu
        with open('debug_pravno_lice.html', 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print("HTML sačuvan u fajl debug_pravno_lice.html")
        
        # Pronalaženje svih linkova
        all_links = soup.find_all('a')
        print(f"Ukupan broj linkova na stranici: {len(all_links)}")
        
        # Prikaz svih linkova
        print("\n=== SVI LINKOVI ===")
        for i, link in enumerate(all_links):
            href = link.get('href', '')
            text = link.text.strip()
            print(f"Link {i}: Text='{text}', href='{href}'")
        
        # Potencijalni linkovi za novu radnu jedinicu
        print("\n=== POTENCIJALNI LINKOVI ZA NOVU RADNU JEDINICU ===")
        for i, link in enumerate(all_links):
            href = link.get('href', '')
            text = link.text.strip().lower()
            if ('radna' in text or 'jedinica' in text or 'rj' in text or 
                'radna' in href or 'jedinica' in href or 'rj' in href):
                print(f"Potencijalni link {i}: Text='{link.text.strip()}', href='{href}'")
        
        # Provera HTML klasa koje mogu sadržati akcije
        action_containers = soup.find_all(['div', 'section'], class_=lambda c: c and ('action' in c.lower() or 'button' in c.lower()))
        print(f"\n=== POTENCIJALNI KONTEJNERI ZA AKCIJE (broj: {len(action_containers)}) ===")
        for i, container in enumerate(action_containers):
            print(f"Container {i}, class='{container.get('class')}', id='{container.get('id')}'")
            links = container.find_all('a')
            for j, link in enumerate(links):
                print(f"  Link {j}: Text='{link.text.strip()}', href='{link.get('href', '')}'")
                
        print("\n=== ANALIZA ZAVRŠENA ===")
        
if __name__ == '__main__':
    unittest.main()
