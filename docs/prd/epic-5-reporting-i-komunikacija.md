# Epic 5: Reporting i komunikacija

**Epic Goal**: Implementirati email funkcionalnost za slanje radnih naloga i osnovne izvještaje za praćenje aktivnosti.

## Story 5.1: Email funkcionalnost
As a serviser,
I want to send work orders to clients via email,
so that they have official documentation.

### Acceptance Criteria:
1. Email template je kreiran za radne naloge
2. Radni nalog se generiše u PDF formatu
3. Email se šalje klijentima sa radnim nalogom u prilogu
4. CC se šalje administratorima i serviseru
5. Email status se prati (poslato/neuspešno)

## Story 5.2: Generisanje radnih naloga
As a serviser,
I want to generate formatted work orders,
so that I can provide professional documentation.

### Acceptance Criteria:
1. Radni nalog o servisiranju (RNS) se generiše sa svim podacima
2. Radni nalog o popravci (RNP) se generiše sa materijalima
3. Radni nalog o montaži (RNM) se generiše sa materijalima
4. Profesionalni format sa company branding
5. Potpisi sekcija je uključena

## Story 5.3: Osnovni reporti
As an administrator,
I want to generate reports,
so that I can monitor business activities.

### Acceptance Criteria:
1. Pregled radnih naloga po periodu
2. Pregled radnih naloga po klijentima
3. Pregled aktivnosti po serviseru
4. Filter opcije po statusu i tipu
5. Export u PDF format

## Story 5.4: Dashboard funkcionalnost
As a korisnik,
I want to see an overview of activities,
so that I can quickly assess current situation.

### Acceptance Criteria:
1. Administratori vide sve aktivne radne naloge
2. Serviseri vide svoje aktivne radne naloge
3. Statistike se prikazuju (ukupan broj naloga, završeni, u radu)
4. Brže akcije su dostupne (novi nalog, pretraži)
5. Responsive design za mobilne uređaje

## Story 5.5: Napomene i komentari
As a korisnik,
I want to add notes and comments,
so that I can provide additional context.

### Acceptance Criteria:
1. Napomene se mogu dodati na nivou radnog naloga
2. Komentari se mogu dodati na nivou stavke
3. Napomene se čuvaju u istoriji
4. Napomene se prikazuju u email-u
5. Serviseri i administratori mogu dodati napomene
