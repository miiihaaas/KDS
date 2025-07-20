# Story 1.5: Upravljanje potrošnim materijalima

## Metadata
- **Story ID**: 1.5
- **Epic**: Epic 1 - Sistem osnove i autentifikacija
- **Priority**: Medium
- **Story Points**: 5
- **Status**: Done
- **Created**: 2025-07-19
- **Assigned To**: AI Developer

## User Story
**As an** administrator  
**I want to** manage consumable materials  
**So that** they can be tracked in work orders

## Business Context
KDS sistem zahteva funkcionalnost za upravljanje potrošnim materijalima koji se koriste tokom servisnih radova. Administratori moraju imati mogućnost dodavanja, ažuriranja i praćenja materijala u sistemu. Ova informacija je ključna za kasnije dodavanje materijala u radne naloge i praćenje potrošnje. Evidencija materijala treba da bude jednostavna za korišćenje i pretraživa, kako bi se olakšao rad administratora prilikom upravljanja resursima kompanije.

## Acceptance Criteria

### AC1: Pregled liste materijala
- **Given** da je administrator ulogovan
- **When** pristupi ruti `/materijali`
- **Then** prikazuje se lista svih materijala sa sledećim informacijama:
  - ID materijala
  - Naziv materijala
  - Jedinica mere
  - Status (aktivno/neaktivno)
  - Datum kreiranja/poslednjeg ažuriranja
  - Akcije (dugmad za izmenu i deaktivaciju/aktivaciju)
- **And** lista je sortirana po nazivu materijala
- **And** postoji paginacija ako ima više od 10 materijala po stranici
- **And** samo korisnici sa administratorskom ulogom mogu pristupiti ovoj strani

### AC2: Pretraga materijala
- **Given** da je administrator na stranici liste materijala
- **When** unese tekst u polje za pretragu
- **Then** lista se filtrira prema unetom tekstu koji se traži u:
  - Nazivu materijala
  - Jedinici mere
- **And** pretraga se vrši dinamički dok korisnik kuca (AJAX)
- **And** ako nema rezultata pretrage, prikazuje se odgovarajuća poruka "Nema pronađenih materijala."

### AC3: Dodavanje novog materijala
- **Given** da je administrator ulogovan
- **When** klikne na dugme "Dodaj novi materijal" na `/materijali` stranici
- **Then** prikazuje se forma za kreiranje novog materijala sa sledećim poljima:
  - Naziv (obavezno, minimum 2 karaktera)
  - Jedinica mere (obavezno, padajuća lista sa predefinisanim opcijama: kg, g, l, ml, kom, m, m²)
  - Status (checkbox: aktivno, podrazumevano čekiran)
- **And** forma ima dugmad "Sačuvaj" i "Otkaži"
- **And** forma koristi Bootstrap 5 stilizovanje
- **And** sva polja imaju odgovarajuće placeholder tekstove na srpskom jeziku

### AC4: Validacija forme za kreiranje materijala
- **Given** da administrator popunjava formu za kreiranje materijala
- **When** unese podatke i klikne "Sačuvaj"
- **Then** sistem validira unete podatke:
  - Naziv i jedinica mere moraju biti popunjeni
  - Naziv mora biti jedinstven u sistemu
- **And** ako validacija ne prođe, prikazuju se odgovarajuće poruke o grešci pored polja
- **And** ako je validacija uspešna, materijal se kreira u bazi podataka
- **And** administrator se preusmerava na listu materijala sa flash porukom "Materijal je uspešno kreiran."

### AC5: Izmena postojećeg materijala
- **Given** da je administrator ulogovan
- **When** klikne na dugme "Izmeni" pored materijala na listi
- **Then** prikazuje se forma za izmenu materijala sa:
  - Popunjenim postojećim podacima materijala
  - Istim poljima kao i forma za kreiranje
- **And** nakon uspešne izmene, prikazuje se poruka "Podaci o materijalu su uspešno ažurirani."

### AC6: Deaktivacija/aktivacija materijala
- **Given** da je administrator ulogovan
- **When** klikne na dugme "Deaktiviraj"/"Aktiviraj" pored materijala
- **Then** prikazuje se modalni dijalog za potvrdu akcije
- **And** ako administrator potvrdi akciju, status materijala se menja u bazi
- **And** prikaz u listi materijala se ažurira prema novom statusu
- **And** prikazuje se flash poruka "Materijal je uspešno deaktiviran." ili "Materijal je uspešno aktiviran."
- **And** deaktivirani materijal ne može da se doda u radni nalog

### AC7: Dostupnost materijala za radne naloge
- **Given** da sistem formira radni nalog
- **When** korisnik treba da izabere materijale za radni nalog
- **Then** u padajućem meniju se prikazuju samo aktivni materijali
- **And** deaktivirani materijali nisu dostupni za odabir

## Technical Implementation Details

### Required Routes
```python
# Material Management Blueprint routes
/materijali (GET) - Lista materijala sa pretragom
/materijali/novi (GET, POST) - Forma i obrada za kreiranje novog materijala
/materijali/<id>/izmeni (GET, POST) - Forma i obrada za izmenu materijala
/materijali/<id>/status (POST) - Endpoint za promenu statusa materijala
/api/materijali (GET) - API endpoint za dohvatanje liste aktivnih materijala za radne naloge
```

