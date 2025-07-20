# Epic 3: Upravljanje uređajima i QR kodovima

**Epic Goal**: Implementirati sistem za registraciju HVAC uređaja sa QR kod funkcionalností za brzu identifikaciju i pristup podacima.

## Story 3.1: Registracija uređaja
As a serviser,
I want to register HVAC devices,
so that I can track their service history.

### Acceptance Criteria:
1. Sistem podržava tri tipa uređaja: rashladna tehnika, grejna tehnika, ventilacioni sistemi
2. Uređaj ima polja: proizvođač, model, serijski broj, inventarski broj, godina proizvodnje, tip
3. Sistem generiše jedinstveni ID za svaki uređaj
4. Uređaj se može dodati u bilo koju prostoriju
5. Lista uređaja je dostupna sa pretrаgom

## Story 3.2: Podtipovi uređaja
As a serviser,
I want to specify device subtypes,
so that I can categorize devices more precisely.

### Acceptance Criteria:
1. Rashladna tehnika ima podtipove: Split sistem, Čileri, Centralna klima, Toplotne pumpe, Kanalska klima, Klima komora, Pokretna klima, Klima orman, Prozorska klima, VRF sistemi, Frižideri
2. Grejna tehnika ima podtipove: TA peć, Grejalice, Kotlovi, Panelni radijatori, Radijatori
3. Ventilacioni sistemi nemaju podtipove
4. Podtip se bira na osnovu glavnog tipa
5. Filtriranje uređaja po tipu i podtipu je dostupno

## Story 3.3: QR kod generisanje
As a serviser,
I want to generate QR codes for devices,
so that I can quickly identify devices in the field.

### Acceptance Criteria:
1. QR kod se generiše automatski pri kreiranju uređaja
2. QR kod sadrži jedinstveni ID uređaja
3. Serviser može odabrati broj QR kodova za štampanje
4. QR kod se prikazuje u printable formatu
5. Sistem omogućava ponovo štampanje QR kodova

## Story 3.4: QR kod skeniranje
As a serviser,
I want to scan QR codes,
so that I can quickly access device information.

### Acceptance Criteria:
1. Camera interface je dostupan za skeniranje QR kodova
2. Skeniranje QR koda učitava podatke o uređaju
3. Breadcrumb navigacija pokazuje punu putanju do uređaja
4. Prethodna istorija servisa se prikazuje
5. Opcija za kreiranje novog radnog naloga je dostupna

## Story 3.5: Upravljanje postojećim uređajima
As a serviser,
I want to edit device information,
so that I can keep device records up to date.

### Acceptance Criteria:
1. Postojeći uređaji se mogu editovati
2. Istorija izmena se čuva
3. QR kod ostaje isti pri editovanju
4. Prethodna istorija servisa se zadržava
5. Uređaj se može premestiti u drugu prostoriju
