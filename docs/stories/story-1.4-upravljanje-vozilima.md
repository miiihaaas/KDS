# Story 1.4: Upravljanje vozilima

## Metadata
- **Story ID**: 1.4
- **Epic**: Epic 1 - Sistem osnove i autentifikacija
- **Priority**: Medium
- **Story Points**: 5
- **Status**: Done
- **Created**: 2025-07-19
- **Assigned To**: AI Developer

## User Story
**As an** administrator  
**I want to** manage company vehicles  
**So that** I can assign them to work orders

## Business Context
KDS sistem zahteva funkcionalnost za upravljanje voznim parkom kompanije. Administratori moraju imati mogućnost dodavanja, ažuriranja i praćenja vozila u sistemu. Ova informacija je ključna za kasnije dodeljivanje vozila radnim nalozima. Evidencija vozila treba da bude jednostavna za korišćenje i pretraživa, kako bi se olakšao rad administratora prilikom upravljanja resursima kompanije.

## Acceptance Criteria

### AC1: Pregled liste vozila
- **Given** da je administrator ulogovan
- **When** pristupi ruti `/vozila`
- **Then** prikazuje se lista svih vozila sa sledećim informacijama:
  - ID vozila
  - Marka vozila
  - Model vozila
  - Registarska oznaka
  - Status (aktivno/neaktivno)
  - Datum registracije/poslednjeg ažuriranja
  - Akcije (dugmad za izmenu i deaktivaciju/aktivaciju)
- **And** lista je sortirana po registarskoj oznaci
- **And** postoji paginacija ako ima više od 10 vozila po stranici
- **And** samo korisnici sa administratorskom ulogom mogu pristupiti ovoj strani

### AC2: Pretraga vozila
- **Given** da je administrator na stranici liste vozila
- **When** unese tekst u polje za pretragu
- **Then** lista se filtrira prema unetom tekstu koji se traži u:
  - Marki vozila
  - Modelu vozila
  - Registarskoj oznaci
- **And** pretraga se vrši dinamički dok korisnik kuca (AJAX)
- **And** ako nema rezultata pretrage, prikazuje se odgovarajuća poruka "Nema pronađenih vozila."

### AC3: Dodavanje novog vozila
- **Given** da je administrator ulogovan
- **When** klikne na dugme "Dodaj novo vozilo" na `/vozila` stranici
- **Then** prikazuje se forma za kreiranje novog vozila sa sledećim poljima:
  - Marka (obavezno, minimum 2 karaktera)
  - Model (obavezno, minimum 2 karaktera)
  - Registarska oznaka (obavezno, jedinstvena u sistemu)
  - Status (checkbox: aktivno, podrazumevano čekiran)
- **And** forma ima dugmad "Sačuvaj" i "Otkaži"
- **And** forma koristi Bootstrap 5 stilizovanje
- **And** sva polja imaju odgovarajuće placeholder tekstove na srpskom jeziku

### AC4: Validacija forme za kreiranje vozila
- **Given** da administrator popunjava formu za kreiranje vozila
- **When** unese podatke i klikne "Sačuvaj"
- **Then** sistem validira unete podatke:
  - Registarska oznaka mora biti jedinstvena u sistemu
  - Sva obavezna polja moraju biti popunjena
- **And** ako validacija ne prođe, prikazuju se odgovarajuće poruke o grešci pored polja
- **And** ako je validacija uspešna, vozilo se kreira u bazi podataka
- **And** administrator se preusmerava na listu vozila sa flash porukom "Vozilo je uspešno kreirano."

### AC5: Izmena postojećeg vozila
- **Given** da je administrator ulogovan
- **When** klikne na dugme "Izmeni" pored vozila na listi
- **Then** prikazuje se forma za izmenu vozila sa:
  - Popunjenim postojećim podacima vozila
  - Istim poljima kao i forma za kreiranje
