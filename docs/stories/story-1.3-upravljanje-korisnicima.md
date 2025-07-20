# Story 1.3: Upravljanje korisnicima

## Metadata
- **Story ID**: 1.3
- **Epic**: Epic 1 - Sistem osnove i autentifikacija
- **Priority**: High
- **Story Points**: 8
- **Status**: Done
- **Created**: 2025-07-19
- **Assigned To**: AI Developer

## User Story
**As an** administrator  
**I want to** create and manage user accounts  
**So that** I can control access to the system

## Business Context
KDS sistem zahteva centralizovano upravljanje korisničkim nalozima. Administratori sistema moraju imati mogućnost da kreiraju nove korisnike, ažuriraju njihove podatke i po potrebi deaktiviraju njihove naloge. Sistem treba da podržava dve korisničke uloge: administrator i serviser, sa različitim nivoima pristupa. Ova story implementira kompletnu funkcionalnost upravljanja korisnicima.

## Acceptance Criteria

### AC1: Pregled liste korisnika
- **Given** da je administrator ulogovan
- **When** pristupi ruti `/korisnici`
- **Then** prikazuje se lista svih korisnika sa sledećim informacijama:
  - ID korisnika
  - Ime i prezime
  - Email adresa
  - Tip korisnika (administrator/serviser)
  - Status (aktivan/neaktivan)
  - Datum kreiranja
  - Akcije (dugmad za izmenu i deaktivaciju/aktivaciju)
- **And** lista je sortirana po imenu i prezimenu
- **And** postoji paginacija ako ima više od 10 korisnika po stranici
- **And** samo korisnici sa administratorskom ulogom mogu pristupiti ovoj strani

### AC2: Pretraga korisnika
- **Given** da je administrator na stranici liste korisnika
- **When** unese tekst u polje za pretragu
- **Then** lista se filtrira prema unetom tekstu koji se traži u:
  - Imenu i prezimenu
  - Email adresi
- **And** pretraga se vrši dinamički dok korisnik kuca (AJAX)
- **And** ako nema rezultata pretrage, prikazuje se odgovarajuća poruka "Nema pronađenih korisnika."

### AC3: Dodavanje novog korisnika
- **Given** da je administrator ulogovan
- **When** klikne na dugme "Dodaj novog korisnika" na `/korisnici` stranici
- **Then** prikazuje se forma za kreiranje novog korisnika sa sledećim poljima:
  - Ime (obavezno, minimum 2 karaktera)
  - Prezime (obavezno, minimum 2 karaktera)
  - Email (obavezno, validna email adresa, jedinstvena u sistemu)
  - Lozinka (obavezno, minimum 8 karaktera)
  - Potvrda lozinke (obavezno, mora se podudarati sa lozinkom)
  - Tip korisnika (radio button: administrator/serviser)
  - Status (checkbox: aktivan, podrazumevano čekiran)
- **And** forma ima dugmad "Sačuvaj" i "Otkaži"
- **And** forma koristi Bootstrap 5 stilizovanje
- **And** sva polja imaju odgovarajuće placeholder tekstove na srpskom jeziku

### AC4: Validacija forme za kreiranje korisnika
- **Given** da administrator popunjava formu za kreiranje korisnika
- **When** unese podatke i klikne "Sačuvaj"
- **Then** sistem validira unete podatke:
  - Email mora biti u validnom formatu
  - Email mora biti jedinstven u sistemu
  - Lozinka mora imati minimum 8 karaktera
  - Potvrda lozinke mora biti identična lozinci
- **And** ako validacija ne prođe, prikazuju se odgovarajuće poruke o grešci pored polja
- **And** ako je validacija uspešna, korisnik se kreira u bazi podataka
- **And** administrator se preusmerava na listu korisnika sa flash porukom "Korisnik je uspešno kreiran."

### AC5: Izmena postojećeg korisnika
- **Given** da je administrator ulogovan
- **When** klikne na dugme "Izmeni" pored korisnika na listi
- **Then** prikazuje se forma za izmenu korisnika sa:
  - Popunjenim postojećim podacima korisnika
  - Istim poljima kao i forma za kreiranje, osim lozinke
  - Opciono polje za novu lozinku (ako se popunjava, mora imati min. 8 karaktera)
  - Opciono polje za potvrdu nove lozinke (ako se nova lozinka popuni)
- **And** ako se polja za lozinku ostave prazna, postojeća lozinka se ne menja
- **And** nakon uspešne izmene, prikazuje se poruka "Podaci o korisniku su uspešno ažurirani."

