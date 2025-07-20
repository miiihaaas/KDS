# KDS Sistem Fullstack Architecture Document

## Introduction

Ovaj dokument definiše kompletnu fullstack arhitekturu za KDS (Sistem radnih naloga) aplikaciju, uključujući backend sisteme, frontend implementaciju i njihovu integraciju. Služi kao jedinstveni izvor istine za AI-driven development, obezbeđujući konzistentnost kroz ceo tehnološki stack.

Ovaj unified pristup kombinuje ono što bi tradicionalno bili zasebni backend i frontend arhitekturni dokumenti, pojednostavljujući development proces za modernu fullstack aplikaciju gde su ovi aspekti sve više isprepletani.

### Starter Template or Existing Project

N/A - Greenfield projekat koji se gradi from scratch.

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2024-01-15 | 1.0 | Inicijalna fullstack arhitektura | Architect |

## High Level Architecture

### Technical Summary

KDS sistem koristi tradicionalnu web arhitekturu sa Flask backend-om i Bootstrap frontend-om, optimizovanim za HVAC servisnu industriju. Sistem je dizajniran kao responzivna web aplikacija sa mobile-first pristupom za servisere u terenu i desktop funkcionalnostima za administratore. Ključne tehnološke komponente uključuju MySQL bazu podataka za perzistentne podatke, QR kod funkcionalnost za brzu identifikaciju uređaja, i email sistem za komunikaciju sa klijentima. Arhitektura podržava role-based pristup sa jasnim razdvojenim workflow-ovima za različite tipove korisnika.

### Platform and Infrastructure Choice

**Platform:** Traditional Web Hosting (VPS/Cloud)
**Key Services:** 
- Web server (Nginx/Apache)
- Flask aplikacija server (Gunicorn)
- MySQL baza podataka
- SMTP email servis
- File storage za QR kodove i reporti

**Deployment Host and Regions:** EU region za GDPR compliance

### Repository Structure

**Structure:** Monorepo
**Monorepo Tool:** N/A (standardna Flask struktura)
**Package Organization:** Modularna organizacija po funkcionalnim domenima

### High Level Architecture Diagram

```mermaid
graph TD
    A[Mobilni Browser - Serviser] --> B[Nginx Reverse Proxy]
    C[Desktop Browser - Administrator] --> B
    B --> D[Flask Application Server]
    D --> E[MySQL Database]
    D --> F[Email Service SMTP]
    D --> G[File Storage QR/Reports]
    D --> H[QR Code Generator/Scanner]
    
    I[QR Code Printer] -.-> A
    J[Camera/Scanner] -.-> A
    
    subgraph "Flask Application"
        D --> K[Authentication Module]
        D --> L[Client Management]
        D --> M[Device Management]
        D --> N[Work Order Module]
        D --> O[Reporting Module]
    end
```

### Architectural Patterns

- **Traditional Web Architecture:** Server-side rendered templates sa client-side enhancements - _Rationale:_ Jednostavnost, brzina development-a i dobra podrška za offline scenarios
- **Model-View-Controller (MVC):** Flask Blueprint organizacija sa jasnim separation of concerns - _Rationale:_ Maintainability i scalability koda
- **Repository Pattern:** Abstraktni data access layer - _Rationale:_ Testabilnost i mogućnost promene baze podataka
- **Role-Based Access Control:** Različiti nivoi pristupa za administratore i servisere - _Rationale:_ Sigurnost i user experience optimizacija
- **Progressive Enhancement:** Osnovna funkcionalnost bez JavaScript, poboljšanja sa JS - _Rationale:_ Pouzdanost u različitim network uslovima

## Tech Stack

### Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-----------|
| Backend Language | Python | 3.9+ | Server-side development | Stabilnost, bogat ecosystem, Flask kompatibilnost |
| Backend Framework | Flask | 2.3.x | Web framework | Lightweight, fleksibilan, dobar za MVP |
| Database | MySQL | 8.0+ | Relational data storage | Pouzdanost, performance, široka podrška |
| Frontend Framework | Bootstrap | 5.3.x | CSS framework | Mobile-first, responsive, komponente |
| Frontend Language | JavaScript (ES6+) | N/A | Client-side interactivity | Native browser support, konzistentnost |
| Template Engine | Jinja2 | 3.1.x | Server-side templating | Integrisan sa Flask, sigurnost |
| ORM | SQLAlchemy | 1.4.x | Database abstraction | Flask-SQLAlchemy integracija |
| Authentication | Flask-Login | 0.6.x | Session management | Standard za Flask aplikacije |
| Form Handling | WTForms | 3.0.x | Form validation | CSRF protection, validacija |
| Email | Flask-Mail | 0.9.x | Email functionality | SMTP integracija za Flask |
| QR Code | qrcode[pil] | 7.4.x | QR code generation | Python biblioteka, PIL podrška |
| Image Processing | Pillow | 10.0.x | Image handling | QR kod processing |
| Testing Framework | pytest | 7.4.x | Unit/integration testing | Pythonic testing approach |
| Web Server | Gunicorn | 21.2.x | WSGI server | Production deployment |
| Reverse Proxy | Nginx | 1.24.x | Load balancing, static files | Performance, security |
| Process Manager | systemd | N/A | Service management | Linux standard |

## Data Models

### User