- **And** nakon uspešne izmene, prikazuje se poruka "Podaci o vozilu su uspešno ažurirani."

### AC6: Deaktivacija/aktivacija vozila
- **Given** da je administrator ulogovan
- **When** klikne na dugme "Deaktiviraj"/"Aktiviraj" pored vozila
- **Then** prikazuje se modalni dijalog za potvrdu akcije
- **And** ako administrator potvrdi akciju, status vozila se menja u bazi
- **And** prikaz u listi vozila se ažurira prema novom statusu
- **And** prikazuje se flash poruka "Vozilo je uspešno deaktivirano." ili "Vozilo je uspešno aktivirano."
- **And** deaktivirano vozilo ne može da se dodeli radnom nalogu

### AC7: Dostupnost vozila za radne naloge
- **Given** da sistem formira radni nalog
- **When** korisnik treba da izabere vozilo za radni nalog
- **Then** u padajućem meniju se prikazuju samo aktivna vozila
- **And** deaktivirana vozila nisu dostupna za odabir

## Technical Implementation Details

### Required Routes
```python
# Vehicle Management Blueprint routes
/vozila (GET) - Lista vozila sa pretragom
/vozila/novo (GET, POST) - Forma i obrada za kreiranje novog vozila
/vozila/<id>/izmeni (GET, POST) - Forma i obrada za izmenu vozila
/vozila/<id>/status (POST) - Endpoint za promenu statusa vozila
/api/vozila (GET) - API endpoint za dohvatanje liste aktivnih vozila za radne naloge
```

### Database Changes
Potrebno je kreirati novi model Vehicle:
```python
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marka = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    registracija = db.Column(db.String(20), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Vehicle {self.marka} {self.model}, {self.registracija}>'
```

### Forms
```python
class VehicleForm(FlaskForm):
    marka = StringField('Marka vozila', validators=[DataRequired(), Length(min=2, max=100)])
    model = StringField('Model vozila', validators=[DataRequired(), Length(min=2, max=100)])
    registracija = StringField('Registarska oznaka', validators=[
        DataRequired(), 
        Length(min=2, max=20),
        Regexp(r'^[A-ZŠĐČĆŽ0-9\-\s]+$', message='Registarska oznaka može sadržati samo velika slova, brojeve, crtice i razmake.')
    ])
    active = BooleanField('Aktivno', default=True)
    submit = SubmitField('Sačuvaj')
```

### Flash Message Categories
- `success` - Uspešne akcije (zelena)
- `error` - Greške (crvena) 
- `warning` - Upozorenja (žuta)
- `info` - Informativne poruke (plava)

## Definition of Done
- [x] Svi Acceptance Criteria su implementirani i testirani
- [x] Lista vozila je responsive i radi na mobilnim uređajima
- [x] Pretraga vozila funkcioniše ispravno
- [x] Forme za kreiranje i izmenu imaju pravilnu validaciju
- [x] Deaktivacija/aktivacija vozila radi ispravno
- [x] Role-based pristup je implementiran
- [x] Flash poruke koriste srpska slova i interpunkciju
- [x] Kod je dokumentovan i prati postojeće konvencije
- [x] Aplikacija se pokreće bez grešaka
- [x] API endpoint za dohvatanje aktivnih vozila radi ispravno

## Status implementacije

### Napredak

#### AC1: Pregled liste vozila ✅
- Lista prikazuje sva polja vozila
- Lista je sortirana po registarskoj oznaci
- Implementirana je paginacija (10 vozila po stranici)
- Pristup je ograničen na administratore pomoću `@admin_required` dekoratora

#### AC2: Pretraga vozila ✅
- Implementirana je dinamička pretraga pomoću AJAX-a
- Pretraga radi po marki, modelu i registarskoj oznaci
- Dodata je poruka kada nema rezultata pretrage

