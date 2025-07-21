# Story 2.3: Upravljanje fizičkim licima

## Metadata
- **Story ID**: 2.3
- **Epic**: Epic 2 - Upravljanje klijentima i strukturom
- **Priority**: High
- **Story Points**: 5
- **Status**: Done
- **Created**: 2025-07-20
- **Assigned To**: AI Developer

## User Story
**As a** serviser  
**I want to** create individual clients with their locations  
**So that** I can track services for residential clients

## Business Context
Sistem za upravljanje servisima mora podržavati rad sa fizičkim licima (individualnim klijentima) koji mogu imati više različitih lokacija. Ova struktura je važna jer omogućava pravilno raspoređivanje i praćenje servisnih aktivnosti za rezidencijalne klijente. Serviseri moraju imati mogućnost da kreiraju fizička lica sa njihovim detaljnim informacijama, kao i da upravljaju lokacijama kuća i dodatnim strukturama, poput objekata i prostorija, što će kasnije omogućiti preciznije kreiranje i praćenje servisnih naloga za kućne korisnike.

## Acceptance Criteria

### AC1: Polja za fizičko lice
- **Given** da je serviser ulogovan i izabrao tip klijenta "Fizičko lice"
- **When** unosi podatke za fizičko lice
- **Then** forma sadrži sledeća polja:
  - Ime (obavezno)
  - Prezime (obavezno)
  - Adresa (obavezno)
  - Mesto (obavezno)
  - Poštanski broj (obavezno)
  - Država (obavezno, default "Srbija")
  - Telefon (obavezno)
  - Email

### AC2: Automatsko kreiranje lokacije kuće
- **Given** da je serviser uneo sve obavezne podatke za fizičko lice
- **When** klikne na dugme "Sačuvaj"
- **Then** sistem kreira fizičko lice
- **And** automatski kreira prvu lokaciju kuće sa podacima:
  - Naziv: "Primarna kuća" (default)
  - Adresa, mesto, poštanski broj, državu preuzeti od fizičkog lica

### AC3: Polja za lokaciju kuće
- **Given** da je serviser ulogovan i otvorio stranicu za dodavanje/izmenu lokacije kuće
- **When** unosi podatke za lokaciju kuće
- **Then** forma sadrži sledeća polja:
  - Naziv (obavezno)
  - Adresa (obavezno)
  - Mesto (obavezno)
  - Poštanski broj (obavezno)
  - Država (obavezno, default "Srbija")

### AC4: Dodavanje dodatnih lokacija
- **Given** da je serviser ulogovan i otvorio detalje fizičkog lica
- **When** klikne na dugme "Dodaj lokaciju"
- **Then** prikazuje se forma za unos podataka nove lokacije kuće
- **And** nakon uspešnog kreiranja, nova lokacija se prikazuje u listi lokacija fizičkog lica
- **And** prikazuje se flash poruka "Nova lokacija je uspešno dodata."


## Technical Implementation Details

### Required Routes
```python
# Person Entity and Location Routes
/klijenti/fizicko-lice/novi (GET, POST) - Kreiranje novog fizičkog lica
/klijenti/fizicko-lice/<int:id> (GET) - Prikaz detalja fizičkog lica
/klijenti/fizicko-lice/<int:id>/izmeni (GET, POST) - Izmena fizičkog lica
/klijenti/fizicko-lice/<int:id>/lokacije/novi (GET, POST) - Dodavanje nove lokacije kuće
/klijenti/lokacija/<int:id> (GET) - Prikaz detalja lokacije kuće
/klijenti/lokacija/<int:id>/izmeni (GET, POST) - Izmena lokacije kuće
```