**Purpose:** Autentifikacija i autorizacija korisnika sistema

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- ime: String(100) - Ime korisnika
- prezime: String(100) - Prezime korisnika
- email: String(255) - Email adresa (unique)
- password_hash: String(255) - Hashovan password
- tip: Enum('administrator', 'serviser') - Tip korisnika
- aktivan: Boolean - Status naloga
- created_at: DateTime - Datum kreiranja
- updated_at: DateTime - Datum poslednje izmene

#### TypeScript Interface
```typescript
interface User {
  id: number;
  ime: string;
  prezime: string;
  email: string;
  tip: 'administrator' | 'serviser';
  aktivan: boolean;
  created_at: string;
  updated_at: string;
}
```

#### Relationships
- One-to-Many sa WorkOrder (serviseri mogu imati više radnih naloga)

### Client

**Purpose:** Upravljanje podacima o klijentima (pravna i fizička lica)

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- naziv: String(255) - Naziv kompanije ili ime fizičkog lica
- tip: Enum('pravno_lice', 'fizicko_lice') - Tip klijenta
- adresa: String(255) - Adresa
- mesto: String(100) - Mesto
- postanski_broj: String(10) - Poštanski broj
- drzava: String(100) - Država
- telefon: String(50) - Telefonski broj
- email: String(255) - Email adresa
- pib: String(20) - PIB (za pravna lica)
- mb: String(20) - Matični broj (za pravna lica)

#### TypeScript Interface
```typescript
interface Client {
  id: number;
  naziv: string;
  tip: 'pravno_lice' | 'fizicko_lice';
  adresa: string;
  mesto: string;
  postanski_broj: string;
  drzava: string;
  telefon?: string;
  email?: string;
  pib?: string;
  mb?: string;
}
```

#### Relationships
- One-to-Many sa Location (klijent može imati više lokacija)

### Location

**Purpose:** Lokacije klijenata (radne jedinice za pravna lica, lokacije kuća za fizička lica)

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- client_id: Integer (Foreign Key) - Referenca na klijenta
- naziv: String(255) - Naziv lokacije
- adresa: String(255) - Adresa lokacije
- mesto: String(100) - Mesto
- postanski_broj: String(10) - Poštanski broj
- drzava: String(100) - Država
- kontakt_osoba: String(255) - Kontakt osoba (za pravna lica)
- telefon: String(50) - Telefonski broj
- email: String(255) - Email adresa

#### TypeScript Interface
```typescript
interface Location {
  id: number;
  client_id: number;
  naziv: string;
  adresa: string;
  mesto: string;
  postanski_broj: string;
  drzava: string;
  kontakt_osoba?: string;
  telefon?: string;
  email?: string;
}
```

#### Relationships
- Many-to-One sa Client
- One-to-Many sa Object

### Object

**Purpose:** Objekti unutar lokacija

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- location_id: Integer (Foreign Key) - Referenca na lokaciju
- naziv: String(255) - Naziv objekta

#### TypeScript Interface
```typescript
interface Object {
  id: number;
  location_id: number;
  naziv: string;
}
```

#### Relationships
- Many-to-One sa Location
- One-to-Many sa Room

### Room

**Purpose:** Prostorije unutar objekata

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- object_id: Integer (Foreign Key) - Referenca na objekat
- naziv: String(255) - Naziv prostorije (opciono)
- numerica_oznaka: String(50) - Numerička oznaka (opciono)

#### TypeScript Interface
```typescript
interface Room {
  id: number;
  object_id: number;
  naziv?: string;
  numerica_oznaka?: string;
}
```

#### Relationships
- Many-to-One sa Object
- One-to-Many sa Device

### Device

**Purpose:** HVAC uređaji u prostórijama

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- room_id: Integer (Foreign Key) - Referenca na prostoriju
- proizvodjac: String(255) - Proizvođač
- model: String(255) - Model uređaja
- serijski_broj: String(255) - Serijski broj (opciono)
- inventarski_broj: String(255) - Inventarski broj kod klijenta (opciono)
- godina_proizvodnje: Integer - Godina proizvodnje (opciono)
- tip: Enum('rashladna_tehnika', 'grejna_tehnika', 'ventilacioni_sistemi') - Tip uređaja
- podtip: String(100) - Podtip uređaja
- jedinstveni_id: String(50) - Jedinstveni ID za QR kod (auto-generated)
- garantni_rok_meseci: Integer - Garantni rok u mesecima

#### TypeScript Interface
```typescript
interface Device {
  id: number;
  room_id: number;
  proizvodjac: string;
  model: string;
  serijski_broj?: string;
  inventarski_broj?: string;
  godina_proizvodnje?: number;
  tip: 'rashladna_tehnika' | 'grejna_tehnika' | 'ventilacioni_sistemi';
  podtip: string;
  jedinstveni_id: string;
  garantni_rok_meseci?: number;
}
```

#### Relationships
- Many-to-One sa Room
- One-to-Many sa WorkOrderItem

### WorkOrder

**Purpose:** Radni nalozi za servise, popravke i montaže

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- broj_naloga: String(50) - Auto-generated broj (RNS/RNP/RNM-YYYY-NNN)
- client_id: Integer (Foreign Key) - Referenca na klijenta
- location_id: Integer (Foreign Key) - Referenca na lokaciju
- status: Enum('u_radu', 'zavrsen', 'fakturisan', 'otkazan') - Status naloga
- datum_otvaranja: DateTime - Datum i vreme otvaranja
- datum_zatvaranja: DateTime - Datum i vreme zatvaranja (opciono)
- broj_naloga_narucioca: String(100) - Broj naloga naručioca (opciono)
- porudzbenica: String(255) - Porudžbenica (opciono)
- napomena_servisa: Text - Opšta napomena za servis
- ukupan_broj_norma_sati: Integer - Ukupan broj norma sati (opciono)

