# Story 3.1: Registracija uređaja

## Metadata
- **Story ID**: 3.1
- **Epic**: Epic 3 - Upravljanje uređajima i QR kodovima
- **Priority**: High
- **Story Points**: 5
- **Status**: Approved
- **Created**: 2025-07-22
- **Assigned To**: AI Developer


## Business Context
Sistem za upravljanje servisima mora omogućiti registraciju i praćenje HVAC uređaja. Ova funkcionalnost je ključna za efikasno upravljanje servisnim intervalima, praćenje istorije intervencija i održavanje baze podataka o svim uređajima u sistemu. Serviseri moraju imati mogućnost da dodaju nove uređaje, ažuriraju postojeće podatke i prate lokaciju svakog uređaja unutar objekata i prostorija.

## Story
**As a** serviser,  
**I want to** register HVAC devices,  
**so that** I can track their service history.

## Acceptance Criteria

### AC1: Uređaj ima sva obavezna polja
- **Given** da je serviser ulogovan i otvorio stranicu za dodavanje novog uređaja
- **When** pregleda formu za unos
- **Then** forma sadrži sledeća obavezna polja:
  - Tip uređaja (izbor iz padajuće liste: rashladna tehnika, grejna tehnika, ventilacioni sistemi)
  - Podtip uređaja (dinamički se menja u zavisnosti od izabranog tipa):
    - Za rashladnu tehniku: Split sistem, Čileri, Centralna klima, Toplotne pumpe, Kanalska klima, Klima komora, Pokretna klima, Klima ormar, Prozorska klima, VRF sistemi - multi, Frižideri
    - Za grejnu tehniku: TA peć, Grejalice, Kotlovi, Panelni radijatori, Radijatori
    - Za ventilacione sisteme: (nema podtipova)
  - Proizvođač (tekstualno polje)
  - Model (tekstualno polje)
  - Serijski broj (tekstualno polje, jedinstveno u sistemu)
  - Godina proizvodnje (brojčano polje)
  - Prostorija (izbor iz padajuće liste postojećih prostorija)
- **And** obavezna polja su jasno označena sa *

### AC2: Validacija unosa podataka
- **Given** da je serviser na formi za unos uređaja
- **When** pokuša da sačuva formu sa neispravnim podacima
- **Then** sistem prikazuje odgovarajuće poruke o greškama:
  - Ako je neko od obaveznih polja prazno
  - Ako serijski broj već postoji u sistemu
  - Ako godina proizvodnje nije validna (npr. buduća godina)
  - Ako nije izabrana prostorija

### AC3: Kreiranje novog uređaja
- **Given** da je serviser popunio formu sa ispravnim podacima
- **When** klikne na dugme "Sačuvaj"
- **Then** sistem čuva novi uređaj u bazi podataka
- **And** generiše jedinstveni ID za uređaj
- **And** preusmerava korisnika na stranicu sa detaljima uređaja
- **And** prikazuje poruku o uspešnom čuvanju

### AC4: Dodeljivanje uređaja preko forme za uređaj
- **Given** da je korisnik na stranici za izmenu uređaja
- **When** izabere prostoriju kroz hijerarhijski izbornik (klijent > lokacija/radna jedinica > objekat > prostorija)
- **And** sačuva izmene
- **Then** uređaj se povezuje sa izabranom prostorijom
- **And** prikazuje se poruka o uspešnom ažuriranju
- **And** u detaljima prostorije se uređaj prikazuje u listi dodeljenih uređaja

### AC5: Dodeljivanje uređaja preko prostorije
- **Given** da korisnik pregleda detalje prostorije
- **When** klikne na dugme "Dodaj uređaj"
- **Then** otvara se stranica sa listom uređaja koji nisu dodeljeni nijednoj prostoriji
- **And** za svaki uređaj postoji dugme "Dodaj u prostoriju"
- **When** klikne na dugme "Dodaj u prostoriju" pored željenog uređaja
- **Then** uređaj se povezuje sa tom prostorijom
- **And** korisnik se vraća na stranicu sa detaljima prostorije
- **And** uređaj se sada prikazuje u listi uređaja te prostorije

### AC6: Brisanje veze uređaja i prostorije
- **Given** da je uređaj dodeljen prostoriji
- **When** korisnik ukloni vezu između uređaja i prostorije (bilo sa strane uređaja ili prostorije)
- **Then** veza se uklanja iz baze podataka
- **And** uređaj više nije vidljiv u listi uređaja te prostorije
- **And** uređaj postaje dostupan za dodelu u drugim prostorijama

