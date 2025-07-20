# Testing Strategy

## Testing Pyramid
```
                Unit Tests
               /            \
          Integration Tests
             /              \
        End-to-End Tests
```

## Test Organization

### Frontend Tests
```
tests/frontend/
├── unit/
│   ├── test_api_client.js          # API client testovi
│   ├── test_state_manager.js       # State management testovi
│   └── test_utils.js               # Utility functions testovi
├── integration/
│   ├── test_qr_scanner.js          # QR scanner integracija
│   ├── test_work_order_flow.js     # Work order workflow
│   └── test_client_management.js   # Client management flow
└── e2e/
    ├── test_login_flow.js          # Login proces
    ├── test_create_work_order.js   # Kreiranje radnog naloga
    └── test_qr_scanning.js         # QR skeniranje workflow
```

### Backend Tests
```
tests/backend/
├── unit/
│   ├── test_models.py              # Model testovi
│   ├── test_services.py            # Service layer testovi
│   └── test_utils.py               # Utility function testovi
├── integration/
│   ├── test_api_endpoints.py       # API endpoint testovi
│   ├── test_database.py           # Database integration
│   └── test_email.py               # Email funkcionalnost
└── e2e/
    ├── test_user_workflows.py      # Complete user workflows
    └── test_admin_workflows.py     # Admin workflows
```

## Test Examples

### Frontend Component Test
```javascript
// tests/frontend/unit/test_state_manager.js
describe('StateManager', () => {
    beforeEach(() => {
        // Reset state before each test
        Object.keys(AppState).forEach(key => {
            if (typeof AppState[key] === 'object') {
                AppState[key] = {};
            } else {
                AppState[key] = null;
            }
        });
    });

    test('should set and get state correctly', () => {
        const testValue = { id: 1, name: 'Test Client' };
        StateManager.setState('currentClient', testValue);
        
        const retrievedValue = StateManager.getState('currentClient');
        expect(retrievedValue).toEqual(testValue);
    });

    test('should notify state changes', (done) => {
        const testValue = 'test value';
        
        document.addEventListener('stateChange', (event) => {
            expect(event.detail.key).toBe('user.name');
            expect(event.detail.value).toBe(testValue);
            done();
        });

        StateManager.setState('user.name', testValue);
    });
});
```

### Backend API Test
```python
# tests/backend/integration/test_api_endpoints.py
import pytest
from app import create_app, db
from app.models.user import User
from app.models.client import Client

class TestClientAPI:
    
    @pytest.fixture
    def app(self):
        app = create_app('testing')
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()
    
    @pytest.fixture
    def client(self, app):
        return app.test_client()
    
    @pytest.fixture
    def auth_headers(self, client):
        # Create test user and login
        user = User(
            ime='Test',
            prezime='User',
            email='test@example.com',
            tip='serviser'
        )
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        
        return {'Authorization': f'Bearer {response.json["token"]}'}
    
    def test_get_clients(self, client, auth_headers):
        """Test getting clients list"""
        # Create test client
        test_client = Client(
            naziv='Test Kompanija',
            tip='pravno_lice',
            adresa='Test adresa 1',
            mesto='Beograd'
        )
        db.session.add(test_client)
        db.session.commit()
        
        response = client.get('/api/clients', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['naziv'] == 'Test Kompanija'
    
    def test_create_client(self, client, auth_headers):
        """Test creating new client"""
        client_data = {
            'naziv': 'Nova Kompanija',
            'tip': 'pravno_lice',
            'adresa': 'Nova adresa 1',
            'mesto': 'Novi Sad',
            'email': 'contact@nova.com'
        }
        
        response = client.post('/api/clients', 
                             json=client_data, 
                             headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['naziv'] == 'Nova Kompanija'
        assert data['email'] == 'contact@nova.com'
        
        # Verify in database
        created_client = Client.query.filter_by(naziv='Nova Kompanija').first()
        assert created_client is not None
        assert created_client.email == 'contact@nova.com'
```

### E2E Test
```javascript
// tests/frontend/e2e/test_create_work_order.js
describe('Create Work Order E2E', () => {
    beforeEach(() => {
        // Setup test data
        cy.login('serviser@test.com', 'password');
        cy.visit('/work-orders/new');
    });

    it('should create work order with QR code scanning', () => {
        // Fill basic work order info
        cy.get('[data-cy=client-select]').select('Test Klijent');
        cy.get('[data-cy=location-select]').select('Glavna lokacija');
        
        // Mock QR code scanning
        cy.get('[data-cy=qr-scanner-btn]').click();
        cy.mockQRScan('DEV-12345'); // Mock QR code scan
        
        // Verify device loaded
        cy.get('[data-cy=device-info]').should('contain', 'Samsung Split');
        
        // Select service type
        cy.get('[data-cy=service-type]').select('redovan_mesecni');
        
        // Add notes
        cy.get('[data-cy=notes]').type('Testiranje E2E workflow-a');
        
        // Save work order
        cy.get('[data-cy=save-btn]').click();
        
        // Verify success
        cy.get('[data-cy=success-message]').should('be.visible');
        cy.url().should('include', '/work-orders/');
        
        // Verify work order was created
        cy.get('[data-cy=work-order-title]').should('contain', 'RNS-2024-');
    });
});
```