#### TypeScript Interface
```typescript
interface WorkOrder {
  id: number;
  broj_naloga: string;
  client_id: number;
  location_id: number;
  status: 'u_radu' | 'zavrsen' | 'fakturisan' | 'otkazan';
  datum_otvaranja: string;
  datum_zatvaranja?: string;
  broj_naloga_narucioca?: string;
  porudzbenica?: string;
  napomena_servisa?: string;
  ukupan_broj_norma_sati?: number;
}
```

#### Relationships
- Many-to-One sa Client
- Many-to-One sa Location
- Many-to-Many sa User (serviseri)
- One-to-Many sa WorkOrderItem

### WorkOrderItem

**Purpose:** Stavke radnog naloga (servisi, popravke, montaže)

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- work_order_id: Integer (Foreign Key) - Referenca na radni nalog
- device_id: Integer (Foreign Key) - Referenca na uređaj
- tip: Enum('servis', 'popravka', 'montaza') - Tip stavke
- vrsta_servisa: String(100) - Vrsta servisa (za servis stavke)
- napomena: Text - Napomena za stavku
- datum_izvrsavanja: DateTime - Datum izvršavanja

#### TypeScript Interface
```typescript
interface WorkOrderItem {
  id: number;
  work_order_id: number;
  device_id: number;
  tip: 'servis' | 'popravka' | 'montaza';
  vrsta_servisa?: string;
  napomena?: string;
  datum_izvrsavanja: string;
}
```

#### Relationships
- Many-to-One sa WorkOrder
- Many-to-One sa Device
- One-to-Many sa MaterialUsage

### Material

**Purpose:** Potrošni materijali

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- naziv: String(255) - Naziv materijala
- jedinica_mere: String(50) - Jedinica mere

#### TypeScript Interface
```typescript
interface Material {
  id: number;
  naziv: string;
  jedinica_mere: string;
}
```

#### Relationships
- One-to-Many sa MaterialUsage

### MaterialUsage

**Purpose:** Korišćenje materijala u radnim nalozima

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- work_order_item_id: Integer (Foreign Key) - Referenca na stavku radnog naloga
- material_id: Integer (Foreign Key) - Referenca na materijal
- kolicina: Decimal(10,2) - Količina
- serijski_broj: String(255) - Serijski broj (opciono)
- ostali_podaci: Text - Ostali podaci (opciono)

#### TypeScript Interface
```typescript
interface MaterialUsage {
  id: number;
  work_order_item_id: number;
  material_id: number;
  kolicina: number;
  serijski_broj?: string;
  ostali_podaci?: string;
}
```

#### Relationships
- Many-to-One sa WorkOrderItem
- Many-to-One sa Material

### Vehicle

**Purpose:** Službena vozila

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- marka: String(100) - Marka vozila
- model: String(100) - Model vozila
- registracija: String(50) - Registracija vozila

#### TypeScript Interface
```typescript
interface Vehicle {
  id: number;
  marka: string;
  model: string;
  registracija: string;
}
```

#### Relationships
- Many-to-Many sa WorkOrder

## API Specification

### REST API Overview

KDS sistem koristi RESTful API dizajn sa jasno definisanim endpoint-ima za sve entitete. API podržava JSON format za komunikaciju i implementira standardne HTTP status kodove.

### Authentication API

```yaml
/auth/login:
  post:
    summary: User authentication
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
    responses:
      200:
        description: Successful login
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                user:
                  $ref: '#/components/schemas/User'
      401:
        description: Invalid credentials

/auth/logout:
  post:
    summary: User logout
    responses:
      200:
        description: Successful logout
```

### Client Management API

```yaml
/api/clients:
  get:
    summary: Get all clients
    parameters:
      - name: search
        in: query
        schema:
          type: string
      - name: tip
        in: query
        schema:
          type: string
          enum: [pravno_lice, fizicko_lice]
    responses:
      200:
        description: List of clients
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Client'
  
  post:
    summary: Create new client
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Client'
    responses:
      201:
        description: Client created
      400:
        description: Validation error

/api/clients/{id}:
  get:
    summary: Get client by ID
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Client details
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Client'
      404:
        description: Client not found
```

### Device Management API

```yaml
/api/devices:
  get:
    summary: Get devices
    parameters:
      - name: room_id
        in: query
        schema:
          type: integer
      - name: tip
        in: query
        schema:
          type: string
    responses:
      200:
        description: List of devices

/api/devices/{id}/qr:
  get:
    summary: Get QR code for device
    responses:
      200:
        description: QR code image
        content:
          image/png:
            schema:
              type: string
              format: binary

/api/qr/scan:
  post:
    summary: Process scanned QR code
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              qr_data:
                type: string
    responses:
      200:
        description: Device information
        content:
          application/json:
            schema:
              type: object
              properties:
                device:
                  $ref: '#/components/schemas/Device'
                breadcrumb:
                  type: array
                  items:
                    type: object
```

### Work Order API

