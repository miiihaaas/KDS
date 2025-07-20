import unittest
from app.models.material import Material
from app import db, create_app
import os

class MaterialModelTest(unittest.TestCase):
    
    def setUp(self):
        # Kreiranje test aplikacije sa prilagođenom konfiguracijom
        self.app = create_app('testing')
        
        # Postavljanje SQLite baze u memoriji bez problematičnih parametara
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_material_init(self):
        """Test inicijalizacije modela Material."""
        material = Material(naziv='Test materijal', jedinica_mere='kom', active=True)
        self.assertEqual(material.naziv, 'Test materijal')
        self.assertEqual(material.jedinica_mere, 'kom')
        print(f"\nActive value: {material.active}, type: {type(material.active)}")
        self.assertTrue(material.active)
    
    def test_material_representation(self):
        """Test string reprezentacije modela Material."""
        material = Material(naziv='Test materijal', jedinica_mere='kom')
        self.assertEqual(repr(material), f"<Material Test materijal, kom>")
    
    def test_get_material_info(self):
        """Test metode za dobijanje informacija o materijalu."""
        material = Material(naziv='Test materijal', jedinica_mere='kom')
        db.session.add(material)
        db.session.commit()
        
        info = material.get_material_info()
        self.assertEqual(info, "Test materijal (kom)")
    
    def test_get_active_materials(self):
        """Test klasne metode za dobijanje aktivnih materijala."""
        material1 = Material(naziv='Materijal 1', jedinica_mere='kom')
        material2 = Material(naziv='Materijal 2', jedinica_mere='kg')
        material3 = Material(naziv='Materijal 3', jedinica_mere='m', active=False)
        
        db.session.add_all([material1, material2, material3])
        db.session.commit()
        
        active_materials = Material.get_active_materials()
        self.assertEqual(len(active_materials), 2)
        self.assertIn(material1, active_materials)
        self.assertIn(material2, active_materials)
        self.assertNotIn(material3, active_materials)
    
    def test_toggle_status(self):
        """Test metode za promenu statusa materijala."""
        material = Material(naziv='Test materijal', jedinica_mere='kom')
        db.session.add(material)
        db.session.commit()
        
        # Inicijalno je materijal aktivan
        self.assertTrue(material.active)
        
        # Deaktiviraj materijal
        material.toggle_status()
        db.session.commit()
        self.assertFalse(material.active)
        
        # Ponovo aktiviraj materijal
        material.toggle_status()
        db.session.commit()
        self.assertTrue(material.active)

if __name__ == '__main__':
    unittest.main()
