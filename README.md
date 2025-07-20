# KDS - Sistem za digitalizaciju servisa HVAC uređaja

## Opis

KDS (Kompjuterski Digitalni Servis) je Flask aplikacija za digitalizaciju procesa servisiranja HVAC uređaja. Sistem omogućava upravljanje servisima, korisnicima i firmama kroz jednostavan web interfejs.

## Funkcionalnosti

- **Autentifikacija korisnika** sa dva nivoa pristupa (administrator, serviser)
- **Role-based pristup** sa kontrolom dozvola
- **Responsive dizajn** optimizovan za mobilne uređaje
- **Sigurno hashovanje lozinki** koristeći Werkzeug
- **Flash poruke** za korisničke obaveštenja
- **Bootstrap 5** za moderni UI

## Tehnologije

- **Backend**: Flask 2.3.3, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Baza podataka**: MySQL (remote server)
- **Autentifikacija**: Flask-Login, Werkzeug security

## Instalacija

### Preduslovi

- Python 3.8+
- MySQL server (remote)
- Git

### Korak po korak

1. **Kloniraj repozitorijum**
   ```bash
   git clone <repository-url>
   cd KDS
   ```

2. **Kreiraj virtuelno okruženje**
   ```bash
   python -m venv venvKDS
   venvKDS\Scripts\activate  # Windows
   ```

3. **Instaliraj zavisnosti**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfiguracija okruženja**
   
   Definisati varijable okruženja u fajlu `.env`:
   

5. **Inicijalizuj bazu podataka**
   ```bash
   flask init-db
   ```

6. **Kreiraj administratorski nalog**
   ```bash
   flask create-admin
   ```

7. **Testiraj konekciju sa bazom**
   ```bash
   flask test-db
   ```

## Pokretanje aplikacije

### Development mode

```bash
python app.py
```

ili

```bash
flask run
```

Aplikacija će biti dostupna na: http://localhost:5000

### Production mode

```bash
export FLASK_ENV=production  # Linux/Mac
set FLASK_ENV=production     # Windows
python app.py
```

## Struktura projekta

```
KDS/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/                  # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── views/                   # Blueprint controllers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── dashboard.py
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   └── auth_service.py
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── decorators.py
│   ├── templates/              # Jinja2 templates
│   │   ├── base.html
│   │   ├── auth/
│   │   │   └── login.html
│   │   └── dashboard/
│   │       └── index.html
│   └── static/                 # CSS, JS, images
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── app.js
│       └── img/
├── config.py                   # Konfiguracija aplikacije
├── app.py                      # Glavna aplikacija
├── requirements.txt            # Python zavisnosti
├── .env                        # Environment varijable
└── README.md                   # Dokumentacija
```

## Korišćenje

### Prijavljivanje

1. Idite na http://localhost:5000
2. Unesite kredencijale:
   - **Administrator**: admin@kds.rs / admin123
   - **Serviser**: (kreirajte preko admin panela)

### Tipovi korisnika

- **Administrator**: Pun pristup sistemu, upravljanje korisnicima i firmama
- **Serviser**: Ograničen pristup, fokus na servisne aktivnosti

### Osnovne funkcionalnosti

- **Dashboard**: Pregled osnovnih informacija i statistika
- **Autentifikacija**: Sigurno prijavljivanje/odjavljivanje
- **Role-based pristup**: Automatska kontrola dozvola
- **Responsive dizajn**: Optimizovano za sve uređaje

## CLI komande

```bash
# Inicijalizuj bazu podataka
flask init-db

# Kreiraj administratorski nalog
flask create-admin

# Testiraj konekciju sa bazom
flask test-db

# Pokreni Flask shell
flask shell
```

## Baza podataka

### User tabela

```sql
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
    INDEX idx_tip (tip),
    INDEX idx_aktivan (aktivan)
);
```

## Sigurnost

- **Password hashing**: Werkzeug security
- **Session management**: Flask-Login
- **CSRF zaštita**: Flask-WTF
- **Role-based pristup**: Custom dekoratori
- **Input validacija**: WTForms validators

## Troubleshooting

### Problemi sa bazom podataka

```bash
# Testiraj konekciju
flask test-db

# Reinicijalizuj tabele
flask init-db
```

### Problemi sa autentifikacijom

1. Proverite da li je korisnik aktivan
2. Resetujte lozinku kroz admin panel
3. Proverite tip korisnika i dozvole

## Razvoj

### Dodavanje novih funkcionalnosti

1. Kreirajte novi model u `app/models/`
2. Dodajte business logiku u `app/services/`
3. Kreirajte blueprint u `app/views/`
4. Dodajte template u `app/templates/`
5. Ažurirajte CSS/JS u `app/static/`

### Coding standards

- Koristite srpski jezik za sve user-facing poruke
- Flash messages umesto JS alert-a
- Sve poruke završavaju tačkom
- Koristite `url_for` za linkove
- Sledite PEP 8 za Python kod

## Autor

AI Developer - Windsurf

## Licenca

Privatni projekat - sva prava zadržana.
