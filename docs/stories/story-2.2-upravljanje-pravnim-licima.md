# Story 2.2: Upravljanje pravnim licima

## Metadata
- **Story ID**: 2.2
- **Epic**: Epic 2 - Upravljanje klijentima i strukturom
- **Priority**: High
- **Story Points**: 6
- **Status**: Done
- **Created**: 2025-07-20
- **Assigned To**: AI Developer

## User Story
**As a** serviser  
**I want to** create legal entities with their locations  
**So that** I can track services across multiple company locations

## Business Context
Sistem za upravljanje servisima mora podržavati rad sa pravnim licima (kompanijama) koje mogu imati više različitih radnih jedinica na različitim lokacijama. Ova hijerarhijska struktura je važna jer omogućava pravilno raspoređivanje i praćenje servisnih aktivnosti unutar organizacije klijenta. Serviseri moraju imati mogućnost da kreiraju pravna lica sa njihovim detaljnim informacijama, kao i da upravljaju radnim jedinicama i dodatnim strukturama, poput objekata i prostorija, što će kasnije omogućiti preciznije kreiranje i praćenje servisnih naloga.

## Acceptance Criteria

### AC1: Polja za pravno lice
- **Given** da je serviser ulogovan i izabrao tip klijenta "Pravno lice"
- **When** unosi podatke za pravno lice
- **Then** forma sadrži sledeća polja:
  - Naziv (obavezno)
  - Adresa (obavezno)
  - Mesto (obavezno)
  - Poštanski broj (obavezno)
  - Država (obavezno, default "Srbija")
  - Telefon (obavezno)
  - Email
  - PIB (obavezno, 9 cifara)
  - MB (obavezno, 8 cifara)

### AC2: Automatsko kreiranje radne jedinice
- **Given** da je serviser uneo sve obavezne podatke za pravno lice
- **When** klikne na dugme "Sačuvaj"
- **Then** sistem kreira pravno lice
- **And** automatski kreira prvu radnu jedinicu sa podacima:
  - Naziv: "Centrala" (default)
  - Adresa, mesto, poštanski broj, državu preuzeti od pravnog lica
  - Prazna polja za kontakt osobu, telefon i email

### AC3: Polja za radnu jedinicu
- **Given** da je serviser ulogovan i otvorio stranicu za dodavanje/izmenu radne jedinice
- **When** unosi podatke za radnu jedinicu
- **Then** forma sadrži sledeća polja:
  - Naziv (obavezno)
  - Adresa (obavezno)
  - Mesto (obavezno)
  - Poštanski broj (obavezno)
  - Država (obavezno, default "Srbija")
  - Kontakt osoba
  - Telefon (obavezno)
  - Email

### AC4: Dodavanje dodatnih radnih jedinica
- **Given** da je serviser ulogovan i otvorio detalje pravnog lica
- **When** klikne na dugme "Dodaj radnu jedinicu"
- **Then** prikazuje se forma za unos podataka nove radne jedinice
- **And** nakon uspešnog kreiranja, nova radna jedinica se prikazuje u listi radnih jedinica pravnog lica
- **And** prikazuje se flash poruka "Nova radna jedinica je uspešno dodata."

### AC5: Hijerarhijska struktura
- **Given** da je serviser ulogovan
- **When** pristupa detaljima pravnog lica
- **Then** prikazuje se hijerarhijska struktura:
  - Pravno lice na vrhu
  - Radne jedinice ispod pravnog lica
  - Opcije za dodavanje objekata ispod radnih jedinica
  - Opcije za dodavanje prostorija ispod objekata
- **And** hijerarhija se vizualno prikazuje u obliku tree view strukture
- **And** elementi hijerarhije su klikabilni i vode na detalje odgovarajućeg entiteta
- **And** breadcrumb navigacija odražava poziciju u hijerarhiji

## Technical Implementation Details

### Required Routes
```python
# Legal Entity and Unit Routes
/klijenti/pravno-lice/novi (GET, POST) - Kreiranje novog pravnog lica
/klijenti/pravno-lice/<int:id> (GET) - Prikaz detalja pravnog lica
/klijenti/pravno-lice/<int:id>/izmeni (GET, POST) - Izmena pravnog lica
/klijenti/pravno-lice/<int:id>/radne-jedinice/novi (GET, POST) - Dodavanje nove radne jedinice
/klijenti/radna-jedinica/<int:id> (GET) - Prikaz detalja radne jedinice
/klijenti/radna-jedinica/<int:id>/izmeni (GET, POST) - Izmena radne jedinice
```