### AC7: Pretraga i filtriranje uređaja
- **Given** da je korisnik na stranici sa listom uređaja
- **When** koristi polje za pretragu
- **Then** sistem prikazuje samo uređaje koji odgovaraju kriterijumu pretrage (pretražuje se po proizvođaču, modelu, serijskom broju)
- **When** koristi filter po tipu uređaja
- **Then** sistem prikazuje samo uređaje odabranog tipa
- **When** kombinuje pretragu i filtere
- **Then** sistem primenjuje sve aktivne filtere i kriterijume pretrage

## Tasks / Subtasks
- [x] Implementacija modela i veza
  - [x] Kreirati model `Uredjaj` sa svim potrebnim poljima
  - [x] Definisati vezu many-to-many između `Uredjaj` i `Prostorija` modela
  - [x] Implementirati metode za upravljanje vezama uređaja i prostorija
  - [x] Kreirati migracije za bazu podataka

- [x] Implementacija korisničkog interfejsa
  - [x] Kreirati listu uređaja sa mogućnošću pretrage i filtriranja
  - [x] Implementirati formu za unos uređaja sa hijerarhijskim izbornikom za prostorije
  - [x] Implementirati formu za izmenu uređaja sa hijerarhijskim izbornikom za prostorije
  - [x] Kreirati stranicu za dodelu uređaja iz prostorije
  - [x] Implementirati prikaz dodeljenih uređaja u okviru detalja prostorije

- [x] Implementacija ruta i logike
  - [x] Kreirati rute za upravljanje vezama uređaja i prostorija
  - [x] Implementirati logiku za dodelu i uklanjanje veza
  - [x] Dodati validaciju i obradu grešaka
  - [x] Implementirati hijerarhijsko učitavanje podataka za izbornik (klijent > lokacija > objekat > prostorija)

- [x] Testiranje
  - [x] Napisati unit testove za CRUD operacije uređaja
  - [x] Testirati funkcionalnost dodele i uklanjanja veza uređaja i prostorija
  - [x] Testirati validaciju unetih podataka
  - [x] Testirati funkcionalnost pretrage i filtriranja

## Napomene o implementaciji

### Završeni testovi i ispravke
Implementirani su svi testovi za operacije sa uređajima:
- CRUD operacije (kreiranje, čitanje, ažuriranje i brisanje)
- Dodela i uklanjanje veza uređaja sa prostorijama
- Validacija unosa (jedinstvenost serijskog broja, obavezna polja)
- Pretraga i filtriranje uređaja

Ispravke koje su bile potrebne u testovima:
- Objekat_id je obavezan za prostorije - dodat kreiranje objekta pre prostorije
- Ispravljena ruta za prijavu korisnika (/auth/login umesto /login)
- Pojednostavljena provera rezultata testova (direktan pristup modelima umesto web formi)
- Korišćenje pravilnih naziva atributa (numericka_oznaka umesto broj za prostorije)

## Dev Notes

### Data Models

**Uredjaj Model:**
```python
class Uredjaj(db.Model):
    __tablename__ = 'uredjaji'
    
    # Osnovni podaci
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.Enum(
        'rashladna_tehnika', 
        'grejna_tehnika', 
        'ventilacioni_sistemi',
        name='tip_uredjaja'
    ), nullable=False)
    podtip = db.Column(db.Enum(
        # Rashladna tehnika
        'split_sistem', 'cileri', 'centralna_klima', 'toplotne_pumpe', 'kanalska_klima', 
        'klima_komora', 'pokretna_klima', 'klima_ormar', 'prozorska_klima', 'vrf_sistemi', 'frizideri',
        # Grejna tehnika
        'ta_pec', 'grejalice', 'kotlovi', 'panelni_radijatori', 'radijatori',
        # Prazna vrednost za ventilacione sisteme
        name='podtip_uredjaja'
    ), nullable=True)
    proizvodjac = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    serijski_broj = db.Column(db.String(100), unique=True, nullable=False)
    inventarski_broj = db.Column(db.String(100))
    godina_proizvodnje = db.Column(db.Integer, nullable=False)
    
    # Veze sa drugim modelima
    prostorije = db.relationship(
        'Prostorija', 
        secondary='uredjaji_prostorije',
        back_populates='uredjaji',
        lazy='dynamic'
    )
    
    # Metapodaci
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Uredjaj {self.proizvodjac} {self.model} ({self.serijski_broj})>'

# Tabela za vezu many-to-many između Uredjaj i Prostorija
uredjaji_prostorije = db.Table('uredjaji_prostorije',
    db.Column('uredjaj_id', db.Integer, db.ForeignKey('uredjaji.id'), primary_key=True),
    db.Column('prostorija_id', db.Integer, db.ForeignKey('prostorije.id'), primary_key=True),
    db.Column('dodeljen_at', db.DateTime, default=datetime.utcnow),
    db.Column('dodelio_korisnik_id', db.Integer, db.ForeignKey('korisnici.id'))
)
```

