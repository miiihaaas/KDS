# Project Brief: KDS Sistem za Upravljanje Servisima HVAC Uređaja

## Executive Summary

KDS (Sistem radnih naloga) je web aplikacija dizajnirana za digitalizaciju i automatizaciju procesa servisiranja, popravke i montaže HVAC uređaja. Sistem omogućava efikasno upravljanje klijentima, uređajima, radnim nalozima i potrošnim materijalima kroz intuitivni interfejs optimizovan za mobilne uređaje (serviseri) i desktop (administratori).

Primarni problem koji rešava je eliminacija papirnog dokumentovanja, poboljšanje praćenja istorije servisa i automatizacija generisanja radnih naloga sa QR kod integracijom za brže identifikovanje uređaja.

## Problem Statement

### Trenutno stanje i problemi:
- **Papirno dokumentovanje**: Ručno vođenje evidencije radnih naloga i servisa
- **Neorganizovano praćenje**: Težko praćenje istorije servisa po uređajima
- **Inefficient komunikacija**: Sporiji proces slanja radnih naloga klijentima
- **Gubljenje podataka**: Rizik od gubitka papirnih dokumenata
- **Neoptimalan workflow**: Dupliciranje unosa podataka i greške

### Uticaj problema:
- Povećano vreme administracije
- Mogućnost grešaka u evidenciji
- Kašnjenje u komunikaciji sa klijentima
- Otežano planiranje preventivnih servisa

### Razlog za hitno rešavanje:
Digitalizacija je postala neophodna za konkurentnost u sektoru servisiranja HVAC uređaja, a postojeći papirni procesi usporavaju rast i skalabilnost biznisa.

## Proposed Solution

### Ključni pristup:
Web aplikacija sa role-based pristupom (administrator/serviser) koja omogućava:
- **Centralizovano upravljanje**: Jedinstvena baza podataka za sve klijente i uređaje
- **Mobilno-optimizovano**: Prilagođeno za rad servisera u terenu
- **QR kod integracija**: Brza identifikacija uređaja skeniranjem
- **Automatsko generisanje**: Radni nalozi i reporti se automatski kreiraju
- **Email notifikacije**: Direktno slanje radnih naloga klijentima

### Ključne prednosti:
- Eliminacija papirnog dokumentovanja
- Brža identifikacija uređaja preko QR kodova
- Automatsko praćenje istorije servisa
- Efikasnija komunikacija sa klijentima
- Mogućnost planiranja preventivnih servisa

## Target Users

### Primary User Segment: Serviseri
- **Profil**: Tehničko osoblje koje izvršava servise u terenu
- **Trenutno ponašanje**: Koriste papirne radne naloge i ručno unose podatke
- **Potrebe**: Brz pristup informacijama o uređajima, jednostavan unos podataka
- **Ciljevi**: Efikasno završavanje servisa sa minimalnim administriranjem
- **Uređaji**: Primarno mobilni telefoni i tableti

### Secondary User Segment: Administratori
- **Profil**: Upravljanje kompanijom i nadgledanje servisa
- **Trenutno ponašanje**: Koordinacija servisa i komunikacija sa klijentima
- **Potrebe**: Potpun pregled nad operacijama, upravljanje korisnicima i resursima
- **Ciljevi**: Optimizacija procesa i poboljšanje zadovoljstva klijenata
- **Uređaji**: Primarno desktop računari

## Goals & Success Metrics

### Business Objectives:
- **Povećanje efikasnosti**: Smanjenje vremena administracije za 50%
- **Poboljšanje accuracy**: Eliminacija grešaka u dokumentaciji
- **Brža komunikacija**: Instant slanje radnih naloga klijentima
- **Skalabilnost**: Mogućnost rasta broja klijenata i servisera

### User Success Metrics:
- **Vreme kreiranja radnog naloga**: Manje od 5 minuta po uređaju
- **Accuracy podataka**: 99% tačnost u evidenciji servisa
- **Zadovoljstvo korisnika**: 4.5/5 ocena zadovoljstva
- **Adoption rate**: 90% korišćenja sistema u prve 3 meseca

### Key Performance Indicators (KPIs):
- **Produktivnost servisera**: Broj servisa po danu
- **Vreme odziva**: Vreme od zahteva do izvršenog servisa
- **Kvalitet servisa**: Broj ponovnih intervencija
- **Zadovoljstvo klijenata**: Feedback scorevi

