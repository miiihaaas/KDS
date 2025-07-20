# Story 1.1: Kreiranje osnovne Flask aplikacije sa autentifikacijom

## Metadata
- **Story ID**: 1.1
- **Epic**: Epic 1 - Sistem osnove i autentifikacija
- **Priority**: High
- **Story Points**: 8
- **Status**: Done
- **Created**: 2025-01-19
- **Assigned To**: AI Developer

## User Story
**As a** developer  
**I want to** set up the basic Flask application structure with authentication  
**So that** the foundation for the KDS system is established with secure user access

## Business Context
KDS sistem treba da digitalizuje kompletan proces servisiranja HVAC uređaja. Ova priča postavlja osnovnu infrastrukturu aplikacije sa sigurnim pristupom koji omogućava dva nivoa korisnika (administrator i serviser).

## Acceptance Criteria

### AC1: Osnovna Flask aplikacija struktura
- **Given** da treba kreirati novu Flask aplikaciju
- **When** se pokreće development server
- **Then** aplikacija se uspešno pokreće bez grešaka
- **And** struktura foldera je organizovana prema backend arhitekturi:
  ```
  app/
  ├── __init__.py              # Flask app factory
  ├── models/                  # SQLAlchemy models
  │   ├── __init__.py
  │   └── user.py
  ├── views/                   # Blueprint controllers
  │   ├── __init__.py
  │   ├── auth.py
  │   └── dashboard.py
  ├── services/               # Business logic layer
  │   ├── __init__.py
  │   └── auth_service.py
  ├── utils/                  # Utility functions
  │   ├── __init__.py
  │   ├── validators.py
  │   └── decorators.py
  ├── templates/              # Jinja2 templates
  │   ├── base.html
  │   ├── auth/
  │   └── dashboard/
  └── static/                 # CSS, JS, images
      ├── css/
      ├── js/
      └── img/
  ```

### AC2: MySQL konekcija i konfiguracija
- **Given** da aplikacija koristi MySQL bazu podataka
- **When** se aplikacija pokreće
- **Then** konekcija sa bazom je uspešno uspostavljena
- **And** SQLAlchemy je konfigurisano sa odgovarajućim connection string-om
- **And** postoji `config.py` fajl sa development i production konfiguracijama

### AC3: Bootstrap integracija za responsive design
- **Given** da aplikacija mora biti optimizovana za mobilne uređaje
- **When** se učitava bilo koja stranica
- **Then** Bootstrap 5 je uspešno integrisan
- **And** stranice su responsive i prilagođavaju se mobilnim uređajima
- **And** postoji osnovni `base.html` template sa Bootstrap komponentama

### AC4: User model i autentifikacija
- **Given** da sistem podržava dva nivoa korisnika
- **When** se kreira User model
- **Then** model sadrži sledeća polja:
  - `id`: Integer (Primary Key)
  - `ime`: String(100) - Ime korisnika
  - `prezime`: String(100) - Prezime korisnika
  - `email`: String(255) - Email adresa (unique)
  - `password_hash`: String(255) - Hashovan password
  - `tip`: Enum('administrator', 'serviser') - Tip korisnika
  - `aktivan`: Boolean - Status naloga
  - `created_at`: DateTime - Datum kreiranja
  - `updated_at`: DateTime - Datum poslednje izmene

### AC5: Login funkcionalnost
- **Given** da korisnik ima validan nalog
- **When** korisnik unese email i password na login formi
- **Then** sistem proverava kredencijale
- **And** ako su kredencijali validni, kreira se sesija
- **And** korisnik se preusmerava na dashboard
- **And** ako kredencijali nisu validni, prikazuje se greška sa porukom "Neispravni kredencijali."

### AC6: Session management
- **Given** da je korisnik ulogovan
- **When** korisnik navigira kroz aplikaciju
- **Then** sesija se održava tokom korišćenja
- **And** Flask-Login je konfigurisano za upravljanje sesijama
- **And** postoji `@login_required` dekorator za zaštićene rute

