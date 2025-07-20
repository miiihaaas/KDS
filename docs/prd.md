# KDS Sistem Product Requirements Document (PRD)

## Goals and Background Context

### Goals
- Digitalizacija kompletnog procesa servisiranja, popravke i montaže HVAC uređaja
- Eliminacija papirnog dokumentovanja i ručnog vođenja evidencije
- Povećanje efikasnosti servisera kroz mobilno-optimizovane interfejse
- Automatizacija generisanja radnih naloga i komunikacije sa klijentima
- Implementacija QR kod sistema za brzu identifikaciju uređaja
- Centralizovano upravljanje klijentima, uređajima i potrošnim materijalima

### Background Context
KDS (Sistem radnih naloga) rešava kritičan problem u HVAC servisnoj industriji - prelazak sa papirnog na digitalno dokumentovanje. Trenutni procesi zahtevaju ručno vođenje evidencije što rezultuje greškama, gubicima podataka i neoptimalnim workflow-om. Sistem omogućava servisnim kompanijama da modernizuju svoje operacije kroz web aplikaciju optimizovanu za mobilne uređaje (serviseri) i desktop (administratori).

### Change Log
| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2024-01-15 | 1.0 | Inicijalna verzija PRD-a | PM |

## Requirements

### Functional
1. **FR1**: Sistem omogućava autentifikaciju sa dva nivoa korisnika (administrator, serviser) sa standardnom opcijom za reset lozinke
2. **FR2**: Administrator može kreirati, editovati i upravljati nalozima servisera
3. **FR3**: Sistem podržava upravljanje podacima o službenim vozilima (marka, model, registracija)
4. **FR4**: Sistem omogućava upravljanje potrošnim materijalima sa karakteristikama (naziv, jedinica mere)
5. **FR5**: Sistem podržava kreiranje i upravljanje klijentima - pravna lica (kompanija > lokacija > objekat > prostorija) i fizička lica (kuća > lokacija > objekat > prostorija)
6. **FR6**: Sistem omogućava registraciju tri tipa HVAC uređaja: rashladna tehnika, grejna tehnika i ventilacioni sistemi sa podtipovima
7. **FR7**: Sistem generiše jedinstvene ID-jeve za uređaje koji se koriste za QR kod funkcionalnnost
8. **FR8**: Sistem omogućava generisanje, štampanje i skeniranje QR kodova za uređaje
9. **FR9**: Skeniranje QR koda prikazuje putanju: Kompanija/Kuća - Lokacija - Objekat - Prostorija - Uređaj
10. **FR10**: Sistem omogućava kreiranje radnih naloga sa tri tipa: servis, popravka, montaža
11. **FR11**: Sistem automatski generiše oznake radnih naloga (RNS, RNP, RNM + godina-broj)
12. **FR12**: Sistem omogućava dodavanje materijala u radne naloge za popravke i montaže
13. **FR13**: Sistem generiše i šalje radne naloge klijentima preko email-a
14. **FR14**: Sistem omogućava praćenje statusa radnih naloga (U radu, Završen, Fakturisan, Otkazan)
15. **FR15**: Sistem omogućava pregled radnih naloga po periodu i klijentima
16. **FR16**: Sistem automatski beleži datum i vreme svake intervencije na uređaju

### Non Functional
1. **NFR1**: Sistem mora biti responzivan i optimizovan za mobilne uređaje (primarno za servisere)
2. **NFR2**: Sistem mora biti kompatibilan sa Chrome, Firefox, Safari, Edge (poslednje 2 verzije)
3. **NFR3**: Vreme odziva sistema mora biti manje od 3 sekunde za osnovne operacije
4. **NFR4**: Sistem mora podržavati kamersku funkcionalnost za QR kod skeniranje
5. **NFR5**: Sistem mora biti dostupan 99.5% vremena tokom radnih sati
6. **NFR6**: Podaci klijenata moraju biti sigurno čuvani u skladu sa GDPR regulations
7. **NFR7**: Sistem mora podržavati paralelno korišćenje od strane više servisera
8. **NFR8**: Email funkcionalnost mora biti pouzdana za slanje radnih naloga

## User Interface Design Goals

