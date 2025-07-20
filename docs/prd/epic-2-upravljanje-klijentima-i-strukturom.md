# Epic 2: Upravljanje klijentima i strukturom

**Epic Goal**: Implementirati kompletan sistem za upravljanje klijentima sa hierarchijskim strukturama koje podržavaju i pravna i fizička lica.

## Story 2.1: Kreiranje osnove za klijente
As a serviser,
I want to create and manage clients,
so that I can organize work orders by client structure.

### Acceptance Criteria:
1. Sistem podržava dva tipa klijenata: pravno lice i fizičko lice
2. Osnovna forma za kreiranje klijenta je dostupna
3. Lista klijenata je dostupna sa pretrаgom
4. Klijent se može editovati
5. Breadcrumb navigacija pokazuje trenutnu lokaciju u hijerarhiji

## Story 2.2: Upravljanje pravnim licima
As a serviser,
I want to create legal entities with their locations,
so that I can track services across multiple company locations.

### Acceptance Criteria:
1. Pravno lice ima polja: naziv, adresa, mesto, poštanski broj, država, telefon, email, PIB, MB
2. Automatski se kreira prva radna jedinica pri dodavanju pravnog lica
3. Radna jedinica ima polja: naziv, adresa, mesto, poštanski broj, država, kontakt osoba, telefon, email
4. Mogu se dodati dodatne radne jedinice
5. Hijerarhija Kompanija > Radna jedinica > Objekat > Prostorija je implementirana

## Story 2.3: Upravljanje fizičkim licima
As a serviser,
I want to create individual clients with their locations,
so that I can track services for residential clients.

### Acceptance Criteria:
1. Fizičko lice ima polja: ime, prezime, adresa, mesto, poštanski broj, država, telefon, email
2. Automatski se kreira prva lokacija kuće pri dodavanju fizičkog lica
3. Lokacija kuće ima polja: naziv, adresa, mesto, poštanski broj, država
4. Mogu se dodati dodatne lokacije
5. Hijerarhija Fizičko lice > Lokacija kuće > Objekat > Prostorija je implementirana

## Story 2.4: Upravljanje objektima i prostorijama
As a serviser,
I want to create objects and rooms within client locations,
so that I can precisely locate devices.

### Acceptance Criteria:
1. Objekat ima polje: naziv objekta
2. Prostorija ima polja: naziv prostorije (opciono), numerička oznaka (opciono)
3. Objekti se mogu dodati u bilo koju lokaciju
4. Prostorije se mogu dodati u bilo koji objekat
5. Navigacija kroz hijerarhiju je intuitivna