### AC7: Role-based pristup
- **Given** da postoje dva tipa korisnika (administrator, serviser)
- **When** korisnik pokušava da pristupi određenoj funkcionalnosti
- **Then** sistem proverava tip korisnika
- **And** administrator ima pristup svim funkcionalnostima
- **And** serviser ima ograničen pristup prema svojoj ulozi
- **And** postoji `@role_required` dekorator za kontrolu pristupa

### AC8: Logout funkcionalnost
- **Given** da je korisnik ulogovan
- **When** korisnik klikne na logout dugme
- **Then** sesija se završava
- **And** korisnik se preusmerava na login stranicu
- **And** prikazuje se poruka "Uspešno ste se odjavili."

### AC9: Password hashing
- **Given** da se kreira ili menja password
- **When** se password čuva u bazu
- **Then** password je hashovan koristeći Werkzeug security
- **And** plain text password se nikad ne čuva u bazi

### AC10: Osnovni routing
- **Given** da aplikacija ima osnovnu strukturu
- **When** se pristupa različitim rutama
- **Then** sledeće rute su dostupne:
  - `/` - Preusmerava na dashboard ili login
  - `/auth/login` - Login forma
  - `/auth/logout` - Logout funkcionalnost
  - `/dashboard` - Glavni dashboard (zaštićeno)

## Technical Implementation Details

### Database Schema
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