```yaml
/api/work-orders:
  get:
    summary: Get work orders
    parameters:
      - name: status
        in: query
        schema:
          type: string
      - name: serviser_id
        in: query
        schema:
          type: integer
      - name: date_from
        in: query
        schema:
          type: string
          format: date
      - name: date_to
        in: query
        schema:
          type: string
          format: date
    responses:
      200:
        description: List of work orders

  post:
    summary: Create new work order
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/WorkOrder'
    responses:
      201:
        description: Work order created

/api/work-orders/{id}/email:
  post:
    summary: Send work order via email
    responses:
      200:
        description: Email sent successfully
      500:
        description: Email sending failed
```

## Frontend Architecture

### Component Architecture

#### Component Organization
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

#### Component Template
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

### State Management Architecture

#### State Structure
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

#### State Management Patterns
- Centralized state u global AppState objektu
- Event-driven state updates sa custom events
- Local storage cache za offline funkcionalnost
- Component-specific state za form podatke

### Routing Architecture

#### Route Organization
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

#### Protected Route Pattern
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

### Frontend Services Layer

#### API Client Setup
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

#### Service Example
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

## Backend Architecture

### Service Architecture

#### Controller Organization
```
app/
├── __init__.py              # Flask app factory
├── models/                  # SQLAlchemy models
│   ├── __init__.py
│   ├── user.py
│   ├── client.py
│   ├── device.py
│   ├── work_order.py
│   └── material.py
├── views/                   # Blueprint controllers
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   ├── dashboard.py        # Dashboard routes
│   ├── clients.py          # Client management
│   ├── devices.py          # Device management
│   ├── work_orders.py      # Work order management
│   ├── admin.py            # Admin-only routes
│   └── api.py              # REST API endpoints
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── auth_service.py
│   ├── client_service.py
│   ├── device_service.py
│   ├── work_order_service.py
│   ├── qr_service.py
│   └── email_service.py
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── validators.py
│   ├── helpers.py
│   └── decorators.py
└── config.py               # Configuration
```

#### Controller Template
```python
# Example: Client management controller
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.services.client_service import ClientService
from app.utils.decorators import role_required
from app.forms.client_forms import ClientForm

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
@login_required
def index():
    """Client list page"""
    search = request.args.get('search', '')
    tip = request.args.get('tip', '')
    
    clients = ClientService.get_clients(
        search=search, 
        tip=tip, 
        user=current_user
    )
    
    return render_template('clients/list.html', 
                         clients=clients, 
                         search=search, 
                         tip=tip)

@clients_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    """Create new client"""
    form = ClientForm()
    
    if form.validate_on_submit():
        try:
            client = ClientService.create_client(form.data, current_user)
            flash('Klijent je uspešno kreiran.', 'success')
            return redirect(url_for('clients.detail', id=client.id))
        except Exception as e:
            flash(f'Greška: {str(e)}', 'error')
    
    return render_template('clients/form.html', form=form)

@clients_bp.route('/<int:id>')
@login_required  
def detail(id):
    """Client details page"""
    client = ClientService.get_client_by_id(id, current_user)
    if not client:
        flash('Klijent nije pronađen.', 'error')
        return redirect(url_for('clients.index'))
    
    return render_template('clients/detail.html', client=client)

# API endpoints
@clients_bp.route('/api/clients', methods=['GET'])
@login_required
def api_get_clients():
    """API endpoint for getting clients"""
    try:
        filters = {
            'search': request.args.get('search', ''),
            'tip': request.args.get('tip', '')
        }
        
        clients = ClientService.get_clients_api(filters, current_user)
        return jsonify(clients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/api/clients', methods=['POST'])
@login_required
def api_create_client():
    """API endpoint for creating client"""
    try:
        data = request.get_json()
        client = ClientService.create_client_api(data, current_user)
        return jsonify(client), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Interna greška servera'}), 500
```

### Database Architecture