### Database Models
```python
# Legal Entity Model
class PravnoLice(Client):
    __tablename__ = 'pravna_lica'
    
    id = db.Column(db.Integer, db.ForeignKey('clients.id'), primary_key=True)
    naziv = db.Column(db.String(255), nullable=False, index=True)
    pib = db.Column(db.String(9), nullable=False, unique=True)
    mb = db.Column(db.String(8), nullable=False, unique=True)
    
    radne_jedinice = db.relationship('RadnaJedinica', backref='pravno_lice', lazy=True, cascade='all, delete-orphan')
    
    __mapper_args__ = {
        'polymorphic_identity': 'pravno_lice',
    }
    
    def __repr__(self):
        return f'<PravnoLice {self.naziv}>'

# Work Unit Model
class RadnaJedinica(db.Model):
    __tablename__ = 'radne_jedinice'
    
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(255), nullable=False)
    adresa = db.Column(db.String(255), nullable=False)
    mesto = db.Column(db.String(100), nullable=False)
    postanski_broj = db.Column(db.String(20), nullable=False)
    drzava = db.Column(db.String(100), nullable=False, default="Srbija")
    kontakt_osoba = db.Column(db.String(255))
    telefon = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255))
    
    pravno_lice_id = db.Column(db.Integer, db.ForeignKey('pravna_lica.id'), nullable=False)
    objekti = db.relationship('Objekat', backref='radna_jedinica', lazy=True, cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<RadnaJedinica {self.naziv} - {self.pravno_lice.naziv}>'

# Building Model
class Objekat(db.Model):
    __tablename__ = 'objekti'
    
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(255), nullable=False)
    opis = db.Column(db.Text)
    
    radna_jedinica_id = db.Column(db.Integer, db.ForeignKey('radne_jedinice.id'), nullable=False)
    prostorije = db.relationship('Prostorija', backref='objekat', lazy=True, cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Objekat {self.naziv}>'

# Room Model
class Prostorija(db.Model):
    __tablename__ = 'prostorije'
    
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(255), nullable=False)
    sprat = db.Column(db.String(50))
    broj = db.Column(db.String(50))
    namena = db.Column(db.String(100))
    
    objekat_id = db.Column(db.Integer, db.ForeignKey('objekti.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Prostorija {self.naziv} - {self.objekat.naziv}>'
```

### Forms
```python
class PravnoLiceForm(ClientBaseForm):
    naziv = StringField('Naziv', validators=[DataRequired(), Length(max=255)])
    pib = StringField('PIB', validators=[
        DataRequired(), 
        Length(min=9, max=9, message="PIB mora sadržati tačno 9 cifara"), 
        Regexp('^\d{9}$', message="PIB mora sadržati samo cifre")
    ])
    mb = StringField('Matični broj', validators=[
        DataRequired(), 
        Length(min=8, max=8, message="Matični broj mora sadržati tačno 8 cifara"), 
        Regexp('^\d{8}$', message="Matični broj mora sadržati samo cifre")
    ])
    submit = SubmitField('Sačuvaj')

class RadnaJedinicaForm(FlaskForm):
    naziv = StringField('Naziv', validators=[DataRequired(), Length(max=255)])
    adresa = StringField('Adresa', validators=[DataRequired(), Length(max=255)])
    mesto = StringField('Mesto', validators=[DataRequired(), Length(max=100)])
    postanski_broj = StringField('Poštanski broj', validators=[DataRequired(), Length(max=20)])
    drzava = StringField('Država', validators=[DataRequired(), Length(max=100)], default="Srbija")
    kontakt_osoba = StringField('Kontakt osoba', validators=[Optional(), Length(max=255)])
    telefon = StringField('Telefon', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=255)])
    submit = SubmitField('Sačuvaj')

class ObjekatForm(FlaskForm):
    naziv = StringField('Naziv', validators=[DataRequired(), Length(max=255)])
    opis = TextAreaField('Opis', validators=[Optional()])
    submit = SubmitField('Sačuvaj')

class ProstorijaForm(FlaskForm):
    naziv = StringField('Naziv', validators=[DataRequired(), Length(max=255)])
    sprat = StringField('Sprat', validators=[Optional(), Length(max=50)])
    broj = StringField('Broj', validators=[Optional(), Length(max=50)])
    namena = StringField('Namena', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Sačuvaj')
```