### Overall UX Vision
Sistem mora pružiti intuitivno korisničko iskustvo optimizovano za dva različita konteksta korišćenja: mobilni za servisere u terenu i desktop za administratore u kancelariji. Interfejs mora biti jednostavan, brz i efikasan za oba korisnika.

### Key Interaction Paradigms
- **Touch-first design** za mobilne uređaje sa velikim dugmićima i jednostavnim gestovima
- **Kamera integracija** za QR kod skeniranje jednim dodirom
- **Breadcrumb navigacija** za lakše snalaženje u hijerarhiji klijent-lokacija-objekat-prostorija
- **Modal dialozi** za kreiranje i editovanje entiteta
- **Swipe actions** za brze akcije na listama

### Core Screens and Views
- **Login Screen**: Jednostavan login sa opcijom za reset lozinke
- **Dashboard**: Različit za administratore i servisere
- **Client Management**: Lista klijenata sa pretragom i filter opcijama
- **Work Order Management**: Kreiranje, editovanje i pregled radnih naloga
- **QR Code Scanner**: Kamera interface za skeniranje QR kodova
- **Device Management**: Registracija i pregled uređaja
- **Reports**: Pregled radnih naloga po različitim kriterijumima

### Accessibility: WCAG AA
Sistem mora biti dostupan korisnicima sa invaliditetom uključujući:
- Visok kontrast za outdoor korišćenje
- Podrška za screen reader-e
- Keyboard navigacija
- Alternativni tekst za slike i QR kodove

### Branding
Profesionalan, clean dizajn koji odražava pouzdanost i efikasnost servisne kompanije. Korišćenje company color scheme-a ako postoji.

### Target Device and Platforms: Web Responsive
Primarno mobilni uređaji za servisere (Android/iOS) i desktop za administratore, sa potpunom responsive funkcionalnosti.

## Technical Assumptions

### Repository Structure: Monorepo
Jednostavna monorepo struktura sa Flask backend-om i frontend template-ima u istom projektu.

### Service Architecture
Monolitna aplikacija za MVP sa jasno definisanim modulima za buduće skaliranje.

### Testing Requirements
- Unit testiranje za kritične business logike
- Integration testiranje za email i QR kod funkcionalnosti
- Manual testiranje za korisničko iskustvo

### Additional Technical Assumptions and Requests
- **Backend Framework**: Flask (Python) za REST API
- **Database**: MySQL za perzistentnu storage
- **Frontend**: HTML, CSS, Bootstrap za responsive design
- **QR Code Library**: Python QR kod biblioteka za generisanje
- **Email Service**: SMTP konfiguracija za slanje email-ova
- **Image Processing**: Podrška za QR kod skeniranje preko web kamera
- **Authentication**: Session-based autentifikacija sa sigurnim password handling
- **File Storage**: Lokalno storage za QR kod slike
- **Printing Integration**: Podrška za portabilne štampače

## Epic List

1. **Epic 1: Sistem osnove i autentifikacija**: Uspostavljanje osnovne aplikacije, autentifikacija korisnika i administrativno upravljanje
2. **Epic 2: Upravljanje klijentima i strukturom**: Kreiranje i upravljanje klijentima sa hijerarhijskim strukturama
3. **Epic 3: Upravljanje uređajima i QR kodovima**: Registracija uređaja, generisanje QR kodova i skeniranje funkcionalnost
4. **Epic 4: Radni nalozi i workflow**: Kreiranje, upravljanje i praćenje radnih naloga sa materijalima
5. **Epic 5: Reporting i komunikacija**: Email funkcionalnost i osnovni reporti

## Epic 1: Sistem osnove i autentifikacija

**Epic Goal**: Uspostaviti osnovnu web aplikaciju sa sigurnim pristupom i administrativnim upravljanjem korisnicima, vozilima i potrošnim materijalima.

### Story 1.1: Kreiranje osnovne Flask aplikacije
As a developer,
I want to set up the basic Flask application structure,
so that the foundation for the KDS system is established.

#### Acceptance Criteria:
1. Flask aplikacija je kreirana sa osnovnom strukturom foldera
2. MySQL konekcija je konfigurisana i testirana
3. Bootstrap je integrisan za responsive design
4. Osnovni routing je implementiran
5. Development server se pokреće bez grešaka

