# Story 2.4: Upravljanje objektima i prostorijama

## Metadata
- **Story ID**: 2.4
- **Epic**: Epic 2 - Upravljanje klijentima i strukturom
- **Priority**: High
- **Story Points**: 5
- **Status**: Done
- **Created**: 2025-07-20
- **Assigned To**: AI Developer

## User Story
**As a** serviser  
**I want to** create objects and rooms within client locations  
**So that** I can precisely locate devices

## Business Context
Sistem za upravljanje servisima mora podržavati rad sa objektima i prostorijama koji mogu imati više različitih lokacija. Ova struktura je važna jer omogućava pravilno raspoređivanje i praćenje servisnih aktivnosti za rezidencijalne klijente. Serviseri moraju imati mogućnost da kreiraju objekte i prostorije sa njihovim detaljnim informacijama, kao i da upravljaju lokacijama kuća i dodatnim strukturama, poput objekata i prostorija, što će kasnije omogućiti preciznije kreiranje i praćenje servisnih naloga za kućne korisnike.

## Acceptance Criteria

### AC1: Objekat ima polje: naziv objekta
- **Given** da je serviser ulogovan i otvorio stranicu za dodavanje/izmenu objekta
- **When** unosi podatke za objekat
- **Then** forma sadrži polje za naziv objekta (obavezno)

### AC2: Prostorija ima polja: naziv prostorije (opciono), numerička oznaka (opciono)
- **Given** da je serviser ulogovan i otvorio stranicu za dodavanje/izmenu prostorije
- **When** unosi podatke za prostoriju
- **Then** forma sadrži polja za naziv prostorije (opciono) i numeričku oznaku prostorije (opciono)
- **And** bar jedno od ovih polja mora biti popunjeno

### AC3: Objekti se mogu dodati u bilo koju lokaciju
- **Given** da je serviser ulogovan i otvorio detalje lokacije
- **When** klikne na dugme "Dodaj objekat"
- **Then** prikazuje se forma za unos podataka novog objekta
- **And** nakon uspešnog kreiranja, novi objekat se prikazuje u listi objekata lokacije
- **And** prikazuje se flash poruka "Novi objekat je uspešno dodat."

### AC4: Prostorije se mogu dodati u bilo koji objekat
- **Given** da je serviser ulogovan i otvorio detalje objekta
- **When** klikne na dugme "Dodaj prostoriju"
- **Then** prikazuje se forma za unos podataka nove prostorije
- **And** nakon uspešnog kreiranja, nova prostorija se prikazuje u listi prostorija objekta
- **And** prikazuje se flash poruka "Nova prostorija je uspešno dodata."

### AC5: Navigacija kroz hijerarhiju je intuitivna
- **Given** da je serviser ulogovan
- **When** pristupa detaljima klijenta, lokacije, objekta ili prostorije
- **Then** prikazuje se breadcrumb navigacija sa linkovima do svih nadređenih elemenata
- **And** na svakom nivou hijerarhije postoji pregled podređenih elemenata (lokacije, objekti, prostorije)

## Tasks / Subtasks

- [x] Implementacija CRUD operacija za objekte (AC: 1, 3)
  - [x] Kreirati/ažurirati model `Objekat` sa odgovarajućim poljima
  - [x] Implementirati formu za kreiranje/izmenu objekta
  - [x] Implementirati rutu za prikaz detalja objekta
  - [x] Implementirati rutu za kreiranje novog objekta
  - [x] Implementirati rutu za izmenu objekta
  - [x] Implementirati rutu za brisanje objekta
  - [x] Dodati prikaz liste objekata na stranici detalja lokacije

- [x] Implementacija CRUD operacija za prostorije (AC: 2, 4)
  - [x] Kreirati/ažurirati model `Prostorija` sa odgovarajućim poljima
  - [x] Implementirati formu za kreiranje/izmenu prostorije
  - [x] Implementirati rutu za prikaz detalja prostorije
  - [x] Implementirati rutu za kreiranje nove prostorije
  - [x] Implementirati rutu za izmenu prostorije
  - [x] Implementirati rutu za brisanje prostorije
  - [x] Dodati prikaz liste prostorija na stranici detalja objekta

- [x] Implementacija intuitivne hijerarhijske navigacije (AC: 5)
  - [x] Proširiti breadcrumb navigaciju za objekte i prostorije

- [x] Testiranje
  - [x] Napisati unit testove za CRUD operacije objekta
  - [x] Napisati unit testove za CRUD operacije prostorije

## Dev Notes

### Prethodni story
Na osnovu story-ja 2.3, već su postavljeni temelji za hijerarhiju Fizičko lice > Lokacija kuće > Objekat > Prostorija. Modeli Objekat i Prostorija su već pripremljeni u prethodnoj priči, ali sada ih je potrebno implementirati u potpunosti.

### Data Models
Iz arhitekturne dokumentacije (data-models.md), ključni atributi za objekte i prostorije su:

**Object Model:**
- id: Integer (Primary Key)
- location_id: Integer (Foreign Key)
- naziv: String(255)

**Room Model:**
- id: Integer (Primary Key)
- object_id: Integer (Foreign Key)
- naziv: String(255) (opciono)
- numerica_oznaka: String(50) (opciono)