#### Schema Design
```sql
-- User table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ime VARCHAR(100) NOT NULL,
    prezime VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    tip ENUM('administrator', 'serviser') NOT NULL,
    aktivan BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_tip (tip)
);

-- Client table
CREATE TABLE clients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    naziv VARCHAR(255) NOT NULL,
    tip ENUM('pravno_lice', 'fizicko_lice') NOT NULL,
    adresa VARCHAR(255) NOT NULL,
    mesto VARCHAR(100) NOT NULL,
    postanski_broj VARCHAR(10),
    drzava VARCHAR(100) DEFAULT 'Srbija',
    telefon VARCHAR(50),
    email VARCHAR(255),
    pib VARCHAR(20),
    mb VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_naziv (naziv),
    INDEX idx_tip (tip),
    INDEX idx_email (email)
);

-- Locations table
CREATE TABLE locations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT NOT NULL,
    naziv VARCHAR(255) NOT NULL,
    adresa VARCHAR(255) NOT NULL,
    mesto VARCHAR(100) NOT NULL,
    postanski_broj VARCHAR(10),
    drzava VARCHAR(100) DEFAULT 'Srbija',
    kontakt_osoba VARCHAR(255),
    telefon VARCHAR(50),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    INDEX idx_client_id (client_id)
);

-- Objects table
CREATE TABLE objects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    location_id INT NOT NULL,
    naziv VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    INDEX idx_location_id (location_id)
);

-- Rooms table
CREATE TABLE rooms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    object_id INT NOT NULL,
    naziv VARCHAR(255),
    numerica_oznaka VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (object_id) REFERENCES objects(id) ON DELETE CASCADE,
    INDEX idx_object_id (object_id)
);

-- Devices table
CREATE TABLE devices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    room_id INT NOT NULL,
    proizvodjac VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    serijski_broj VARCHAR(255),
    inventarski_broj VARCHAR(255),
    godina_proizvodnje INT,
    tip ENUM('rashladna_tehnika', 'grejna_tehnika', 'ventilacioni_sistemi') NOT NULL,
    podtip VARCHAR(100),
    jedinstveni_id VARCHAR(50) UNIQUE NOT NULL,
    garantni_rok_meseci INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    INDEX idx_room_id (room_id),
    INDEX idx_jedinstveni_id (jedinstveni_id),
    INDEX idx_tip (tip)
);

-- Work orders table
CREATE TABLE work_orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    broj_naloga VARCHAR(50) UNIQUE NOT NULL,
    client_id INT NOT NULL,
    location_id INT NOT NULL,
    status ENUM('u_radu', 'zavrsen', 'fakturisan', 'otkazan') DEFAULT 'u_radu',
    datum_otvaranja TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    datum_zatvaranja TIMESTAMP NULL,
    broj_naloga_narucioca VARCHAR(100),
    porudzbenica VARCHAR(255),
    napomena_servisa TEXT,
    ukupan_broj_norma_sati INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
    INDEX idx_broj_naloga (broj_naloga),
    INDEX idx_client_id (client_id),
    INDEX idx_status (status),
    INDEX idx_datum_otvaranja (datum_otvaranja)
);

-- Work order items table  
CREATE TABLE work_order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    work_order_id INT NOT NULL,
    device_id INT NOT NULL,
    tip ENUM('servis', 'popravka', 'montaza') NOT NULL,
    vrsta_servisa VARCHAR(100),
    napomena TEXT,
    datum_izvrsavanja TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (work_order_id) REFERENCES work_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (device_id) REFERENCES devices(id),
    INDEX idx_work_order_id (work_order_id),
    INDEX idx_device_id (device_id),
    INDEX idx_tip (tip)
);

-- Materials table
CREATE TABLE materials (
    id INT PRIMARY KEY AUTO_INCREMENT,
    naziv VARCHAR(255) NOT NULL,
    jedinica_mere VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_naziv (naziv)
);

-- Material usage table
CREATE TABLE material_usage (
    id INT PRIMARY KEY AUTO_INCREMENT,
    work_order_item_id INT NOT NULL,
    material_id INT NOT NULL,
    kolicina DECIMAL(10,2) NOT NULL,
    serijski_broj VARCHAR(255),
    ostali_podaci TEXT,
    FOREIGN KEY (work_order_item_id) REFERENCES work_order_items(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materials(id),
    INDEX idx_work_order_item_id (work_order_item_id),
    INDEX idx_material_id (material_id)
);

-- Vehicles table
CREATE TABLE vehicles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    marka VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    registracija VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_registracija (registracija)
);

-- Work order servicer assignment (many-to-many)
CREATE TABLE work_order_servicers (
    work_order_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (work_order_id, user_id),
    FOREIGN KEY (work_order_id) REFERENCES work_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Work order vehicle assignment (many-to-many)  
CREATE TABLE work_order_vehicles (
    work_order_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    PRIMARY KEY (work_order_id, vehicle_id),
    FOREIGN KEY (work_order_id) REFERENCES work_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);
```

#### Data Access Layer
```python
# Repository pattern implementation
from app import db
from app.models.client import Client
from sqlalchemy import or_

class ClientRepository:
    
    @staticmethod
    def find_all(search=None, tip=None, limit=None, offset=None):
        """Find clients with optional filtering"""
        query = Client.query
        
        if search:
            query = query.filter(
                or_(
                    Client.naziv.ilike(f'%{search}%'),
                    Client.email.ilike(f'%{search}%'),
                    Client.mesto.ilike(f'%{search}%')
                )
            )
        
        if tip:
            query = query.filter(Client.tip == tip)
        
        query = query.order_by(Client.naziv)
        
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        
        return query.all()
    
    @staticmethod
    def find_by_id(client_id):
        """Find client by ID"""
        return Client.query.get(client_id)
    
    @staticmethod
    def create(client_data):
        """Create new client"""
        client = Client(**client_data)
        db.session.add(client)
        db.session.commit()
        return client
    
    @staticmethod
    def update(client_id, update_data):
        """Update existing client"""
        client = Client.query.get(client_id)
        if not client:
            return None
        
        for key, value in update_data.items():
            setattr(client, key, value)
        
        db.session.commit()
        return client
    
    @staticmethod
    def delete(client_id):
        """Delete client"""
        client = Client.query.get(client_id)
        if not client:
            return False
        
        db.session.delete(client)
        db.session.commit()
        return True
    
    @staticmethod
    def count(search=None, tip=None):
        """Count clients with optional filtering"""
        query = Client.query
        
        if search:
            query = query.filter(
                or_(
                    Client.naziv.ilike(f'%{search}%'),
                    Client.email.ilike(f'%{search}%'),
                    Client.mesto.ilike(f'%{search}%')
                )
            )
        
        if tip:
            query = query.filter(Client.tip == tip)
        
        return query.count()
```

### Authentication and Authorization

