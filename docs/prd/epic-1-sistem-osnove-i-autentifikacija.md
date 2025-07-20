# Epic 1: Sistem osnove i autentifikacija

**Epic Goal**: Uspostaviti osnovnu web aplikaciju sa sigurnim pristupom i administrativnim upravljanjem korisnicima, vozilima i potrošnim materijalima.

## Story 1.1: Kreiranje osnovne Flask aplikacije
As a developer,
I want to set up the basic Flask application structure,
so that the foundation for the KDS system is established.

### Acceptance Criteria:
1. Flask aplikacija je kreirana sa osnovnom strukturom foldera
2. MySQL konekcija je konfigurisana i testirana
3. Bootstrap je integrisan za responsive design
4. Osnovni routing je implementiran
5. Development server se pokреće bez grešaka

## Story 1.2: Implementacija autentifikacije
As a korisnik sistema,
I want to log in with my credentials,
so that I can access the system securely.

### Acceptance Criteria:
1. Login forma je kreirana sa username/password poljima
2. Session management je implementiran
3. Password hashing je sigurno implementiran
4. "Reset password" funkcionalnost je dostupna
5. Logout funkcionalnost je implementirana
6. Role-based pristup (administrator/serviser) je implementiran

## Story 1.3: Upravljanje korisnicima
As an administrator,
I want to create and manage user accounts,
so that I can control access to the system.

### Acceptance Criteria:
1. Administrator može kreirati nove korisničke naloge
2. Korisnik ima polja: ime, prezime, email, password, tip (admin/serviser)
3. Administrator može editovati postojeće naloge
4. Administrator može deaktivirati naloge
5. Lista korisnika je dostupna sa pretrаgom

## Story 1.4: Upravljanje vozilima
As an administrator,
I want to manage company vehicles,
so that I can assign them to work orders.

### Acceptance Criteria:
1. Administrator može dodati novo vozilo
2. Vozilo ima polja: marka, model, registracija
3. Administrator može editovati podatke o vozilu
4. Lista vozila je dostupna sa pretrаgom
5. Vozilo se može dodeliti radnom nalogu

## Story 1.5: Upravljanje potrošnim materijalima
As an administrator,
I want to manage consumable materials,
so that they can be tracked in work orders.

### Acceptance Criteria:
1. Administrator može dodati novi materijal
2. Materijal ima polja: naziv, jedinica mere
3. Administrator može editovati podatke o materijalu
4. Lista materijala je dostupna sa pretrаgom
5. Materijal se može dodati u radni nalog