### Story 1.2: Implementacija autentifikacije
As a korisnik sistema,
I want to log in with my credentials,
so that I can access the system securely.

#### Acceptance Criteria:
1. Login forma je kreirana sa username/password poljima
2. Session management je implementiran
3. Password hashing je sigurno implementiran
4. "Reset password" funkcionalnost je dostupna
5. Logout funkcionalnost je implementirana
6. Role-based pristup (administrator/serviser) je implementiran

### Story 1.3: Upravljanje korisnicima
As an administrator,
I want to create and manage user accounts,
so that I can control access to the system.

#### Acceptance Criteria:
1. Administrator može kreirati nove korisničke naloge
2. Korisnik ima polja: ime, prezime, email, password, tip (admin/serviser)
3. Administrator može editovati postojeće naloge
4. Administrator može deaktivirati naloge
5. Lista korisnika je dostupna sa pretrаgom

### Story 1.4: Upravljanje vozilima
As an administrator,
I want to manage company vehicles,
so that I can assign them to work orders.

#### Acceptance Criteria:
1. Administrator može dodati novo vozilo
2. Vozilo ima polja: marka, model, registracija
3. Administrator može editovati podatke o vozilu
4. Lista vozila je dostupna sa pretrаgom
5. Vozilo se može dodeliti radnom nalogu

### Story 1.5: Upravljanje potrošnim materijalima
As an administrator,
I want to manage consumable materials,
so that they can be tracked in work orders.

#### Acceptance Criteria:
1. Administrator može dodati novi materijal
2. Materijal ima polja: naziv, jedinica mere
3. Administrator može editovati podatke o materijalu
4. Lista materijala je dostupna sa pretrаgom
5. Materijal se može dodati u radni nalog

## Epic 2: Upravljanje klijentima i strukturom

**Epic Goal**: Implementirati kompletan sistem za upravljanje klijentima sa hierarchijskim strukturama koje podržavaju i pravna i fizička lica.

### Story 2.1: Kreiranje osnove za klijente
As a serviser,
I want to create and manage clients,
so that I can organize work orders by client structure.

#### Acceptance Criteria:
1. Sistem podržava dva tipa klijenata: pravno lice i fizičko lice
2. Osnovna forma za kreiranje klijenta je dostupna
3. Lista klijenata je dostupna sa pretrаgom
4. Klijent se može editovati
5. Breadcrumb navigacija pokazuje trenutnu lokaciju u hijerarhiji

### Story 2.2: Upravljanje pravnim licima
As a serviser,
I want to create legal entities with their locations,
so that I can track services across multiple company locations.

#### Acceptance Criteria:
1. Pravno lice ima polja: naziv, adresa, mesto, poštanski broj, država, telefon, email, PIB, MB
2. Automatski se kreira prva radna jedinica pri dodavanju pravnog lica
3. Radna jedinica ima polja: naziv, adresa, mesto, poštanski broj, država, kontakt osoba, telefon, email
4. Mogu se dodati dodatne radne jedinice
5. Hijerarhija Kompanija > Radna jedinica > Objekat > Prostorija je implementirana

### Story 2.3: Upravljanje fizičkim licima
As a serviser,
I want to create individual clients with their locations,
so that I can track services for residential clients.

#### Acceptance Criteria:
1. Fizičko lice ima polja: ime, prezime, adresa, mesto, poštanski broj, država, telefon, email
2. Automatski se kreira prva lokacija kuće pri dodavanju fizičkog lica
3. Lokacija kuće ima polja: naziv, adresa, mesto, poštanski broj, država
4. Mogu se dodati dodatne lokacije
5. Hijerarhija Fizičko lice > Lokacija kuće > Objekat > Prostorija je implementirana

### Story 2.4: Upravljanje objektima i prostorijama
As a serviser,
I want to create objects and rooms within client locations,
so that I can precisely locate devices.

#### Acceptance Criteria:
1. Objekat ima polje: naziv objekta
2. Prostorija ima polja: naziv prostorije (opciono), numerička oznaka (opciono)
3. Objekti se mogu dodati u bilo koju lokaciju
4. Prostorije se mogu dodati u bilo koji objekat
5. Navigacija kroz hijerarhiju je intuitivna

## Epic 3: Upravljanje uređajima i QR kodovima