### Database Changes
Potrebno je kreirati novi model Material:
```python
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False, unique=True)
    jedinica_mere = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Material {self.naziv}, {self.jedinica_mere}>'
```

### Forms
```python
class MaterialForm(FlaskForm):
    naziv = StringField('Naziv materijala', validators=[DataRequired(), Length(min=2, max=100)])
    jedinica_mere = SelectField('Jedinica mere', 
        choices=[('kg', 'kg'), ('g', 'g'), ('l', 'l'), ('ml', 'ml'), ('kom', 'kom'), ('m', 'm'), ('m²', 'm²')],
        validators=[DataRequired()]
    )
    active = BooleanField('Aktivno', default=True)
    submit = SubmitField('Sačuvaj')
```

### Flash Message Categories
- `success` - Uspešne akcije (zelena)
- `error` - Greške (crvena) 
- `warning` - Upozorenja (žuta)
- `info` - Informativne poruke (plava)

## Definition of Done
- [ ] Svi Acceptance Criteria su implementirani i testirani
- [ ] Lista materijala je responsive i radi na mobilnim uređajima
- [ ] Pretraga materijala funkcioniše ispravno
- [ ] Forme za kreiranje i izmenu imaju pravilnu validaciju
- [ ] Deaktivacija/aktivacija materijala radi ispravno
- [ ] Role-based pristup je implementiran
- [ ] Flash poruke koriste srpska slova i interpunkciju
- [ ] Kod je dokumentovan i prati postojeće konvencije
- [ ] Aplikacija se pokreće bez grešaka
- [ ] API endpoint za dohvatanje aktivnih materijala radi ispravno

## Status implementacije

### Napredak

#### AC1: Pregled liste materijala ⬜
- Lista materijala treba da prikaže sva navedena polja
- Lista treba da bude sortirana po nazivu materijala
- Paginacija treba da prikaže 10 materijala po stranici
- Pristup treba ograničiti na administratore pomoću `@admin_required` dekoratora

#### AC2: Pretraga materijala ⬜
- Implementirati dinamičku pretragu pomoću AJAX-a
- Pretraga treba da radi po nazivu materijala i jedinici mere
- Dodati poruku kada nema rezultata pretrage

#### AC3: Dodavanje novog materijala ⬜
- Kreirati formu za novi materijal sa svim potrebnim poljima
- Implementirati Bootstrap 5 stilizovanje
- Dodati odgovarajuće placeholder tekstove na srpskom jeziku

#### AC4: Validacija forme za kreiranje materijala ⬜
- Implementirati validaciju jedinstvenosti naziva materijala
- Dodati validaciju za obavezna polja
- Nakon uspešnog kreiranja, preusmeriti korisnika na listu materijala sa flash porukom

#### AC5: Izmena postojećeg materijala ⬜
- Kreirati formu za izmenu materijala koja prikazuje postojeće podatke
- Nakon uspešne izmene prikazati odgovarajuću flash poruku

#### AC6: Deaktivacija/aktivacija materijala ⬜
- Implementirati modalni dijalog za potvrdu akcije
- Implementirati promenu statusa u bazi i ažuriranje prikaza
- Prikazati odgovarajuću flash poruku

#### AC7: Dostupnost materijala za radne naloge ⬜
- Implementirati API endpoint za dohvatanje samo aktivnih materijala
- Obezbediti da se u radnim nalozima mogu koristiti samo aktivni materijali

### Sugestije za poboljšanje

1. **Unapređenje podataka o materijalu**:
   - Dodati mogućnost unosa nabavne cene materijala
   - Implementirati praćenje zaliha materijala
   - Omogućiti grupisanje materijala po kategorijama

2. **Unapređenje korisničkog iskustva**:
   - Dodati sortiranje po kolonama u tabeli materijala
   - Implementirati izvoz liste materijala u CSV/Excel
   - Dodati funkcionalnost za masovne akcije (npr. deaktivacija više materijala odjednom)

3. **Optimizacija performansi**:
   - Implementirati keš za učestale upite kako bi se smanjio broj poziva baze podataka

## File List

Sledeći fajlovi treba da budu kreirani ili modifikovani u toku implementacije:

1. `app/models/material.py` - Model za materijale sa poljima i metodama
2. `app/utils/forms.py` - Dodati MaterialForm klasu za validaciju forme
3. `app/views/materijali.py` - Blueprint sa rutama za upravljanje materijalima
4. `app/templates/materijali/lista.html` - Glavni template za prikaz liste materijala
5. `app/templates/materijali/_lista_partial.html` - Parcijalni template za AJAX ažuriranje liste
6. `app/templates/materijali/form.html` - Template za kreiranje i izmenu materijala
7. `app/__init__.py` - Registracija blueprint-a za materijale
8. `app/templates/base.html` - Dodati link na materijale u administratorskom meniju

## Zaključak

Implementacija upravljanja potrošnim materijalima treba da prati isti obrazac kao i upravljanje vozilima. Potrebno je kreirati novi model Material u bazi podataka, implementirati CRUD operacije, pretragu, validaciju i kontrolu pristupa. Korisničko iskustvo treba da bude konzistentno sa ostatkom aplikacije, koristeći Bootstrap 5 za responzivan dizajn i Flash poruke za obaveštenja korisniku. Svi tekstovi u korisničkom interfejsu treba da budu na srpskom jeziku sa ispravnim korišćenjem srpskih slova.