### Database Models
```python
# Person Entity Model
class FizickoLice(Client):
    __tablename__ = 'fizicka_lica'
    
    id = db.Column(db.Integer, db.ForeignKey('clients.id'), primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    
    lokacije = db.relationship('LokacijaKuce', backref='fizicko_lice', lazy=True, cascade='all, delete-orphan')
    
    __mapper_args__ = {
        'polymorphic_identity': 'fizicko_lice',
    }
    
    def __repr__(self):
        return f'<FizickoLice {self.ime} {self.prezime}>'
    
    @property
    def puno_ime(self):
        return f"{self.ime} {self.prezime}"

# Home Location Model
class LokacijaKuce(db.Model):
    __tablename__ = 'lokacije_kuce'
    
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(255), nullable=False)
    adresa = db.Column(db.String(255), nullable=False)
    mesto = db.Column(db.String(100), nullable=False)
    postanski_broj = db.Column(db.String(20), nullable=False)
    drzava = db.Column(db.String(100), nullable=False, default="Srbija")
    
    fizicko_lice_id = db.Column(db.Integer, db.ForeignKey('fizicka_lica.id'), nullable=False)
    objekti = db.relationship('Objekat', backref='lokacija_kuce', lazy=True, cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<LokacijaKuce {self.naziv} - {self.fizicko_lice.puno_ime}>'

# Building Model (reused from existing implementation)
class Objekat(db.Model):
    __tablename__ = 'objekti'
    
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(255), nullable=False)
    opis = db.Column(db.Text)
    
    # Polymorphic relationship - can belong to either work unit or home location
    radna_jedinica_id = db.Column(db.Integer, db.ForeignKey('radne_jedinice.id'), nullable=True)
    lokacija_kuce_id = db.Column(db.Integer, db.ForeignKey('lokacije_kuce.id'), nullable=True)
    
    prostorije = db.relationship('Prostorija', backref='objekat', lazy=True, cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Objekat {self.naziv}>'

# Room Model (reused from existing implementation)
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
class FizickoLiceForm(ClientBaseForm):
    ime = StringField('Ime', validators=[DataRequired(), Length(max=100)])
    prezime = StringField('Prezime', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Sačuvaj')

class LokacijaKuceForm(FlaskForm):
    naziv = StringField('Naziv', validators=[DataRequired(), Length(max=255)])
    adresa = StringField('Adresa', validators=[DataRequired(), Length(max=255)])
    mesto = StringField('Mesto', validators=[DataRequired(), Length(max=100)])
    postanski_broj = StringField('Poštanski broj', validators=[DataRequired(), Length(max=20)])
    drzava = StringField('Država', validators=[DataRequired(), Length(max=100)], default="Srbija")
    submit = SubmitField('Sačuvaj')

# Reusing existing forms for Objekat and Prostorija
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
- [x] Svi Acceptance Criteria su implementirani i testirani
- [x] Fizičko lice ima sva potrebna polja i validacije
- [x] Automatsko kreiranje lokacije kuće pri dodavanju fizičkog lica je implementirano
- [x] Lokacija kuće ima sva potrebna polja
- [x] Dodavanje dodatnih lokacija je implementirano
- [x] Hijerarhijska struktura Fizičko lice > Lokacija kuće > Objekat > Prostorija je implementirana
- [x] Breadcrumb navigacija odražava poziciju u hijerarhiji
- [x] Sve flash poruke koriste srpska slova i interpunkciju
- [x] Kod je dokumentovan i prati postojeće konvencije
- [x] Aplikacija se pokreće bez grešaka
- [x] Unit testovi napisani
- [x] Unit testovi prošli

## Status implementacije

Story je **završen**. 

Svi acceptance kriterijumi su implementirani, testirani i dokumentovani. Kreirani su svi potrebni modeli, forme, rute i templati za upravljanje fizičkim licima i njihovim lokacijama. Implementirana je automatska kreacija primarne lokacije kuće prilikom dodavanja novog fizičkog lica. Svi unit testovi su napisani i uspešno prolaze.

### Kreiran kod

- Model FizickoLice implementiran u app/models/client.py
- Model LokacijaKuce implementiran u app/models/client.py
- Forme FizickoLiceForm i LokacijaKuceForm implementirane u app/utils/client_forms.py
- Rute za upravljanje fizičkim licima i lokacijama implementirane u app/views/klijenti.py
- Templates za prikaz, kreiranje i izmenu fizičkih lica i lokacija

### Testirano

- Testovi za modele: tests/test_fizicko_lice_model.py
- Testovi za forme: tests/test_fizicko_lice_form.py
- Testovi za rute: tests/test_fizicko_lice_routes.py

Svi testovi uspešno prolaze.

### Napredak

#### AC1: Polja za fizičko lice ✅
- Implementirati model FizickoLice sa svim potrebnim poljima
- Implementirati formu za fizičko lice sa validacijama

#### AC2: Automatsko kreiranje lokacije kuće ✅
- Implementirati automatsko kreiranje lokacije kuće pri čuvanju fizičkog lica
- Preuzeti podatke adrese iz fizičkog lica
- Postaviti default vrednost "Primarna kuća" za naziv

#### AC3: Polja za lokaciju kuće ✅
- Implementirati model LokacijaKuce sa svim potrebnim poljima
- Implementirati formu za lokaciju kuće sa validacijama

#### AC4: Dodavanje dodatnih lokacija ✅
- Implementirati rutu i kontroler za dodavanje novih lokacija
- Implementirati prikaz liste lokacija na stranici detalja fizičkog lica
- Dodati flash poruku nakon uspešnog kreiranja


### Sugestije za poboljšanje

1. **Unapređenje upravljanja fizičkim licima**:
   - Implementirati funkcionalnost za grupisanje fizičkih lica (npr. po regionima ili statusu)
   - Dodati mogućnost za unos više kontakt brojeva i email adresa
   - Implementirati istoriju promena podataka fizičkog lica

2. **Unapređenje upravljanja lokacijama**:
   - Dodati mogućnost označavanja primarne lokacije
   - Implementirati prikaz lokacija na mapi
   - Dodati polja za bilješke i specifične instrukcije za pristup lokaciji

3. **Integracije**:
   - Implementirati sinhronizaciju kontakata sa mobilnim telefonom
   - Dodati mogućnost slanja automatskih obaveštenja klijentima putem SMS-a ili email-a
   - Integrisati sa navigacijskim sistemom za servisere na terenu

## File List

Sledeći fajlovi treba da budu kreirani ili modifikovani u toku implementacije:

1. `app/models/client.py` - Dodati modele za FizickoLice i LokacijaKuce, proširiti Objekat model
2. `app/utils/forms.py` - Dodati forme za fizička lica i njihove komponente
3. `app/views/klijenti.py` - Proširiti blueprint sa rutama za upravljanje fizičkim licima i hijerarhijom
4. `app/templates/klijenti/fizicko_lice_form.html` - Template za kreiranje i izmenu fizičkog lica
5. `app/templates/klijenti/fizicko_lice_detalji.html` - Template za prikaz detalja fizičkog lica
6. `app/templates/klijenti/lokacija_form.html` - Template za kreiranje i izmenu lokacije kuće
7. `app/templates/klijenti/lokacija_detalji.html` - Template za prikaz detalja lokacije kuće
8. `app/templates/partials/breadcrumb.html` - Proširiti parcijalni template za breadcrumb navigaciju
9. `app/static/js/treeview.js` - Proširiti JavaScript za interaktivni prikaz tree view hijerarhije za fizička lica

## Zaključak

Implementacija upravljanja fizičkim licima predstavlja važan dodatak sistemu za upravljanje servisima, omogućavajući sveobuhvatan rad sa rezidencijalnim klijentima. Ovaj story će omogućiti servisnim timovima da precizno organizuju svoje aktivnosti prema lokacijama rezidencijalnih klijenata, što će dovesti do boljeg praćenja servisa i bolje organizacije rada na terenu. Posebna pažnja biće posvećena kreiranju intuitivne hijerarhijske navigacije koja će korisnicima olakšati snalaženje u kompleksnim strukturama lokacija.

## QA Results

### Pregled usklađenosti sa acceptance kriterijumima

✅ **AC1: Polja za fizičko lice** - Implementirano potpuno. Model i forma sadrže sva potrebna polja sa pravilnim validacijama.

✅ **AC2: Automatsko kreiranje lokacije kuće** - Implementirano, ali postoji neusklađenost u nazivu. U AC2 se navodi default naziv "Primarna kuća", dok u testu (linija 80) postoji provera za "Primarna kuća". Potrebno je uskladiti nazive.

✅ **AC3: Polja za lokaciju kuće** - Implementirano potpuno. Model i forma sadrže sva potrebna polja.

✅ **AC4: Dodavanje dodatnih lokacija** - Implementirano potpuno, sa pravilnim flash porukama i prikazom u listi.

### Kvalitet testova

✅ **Test pokrivenost** - Odlična pokrivenost CRUD operacija za fizička lica i lokacije kuće.

✅ **Jasnoća testova** - Testovi su jasno napisani i dobro dokumentovani.

✅ **Kompletnost** - Obuhvaćeni su scenariji za kreiranje, čitanje, ažuriranje i brisanje.

✅ **Dodatni testovi** - Implementirani su dodatni testovi za validaciju email formata, validaciju obaveznih polja, brisanje lokacija sa povezanim objektima i pristup rutama bez autentifikacije. Svi testovi uspešno prolaze.

### Kvalitet koda

✅ **Struktura modela** - Hijerarhijska struktura je dobro implementirana sa odgovarajućim relacijama.

✅ **Validacije** - Implementirane su validacije za obavezna polja, email format i integritet podataka. 

✅ **Flash poruke** - Koriste srpski jezik i pravilnu interpunkciju.

⚠️ **Brisanje lokacija** - Implementirano je brisanje lokacija (test linija 262-269), ali to nije eksplicitno navedeno u AC. Trebalo bi razmotriti kako brisanje lokacija utiče na sistemske podatke i servise povezane sa lokacijom.

### Preporuke za poboljšanja

1. **Uskladiti naziv primarne lokacije** - Uskladiti naziv koji se koristi za primarnu lokaciju između AC, implementacije i testova. U AC2 se navodi default naziv "Primarna kuća", dok u testu se koristi "Primarna kuća".

2. **UX poboljšanja**:
   - Razmotriti dodavanje potvrde pre brisanja lokacije
   - Implementirati sortiranje i filtriranje liste lokacija za klijente sa više lokacija
   - Dodati mogućnost označavanja primarne lokacije kada klijent ima više lokacija

3. **Proširiti funkcionalnosti**:
   - Implementirati istoriju promena podataka fizičkog lica
   - Dodati mogućnost za unos više kontakt brojeva i email adresa
   - Implementirati prikaz lokacija na mapi za lakši pregled

### Zaključak QA pregleda

Implementacija story-ja 2.3 je izuzetno dobro urađena sa potpunim pokrivanjem svih acceptance kriterijuma. Testovi su sveobuhvatni i kvalitetni, uključujući dodatne testove za validaciju unosa, testiranje brisanja povezanih objekata i proveru autorizacije. Validacija podataka je pravilno implementirana za email format i obavezna polja. Hijerarhijska struktura modela je dobro projektovana i podržava planiranu funkcionalnost. 


**Zaključak**: Story 2.3 je spreman za produkciju uz sitnu izmenu naziva primarne lokacije.