**Epic Goal**: Implementirati sistem za registraciju HVAC uređaja sa QR kod funkcionalností za brzu identifikaciju i pristup podacima.

### Story 3.1: Registracija uređaja
As a serviser,
I want to register HVAC devices,
so that I can track their service history.

#### Acceptance Criteria:
1. Sistem podržava tri tipa uređaja: rashladna tehnika, grejna tehnika, ventilacioni sistemi
2. Uređaj ima polja: proizvođač, model, serijski broj, inventarski broj, godina proizvodnje, tip
3. Sistem generiše jedinstveni ID za svaki uređaj
4. Uređaj se može dodati u bilo koju prostoriju
5. Lista uređaja je dostupna sa pretrаgom

### Story 3.2: Podtipovi uređaja
As a serviser,
I want to specify device subtypes,
so that I can categorize devices more precisely.

#### Acceptance Criteria:
1. Rashladna tehnika ima podtipove: Split sistem, Čileri, Centralna klima, Toplotne pumpe, Kanalska klima, Klima komora, Pokretna klima, Klima orman, Prozorska klima, VRF sistemi, Frižideri
2. Grejna tehnika ima podtipove: TA peć, Grejalice, Kotlovi, Panelni radijatori, Radijatori
3. Ventilacioni sistemi nemaju podtipove
4. Podtip se bira na osnovu glavnog tipa
5. Filtriranje uređaja po tipu i podtipu je dostupno

### Story 3.3: QR kod generisanje
As a serviser,
I want to generate QR codes for devices,
so that I can quickly identify devices in the field.

#### Acceptance Criteria:
1. QR kod se generiše automatski pri kreiranju uređaja
2. QR kod sadrži jedinstveni ID uređaja
3. Serviser može odabrati broj QR kodova za štampanje
4. QR kod se prikazuje u printable formatu
5. Sistem omogućava ponovo štampanje QR kodova

### Story 3.4: QR kod skeniranje
As a serviser,
I want to scan QR codes,
so that I can quickly access device information.

#### Acceptance Criteria:
1. Camera interface je dostupan za skeniranje QR kodova
2. Skeniranje QR koda učitava podatke o uređaju
3. Breadcrumb navigacija pokazuje punu putanju do uređaja
4. Prethodna istorija servisa se prikazuje
5. Opcija za kreiranje novog radnog naloga je dostupna

### Story 3.5: Upravljanje postojećim uređajima
As a serviser,
I want to edit device information,
so that I can keep device records up to date.

#### Acceptance Criteria:
1. Postojeći uređaji se mogu editovati
2. Istorija izmena se čuva
3. QR kod ostaje isti pri editovanju
4. Prethodna istorija servisa se zadržava
5. Uređaj se može premestiti u drugu prostoriju

## Epic 4: Radni nalozi i workflow

**Epic Goal**: Implementirati kompletan sistem za upravljanje radnim nalozima sa podrškom za tri tipa intervencija i praćenje materijala.

### Story 4.1: Kreiranje radnog naloga
As a serviser,
I want to create work orders,
so that I can document service activities.

#### Acceptance Criteria:
1. Radni nalog se može kreirati sa osnovnim podacima
2. Polja: tip (servis/popravka/montaža), klijent, lokacija, serviseri, vozilo
3. Sistem generiše jedinstveni broj naloga sa prefiksom (RNS/RNP/RNM + godina-broj)
4. Datum i vreme otvaranja se automatski beleži
5. Status se postavlja na "U radu"

### Story 4.2: Dodavanje stavki u radni nalog
As a serviser,
I want to add service items to work orders,
so that I can document all performed activities.

#### Acceptance Criteria:
1. Mogu se dodati stavke tipa: servis, popravka, montaža
2. Stavka se može dodati preko QR koda ili manuelno
3. Uređaj se može dodati iz baze ili kreirati novi
4. Svaka stavka ima napomenu
5. Materijali se mogu dodati za popravke i montaže

### Story 4.3: Upravljanje materijalima u radnom nalogu
As a serviser,
I want to track materials used in work orders,
so that I can document resource consumption.