#### Auth Flow
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Flask
    participant Database
    
    User->>Frontend: Enter credentials
    Frontend->>Flask: POST /auth/login
    Flask->>Database: Verify user credentials
    Database-->>Flask: User data
    Flask->>Flask: Create session
    Flask-->>Frontend: Login success + user data
    Frontend->>Frontend: Update UI state
    Frontend-->>User: Dashboard redirect
    
    Note over Flask: Session-based authentication
    Note over Frontend: Store user state in JavaScript
```

#### Middleware/Guards
```python
# Authentication middleware for API routes
from functools import wraps
from flask import jsonify, session
from flask_login import current_user

def api_auth_required(f):
    """Decorator for API routes requiring authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentifikacija je potrebna'}), 401
        return f(*args, **kwargs)
    return decorated_function

def api_role_required(required_role):
    """Decorator for API routes requiring specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentifikacija je potrebna'}), 401
            
            if (current_user.tip != required_role and 
                current_user.tip != 'administrator'):
                return jsonify({'error': 'Nemate dozvolu'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage example
@api_bp.route('/admin/users', methods=['GET'])
@api_auth_required
@api_role_required('administrator')
def get_users():
    """API endpoint for getting users - admin only"""
    users = UserService.get_all_users()
    return jsonify([user.to_dict() for user in users])
```

## Unified Project Structure

```
kds-sistem/
├── app/                              # Flask application
│   ├── __init__.py                   # App factory
│   ├── models/                       # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── device.py
│   │   ├── work_order.py
│   │   ├── material.py
│   │   └── vehicle.py
│   ├── views/                        # Flask blueprints
│   │   ├── __init__.py
│   │   ├── auth.py                   # Authentication routes
│   │   ├── dashboard.py              # Dashboard routes
│   │   ├── clients.py                # Client management
│   │   ├── devices.py                # Device management
│   │   ├── work_orders.py            # Work order management
│   │   ├── admin.py                  # Admin routes
│   │   └── api.py                    # REST API endpoints
│   ├── services/                     # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── client_service.py
│   │   ├── device_service.py
│   │   ├── work_order_service.py
│   │   ├── qr_service.py
│   │   └── email_service.py
│   ├── forms/                        # WTForms form classes
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── client_forms.py
│   │   ├── device_forms.py
│   │   └── work_order_forms.py
│   ├── utils/                        # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── decorators.py
│   ├── static/                       # Static files
│   │   ├── css/
│   │   │   ├── bootstrap.min.css
│   │   │   ├── custom.css
│   │   │   └── mobile.css
│   │   ├── js/
│   │   │   ├── bootstrap.bundle.min.js
│   │   │   ├── app.js               # Main app logic
│   │   │   ├── qr-scanner.js        # QR functionality
│   │   │   ├── work-orders.js       # Work order management
│   │   │   ├── client-management.js # Client management
│   │   │   └── utils.js             # Utility functions
│   │   ├── images/
│   │   │   ├── icons/
│   │   │   └── qr-codes/            # Generated QR codes
│   │   └── fonts/
│   └── templates/                    # Jinja2 templates
│       ├── base.html                 # Base template
│       ├── partials/                 # Reusable template parts
│       │   ├── navigation.html
│       │   ├── breadcrumb.html
│       │   └── notifications.html
│       ├── auth/
│       │   ├── login.html
│       │   └── reset-password.html
│       ├── dashboard/
│       │   ├── serviser.html
│       │   └── administrator.html
│       ├── clients/
│       │   ├── list.html
│       │   ├── detail.html
│       │   ├── form.html
│       │   └── hierarchy.html
│       ├── devices/
│       │   ├── list.html
│       │   ├── detail.html
│       │   ├── form.html
│       │   └── qr-scanner.html
│       ├── work-orders/
│       │   ├── list.html
│       │   ├── create.html
│       │   ├── detail.html
│       │   ├── edit.html
│       │   └── email-template.html
│       ├── admin/
│       │   ├── users.html
│       │   ├── vehicles.html
│       │   ├── materials.html
│       │   └── reports.html
│       └── errors/
│           ├── 404.html
│           └── 500.html
├── migrations/                       # Database migrations
│   ├── versions/
│   └── alembic.ini
├── tests/                           # Test files
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── test_api.py
│   │   ├── test_auth.py
│   │   └── test_workflows.py
│   └── fixtures/
│       ├── test_data.sql
│       └── sample_qr_codes.py
├── scripts/                         # Utility scripts
│   ├── init_db.py                   # Database initialization
│   ├── create_admin.py              # Create admin user
│   └── generate_sample_data.py      # Sample data for testing
├── docs/                           # Project documentation
│   ├── project-brief.md
│   ├── prd.md
│   ├── front-end-spec.md
│   └── fullstack-architecture.md
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project readme
└── run.py                          # Application entry point
```

## Development Workflow

### Local Development Setup

#### Prerequisites
```bash
# Python 3.9+ installation
python --version  # Should be 3.9 or higher

# MySQL installation and setup
mysql --version   # Should be 8.0 or higher

# Virtual environment creation
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

#### Initial Setup
```bash
# Clone/create project directory
mkdir kds-sistem
cd kds-sistem

# Install dependencies
pip install -r requirements.txt

# Database setup
mysql -u root -p
CREATE DATABASE kds_sistem CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'kds_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON kds_sistem.* TO 'kds_user'@'localhost';
FLUSH PRIVILEGES;
exit

# Environment configuration
cp .env.example .env
# Edit .env with your database credentials and other settings

# Initialize database
python scripts/init_db.py

# Create admin user
python scripts/create_admin.py

# Generate sample data (optional)
python scripts/generate_sample_data.py
```

#### Dev Commands
```bash
# Start development server
python run.py

# Run with debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py

# Database migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run tests
pytest
pytest --coverage

# Code formatting
black app/
flake8 app/
```

### Environment Configuration

#### Required Environment Variables
```bash
# Database configuration (.env)
DATABASE_URL=mysql://kds_user:your_password@localhost/kds_sistem

# Flask configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1

# Email configuration (SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# File upload settings
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# QR Code settings
QR_CODE_FOLDER=app/static/images/qr-codes
QR_CODE_SIZE=200

# Security settings
SESSION_TIMEOUT=3600  # 1 hour
PASSWORD_MIN_LENGTH=8
LOGIN_ATTEMPTS_LIMIT=5
```

## Deployment Architecture

### Deployment Strategy

**Frontend Deployment:**
- **Platform:** Same server as backend (integrated Flask app)
- **Build Command:** N/A (static files served directly)
- **Output Directory:** app/static/
- **CDN/Edge:** Optional Nginx caching for static assets

**Backend Deployment:**
- **Platform:** Ubuntu/CentOS VPS or cloud instance
- **Build Command:** pip install -r requirements.txt
- **Deployment Method:** Gunicorn + Nginx reverse proxy

### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml (GitHub Actions example)
name: Deploy KDS Sistem

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /var/www/kds-sistem
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          flask db upgrade
          sudo systemctl restart kds-sistem
          sudo systemctl reload nginx
```

### Environments

| Environment | Frontend URL | Backend URL | Purpose |
|-------------|--------------|-------------|---------|
| Development | http://localhost:5000 | http://localhost:5000 | Lokalni development |
| Staging | https://staging.kds-sistem.com | https://staging.kds-sistem.com | Pre-production testing |
| Production | https://kds-sistem.com | https://kds-sistem.com | Live environment |

## Security and Performance

### Security Requirements

**Frontend Security:**
- CSP Headers: `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';`
- XSS Prevention: Jinja2 auto-escaping enabled, input sanitization
- Secure Storage: Session cookies with secure flags

**Backend Security:**
- Input Validation: WTForms validation za sve forme
- Rate Limiting: Flask-Limiter za login endpoint-e
- CORS Policy: Restricted to same origin

**Authentication Security:**
- Token Storage: Server-side sessions sa Flask-Login
- Session Management: Secure session cookies, auto logout
- Password Policy: Minimum 8 karaktera, hash sa werkzeug

### Performance Optimization

**Frontend Performance:**
- Bundle Size Target: < 500KB total JavaScript
- Loading Strategy: Lazy loading za QR scanner komponente
- Caching Strategy: Browser caching za static assets (1 mesec)

**Backend Performance:**
- Response Time Target: < 500ms za API pozive
- Database Optimization: Proper indexing, query optimization
- Caching Strategy: Flask-Caching za često pristupane podatke

## Testing Strategy

### Testing Pyramid
```
                Unit Tests
               /            \
          Integration Tests
             /              \
        End-to-End Tests
```

### Test Organization

#### Frontend Tests
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

#### Backend Tests
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

### Test Examples

#### Frontend Component Test
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

#### Backend API Test
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

#### E2E Test
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

## Coding Standards

### Critical Fullstack Rules

- **Konzistentnost JavaScript-a**: Koristi vanilla ES6+ JavaScript kroz ceo frontend bez mešanja framework-ova
- **Flask Blueprint organizacija**: Svaki funkcionalni domen ima svoj blueprint (auth, clients, devices, work_orders, admin)
- **Template nasleđivanje**: Svi template-i naslеđuju base.html i koriste block strukture
- **API response format**: Svi API endpoint-i vraćaju konzistentne JSON structure sa standardnim error handling-om
- **Database transaction handling**: Koristi try/except/rollback pattern za sve database operacije
- **QR kod standard**: Svi QR kodovi koriste isti format (jedinstveni_id) i generation/scanning library
- **Session management**: Koristi Flask-Login za sve authentication/authorization potrebe

### Naming Conventions

| Element | Frontend | Backend | Example |
|---------|----------|---------|---------|
| CSS Classes | kebab-case | N/A | `.client-card`, `.qr-scanner-btn` |
| JavaScript Functions | camelCase | N/A | `scanQRCode()`, `createWorkOrder()` |
| JavaScript Variables | camelCase | N/A | `currentClient`, `workOrderData` |
| Python Functions | snake_case | snake_case | `get_client_by_id()`, `create_work_order()` |
| Python Classes | PascalCase | PascalCase | `ClientService`, `WorkOrderForm` |
| Database Tables | snake_case | snake_case | `work_orders`, `material_usage` |
| Flask Routes | kebab-case | kebab-case | `/work-orders/new`, `/api/qr-scan` |
| Template Files | kebab-case | snake_case | `work-order-detail.html` |

## Error Handling Strategy

### Error Flow
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Flask
    participant Database
    
    User->>Frontend: Submit form/action
    Frontend->>Flask: API request
    Flask->>Database: Query
    Database-->>Flask: Error response
    Flask->>Flask: Log error
    Flask-->>Frontend: Structured error response
    Frontend->>Frontend: Parse error & update UI
    Frontend-->>User: User-friendly error message
```

### Error Response Format
```typescript
interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
    timestamp: string;
    request_id: string;
  };
}
```

### Frontend Error Handling
```javascript
// Global error handler
class ErrorHandler {
    static handle(error, context = '') {
        console.error(`Error in ${context}:`, error);
        
        // Parse API errors
        if (error.response && error.response.error) {
            this.showUserError(error.response.error.message);
            this.logError(error.response.error);
        } else if (error.message) {
            this.showUserError('Došlo je do greške. Molimo pokušajte ponovo.');
            this.logError({ message: error.message, context });
        } else {
            this.showUserError('Neočekivana greška. Molimo kontaktirajte podršku.');
            this.logError({ error: 'Unknown error', context });
        }
    }
    