## Definition of Done
- [ ] Svi Acceptance Criteria su implementirani i testirani
- [ ] Pravno lice ima sva potrebna polja i validacije
- [ ] Automatsko kreiranje radne jedinice pri dodavanju pravnog lica je implementirano
- [ ] Radna jedinica ima sva potrebna polja
- [ ] Dodavanje dodatnih radnih jedinica je implementirano
- [ ] Hijerarhijska struktura Kompanija > Radna jedinica > Objekat > Prostorija je implementirana
- [ ] Breadcrumb navigacija odražava poziciju u hijerarhiji
- [ ] Sve flash poruke koriste srpska slova i interpunkciju
- [ ] Kod je dokumentovan i prati postojeće konvencije
- [ ] Aplikacija se pokreće bez grešaka

## Status implementacije

### Napredak

#### AC1: Polja za pravno lice ⬜
- Implementirati model PravnoLice sa svim potrebnim poljima
- Implementirati formu za pravno lice sa validacijama
- Validirati PIB i MB kao jedinstvene vrednosti

#### AC2: Automatsko kreiranje radne jedinice ⬜
- Implementirati automatsko kreiranje radne jedinice pri čuvanju pravnog lica
- Preuzeti podatke adrese iz pravnog lica
- Postaviti default vrednost "Centrala" za naziv

#### AC3: Polja za radnu jedinicu ⬜
- Implementirati model RadnaJedinica sa svim potrebnim poljima
- Implementirati formu za radnu jedinicu sa validacijama

#### AC4: Dodavanje dodatnih radnih jedinica ⬜
- Implementirati rutu i kontroler za dodavanje novih radnih jedinica
- Implementirati prikaz liste radnih jedinica na stranici detalja pravnog lica
- Dodati flash poruku nakon uspešnog kreiranja

#### AC5: Hijerarhijska struktura ⬜
- Implementirati modele za Objekat i Prostorija
- Implementirati tree view vizuelizaciju hijerarhijske strukture
- Povezati breadcrumb navigaciju sa hijerarhijskom pozicijom

### Sugestije za poboljšanje

1. **Unapređenje upravljanja pravnim licima**:
   - Implementirati funkcionalnost za grupisanje pravnih lica (npr. po delatnostima ili regionima)
   - Dodati mogućnost za unos dodatnih kontakt osoba za pravno lice
   - Implementirati istoriju promena podataka pravnog lica

2. **Unapređenje upravljanja hijerarhijskom strukturom**:
   - Implementirati drag-and-drop funkcionalnost za reorganizaciju hijerarhije
   - Dodati mogućnost kloniranja postojeće strukture za brže kreiranje sličnih struktura
   - Implementirati bulk operacije za objekte i prostorije

3. **Unapređenje validacije podataka**:
   - Implementirati proveru validnosti PIB-a i MB-a prema algoritmima za proveru
   - Dodati online proveru adrese pomoću neke geo-API usluge
   - Implementirati validaciju jedinstvenih email adresa u okviru jednog pravnog lica

## File List

Sledeći fajlovi treba da budu kreirani ili modifikovani u toku implementacije:

1. `app/models/client.py` - Dodati modele za PravnoLice, RadnaJedinica, Objekat i Prostorija
2. `app/utils/forms.py` - Dodati forme za pravna lica i njihove komponente
3. `app/views/klijenti.py` - Proširiti blueprint sa rutama za upravljanje pravnim licima i hijerarhijom
4. `app/templates/klijenti/pravno_lice_form.html` - Template za kreiranje i izmenu pravnog lica
5. `app/templates/klijenti/pravno_lice_detalji.html` - Template za prikaz detalja pravnog lica
6. `app/templates/klijenti/radna_jedinica_form.html` - Template za kreiranje i izmenu radne jedinice
7. `app/templates/klijenti/radna_jedinica_detalji.html` - Template za prikaz detalja radne jedinice
8. `app/templates/partials/breadcrumb.html` - Proširiti parcijalni template za breadcrumb navigaciju
9. `app/static/js/treeview.js` - JavaScript za interaktivni prikaz tree view hijerarhije

## Zaključak

Implementacija upravljanja pravnim licima je važan korak u razvoju sistema za upravljanje servisima, jer postavlja osnovu za kompleksnu hijerarhijsku strukturu klijenata. Ovaj story će omogućiti servisnim timovima da precizno organizuju svoje aktivnosti prema organizacionoj strukturi klijenta, što će dovesti do boljeg praćenja servisa i bolje organizacije rada. Posebna pažnja mora biti posvećena validaciji poslovnih podataka kao što su PIB i MB, kao i kreiranju intuitivne hijerarhijske navigacije koja će korisnicima olakšati snalaženje u kompleksnim organizacionim strukturama.