#### AC3: Dodavanje novog vozila ✅
- Forma za kreiranje sadrži sva potrebna polja
- Implementirano je Bootstrap 5 stilizovanje
- Dodati su odgovarajući placeholder tekstovi na srpskom jeziku

#### AC4: Validacija forme za kreiranje vozila ✅
- Implementirana je validacija jedinstvenosti registarske oznake
- Dodata je validacija za obavezna polja
- Nakon uspešnog kreiranja, korisnik se preusmerava na listu vozila sa odgovarajućom flash porukom

#### AC5: Izmena postojećeg vozila ✅
- Forma za izmenu sadrži popunjene postojeće podatke
- Nakon uspešne izmene prikazuje se odgovarajuća flash poruka

#### AC6: Deaktivacija/aktivacija vozila ✅
- Implementiran je modalni dijalog za potvrdu akcije
- Implementirana je promena statusa u bazi i ažuriranje prikaza
- Prikazuje se odgovarajuća flash poruka

#### AC7: Dostupnost vozila za radne naloge ✅
- Implementiran je API endpoint za dohvatanje samo aktivnih vozila
- Obezbeđeno je da se u radnim nalozima mogu koristiti samo aktivna vozila

### Sugestije za poboljšanje

1. **Unapređenje podataka o vozilu**:
   - Dodati više polja za detalje o vozilu (godina proizvodnje, tip vozila, nosivost)
   - Dodati opciju za upload slika vozila

## File List

Sledeći fajlovi su kreirani ili modifikovani u toku implementacije:

1. `app/models/vehicle.py` - Model za vozila sa poljima i metodama
2. `app/utils/forms.py` - Dodata VehicleForm klasa za validaciju forme
3. `app/views/vozila.py` - Blueprint sa rutama za upravljanje vozilima
4. `app/templates/vozila/lista.html` - Glavni template za prikaz liste vozila
5. `app/templates/vozila/_lista_partial.html` - Parcijalni template za AJAX ažuriranje liste
6. `app/templates/vozila/form.html` - Template za kreiranje i izmenu vozila
7. `app/__init__.py` - Registracija blueprint-a za vozila
8. `app/templates/base.html` - Dodat link na vozila u administratorskom meniju

## Dev Agent Record

### Opis implementacije

Implementirana je funkcionalnost za upravljanje vozilima u kompaniji prema zadatim acceptance kriterijima. Implementacija obuhvata:

- Kreiranje modela `Vehicle` sa potrebnim poljima (marka, model, registracija, aktivno stanje)
- CRUD operacije za vozila sa odgovarajućim rutama i kontrolerima
- Role-based pristup ograničen samo na administratore
- Validacija forme sa proverom jedinstvenosti registarske oznake
- Dinamička pretraga vozila po marki, modelu i registraciji koristeći AJAX
- Paginacija liste vozila (10 vozila po stranici)
- Bootstrap 5 stilizovanje svih elemenata korisničkog interfejsa
- Modalni dijalog za potvrdu promene statusa vozila
- API endpoint za dohvatanje samo aktivnih vozila

Svi elementi korisničkog interfejsa su implementirani na srpskom jeziku sa pravilnom interpunkcijom i korišćenjem srpskih karaktera (č, ć, ž, š, đ).

### Teškoće i rešenja

Posebna pažnja posvećena je:

1. **Case-insensitive pretrazi** - implementirana je ilike pretraga za efikasno pronalaženje vozila
2. **Validaciji jedinstvenosti registracije** - korišćen je custom validator koji ignoriše trenutno vozilo pri proveri jedinstvenosti
3. **AJAX komunikaciji** - implementiran je parcijalni template za ažuriranje liste bez potrebe za osvježavanjem cele stranice
4. **Flash porukama** - sve poruke su na srpskom jeziku i koriste znake interpunkcije

### Sugestije za budući razvoj

1. Dodati više informacija o vozilima (godina proizvodnje, tip vozila, nosivost)
2. Implementirati upload i prikaz slika vozila
3. Dodati istoriju korišćenja vozila
4. Implementirati izvoz podataka o vozilima u Excel/CSV format