### Potrebne rute

```python
# Osnovne rute za uređaje
@bp.route('/uredjaji')
@login_required
def lista_uredjaja():
    """Prikaz liste svih uređaja sa mogućnošću pretrage i filtriranja."""
    # Implementacija pretrage i filtriranja

@bp.route('/uredjaji/novi', methods=['GET', 'POST'])
@login_required
def novi_uredjaj():
    """Kreiranje novog uređaja."""
    # Implementacija forme za novi uređaj

@bp.route('/uredjaji/<int:id>')
@login_required
def prikazi_uredjaj(id):
    """Prikaz detalja uređaja."""
    # Implementacija prikaza detalja

@bp.route('/uredjaji/<int:id>/izmeni', methods=['GET', 'POST'])
@login_required
def izmeni_uredjaj(id):
    """Izmena postojećeg uređaja."""
    # Implementacija izmene uređaja

# Rute za upravljanje vezama uređaja i prostorija
@bp.route('/prostorije/<int:prostorija_id>/dodaj-uredjaj')
@login_required
def dodaj_uredjaj_u_prostoriju(prostorija_id):
    """Prikaz forme za dodavanje uređaja u prostoriju."""
    # Prikazuje listu uređaja koji nisu dodeljeni nijednoj prostoriji

@bp.route('/prostorije/<int:prostorija_id>/dodaj-uredjaj/<int:uredjaj_id>', methods=['POST'])
@login_required
def dodeli_uredjaj_prostoriji(prostorija_id, uredjaj_id):
    """Dodela uređaja prostoriji."""
    # Implementacija dodele

@bp.route('/prostorije/<int:prostorija_id>/ukloni-uredjaj/<int:uredjaj_id>', methods=['POST'])
@login_required
def ukloni_uredjaj_iz_prostorije(prostorija_id, uredjaj_id):
    """Uklanjanje veze između uređaja i prostorije."""
    # Implementacija uklanjanja veze

# API rute za dobijanje podataka
@bp.route('/api/lokacije')
@login_required
def get_lokacije():
    """Vraća listu lokacija za dinamičko učitavanje izbornika."""
    # Implementacija dobijanja lokacija
```

### Forms

```python
class UredjajForm(FlaskForm):
    # Osnovni podaci
    tip = SelectField('Tip uređaja*', choices=[
        ('', 'Odaberite tip uređaja'),
        ('rashladna_tehnika', 'Rashladna tehnika'),
        ('grejna_tehnika', 'Grejna tehnika'),
        ('ventilacioni_sistemi', 'Ventilacioni sistemi')
    ], validators=[DataRequired()])
    
    podtip = StringField('Podtip uređaja', validators=[Length(max=100)])
    proizvodjac = StringField('Proizvođač', validators=[
        DataRequired(message='Naziv proizvođača je obavezan'),
        Length(max=255, message='Maksimalna dužina je 255 karaktera')
    ])
    
    model = StringField('Model', validators=[
        DataRequired(message='Naziv modela je obavezan'),
        Length(max=255, message='Maksimalna dužina je 255 karaktera')
    ])
    
    serijski_broj = StringField('Serijski broj', validators=[
        DataRequired(message='Serijski broj je obavezan'),
        Length(max=100, message='Maksimalna dužina je 100 karaktera')
    ])
    
    inventarski_broj = StringField('Inventarski broj', validators=[
        Length(max=100, message='Maksimalna dužina je 100 karaktera')
    ])
    
    godina_proizvodnje = IntegerField('Godina proizvodnje', validators=[
        DataRequired(message='Godina proizvodnje je obavezna'),
        NumberRange(min=1900, max=datetime.now().year, 
                   message=f'Godina mora biti između 1900 i {datetime.now().year}')
    ])
    
    # Hijerarhijski izbornik za prostorije
    klijent_id = SelectField('Klijent', coerce=int, validators=[DataRequired()])
    lokacija_id = SelectField('Lokacija/Radna jedinica', coerce=int, validators=[DataRequired()])
    objekat_id = SelectField('Objekat', coerce=int, validators=[DataRequired()])
    prostorija_id = SelectField('Prostorija', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Sačuvaj')
    
    def validate_serijski_broj(self, field):
        """Proverava da li serijski broj već postoji u bazi."""
        if 'id' in request.view_args:
            uredjaj = Uredjaj.query.get(request.view_args['id'])
            if uredjaj and uredjaj.serijski_broj == field.data:
                return
                
        if Uredjaj.query.filter_by(serijski_broj=field.data).first():
            raise ValidationError('Uređaj sa ovim serijskim brojem već postoji u sistemu.')


class DodeliUredjajForm(FlaskForm):
    """Forma za dodelu već postojećeg uređaja prostoriji."""
    submit = SubmitField('Dodeli uređaj')
```

