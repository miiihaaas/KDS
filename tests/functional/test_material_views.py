import unittest
import json
from flask import url_for
from app import create_app, db
from app.models.material import Material
from app.models.user import User

class MaterialViewsTest(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Kreiraj test korisnika (administratora)
        self.admin = User(
            ime='Admin',
            prezime='Korisnik',
            email='admin@test.com',
            tip='administrator'
        )
        self.admin.set_password('password')
        
        # Kreiraj test korisnika (običnog)
        self.user = User(
            ime='Obični',
            prezime='Korisnik',
            email='user@test.com',
            tip='serviser'
        )
        self.user.set_password('password')
        
        # Dodaj test materijale
        self.material1 = Material(naziv='Test materijal 1', jedinica_mere='kom')
        self.material2 = Material(naziv='Test materijal 2', jedinica_mere='kg')
        self.material3 = Material(naziv='Neaktivni materijal', jedinica_mere='m', active=False)
        
        db.session.add_all([self.admin, self.user, self.material1, self.material2, self.material3])
        db.session.commit()
        
        self.client = self.app.test_client()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def login(self, email, password):
        return self.client.post(
            '/auth/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )
    
    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)
    
    def test_lista_materials_unauthorized(self):
        """Test pristupa listi materijala bez prijave."""
        response = self.client.get('/materijali/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Morate se prijaviti', response.data)
    
    def test_lista_materials_non_admin(self):
        """Test pristupa listi materijala sa običnim korisnikom."""
        self.login('user@test.com', 'password')
        response = self.client.get('/materijali/', follow_redirects=True)
        self.assertEqual(response.status_code, 403)
        self.assertIn(b'Forbidden', response.data)
        self.logout()
    
    def test_lista_materials_admin(self):
        """Test pristupa listi materijala sa administratorom."""
        self.login('admin@test.com', 'password')
        response = self.client.get('/materijali/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lista materijala', response.data)
        self.assertIn(b'Test materijal 1', response.data)
        self.assertIn(b'Test materijal 2', response.data)
        self.assertIn(b'Neaktivni materijal', response.data)
        self.logout()
    
    def test_search_materials(self):
        """Test AJAX pretrage materijala."""
        self.login('admin@test.com', 'password')
        response = self.client.get(
            '/materijali/?q=materijal 1',
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test materijal 1', response.data)
        self.assertNotIn(b'Test materijal 2', response.data)
        self.logout()
    
    def test_add_material(self):
        """Test dodavanja novog materijala."""
        self.login('admin@test.com', 'password')
        
        # Provera forme za dodavanje
        response = self.client.get('/materijali/novi')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Novi materijal', response.data)
        
        # Dodavanje novog materijala
        response = self.client.post(
            '/materijali/novi',
            data=dict(
                naziv='Novi test materijal',
                jedinica_mere='l',
                active=True,
                submit='Sačuvaj'
            ),
            follow_redirects=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Materijal je uspešno kreiran.', response.data.decode('utf-8'))
        self.assertIn('Novi test materijal', response.data.decode('utf-8'))
        
        # Provera da li je materijal zaista dodat
        material = Material.query.filter_by(naziv='Novi test materijal').first()
        self.assertIsNotNone(material)
        self.assertEqual(material.jedinica_mere, 'l')
        self.assertTrue(material.active)
        
        self.logout()
    
    def test_edit_material(self):
        """Test izmene postojećeg materijala."""
        self.login('admin@test.com', 'password')
        
        # Provera forme za izmenu
        response = self.client.get(f'/materijali/{self.material1.id}/izmeni')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Izmena materijala', response.data.decode('utf-8'))
        self.assertIn('Test materijal 1', response.data.decode('utf-8'))
        
        # Izmena materijala
        response = self.client.post(
            f'/materijali/{self.material1.id}/izmeni',
            data=dict(
                naziv='Izmenjen materijal',
                jedinica_mere='kg',
                active=True,
                submit='Sačuvaj'
            ),
            follow_redirects=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Podaci o materijalu su uspešno ažurirani.', response.data.decode('utf-8'))
        self.assertIn('Izmenjen materijal', response.data.decode('utf-8'))
        
        # Provera da li je materijal zaista izmenjen
        material = Material.query.get(self.material1.id)
        self.assertEqual(material.naziv, 'Izmenjen materijal')
        self.assertEqual(material.jedinica_mere, 'kg')
        
        self.logout()
    
    def test_toggle_material_status(self):
        """Test promene statusa materijala."""
        self.login('admin@test.com', 'password')
        
        # Deaktivacija materijala
        response = self.client.post(
            f'/materijali/{self.material1.id}/status',
            follow_redirects=True
        )
        
        self.assertEqual(response.status_code, 200)
        # Provera da li je neki alert sa uspešnom porukom prisutan
        self.assertIn('alert-success', response.data.decode('utf-8'))
        
        # Provera da li je materijal zaista deaktiviran
        material = Material.query.get(self.material1.id)
        self.assertFalse(material.active)
        
        # Aktivacija materijala
        response = self.client.post(
            f'/materijali/{self.material1.id}/status',
            follow_redirects=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Materijal je uspešno aktiviran.', response.data.decode('utf-8'))
        
        # Provera da li je materijal zaista aktiviran
        material = Material.query.get(self.material1.id)
        self.assertTrue(material.active)
        
        self.logout()
    
    def test_toggle_material_status_ajax(self):
        """Test AJAX promene statusa materijala."""
        self.login('admin@test.com', 'password')
        
        # AJAX Deaktivacija materijala
        response = self.client.post(
            f'/materijali/{self.material1.id}/status',
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue('success' in data)
        self.assertTrue(data['success'])
        self.assertFalse(data['active'])
        
        # Provera da li je materijal zaista deaktiviran
        material = Material.query.get(self.material1.id)
        self.assertFalse(material.active)
        
        self.logout()
    
    def test_api_active_materials(self):
        """Test API endpointa za aktivne materijale."""
        # Login kao admin pre pristupa API-u
        self.login('admin@test.com', 'password')
        response = self.client.get('/api/materijali')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        
        materijali_ids = [m['id'] for m in data]
        self.assertIn(self.material1.id, materijali_ids)
        self.assertIn(self.material2.id, materijali_ids)
        self.assertNotIn(self.material3.id, materijali_ids)

if __name__ == '__main__':
    unittest.main()
