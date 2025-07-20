# Data Models

## User

**Purpose:** Autentifikacija i autorizacija korisnika sistema

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- ime: String(100) - Ime korisnika
- prezime: String(100) - Prezime korisnika
- email: String(255) - Email adresa (unique)
- password_hash: String(255) - Hashovan password
- tip: Enum('administrator', 'serviser') - Tip korisnika
- aktivan: Boolean - Status naloga
- created_at: DateTime - Datum kreiranja
- updated_at: DateTime - Datum poslednje izmene

### TypeScript Interface
```typescript
interface User {
  id: number;
  ime: string;
  prezime: string;
  email: string;
  tip: 'administrator' | 'serviser';
  aktivan: boolean;
  created_at: string;
  updated_at: string;
}
```

### Relationships
- One-to-Many sa WorkOrder (serviseri mogu imati više radnih naloga)

## Client

**Purpose:** Upravljanje podacima o klijentima (pravna i fizička lica)

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- naziv: String(255) - Naziv kompanije ili ime fizičkog lica
- tip: Enum('pravno_lice', 'fizicko_lice') - Tip klijenta
- adresa: String(255) - Adresa
- mesto: String(100) - Mesto
- postanski_broj: String(10) - Poštanski broj
- drzava: String(100) - Država
- telefon: String(50) - Telefonski broj
- email: String(255) - Email adresa
- pib: String(20) - PIB (za pravna lica)
- mb: String(20) - Matični broj (za pravna lica)

### TypeScript Interface
```typescript
interface Client {
  id: number;
  naziv: string;
  tip: 'pravno_lice' | 'fizicko_lice';
  adresa: string;
  mesto: string;
  postanski_broj: string;
  drzava: string;
  telefon?: string;
  email?: string;
  pib?: string;
  mb?: string;
}
```

### Relationships
- One-to-Many sa Location (klijent može imati više lokacija)

## Location

**Purpose:** Lokacije klijenata (radne jedinice za pravna lica, lokacije kuća za fizička lica)

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- client_id: Integer (Foreign Key) - Referenca na klijenta
- naziv: String(255) - Naziv lokacije
- adresa: String(255) - Adresa lokacije
- mesto: String(100) - Mesto
- postanski_broj: String(10) - Poštanski broj
- drzava: String(100) - Država
- kontakt_osoba: String(255) - Kontakt osoba (za pravna lica)
- telefon: String(50) - Telefonski broj
- email: String(255) - Email adresa

### TypeScript Interface
```typescript
interface Location {
  id: number;
  client_id: number;
  naziv: string;
  adresa: string;
  mesto: string;
  postanski_broj: string;
  drzava: string;
  kontakt_osoba?: string;
  telefon?: string;
  email?: string;
}
```

### Relationships
- Many-to-One sa Client
- One-to-Many sa Object

## Object

**Purpose:** Objekti unutar lokacija

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- location_id: Integer (Foreign Key) - Referenca na lokaciju
- naziv: String(255) - Naziv objekta

### TypeScript Interface
```typescript
interface Object {
  id: number;
  location_id: number;
  naziv: string;
}
```

### Relationships
- Many-to-One sa Location
- One-to-Many sa Room

## Room

**Purpose:** Prostorije unutar objekata

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- object_id: Integer (Foreign Key) - Referenca na objekat
- naziv: String(255) - Naziv prostorije (opciono)
- numerica_oznaka: String(50) - Numerička oznaka (opciono)

### TypeScript Interface
```typescript
interface Room {
  id: number;
  object_id: number;
  naziv?: string;
  numerica_oznaka?: string;
}
```

### Relationships
- Many-to-One sa Object
- One-to-Many sa Device

## Device

**Purpose:** HVAC uređaji u prostórijama

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- room_id: Integer (Foreign Key) - Referenca na prostoriju
- proizvodjac: String(255) - Proizvođač
- model: String(255) - Model uređaja
- serijski_broj: String(255) - Serijski broj (opciono)
- inventarski_broj: String(255) - Inventarski broj kod klijenta (opciono)
- godina_proizvodnje: Integer - Godina proizvodnje (opciono)
- tip: Enum('rashladna_tehnika', 'grejna_tehnika', 'ventilacioni_sistemi') - Tip uređaja
- podtip: String(100) - Podtip uređaja
- jedinstveni_id: String(50) - Jedinstveni ID za QR kod (auto-generated)
- garantni_rok_meseci: Integer - Garantni rok u mesecima

