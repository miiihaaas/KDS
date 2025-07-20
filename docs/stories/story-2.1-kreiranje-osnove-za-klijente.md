# Story 2.1: Kreiranje osnove za klijente

## Metadata
- **Story ID**: 2.1
- **Epic**: Epic 2 - Upravljanje klijentima i strukturom
- **Priority**: High
- **Story Points**: 8
- **Status**: Done
- **Created**: 2025-07-20
- **Assigned To**: AI Developer

## User Story
**As a** serviser  
**I want to** create and manage clients  
**So that** I can organize work orders by client structure

## Business Context
Sistem za upravljanje servisima zahteva funkcionalnost za kreiranje i upravljanje klijentima. Klijenti mogu biti pravna ili fizička lica, i svako od njih ima svoju hijerarhijsku strukturu lokacija. Serviseri moraju imati mogućnost kreiranja, pregledanja i upravljanja klijentima kako bi kasnije mogli da povezuju radne naloge sa odgovarajućim klijentima i njihovim lokacijama. Jednostavan pristup informacijama o klijentima omogućava efikasnije planiranje servisnih aktivnosti i praćenje istorije servisa po klijentu.

## Acceptance Criteria

### AC1: Tipovi klijenata
- **Given** da je serviser ulogovan
- **When** započne proces kreiranja klijenta
- **Then** sistem nudi izbor dva tipa klijenta:
  - Pravno lice (kompanije, organizacije)
  - Fizičko lice (individualni korisnici)
- **And** tip klijenta određuje koje će se dodatne informacije prikupljati

### AC2: Osnovna forma za kreiranje klijenta
- **Given** da je serviser ulogovan
- **When** klikne na dugme "Dodaj novog klijenta" na početnoj stranici klijenata
- **Then** prikazuje se forma za kreiranje novog klijenta sa:
  - Radio dugmadima za izbor tipa klijenta (pravno/fizičko lice)
  - Osnovnim poljima zavisno od izabranog tipa
  - Dugmadima "Sačuvaj" i "Otkaži"
- **And** forma je responzivna i pravilno formatirana na svim veličinama ekrana
- **And** forma koristi Bootstrap 5 stilizovanje
- **And** sva polja imaju odgovarajuće placeholder tekstove na srpskom jeziku

### AC3: Lista klijenata sa pretragom
- **Given** da je serviser ulogovan
- **When** pristupi ruti `/klijenti`
- **Then** prikazuje se lista svih klijenata sa sledećim informacijama:
  - ID klijenta
  - Tip klijenta (pravno/fizičko lice)
  - Naziv (za pravna lica) ili ime i prezime (za fizička lica)
  - Adresa
  - Kontakt telefon
  - Email
  - Datum kreiranja/poslednjeg ažuriranja
  - Akcije (dugmad za pregled, izmenu i druge operacije)
- **And** lista je sortirana po nazivu/imenu klijenta
- **And** postoji paginacija ako ima više od 10 klijenata po stranici
- **And** postoji polje za pretragu koje omogućava filtriranje liste prema:
  - Nazivu/imenu klijenta
  - Adresi
  - Kontakt telefonu
  - Email-u
- **And** pretraga se vrši dinamički dok korisnik kuca (AJAX)
- **And** ako nema rezultata pretrage, prikazuje se odgovarajuća poruka "Nema pronađenih klijenata."

### AC4: Izmena klijenta
- **Given** da je serviser ulogovan
- **When** klikne na dugme "Izmeni" pored klijenta na listi
- **Then** prikazuje se forma za izmenu klijenta sa:
  - Popunjenim postojećim podacima klijenta
  - Istim poljima kao i forma za kreiranje
  - Nemogućnošću promene tipa klijenta (pravno/fizičko)
- **And** nakon uspešne izmene, prikazuje se poruka "Podaci o klijentu su uspešno ažurirani."
- **And** forma sadrži validaciju za sva obavezna polja
- **And** ako validacija ne prođe, prikazuju se odgovarajuće poruke o grešci pored polja