2. **Unapređenje korisničkog iskustva**:
   - Dodati sortiranje po kolonama u tabeli vozila
   - Implementirati izvoz liste vozila u CSV/Excel
   - Dodati funkcionalnost za masovne akcije (npr. deaktivacija više vozila odjednom)

3. **Optimizacija performansi**:
   - Implementirati keš za učestale upite kako bi se smanjio broj poziva baze podataka

## Zaključak

Implementacija upravljanja vozilima treba da prati isti obrazac kao i upravljanje korisnicima. Potrebno je kreirati novi model Vehicle u bazi podataka, implementirati CRUD operacije, pretragu, validaciju i kontrolu pristupa. Korisničko iskustvo treba da bude konzistentno sa ostatkom aplikacije, koristeći Bootstrap 5 za responzivan dizajn i Flash poruke za obaveštenja korisniku. Svi tekstovi u korisničkom interfejsu treba da budu na srpskom jeziku sa ispravnim korišćenjem srpskih slova.

## QA Results

### Pregled implementacije

Implementacija modula za upravljanje vozilima je uspešno završena prema svim zadatim acceptance kriterijumima. Kod je dobro strukturiran, prati standardne Flask konvencije i sadrži svu traženu funkcionalnost.

### Usklađenost sa acceptance kriterijumima

✅ **AC1: Pregled liste vozila**
- Lista vozila prikazuje sve tražene informacije
- Implementirana je paginacija (10 vozila po stranici)
- Pristup je pravilno ograničen na administratore kroz @admin_required dekorator
- Lista je sortirana po registarskoj oznaci

✅ **AC2: Pretraga vozila**
- Pretraga je implementirana kroz case-insensitive ilike pretragu po marki, modelu i registraciji
- AJAX implementacija omogućava dinamičko osvežavanje rezultata
- Poruka o nepostojećim rezultatima se prikazuje kada nema poklapanja

✅ **AC3-AC5: Forme za kreiranje i izmenu vozila**
- Forme sadrže sva potrebna polja sa odgovarajućim validatorima
- Bootstrap 5 stilizovanje je primenjeno
- Flash poruke sadrže srpska slova i tačku na kraju rečenice
- Registarske oznake se automatski čuvaju velikim slovima, što je dobra praksa

✅ **AC6: Deaktivacija/aktivacija vozila**
- Implementirana je funkcionalnost promene statusa vozila
- Prikazuju se odgovarajuće poruke o uspešnoj promeni

✅ **AC7: Dostupnost vozila za radne naloge**
- API endpoint vraća samo aktivna vozila

### Kvalitet koda

- ✅ **DRY princip**: Kod izbegava ponavljanje, koristi parcijalne template-e
- ✅ **Struktura**: Blueprint struktura je dobro organizovana
- ✅ **Dokumentacija**: Sve funkcije imaju docstring komentare
- ✅ **Validacija**: Implementirana je odgovarajuća validacija podataka
- ✅ **Lokalizacija**: Sve poruke su pravilno na srpskom jeziku sa znakovima interpunkcije

### Preporuke za poboljšanje

1. **Bezbednost i optimizacija**:
   - Razmotriti dodavanje rate-limiting mehanizma za API endpoint
   - Uvesti caching mehanizam za najčešće pristupane liste vozila

2. **Refaktoring**:
   - Funkcije za validaciju registarskih oznaka izdvojiti u poseban modul za potencijalnu ponovnu upotrebu
   - Dodati više testova, posebno za jedinstvenu validaciju registarskih oznaka

3. **Korisničko iskustvo**:
   - Razmotriti vizuelno poboljšanje liste vozila sa ikonicama i bojama za status
   - Dodati potvrdu pre pokušaja unosa duplikata registarskih oznaka

Ukupna ocena: **Odlično** ✓