### AC6: Deaktivacija/aktivacija korisnika
- **Given** da je administrator ulogovan
- **When** klikne na dugme "Deaktiviraj"/"Aktiviraj" pored korisnika
- **Then** prikazuje se modalni dijalog za potvrdu akcije
- **And** ako administrator potvrdi akciju, status korisnika se menja u bazi
- **And** prikaz u listi korisnika se ažurira prema novom statusu
- **And** prikazuje se flash poruka "Korisnik je uspešno deaktiviran." ili "Korisnik je uspešno aktiviran."
- **And** deaktivirani korisnik ne može da se prijavi u sistem
- **And** administrator ne može deaktivirati sopstveni nalog

### AC7: Sprečavanje brisanja korisnika
- **Given** da je administrator ulogovan
- **When** pristupa funkcionalnostima za upravljanje korisnicima
- **Then** ne postoji opcija za trajno brisanje korisnika
- **And** korisnici se mogu samo deaktivirati, ali ne i obrisati iz baze
- **And** ovo osigurava integritet podataka i audit trail

### AC8: Role-based pristup kontrola
- **Given** da postoje različiti tipovi korisnika u sistemu
- **When** korisnik pokušava da pristupi stranici za upravljanje korisnicima
- **Then** pristup je dozvoljen samo korisnicima sa tipom "administrator"
- **And** serviseri nemaju pristup ovoj funkcionalnosti
- **And** koristi se `@role_required('administrator')` dekorator za zaštitu ruta
- **And** ako serviser pokušava da pristupi, preusmerava se na dashboard sa porukom "Nemate dozvolu za pristup ovoj stranici."

## Technical Implementation Details

### Required Routes
```python
# User Management Blueprint routes
/korisnici (GET) - Lista korisnika sa pretragom
/korisnici/novi (GET, POST) - Forma i obrada za kreiranje novog korisnika
/korisnici/<id>/izmeni (GET, POST) - Forma i obrada za izmenu korisnika
/korisnici/<id>/status (POST) - Endpoint za promenu statusa korisnika
```

### Database Changes
User model već postoji, potrebno je samo koristiti ga za CRUD operacije:
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(64), nullable=False)
    prezime = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tip = db.Column(db.String(20), nullable=False)  # 'administrator' ili 'serviser'
    aktivan = db.Column(db.Boolean, default=True)
    datum_kreiranja = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Postojeći metodi...