### AC5: Breadcrumb navigacija
- **Given** da je serviser ulogovan
- **When** pristupa bilo kojoj strani u hijerarhiji klijenata
- **Then** prikazuje se breadcrumb navigacija koja pokazuje:
  - Trenutnu lokaciju u hijerarhiji (npr. Klijenti > Pravno lice "Firma" > Radna jedinica "Centrala")
  - Svaki element u breadcrumb-u je klikabilan i vodi na odgovarajuću stranicu
  - Trenutna lokacija je istaknuta i nije klikabilna
- **And** breadcrumb je konzistentno prikazan na svim stranicama vezanim za klijente
- **And** navigacija je intuitivna i olakšava kretanje kroz hijerarhijsku strukturu

## Technical Implementation Details

### Required Routes
```python
# Client Management Blueprint routes
/klijenti (GET) - Lista klijenata sa pretragom
/klijenti/novi (GET, POST) - Kreiranje novog klijenta
/klijenti/<int:id> (GET) - Prikaz detalja klijenta
/klijenti/<int:id>/izmeni (GET, POST) - Izmena klijenta
```

### Database Models
```python
# Base Client Model
class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.String(20), nullable=False)  # 'pravno_lice' ili 'fizicko_lice'
    adresa = db.Column(db.String(255), nullable=False)
    mesto = db.Column(db.String(100), nullable=False)
    postanski_broj = db.Column(db.String(20), nullable=False)
    drzava = db.Column(db.String(100), nullable=False, default='Srbija')
    telefon = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'client',
        'polymorphic_on': tip
    }

# Legal Entity Model
class PravnoLice(Client):
    __tablename__ = 'pravna_lica'
    
    id = db.Column(db.Integer, db.ForeignKey('clients.id'), primary_key=True)
    naziv = db.Column(db.String(255), nullable=False, index=True)
    pib = db.Column(db.String(20), unique=True, nullable=False, index=True)
    mb = db.Column(db.String(20), unique=True, nullable=False)
    
    radne_jedinice = db.relationship('RadnaJedinica', backref='pravno_lice', lazy='dynamic')
    
    __mapper_args__ = {
        'polymorphic_identity': 'pravno_lice',
    }
    
    def __repr__(self):
        return f'<PravnoLice {self.naziv}, PIB: {self.pib}>'

# Individual Client Model
class FizickoLice(Client):
    __tablename__ = 'fizicka_lica'
    
    id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
    ime = db.Column(db.String(100), nullable=False, index=True)
    prezime = db.Column(db.String(100), nullable=False, index=True)
    
    lokacije = db.relationship('LokacijaKuce', backref='fizicko_lice', lazy='dynamic')
    
    __mapper_args__ = {
        'polymorphic_identity': 'fizicko_lice',
    }
    
    def __repr__(self):
        return f'<FizickoLice {self.ime} {self.prezime}>'
    
    def get_full_name(self):
        return f"{self.ime} {self.prezime}"
```

### Forms
```python
class ClientBaseForm(FlaskForm):
    adresa = StringField('Adresa', validators=[DataRequired(), Length(max=255)])
    mesto = StringField('Mesto', validators=[DataRequired(), Length(max=100)])
    postanski_broj = StringField('Poštanski broj', validators=[DataRequired(), Length(max=20)])
    drzava = StringField('Država', default='Srbija', validators=[DataRequired(), Length(max=100)])
    telefon = StringField('Telefon', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])

class PravnoLiceForm(ClientBaseForm):
    naziv = StringField('Naziv firme', validators=[DataRequired(), Length(min=2, max=255)])
    pib = StringField('PIB', validators=[DataRequired(), Length(min=9, max=9)])
    mb = StringField('Matični broj', validators=[DataRequired(), Length(min=8, max=8)])

class FizickoLiceForm(ClientBaseForm):
    ime = StringField('Ime', validators=[DataRequired(), Length(min=2, max=100)])
    prezime = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=100)])
```

## Definition of Done
- [ ] Svi Acceptance Criteria su implementirani i testirani
- [ ] Sistem podržava pravna i fizička lica kao različite tipove klijenata
- [ ] Lista klijenata je implementirana sa pretragom i paginacijom
- [ ] Forme za kreiranje i izmenu imaju pravilnu validaciju
- [ ] Breadcrumb navigacija je implementirana i pokazuje trenutnu lokaciju u hijerarhiji
- [ ] Sve funkcionalnosti su testirane i rade ispravno
- [ ] Flash poruke koriste srpska slova i interpunkciju
- [ ] Kod je dokumentovan i prati postojeće konvencije
- [ ] Aplikacija se pokreće bez grešaka