#### Acceptance Criteria:
1. Materijal se može dodati sa poljima: naziv, jedinica mere, količina, serijski broj
2. Automatski se generiše stavka "radni sat"
3. Materijali se prikazuju u tabeli sa opcijom brisanja
4. Ukupni troškovi se kalkulišu (opciono za određene klijente)
5. Materijali se čuvaju u istoriji radnog naloga

### Story 4.4: Upravljanje statusima radnog naloga
As a serviser,
I want to update work order status,
so that I can track progress and completion.

#### Acceptance Criteria:
1. Status se može menjati između: U radu, Završen, Fakturisan, Otkazan
2. Samo serviseri mogu menjati status na "Završen"
3. Samo administratori mogu menjati status na "Fakturisan"
4. Datum i vreme zatvaranja se automatski beleži
5. Email notifikacija se šalje pri promeni statusa

### Story 4.5: Pregled i editovanje radnih naloga
As a korisnik,
I want to view and edit work orders,
so that I can maintain accurate records.

#### Acceptance Criteria:
1. Lista radnih naloga je dostupna sa filter opcijama
2. Administratori vide sve radne naloge
3. Serviseri vide samo svoje radne naloge
4. Radni nalog se može editovati sa određenim ograničenjima
5. Istorija izmena se čuva

## Epic 5: Reporting i komunikacija

**Epic Goal**: Implementirati email funkcionalnost za slanje radnih naloga i osnovne izvještaje za praćenje aktivnosti.

### Story 5.1: Email funkcionalnost
As a serviser,
I want to send work orders to clients via email,
so that they have official documentation.

#### Acceptance Criteria:
1. Email template je kreiran za radne naloge
2. Radni nalog se generiše u PDF formatu
3. Email se šalje klijentima sa radnim nalogom u prilogu
4. CC se šalje administratorima i serviseru
5. Email status se prati (poslato/neuspešno)

### Story 5.2: Generisanje radnih naloga
As a serviser,
I want to generate formatted work orders,
so that I can provide professional documentation.

#### Acceptance Criteria:
1. Radni nalog o servisiranju (RNS) se generiše sa svim podacima
2. Radni nalog o popravci (RNP) se generiše sa materijalima
3. Radni nalog o montaži (RNM) se generiše sa materijalima
4. Profesionalni format sa company branding
5. Potpisi sekcija je uključena

### Story 5.3: Osnovni reporti
As an administrator,
I want to generate reports,
so that I can monitor business activities.

#### Acceptance Criteria:
1. Pregled radnih naloga po periodu
2. Pregled radnih naloga po klijentima
3. Pregled aktivnosti po serviseru
4. Filter opcije po statusu i tipu
5. Export u PDF format

### Story 5.4: Dashboard funkcionalnost
As a korisnik,
I want to see an overview of activities,
so that I can quickly assess current situation.

#### Acceptance Criteria:
1. Administratori vide sve aktivne radne naloge
2. Serviseri vide svoje aktivne radne naloge
3. Statistike se prikazuju (ukupan broj naloga, završeni, u radu)
4. Brže akcije su dostupne (novi nalog, pretraži)
5. Responsive design za mobilne uređaje

### Story 5.5: Napomene i komentari
As a korisnik,
I want to add notes and comments,
so that I can provide additional context.

#### Acceptance Criteria:
1. Napomene se mogu dodati na nivou radnog naloga
2. Komentari se mogu dodati na nivou stavke
3. Napomene se čuvaju u istoriji
4. Napomene se prikazuju u email-u
5. Serviseri i administratori mogu dodati napomene

## Checklist Results Report

*Ovaj deo će biti popunjen nakon izvršavanja pm-checklist-a*

## Next Steps

### UX Expert Prompt
Molim vas da kreirate UI/UX specifikaciju za KDS sistem koristeći ovaj PRD kao osnovu. Fokusirajte se na mobilno-optimizovan dizajn za servisere i desktop funkcionalnost za administratore. Posebno obratite pažnju na QR kod skeniranje interfejs i workflow za kreiranje radnih naloga.

### Architect Prompt
Molim vas da kreirate fullstack arhitekturu za KDS sistem koristeći ovaj PRD kao osnovu. Koristite Flask backend, MySQL bazu podataka i Bootstrap frontend. Posebno se fokusirajte na QR kod funkcionalnost, email sistem i responsive design.