### Potrebne rute
```python
# Object Routes
/klijenti/lokacija/<int:id>/objekti/novi (GET, POST) - Kreiranje novog objekta
/klijenti/objekat/<int:id> (GET) - Prikaz detalja objekta
/klijenti/objekat/<int:id>/izmeni (GET, POST) - Izmena objekta
/klijenti/objekat/<int:id>/obrisi (POST) - Brisanje objekta

# Room Routes
/klijenti/objekat/<int:id>/prostorije/novi (GET, POST) - Kreiranje nove prostorije
/klijenti/prostorija/<int:id> (GET) - Prikaz detalja prostorije
/klijenti/prostorija/<int:id>/izmeni (GET, POST) - Izmena prostorije
/klijenti/prostorija/<int:id>/obrisi (POST) - Brisanje prostorije
```

### Database Models
```python
# Object Model - već definisan u Story 2.3, ali treba proširiti funkcionalnost
class Objekat(db.Model):
    __tablename__ = 'objekti'
    
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(255), nullable=False)
    
    lokacija_id = db.Column(db.Integer, db.ForeignKey('lokacije_kuce.id'), nullable=False)
    lokacija = db.relationship('LokacijaKuce', backref=db.backref('objekti', lazy=True, cascade='all, delete-orphan'))
    
    prostorije = db.relationship('Prostorija', backref='objekat', lazy=True, cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Objekat {self.naziv}>'

# Room Model - već definisan u Story 2.3, ali treba proširiti funkcionalnost
class Prostorija(db.Model):
    __tablename__ = 'prostorije'
    
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(255), nullable=True)
    numericka_oznaka = db.Column(db.String(50), nullable=True)
    
    objekat_id = db.Column(db.Integer, db.ForeignKey('objekti.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Prostorija {self.naziv if self.naziv else self.numericka_oznaka}>'
```

### Forms
```python
# Object Form - ažurirati/proširiti postojeću formu
class ObjekatForm(FlaskForm):
    naziv = StringField('Naziv', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Sačuvaj')

# Room Form - ažurirati/proširiti postojeću formu
class ProstorijaForm(FlaskForm):
    naziv = StringField('Naziv prostorije', validators=[Length(max=255)])
    numericka_oznaka = StringField('Numerička oznaka', validators=[Length(max=50)])
    submit = SubmitField('Sačuvaj')
    
    def validate(self):
        if not super(ProstorijaForm, self).validate():
            return False
        if not self.naziv.data and not self.numericka_oznaka.data:
            self.naziv.errors.append('Bar jedno od polja Naziv prostorije ili Numerička oznaka mora biti popunjeno.')
            return False
        return True
```

### Testing
```python
# Test Object CRUD
def test_kreiranje_objekta(self):
    """Test kreiranja novog objekta u lokaciji."""
    with self.client:
        self.login()
        response = self.client.post(
            f'/klijenti/lokacija/{self.test_lokacija.id}/objekti/novi',
            data=dict(naziv='Test objekat'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Novi objekat je uspešno dodat.', response.get_data(as_text=True))
        objekat = Objekat.query.filter_by(naziv='Test objekat').first()
        self.assertIsNotNone(objekat)

# Test Room CRUD
def test_kreiranje_prostorije(self):
    """Test kreiranja nove prostorije u objektu."""
    with self.client:
        self.login()
        response = self.client.post(
            f'/klijenti/objekat/{self.test_objekat.id}/prostorije/novi',
            data=dict(naziv='Test prostorija'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nova prostorija je uspešno dodata.', response.get_data(as_text=True))
        prostorija = Prostorija.query.filter_by(naziv='Test prostorija').first()
        self.assertIsNotNone(prostorija)
```

## Testing

### Unit testovi
- Testovi za model Objekat
- Testovi za model Prostorija
- Testovi za forme ObjekatForm i ProstorijaForm
- Testovi za rute objekta i prostorije

### Integracioni testovi
- Testovi za navigaciju kroz hijerarhiju
- Testovi za prikaz podređenih elemenata
- Testovi za breadcrumb navigaciju

## Change Log

| Datum | Verzija | Opis | Autor |
|-------|---------|------|-------|
| 2025-07-21 | 1.0 | Kreiran inicijalni draft | Bob (SM) |

## QA Results

### Review Date: 2025-07-21
### Reviewed By: Quinn (Senior Developer QA)

### Code Quality Assessment
Implementacija je kompletirana prema zahtevima i prihvaćenim kriterijumima. Kod je dobro organizovan i prati strukture već uspostavljene u prethodnim story-jima. UI komponente su standardizovane i koriste Bootstrap 5, a svi tekstovi su na srpskom jeziku sa pravilnim dijakritičkim znakovima.

### Refactoring Performed
Nisu bile potrebne značajne refaktoring izmene jer implementacija prati dobre prakse.

### Compliance Check
- Coding Standards: ✓ Kod je usklađen sa standardima projekta, koristi se pravilna srpska latinica
- Project Structure: ✓ Fajlovi su organizovani prema strukturi projekta
- Testing Strategy: ✓ Postoje unit testovi za modele i CRUD operacije
- All ACs Met: ✓ Svi prihvatni kriterijumi su ispunjeni

### Posebne napomene
1. Implementirana je validacija prostorija koja zahteva da bar jedan od atributa (naziv ili numerička oznaka) bude popunjen, što je u skladu sa AC2
2. Breadcrumbs i hijerarhijska navigacija funkcionišu kako je traženo u AC5
3. Flash poruke za uspešno dodavanje objekata i prostorija su implementirane prema zahtevima
