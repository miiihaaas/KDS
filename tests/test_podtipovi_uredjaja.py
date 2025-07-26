import unittest
import sys
import os
import json
from datetime import datetime

# Dodajemo root direktorijum projekta u Python path da bi moduli bili dostupni
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import url_for
from app import create_app, db
from app.models.device import Uredjaj
from app.utils.device_forms import UredjajForm, UredjajFilterForm
from wtforms.validators import ValidationError

class TestPodtipoviUredjaja(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        db.drop_all()     # obriši sve prethodne tabele
        db.create_all()   # napravi ih iznova
        
        self.client = self.app.test_client()
        
        # WTForms zahteva SECRET_KEY za CSRF zaštitu
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Isključujemo CSRF za testove
        
        # Kreiranje test korisnika
        from app.models.user import User
        user = User(ime='Test', prezime='Administrator', email='test@example.com', tip='administrator')
        user.set_password('test_password')
        db.session.add(user)
        db.session.commit()
        
        # Prijava korisnika
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'test_password'
        }, follow_redirects=True)
        
        # Kreiranje testnih uređaja sa različitim tipovima i podtipovima
        self.uredjaji = [
            Uredjaj(
                tip='rashladna_tehnika',
                podtip='split_sistem',
                proizvodjac='Mitsubishi',
                model='MSZ-A1',
                serijski_broj='TEST-RS-001',
                godina_proizvodnje=2023
            ),
            Uredjaj(
                tip='rashladna_tehnika',
                podtip='vrf_sistemi',
                proizvodjac='Daikin',
                model='VRV-2000',
                serijski_broj='TEST-RV-001',
                godina_proizvodnje=2022
            ),
            Uredjaj(
                tip='grejna_tehnika',
                podtip='kotlovi',
                proizvodjac='Vaillant',
                model='TURBO-2000',
                serijski_broj='TEST-GK-001',
                godina_proizvodnje=2021
            ),
            Uredjaj(
                tip='grejna_tehnika',
                podtip='radijatori',
                proizvodjac='Nepoznat',
                model='Standard 22',
                serijski_broj='TEST-GR-001',
                godina_proizvodnje=2020
            ),
            Uredjaj(
                tip='ventilacioni_sistemi',
                podtip=None,
                proizvodjac='Systemair',
                model='CAU-1000',
                serijski_broj='TEST-VS-001',
                godina_proizvodnje=2019
            )
        ]
        
        db.session.add_all(self.uredjaji)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_model_podtip_validacija(self):
        """Test validacije podtipa u modelu Uredjaj"""
        # 1. Test validnog tipa i podtipa za rashladnu tehniku
        uredjaj1 = Uredjaj(
            tip='rashladna_tehnika',
            podtip='split_sistem',
            proizvodjac='Test',
            model='Test Model',
            serijski_broj='TEST-VALID-001'
        )
        db.session.add(uredjaj1)
        db.session.commit()
        self.assertEqual(uredjaj1.podtip, 'split_sistem')
        
        # 2. Test validnog tipa i podtipa za grejnu tehniku
        uredjaj2 = Uredjaj(
            tip='grejna_tehnika',
            podtip='kotlovi',
            proizvodjac='Test',
            model='Test Model',
            serijski_broj='TEST-VALID-002'
        )
        db.session.add(uredjaj2)
        db.session.commit()
        self.assertEqual(uredjaj2.podtip, 'kotlovi')
        
        # 3. Test ventilacionih sistema bez podtipa
        uredjaj3 = Uredjaj(
            tip='ventilacioni_sistemi',
            podtip=None,  # None je validno za ventilacione sisteme
            proizvodjac='Test',
            model='Test Model',
            serijski_broj='TEST-VALID-003'
        )
        db.session.add(uredjaj3)
        db.session.commit()
        self.assertIsNone(uredjaj3.podtip)
    
    def test_form_podtip_validacija(self):
        """Test validacije podtipa u UredjajForm"""
        with self.app.test_request_context():
            # 1. Test validnog tipa i podtipa
            form = UredjajForm(
                tip='rashladna_tehnika',
                podtip='split_sistem',
                proizvodjac='Test',
                model='Test Model',
                serijski_broj='TEST-FORM-001'
            )
            self.assertTrue(form.validate())
            
            # 2. Test nevalidnog podtipa za tip
            form = UredjajForm(
                tip='rashladna_tehnika',
                podtip='kotlovi',  # Kotlovi su za grejnu tehniku, ne za rashladnu
                proizvodjac='Test',
                model='Test Model',
                serijski_broj='TEST-FORM-002'
            )
            self.assertFalse(form.validate())
            self.assertIn('podtip', form.errors)
            
            # 3. Test ventilacionih sistema sa podtipom (treba da bude invalid)
            form = UredjajForm(
                tip='ventilacioni_sistemi',
                podtip='split_sistem',  # Ventilacioni sistemi ne bi trebalo da imaju podtip
                proizvodjac='Test',
                model='Test Model',
                serijski_broj='TEST-FORM-003'
            )
            self.assertFalse(form.validate())
            self.assertIn('podtip', form.errors)
            
            # 4. Test ventilacionih sistema bez podtipa (treba da bude valid)
            form = UredjajForm(
                tip='ventilacioni_sistemi',
                podtip='',
                proizvodjac='Test',
                model='Test Model',
                serijski_broj='TEST-FORM-004'
            )
            self.assertTrue(form.validate())
    
    def test_api_podtipovi(self):
        """Test API endpointa za dobavljanje podtipova"""
        with self.app.test_client() as client:
            # 1. Test API endpointa za rashladnu tehniku
            response = client.get('/uredjaji/api/podtipovi-uredjaja/rashladna_tehnika')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            podtipovi = [item['id'] for item in data]
            self.assertIn('split_sistem', podtipovi)
            self.assertIn('vrf_sistemi', podtipovi)
            
            # 2. Test API endpointa za grejnu tehniku
            response = client.get('/uredjaji/api/podtipovi-uredjaja/grejna_tehnika')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            podtipovi = [item['id'] for item in data]
            self.assertIn('kotlovi', podtipovi)
            self.assertIn('radijatori', podtipovi)
            
            # 3. Test API endpointa za ventilacione sisteme (treba da bude prazna lista)
            response = client.get('/uredjaji/api/podtipovi-uredjaja/ventilacioni_sistemi')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data), 0)  # Prazna lista jer ventilacioni sistemi nemaju podtipove
            
            # 4. Test nevalidnog tipa
            response = client.get('/uredjaji/api/podtipovi-uredjaja/nepostojeci_tip')
            self.assertEqual(response.status_code, 400)  # Bad Request
    
    def test_filtriranje_po_podtipu(self):
        """Test filtriranja uređaja po podtipu"""
        with self.app.test_client() as client:
            # 1. Test filtriranja po podtipu split_sistem
            response = client.get('/uredjaji/?podtip=split_sistem')
            self.assertEqual(response.status_code, 200)
            # Provera da li je rezultat filtriranja tačan
            self.assertIn(b'MSZ-A1', response.data)  # Treba da sadrži Mitsubishi MSZ-A1
            self.assertNotIn(b'VRV-2000', response.data)  # Ne treba da sadrži Daikin VRV-2000
            
            # 2. Test filtriranja po podtipu vrf_sistemi
            response = client.get('/uredjaji/?podtip=vrf_sistemi')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'VRV-2000', response.data)
            self.assertNotIn(b'MSZ-A1', response.data)
            
            # 3. Test filtriranja po podtipu kotlovi
            response = client.get('/uredjaji/?podtip=kotlovi')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'TURBO-2000', response.data)
            self.assertNotIn(b'Standard 22', response.data)
    
    def test_kombinovano_filtriranje(self):
        """Test kombinovanog filtriranja uređaja po tipu i podtipu"""
        with self.app.test_client() as client:
            # 1. Test kombinovanog filtriranja za rashladnu tehniku i split sisteme
            response = client.get('/uredjaji/?tip=rashladna_tehnika&podtip=split_sistem')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'MSZ-A1', response.data)
            self.assertNotIn(b'VRV-2000', response.data)
            self.assertNotIn(b'TURBO-2000', response.data)
            
            # 2. Test kombinovanog filtriranja za grejnu tehniku i kotlove
            response = client.get('/uredjaji/?tip=grejna_tehnika&podtip=kotlovi')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'TURBO-2000', response.data)
            self.assertNotIn(b'Standard 22', response.data)
            self.assertNotIn(b'MSZ-A1', response.data)

if __name__ == '__main__':
    unittest.main()