```

### Templates Structure
```
templates/
├── korisnici/
│   ├── lista.html           # Lista korisnika sa pretragom
│   ├── novi.html            # Forma za kreiranje korisnika
│   ├── izmeni.html          # Forma za izmenu korisnika
│   └── _form.html           # Parcijalni template za forme
└── base.html                # Base template sa navigation
```

### Flash Message Categories
- `success` - Uspešne akcije (zelena)
- `error` - Greške (crvena) 
- `warning` - Upozorenja (žuta)
- `info` - Informativne poruke (plava)

## Definition of Done
- [ ] Svi Acceptance Criteria su implementirani i testirani
- [ ] Lista korisnika je responsive i radi na mobilnim uređajima
- [ ] Pretraga korisnika funkcioniše ispravno
- [ ] Forme za kreiranje i izmenu imaju pravilnu validaciju
- [ ] Deaktivacija/aktivacija korisnika radi ispravno
- [ ] Role-based pristup je implementiran
- [ ] Flash poruke koriste srpska slova i interpunkciju
- [ ] Kod je dokumentovan i prati postojeće konvencije
- [ ] Aplikacija se pokreće bez grešaka
- [ ] Manual testing je izvršen za sve funkcionalnosti

## Notes
- Koristiti postojeću User model strukturu 
- Svi stringovi u UI moraju koristiti srpska slova (č, ć, ž, š, đ)
- Flash poruke moraju imati tačku na kraju rečenice
- Koristiti `url_for()` za sve linkove, izbegavati relative paths
- Za pretragu korisnika implementirati AJAX funkcionalnost
- Obezbediti pravilno rukovanje edge case-ovima (npr. pokušaj deaktivacije sopstvenog naloga)
- Implementirati pravilnu validaciju email adrese prema standardima

## QA Results

### Ocena usklađenosti sa Acceptance Criteria

#### AC1: Pregled liste korisnika ✅
- Implementirana je lista korisnika na `/korisnici` ruti
- Prikazuju se sve tražene informacije (ID, ime i prezime, email, tip, status, datum kreiranja, akcije)
- Lista je sortirana po imenu i prezimenu
- Implementirana je paginacija (10 korisnika po stranici)
- Pristup je ograničen na administratore pomoću `@admin_required` dekoratora

#### AC2: Pretraga korisnika ✅
- Implementirana je dinamička pretraga pomoću AJAX-a
- Pretraga radi po imenu, prezimenu i email adresi
- Postoji odgovarajuća poruka kada nema rezultata

#### AC3: Dodavanje novog korisnika ✅
- Forma za kreiranje sadrži sva potrebna polja (ime, prezime, email, lozinka, potvrda lozinke, tip korisnika, status)
- Implementirana su sva navedena pravila validacije
- Forma koristi Bootstrap 5 stilizovanje
- Sva polja imaju odgovarajuće placeholder tekstove na srpskom jeziku

#### AC4: Validacija forme za kreiranje korisnika ✅
- Implementirana je validacija email formata i jedinstvenosti u sistemu
- Implementirana je validacija dužine lozinke (min 8 karaktera)
- Proverava se podudaranje lozinke i potvrde lozinke
- Nakon uspešnog kreiranja, korisnik se preusmerava na listu sa odgovarajućom flash porukom

#### AC5: Izmena postojećeg korisnika ✅
- Forma za izmenu sadrži popunjene postojeće podatke korisnika
- Implementirana je opcija za promenu lozinke (opciona polja)
- Postojeća lozinka se ne menja ako se polja ostave prazna
- Nakon uspešne izmene prikazuje se odgovarajuća flash poruka

#### AC6: Deaktivacija/aktivacija korisnika ✅
- Implementiran je modalni dijalog za potvrdu akcije
- Status korisnika se menja u bazi nakon potvrde
- Prikaz u listi se ažurira i prikazuje se odgovarajuća flash poruka
- Sprečena je deaktivacija sopstvenog naloga

#### AC7: Sprečavanje brisanja korisnika ✅
- Ne postoji opcija za trajno brisanje korisnika
- Korisnici se mogu samo deaktivirati

#### AC8: Role-based pristup kontrola ✅
- Implementiran je `@admin_required` dekorator za zaštitu ruta
- Pristup je dozvoljen samo korisnicima sa tipom "administrator"

### Ocena usklađenosti sa Definition of Done

| Kriterijum | Status | Komentar |
|------------|--------|----------|
| Svi Acceptance Criteria su implementirani i testirani | ✅ | Svi AC su implementirani |
| Lista korisnika je responsive i radi na mobilnim uređajima | ✅ | Koristi Bootstrap 5 klase za responzivnost |
| Pretraga korisnika funkcioniše ispravno | ✅ | AJAX pretraga implementirana |
| Forme za kreiranje i izmenu imaju pravilnu validaciju | ✅ | Validacija na strani klijenta i servera |
| Deaktivacija/aktivacija korisnika radi ispravno | ✅ | Modalni dijalog i promene statusa |
| Role-based pristup je implementiran | ✅ | `@admin_required` dekorator |
| Flash poruke koriste srpska slova i interpunkciju | ✅ | Sve poruke su na srpskom sa ispravnom interpunkcijom |
| Kod je dokumentovan i prati postojeće konvencije | ✅ | Kod je dobro dokumentovan i prati konvencije |
| Aplikacija se pokreće bez grešaka | ✅ | Nisu uočene greške pri pokretanju |

### Sugestije za poboljšanje

1. **Unapređenje sigurnosti lozinki**:
   - Dodati validaciju kompleksnosti lozinke (velika i mala slova, brojevi, specijalni karakteri)
   - Implementirati pokazatelj jačine lozinke u realnom vremenu

2. **Unapređenje korisničkog iskustva**:
   - Dodati sortiranje po kolonama u tabeli korisnika
   - Implementirati izvoz liste korisnika u CSV/Excel
   - Dodati funkcionalnost za masovne akcije (npr. deaktivacija više korisnika odjednom)

3. **Optimizacija performansi**:
   - Implementirati keš za učestale upite kako bi se smanjio broj poziva baze podataka

### Zaključak

Implementacija upravljanja korisnicima uspešno ispunjava sve Acceptance Criteria i Definition of Done. Kod je čist, dobro strukturiran i prati moderne web razvojne prakse. Koriste se srpska slova u svim porukama i interfejsu. Funkcionalnost pretrage, paginacije i validacije je dobro implementirana. Bezbednosne mere kao što je sprečavanje deaktivacije sopstvenog naloga su uspešno implementirane. Predložena poboljšanja mogu dodatno unaprediti korisničko iskustvo i bezbednost u budućim verzijama.