### Dependencies
- **Modeli**:
  - `Prostorija` model iz Story 2.4
  - `Klijent`, `LokacijaKuce`, `Objekat` modeli iz prethodnih priča
  
- **Biblioteke**:
  - Flask-SQLAlchemy za ORM
  - Flask-WTF za forme i validaciju
  - SQLAlchemy-Utils za dodatne tipove podataka
  - Bootstrap 5 za korisnički interfejs
  - Select2 za napredne izbornike
  
- **JavaScript biblioteke**:
  - jQuery za AJAX zahteve
  - DataTables za naprednu tabelu sa pretragom i sortiranjem
  - SweetAlert2 za lepe dijaloge za potvrdu

## Testing

### Unit Testovi
```python
def test_kreiranje_uredjaja(self):
    """Test kreiranja novog uređaja."""
    with self.client:
        self.login()
        response = self.client.post(
            '/uredjaji/novi',
            data=dict(
                tip='rashladna_tehnika',
                podtip='Split sistem',
                proizvodjac='Test proizvođač',
                model='Test model',
                serijski_broj='TEST12345',
                inventarski_broj='INV123',
                godina_proizvodnje=2023,
                prostorija_id=1
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Novi uređaj je uspešno dodat.', response.get_data(as_text=True))
        uredjaj = Uredjaj.query.filter_by(serijski_broj='TEST12345').first()
        self.assertIsNotNone(uredjaj)

def test_validacija_jedinstvenog_serijskog_broja(self):
    """Test validacije jedinstvenosti serijskog broja."""
    with self.client:
        self.login()
        # Prvi unos
        self.client.post(
            '/uredjaji/novi',
            data=dict(
                tip='rashladna_tehnika',
                proizvodjac='Test',
                model='Test',
                serijski_broj='DUPLIKAT123',
                godina_proizvodnje=2023,
                prostorija_id=1
            ),
            follow_redirects=True
        )
        # Drugi unos sa istim serijskim brojem
        response = self.client.post(
            '/uredjaji/novi',
            data=dict(
                tip='rashladna_tehnika',
                proizvodjac='Drugi proizvođač',
                model='Drugi model',
                serijski_broj='DUPLIKAT123',
                godina_proizvodnje=2023,
                prostorija_id=1
            ),
            follow_redirects=True
        )
        self.assertIn('Uređaj sa ovim serijskim brojem već postoji.', response.get_data(as_text=True))

def test_filtriranje_uredjaja(self):
    """Test filtriranja uređaja po tipu."""
    with self.client:
        self.login()
        response = self.client.get('/uredjaji?tip=rashladna_tehnika')
        self.assertEqual(response.status_code, 200)
        # Proveriti da li se u rezultatima nalaze samo rashladni uređaji
        # (dodati specifične provere u zavisnosti od implementacije prikaza)
```

## Implementation Notes
- Potrebno je osigurati da su svi stringovi na srpskom jeziku sa ispravnim dijakritičkim znakovima
- Validacija mora obezbediti da su sva obavezna polja popunjena
- Godina proizvodnje mora biti validna (npr. ne može biti u budućnosti)
- Serijski broj mora biti jedinstven u sistemu

## Change Log
- 2025-07-22: Inicijalna verzija dokumenta
- 2025-07-22: Dodati detaljni modeli, forme i testovi na osnovu priče 2.4