## MVP Scope

### Core Features (Must Have):
- **Autentifikacija**: Login sistem sa reset lozinke
- **Upravljanje korisnicima**: Kreiranje i editovanje naloga (admin/serviser)
- **Upravljanje klijentima**: Dodavanje pravnih i fizičkih lica sa hijerarhijom lokacija
- **Upravljanje uređajima**: Registracija HVAC uređaja sa QR kodovima
- **Radni nalozi**: Kreiranje, editovanje i praćenje radnih naloga
- **QR kod funkcionalnost**: Generisanje, štampanje i skeniranje QR kodova
- **Email sistem**: Slanje radnih naloga klijentima
- **Osnovni reporti**: Pregled radnih naloga po periodu i klijentima

### Out of Scope for MVP:
- Napredni reporting i analytics
- Integracija sa računovodstvenim sistemima
- Mobilna aplikacija (native)
- Digitalni potpisi
- Automatski podsetnici za servise
- Fakturisanje i praćenje plaćanja

### MVP Success Criteria:
Sistem omogućava kompletno digitalno dokumentovanje servisa sa QR kod integracijom i automatskim generisanjem radnih naloga.

## Post-MVP Vision

### Phase 2 Features:
- **Napredni reporting**: Detaljni analytics i dashboards
- **Automatski podsetnici**: Email notifikacije za redovne servise
- **Mobilna aplikacija**: Native iOS/Android aplikacije
- **Digitalni potpisi**: Potpisivanje na tablet uređajima

### Long-term Vision:
KDS sistem postaje centralna platforma za upravljanje servisnim operacijama sa mogućnostima prediktivnog održavanja i integracije sa IoT uređajima.

### Expansion Opportunities:
- Integracija sa računovodstvenim sistemima
- CRM funkcionalnosti
- Inventory management
- Workforce management

## Technical Considerations

### Platform Requirements:
- **Target Platforms**: Web aplikacija (responsive design)
- **Browser Support**: Chrome, Firefox, Safari, Edge (poslednje 2 verzije)
- **Performance**: Brz odziv na mobilnim uređajima

### Technology Preferences:
- **Frontend**: HTML, CSS, Bootstrap (responsive design)
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Hosting**: Cloud hosting sa mogućnošću skaliranja

### Architecture Considerations:
- **Repository Structure**: Monorepo struktura
- **Service Architecture**: Monolitna aplikacija za MVP
- **Integration Requirements**: Email sistem, QR kod generisanje/skeniranje
- **Security/Compliance**: Sigurno čuvanje podataka klijenata

## Constraints & Assumptions

### Constraints:
- **Budget**: Srednji budžet za MVP razvoj
- **Timeline**: 4-6 meseci za MVP implementaciju
- **Resources**: Mala razvojna ekipa
- **Technical**: Korišćenje specifičnih tehnologija (Flask, MySQL, Bootstrap)

### Key Assumptions:
- Serviseri imaju pristup mobilnim uređajima sa kamerama
- Klijenti imaju email adrese za prijem radnih naloga
- Postojeći procesi mogu biti digitalizovani bez velikih izmena
- Portabilni štampači mogu da se integrišu za QR kodove

## Risks & Open Questions

### Key Risks:
- **User adoption**: Otpor prema promeni od papirnih procesa
- **Technical complexity**: QR kod integracija sa različitim uređajima
- **Data migration**: Prebacivanje postojećih podataka u novi sistem

### Open Questions:
- Kako rešiti offline funkcionalnost za servisere?
- Kakav je optimalni workflow za digitalne potpise?
- Kako integrisati sa postojećim štampačima?

### Areas Needing Further Research:
- Analiza konkurentskih rešenja
- Testiranje QR kod tehnologija
- Analiza mobilnih uređaja servisera

## Next Steps

### Immediate Actions:
1. Kreiranje detaljnog PRD-a na osnovu ovog brief-a
2. Tehničko istraživanje QR kod implementacije
3. UX/UI dizajn za mobilne i desktop interfejse
4. Arhitekturno planiranje sistema

### PM Handoff:
Ovaj Project Brief pruža kompletnu osnovu za KDS sistem. Molim vas da prođete u 'PRD Generation Mode', proverite brief temeljno i radite sa korisnikom na kreiranju PRD-a sekciju po sekciju kako template označava, tražeći sva potrebna pojašnjenja ili predlažući poboljšanja.