## Status implementacije

### Napredak

#### AC1: Tipovi klijenata ⬜
- Implementirati model koji podržava dva tipa klijenata (pravna i fizička lica)
- Implementirati različite forme za različite tipove klijenata

#### AC2: Osnovna forma za kreiranje klijenta ⬜
- Kreirati formu za novi klijent sa svim potrebnim poljima
- Implementirati Bootstrap 5 stilizovanje
- Implementirati dinamičko menjanje polja forme u zavisnosti od izabranog tipa klijenta
- Dodati odgovarajuće placeholder tekstove na srpskom jeziku

#### AC3: Lista klijenata sa pretragom ⬜
- Implementirati listu klijenata sa svim potrebnim informacijama
- Implementirati dinamičku pretragu pomoću AJAX-a
- Implementirati paginaciju
- Dodati poruku kada nema rezultata pretrage

#### AC4: Izmena klijenta ⬜
- Kreirati formu za izmenu klijenta koja prikazuje postojeće podatke
- Implementirati validaciju svih polja
- Nakon uspešne izmene prikazati odgovarajuću flash poruku

#### AC5: Breadcrumb navigacija ⬜
- Implementirati breadcrumb navigaciju za sve stranice vezane za klijente
- Obezbediti konzistentnost prikaza breadcrumb-a kroz celu aplikaciju
- Omogućiti intuitivnu navigaciju kroz hijerarhijsku strukturu

### Sugestije za poboljšanje

1. **Unapređenje upravljanja klijentima**:
   - Implementirati funkcionalnost za izvoz liste klijenata u CSV/Excel
   - Dodati mogućnost masovnog importa klijenata iz Excel fajla
   - Dodati funkcionalnost za arhiviranje klijenata umesto trajnog brisanja

2. **Unapređenje korisničkog iskustva**:
   - Implementirati vizuelno razlikovanje različitih tipova klijenata u listi
   - Dodati mini-dashboard za brzi pregled statistike klijenata
   - Implementirati funkcionalnost za tagovanje klijenata i filtriranje po tagovima

3. **Unapređenje sigurnosti**:
   - Implementirati dodatnu validaciju jedinstvenih polja (PIB, MB) sa proverom validnosti
   - Implementirati log aktivnosti na klijentima (ko je i kada menjao podatke)

## File List

Sledeći fajlovi treba da budu kreirani ili modifikovani u toku implementacije:

1. `app/models/client.py` - Modeli za klijente sa poljima i metodama
2. `app/utils/forms.py` - Dodati forme za klijente (ClientBaseForm, PravnoLiceForm, FizickoLiceForm)
3. `app/views/klijenti.py` - Blueprint sa rutama za upravljanje klijentima
4. `app/templates/klijenti/lista.html` - Glavni template za prikaz liste klijenata
5. `app/templates/klijenti/_lista_partial.html` - Parcijalni template za AJAX ažuriranje liste
6. `app/templates/klijenti/form.html` - Template za kreiranje i izmenu klijenata
7. `app/templates/klijenti/detalji.html` - Template za prikaz detalja klijenta
8. `app/templates/partials/breadcrumb.html` - Parcijalni template za breadcrumb navigaciju
9. `app/__init__.py` - Registracija blueprint-a za klijente
10. `app/templates/base.html` - Dodati link na klijente u glavnom meniju

## Zaključak

Implementacija osnove za klijente je ključni deo sistema koji će omogućiti servisnim timovima da efikasno upravljaju podacima o klijentima i njihovim lokacijama. Sistem treba da bude fleksibilan i da podržava različite tipove klijenata (pravna i fizička lica) sa njihovim specifičnim atributima. Korisničko iskustvo treba da bude intuitivno, sa jasnom navigacijom kroz hijerarhijsku strukturu pomoću breadcrumb-a. Svi tekstovi u korisničkom interfejsu treba da budu na srpskom jeziku sa ispravnim korišćenjem srpskih slova, a flash poruke treba da sadrže pravilnu interpunkciju.