    static showUserError(message) {
        // Show user-friendly notification
        const notification = {
            type: 'error',
            message: message,
            duration: 5000
        };
        
        StateManager.setState('ui.notifications', [notification]);
    }
    
    static logError(errorData) {
        // Send error to logging service (optional)
        if (window.errorLoggingEnabled) {
            fetch('/api/log-error', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ...errorData,
                    userAgent: navigator.userAgent,
                    url: window.location.href,
                    timestamp: new Date().toISOString()
                })
            }).catch(() => {
                // Silent fail for logging
            });
        }
    }
}

// Usage in API calls
async function createWorkOrder(workOrderData) {
    try {
        const result = await api.post('/work-orders', workOrderData);
        return result;
    } catch (error) {
        ErrorHandler.handle(error, 'createWorkOrder');
        throw error; // Re-throw for component handling
    }
}
```

### Backend Error Handling
```python
# Global error handlers
from flask import jsonify, request
import logging
import uuid
from datetime import datetime

class KDSException(Exception):
    """Base exception class for KDS system"""
    def __init__(self, message, code='GENERAL_ERROR', details=None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(KDSException):
    def __init__(self, message, field=None):
        super().__init__(message, 'VALIDATION_ERROR', {'field': field})

class NotFoundError(KDSException):
    def __init__(self, resource, resource_id=None):
        message = f'{resource} nije pronađen'
        if resource_id:
            message += f' (ID: {resource_id})'
        super().__init__(message, 'NOT_FOUND')

# Error handlers registration
def register_error_handlers(app):
    
    @app.errorhandler(KDSException)
    def handle_kds_exception(error):
        request_id = str(uuid.uuid4())
        
        # Log error
        app.logger.error(f'KDS Exception [{request_id}]: {error.message}', 
                        extra={'details': error.details})
        
        return jsonify({
            'error': {
                'code': error.code,
                'message': error.message,
                'details': error.details,
                'timestamp': datetime.utcnow().isoformat(),
                'request_id': request_id
            }
        }), 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        request_id = str(uuid.uuid4())
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': {
                    'code': 'NOT_FOUND',
                    'message': 'Endpoint nije pronađen',
                    'timestamp': datetime.utcnow().isoformat(),
                    'request_id': request_id
                }
            }), 404
        
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        request_id = str(uuid.uuid4())
        
        # Log detailed error
        app.logger.error(f'Internal Server Error [{request_id}]: {str(error)}')
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'Interna greška servera',
                    'timestamp': datetime.utcnow().isoformat(),
                    'request_id': request_id
                }
            }), 500
        
        return render_template('errors/500.html'), 500