### TypeScript Interface
```typescript
interface Device {
  id: number;
  room_id: number;
  proizvodjac: string;
  model: string;
  serijski_broj?: string;
  inventarski_broj?: string;
  godina_proizvodnje?: number;
  tip: 'rashladna_tehnika' | 'grejna_tehnika' | 'ventilacioni_sistemi';
  podtip: string;
  jedinstveni_id: string;
  garantni_rok_meseci?: number;
}
```

### Relationships
- Many-to-One sa Room
- One-to-Many sa WorkOrderItem

## WorkOrder

**Purpose:** Radni nalozi za servise, popravke i montaže

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- broj_naloga: String(50) - Auto-generated broj (RNS/RNP/RNM-YYYY-NNN)
- client_id: Integer (Foreign Key) - Referenca na klijenta
- location_id: Integer (Foreign Key) - Referenca na lokaciju
- status: Enum('u_radu', 'zavrsen', 'fakturisan', 'otkazan') - Status naloga
- datum_otvaranja: DateTime - Datum i vreme otvaranja
- datum_zatvaranja: DateTime - Datum i vreme zatvaranja (opciono)
- broj_naloga_narucioca: String(100) - Broj naloga naručioca (opciono)
- porudzbenica: String(255) - Porudžbenica (opciono)
- napomena_servisa: Text - Opšta napomena za servis
- ukupan_broj_norma_sati: Integer - Ukupan broj norma sati (opciono)

### TypeScript Interface
```typescript
interface WorkOrder {
  id: number;
  broj_naloga: string;
  client_id: number;
  location_id: number;
  status: 'u_radu' | 'zavrsen' | 'fakturisan' | 'otkazan';
  datum_otvaranja: string;
  datum_zatvaranja?: string;
  broj_naloga_narucioca?: string;
  porudzbenica?: string;
  napomena_servisa?: string;
  ukupan_broj_norma_sati?: number;
}
```

### Relationships
- Many-to-One sa Client
- Many-to-One sa Location
- Many-to-Many sa User (serviseri)
- One-to-Many sa WorkOrderItem

## WorkOrderItem

**Purpose:** Stavke radnog naloga (servisi, popravke, montaže)

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- work_order_id: Integer (Foreign Key) - Referenca na radni nalog
- device_id: Integer (Foreign Key) - Referenca na uređaj
- tip: Enum('servis', 'popravka', 'montaza') - Tip stavke
- vrsta_servisa: String(100) - Vrsta servisa (za servis stavke)
- napomena: Text - Napomena za stavku
- datum_izvrsavanja: DateTime - Datum izvršavanja

### TypeScript Interface
```typescript
interface WorkOrderItem {
  id: number;
  work_order_id: number;
  device_id: number;
  tip: 'servis' | 'popravka' | 'montaza';
  vrsta_servisa?: string;
  napomena?: string;
  datum_izvrsavanja: string;
}
```

### Relationships
- Many-to-One sa WorkOrder
- Many-to-One sa Device
- One-to-Many sa MaterialUsage

## Material

**Purpose:** Potrošni materijali

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- naziv: String(255) - Naziv materijala
- jedinica_mere: String(50) - Jedinica mere

### TypeScript Interface
```typescript
interface Material {
  id: number;
  naziv: string;
  jedinica_mere: string;
}
```

### Relationships
- One-to-Many sa MaterialUsage

## MaterialUsage

**Purpose:** Korišćenje materijala u radnim nalozima

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- work_order_item_id: Integer (Foreign Key) - Referenca na stavku radnog naloga
- material_id: Integer (Foreign Key) - Referenca na materijal
- kolicina: Decimal(10,2) - Količina
- serijski_broj: String(255) - Serijski broj (opciono)
- ostali_podaci: Text - Ostali podaci (opciono)

### TypeScript Interface
```typescript
interface MaterialUsage {
  id: number;
  work_order_item_id: number;
  material_id: number;
  kolicina: number;
  serijski_broj?: string;
  ostali_podaci?: string;
}
```

### Relationships
- Many-to-One sa WorkOrderItem
- Many-to-One sa Material

## Vehicle

**Purpose:** Službena vozila

**Key Attributes:**
- id: Integer (Primary Key) - Jedinstveni identifikator
- marka: String(100) - Marka vozila
- model: String(100) - Model vozila
- registracija: String(50) - Registracija vozila

### TypeScript Interface
```typescript
interface Vehicle {
  id: number;
  marka: string;
  model: string;
  registracija: string;
}
```

### Relationships
- Many-to-Many sa WorkOrder
