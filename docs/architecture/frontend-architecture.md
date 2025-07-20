# Frontend Architecture

## Component Architecture

### Component Organization
```
frontend/
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   ├── custom.css
│   │   └── mobile.css
│   ├── js/
│   │   ├── bootstrap.bundle.min.js
│   │   ├── app.js              # Main application logic
│   │   ├── qr-scanner.js       # QR code scanning functionality
│   │   ├── work-orders.js      # Work order management
│   │   ├── client-management.js # Client management
│   │   └── utils.js            # Utility functions
│   └── images/
│       ├── icons/
│       └── qr-codes/
├── templates/
│   ├── base.html               # Base template
│   ├── auth/
│   │   ├── login.html
│   │   └── reset-password.html
│   ├── dashboard/
│   │   ├── serviser.html
│   │   └── administrator.html
│   ├── clients/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── form.html
│   ├── devices/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── qr-scanner.html
│   └── work-orders/
│       ├── list.html
│       ├── create.html
│       └── detail.html
```

### Component Template
```html
<!-- Base template structure -->
<!DOCTYPE html>
<html lang="sr" data-bs-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}KDS Sistem{% endblock %}</title>
    <link href="{{ url_for('static', filename='css/bootstrap.min.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/custom.css') }}" rel="stylesheet">
</head>
<body>
    <!-- Navigation based on user role -->
    {% include 'partials/navigation.html' %}
    
    <!-- Main content -->
    <main class="container-fluid">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Scripts -->
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

## State Management Architecture

### State Structure
```javascript
// Global application state - vanilla JavaScript
const AppState = {
    user: {
        id: null,
        ime: '',
        prezime: '',
        tip: null,
        authenticated: false
    },
    
    currentClient: null,
    currentLocation: null,
    currentWorkOrder: null,
    
    breadcrumb: [],
    
    ui: {
        loading: false,
        sidebarCollapsed: false,
        notifications: []
    },
    
    cache: {
        clients: new Map(),
        devices: new Map(),
        workOrders: new Map()
    }
};

// State management patterns
const StateManager = {
    setState(key, value) {
        const keys = key.split('.');
        let current = AppState;
        
        for (let i = 0; i < keys.length - 1; i++) {
            current = current[keys[i]];
        }
        
        current[keys[keys.length - 1]] = value;
        this.notifyStateChange(key, value);
    },
    
    getState(key) {
        const keys = key.split('.');
        let current = AppState;
        
        for (const k of keys) {
            current = current[k];
            if (current === undefined) return null;
        }
        
        return current;
    },
    
    notifyStateChange(key, value) {
        document.dispatchEvent(new CustomEvent('stateChange', {
            detail: { key, value }
        }));
    }
};
```

### State Management Patterns
- Centralized state u global AppState objektu
- Event-driven state updates sa custom events
- Local storage cache za offline funkcionalnost
- Component-specific state za form podatke

## Routing Architecture

### Route Organization
```
# Flask routes organization
/                          # Dashboard (redirect based on user role)
/auth/login               # Login page
/auth/logout              # Logout action
/auth/reset-password      # Password reset

# Client management
/clients                  # Client list
/clients/new              # Create new client
/clients/<id>             # Client details
/clients/<id>/edit        # Edit client
/clients/<id>/locations   # Location management

# Device management  
/devices                  # Device list (filtered by location)
/devices/new              # Add new device
/devices/<id>             # Device details
/devices/<id>/qr          # QR code view/print
/qr-scanner               # QR code scanner

# Work order management
/work-orders              # Work order list
/work-orders/new          # Create new work order
/work-orders/<id>         # Work order details
/work-orders/<id>/edit    # Edit work order
/work-orders/<id>/email   # Send email

# Admin only routes
/admin/users              # User management
/admin/vehicles           # Vehicle management  
/admin/materials          # Material management
/admin/reports            # Reports
```

### Protected Route Pattern
```python
from functools import wraps
from flask import session, redirect, url_for, flash
from flask_login import current_user

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Potrebna je prijava.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.tip != role and current_user.tip != 'administrator':
                flash('Nemate dozvolu za pristup ovoj stranici.', 'error')
                return redirect(url_for('dashboard.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage
@admin_bp.route('/users')
@role_required('administrator')
def users():
    return render_template('admin/users.html')
```

## Frontend Services Layer

### API Client Setup
```javascript
// API client za komunikaciju sa backend-om
class ApiClient {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        };
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: { ...this.defaultHeaders, ...options.headers },
            ...options
        };
        
        // Add CSRF token
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken;
        }
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return await response.text();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    // HTTP method helpers
    get(endpoint, params = {}) {
        const url = new URL(endpoint, window.location.origin + this.baseURL);
        Object.keys(params).forEach(key => 
            url.searchParams.append(key, params[key])
        );
        
        return this.request(url.pathname + url.search);
    }
    
    post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }
}

// Global API instance
const api = new ApiClient();
```

### Service Example
```javascript
// Client management service
class ClientService {
    
    async getClients(filters = {}) {
        try {
            StateManager.setState('ui.loading', true);
            const clients = await api.get('/clients', filters);
            
            // Cache results
            clients.forEach(client => {
                AppState.cache.clients.set(client.id, client);
            });
            
            return clients;
        } catch (error) {
            this.handleError('Greška pri učitavanju klijenata', error);
            throw error;
        } finally {
            StateManager.setState('ui.loading', false);
        }
    }
    
    async createClient(clientData) {
        try {
            const newClient = await api.post('/clients', clientData);
            
            // Update cache
            AppState.cache.clients.set(newClient.id, newClient);
            
            // Show success message
            this.showNotification('Klijent je uspešno kreiran', 'success');
            
            return newClient;
        } catch (error) {
            this.handleError('Greška pri kreiranju klijenta', error);
            throw error;
        }
    }
    
    async scanQRCode(qrData) {
        try {
            const result = await api.post('/qr/scan', { qr_data: qrData });
            
            // Update breadcrumb
            StateManager.setState('breadcrumb', result.breadcrumb);
            StateManager.setState('currentDevice', result.device);
            
            return result;
        } catch (error) {
            this.handleError('QR kod nije prepoznat', error);
            throw error;
        }
    }
    
    handleError(message, error) {
        console.error(message, error);
        this.showNotification(message, 'error');
    }
    
    showNotification(message, type = 'info') {
        const notification = {
            id: Date.now(),
            message,
            type,
            timestamp: new Date()
        };
        
        const notifications = StateManager.getState('ui.notifications') || [];
        notifications.push(notification);
        StateManager.setState('ui.notifications', notifications);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            this.removeNotification(notification.id);
        }, 5000);
    }
    
    removeNotification(id) {
        const notifications = StateManager.getState('ui.notifications') || [];
        const filtered = notifications.filter(n => n.id !== id);
        StateManager.setState('ui.notifications', filtered);
    }
}

// Global service instances
const clientService = new ClientService();
const deviceService = new DeviceService();
const workOrderService = new WorkOrderService();
```
