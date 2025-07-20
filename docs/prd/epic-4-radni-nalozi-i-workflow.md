# Epic 4: Radni nalozi i workflow

**Epic Goal**: Implementirati kompletan sistem za upravljanje radnim nalozima sa podrškom za tri tipa intervencija i praćenje materijala.

## Story 4.1: Kreiranje radnog naloga
As a serviser,
I want to create work orders,
so that I can document service activities.

### Acceptance Criteria:
1. Radni nalog se može kreirati sa osnovnim podacima
2. Polja: tip (servis/popravka/montaža), klijent, lokacija, serviseri, vozilo
3. Sistem generiše jedinstveni broj naloga sa prefiksom (RNS/RNP/RNM + godina-broj)
4. Datum i vreme otvaranja se automatski beleži
5. Status se postavlja na "U radu"

## Story 4.2: Dodavanje stavki u radni nalog
As a serviser,
I want to add service items to work orders,
so that I can document all performed activities.

### Acceptance Criteria:
1. Mogu se dodati stavke tipa: servis, popravka, montaža
2. Stavka se može dodati preko QR koda ili manuelno
3. Uređaj se može dodati iz baze ili kreirati novi
4. Svaka stavka ima napomenu
5. Materijali se mogu dodati za popravke i montaže

## Story 4.3: Upravljanje materijalima u radnom nalogu
As a serviser,
I want to track materials used in work orders,
so that I can document resource consumption.

### Acceptance Criteria:
1. Materijal se može dodati sa poljima: naziv, jedinica mere, količina, serijski broj
2. Automatski se generiše stavka "radni sat"
3. Materijali se prikazuju u tabeli sa opcijom brisanja
4. Ukupni troškovi se kalkulišu (opciono za određene klijente)
5. Materijali se čuvaju u istoriji radnog naloga

## Story 4.4: Upravljanje statusima radnog naloga
As a serviser,
I want to update work order status,
so that I can track progress and completion.

### Acceptance Criteria:
1. Status se može menjati između: U radu, Završen, Fakturisan, Otkazan
2. Samo serviseri mogu menjati status na "Završen"
3. Samo administratori mogu menjati status na "Fakturisan"
4. Datum i vreme zatvaranja se automatski beleži
5. Email notifikacija se šalje pri promeni statusa

## Story 4.5: Pregled i editovanje radnih naloga
As a korisnik,
I want to view and edit work orders,
so that I can maintain accurate records.

### Acceptance Criteria:
1. Lista radnih naloga je dostupna sa filter opcijama
2. Administratori vide sve radne naloge
3. Serviseri vide samo svoje radne naloge
4. Radni nalog se može editovati sa određenim ograničenjima
5. Istorija izmena se čuva