# Usage in services
class ClientService:
    
    @staticmethod
    def get_client_by_id(client_id, user):
        client = ClientRepository.find_by_id(client_id)
        
        if not client:
            raise NotFoundError('Klijent', client_id)
        
        # Additional authorization check
        if user.tip == 'serviser' and not client.accessible_by_user(user):
            raise KDSException('Nemate dozvolu za pristup ovom klijentu', 
                             'ACCESS_DENIED')
        
        return client
    
    @staticmethod
    def create_client(client_data, user):
        try:
            # Validate data
            if not client_data.get('naziv'):
                raise ValidationError('Naziv je obavezan', 'naziv')
            
            if not client_data.get('tip'):
                raise ValidationError('Tip klijenta je obavezan', 'tip')
            
            # Create client
            client = ClientRepository.create(client_data)
            
            app.logger.info(f'Client created: {client.id} by user {user.id}')
            return client
            
        except Exception as e:
            db.session.rollback()
            if isinstance(e, KDSException):
                raise
            else:
                app.logger.error(f'Unexpected error creating client: {str(e)}')
                raise KDSException('Greška pri kreiranju klijenta')
```

## Monitoring and Observability

### Monitoring Stack

- **Frontend Monitoring:** Browser console logging + optional external service
- **Backend Monitoring:** Python logging + Flask-Logging
- **Error Tracking:** Custom error logging to database
- **Performance Monitoring:** Basic response time logging

### Key Metrics

**Frontend Metrics:**
- Page load times
- JavaScript errors
- API response times
- User interactions (QR scans, form submissions)

**Backend Metrics:**
- Request rate per endpoint
- Response times
- Database query performance
- Email delivery success rate
- Authentication success/failure rates

Ovo je kompletna fullstack arhitektura za KDS sistem koja pokriva sve aspekte od backend-a do frontend-a. Arhitektura je optimizovana za HVAC servisnu industriju sa fokusom na mobilno korišćenje i QR kod funkcionalnost.