### Required Dependencies
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Flask-WTF==1.1.1
WTForms==3.0.1
PyMySQL==1.1.0
Werkzeug==2.3.7
python-dotenv==1.0.0
```

### Environment Variables
```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://username:password@localhost/kds_db
```

### Key Files to Create

#### 1. `app/__init__.py` - Flask App Factory
- Kreirati Flask aplikaciju sa factory pattern
- Konfigurisati SQLAlchemy
- Registrovati blueprints
- Konfigurisati Flask-Login

#### 2. `app/models/user.py` - User Model
- SQLAlchemy model za korisnika
- Metode za password hashing i verifikaciju
- Flask-Login integration

#### 3. `app/views/auth.py` - Authentication Blueprint
- Login/logout rute
- Form handling
- Session management

#### 4. `app/services/auth_service.py` - Authentication Service
- Business logika za autentifikaciju
- User validation
- Password operations

#### 5. `app/utils/decorators.py` - Custom Decorators
- `@role_required` dekorator
- Dodatni security decoratori

#### 6. Templates
- `templates/base.html` - Osnovni template sa Bootstrap
- `templates/auth/login.html` - Login forma
- `templates/dashboard/index.html` - Dashboard stranica

## Definition of Done
- [ ] Svi acceptance criteria su ispunjeni
- [ ] Kod je testiran lokalno
- [ ] Flask aplikacija se pokreće bez grešaka
- [ ] MySQL konekcija radi
- [ ] Login/logout funkcionalnost radi
- [ ] Role-based pristup je implementiran
- [ ] Responsive design sa Bootstrap-om
- [ ] Kod prati coding standards iz arhitekture
- [ ] Dokumentacija je ažurirana

## Dependencies
- MySQL server mora biti instaliran i pokrenut
- Python 3.8+ okruženje
- Potrebne Python biblioteke iz requirements.txt

## Risks and Mitigation
- **Risk**: MySQL konekcija problemi
  - **Mitigation**: Testirati konekciju tokom development-a, dodati error handling
- **Risk**: Security vulnerabilities u autentifikaciji
  - **Mitigation**: Koristiti Flask-Login i Werkzeug security, testirati različite scenarije

## Notes
- Ova priča postavlja temelje za ceo sistem
- Sledeća priča će dodati upravljanje korisnicima od strane administratora
- Fokus je na sigurnosti i pravilnoj arhitekturi
- Koristiti srpski jezik za sve user-facing poruke
- Implementirati flash messages umesto JS alert-a
- Koristiti url_for za sve linkove

## QA Results

### QA Review Status: ✅ APPROVED WITH RECOMMENDATIONS
**Reviewed by**: Quinn (Senior Developer & QA Architect)  
**Review Date**: 2025-01-19  
**Overall Assessment**: Story je dobro strukturisana i pokriva osnovne zahteve za Flask aplikaciju sa autentifikacijom.

### ✅ Strengths (Što je dobro)

1. **Jasna struktura foldera** - Odlična organizacija sa separation of concerns (models, views, services, utils)
2. **Kompletni Acceptance Criteria** - Svi AC su jasno definisani i merljivi
3. **Sigurnosni aspekti** - Password hashing, session management, role-based pristup
4. **Database schema** - Dobro dizajniran User model sa potrebnim indeksima
5. **Responsive design** - Bootstrap 5 integracija za mobilne uređaje
6. **Srpski jezik** - Pravilno korišćenje ć, č, ž, š, đ u user-facing porukama
7. **Flask best practices** - Factory pattern, blueprints, decoratori

### ⚠️ Recommendations (Preporuke za poboljšanje)

1. **Testing Strategy Missing**
   - **Issue**: Nema definisane test strategije
   - **Recommendation**: Dodati unit testove za auth_service, integration testove za login flow
   - **Priority**: High

2. **Error Handling**
   - **Issue**: Nedostaju detalji o error handling-u
   - **Recommendation**: Definisati kako se rukuje sa MySQL konekcijskim greškama, validation errors
   - **Priority**: Medium

3. **Security Enhancements**
   - **Issue**: Nema spominjanja CSRF zaštite
   - **Recommendation**: Eksplicitno spomenuti Flask-WTF CSRF tokens u formama
   - **Priority**: High

4. **Logging Strategy**
   - **Issue**: Nema logging strategije
   - **Recommendation**: Dodati logging za security events (failed logins, role violations)
   - **Priority**: Medium

5. **Password Policy**
   - **Issue**: Nema definisane password policy
   - **Recommendation**: Definisati minimum requirements za password (dužina, složenost)
   - **Priority**: Medium

6. **Session Security**
   - **Issue**: Nema detalja o session timeout-u
   - **Recommendation**: Definisati session timeout i secure cookie settings
   - **Priority**: Medium

### 🔧 Technical Implementation Notes

1. **Database Migrations**: Koristiti Flask-Migrate za schema versioning
2. **Environment Config**: Dodati validation za required environment variables
3. **Flash Messages**: Koristiti kategorije (success, error, warning, info) za bolje UX
4. **URL Generation**: Svi linkovi kroz url_for() - ✅ već spomenuto
5. **Decimal Handling**: Za buduće novčane vrednosti koristiti 2 decimalna mesta

### 📋 Acceptance Criteria Validation

- **AC1-AC10**: ✅ Svi AC su jasno definisani i testabilni
- **Database Schema**: ✅ Kompletna i optimizovana sa indeksima
- **Dependencies**: ✅ Sve potrebne biblioteke su navedene
- **Environment Setup**: ✅ Jasno definisane environment varijable

### 🎯 Definition of Done Assessment

**Current DoD Coverage**: 85%
- ✅ Funkcionalnost definisana
- ✅ Arhitektura definisana  
- ⚠️ Testing strategy nedostaje
- ⚠️ Error handling details nedostaju
- ✅ Security considerations pokrivene
- ✅ Documentation requirements jasni

### 🚀 Implementation Priority Recommendations

1. **Phase 1 (Critical)**: Implementirati osnovnu strukturu, auth, database
2. **Phase 2 (Important)**: Dodati comprehensive error handling i logging
3. **Phase 3 (Enhancement)**: Implementirati advanced security features

### 📝 Final Notes

Story je solidna osnova za Flask aplikaciju. Glavne preporuke su dodavanje test strategije i detaljnijeg error handling-a. Implementacija može početi sa trenutnim zahtevima, ali preporučujem dodavanje spomenutih poboljšanja u sledeće iteracije.

**QA Approval**: ✅ **APPROVED** - Story može ići u implementaciju sa napomenama da se preporuke uzmu u obzir tokom development-a.
