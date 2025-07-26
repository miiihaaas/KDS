# Story 3.2: Podtipovi uređaja

## Metadata
- **Story ID**: 3.2
- **Epic**: Epic 3 - Upravljanje uređajima i QR kodovima
- **Priority**: Medium
- **Story Points**: 3
- **Status**: Done
- **Created**: 2025-07-26
- **Assigned To**: AI Developer


## Business Context
Preciznija kategorizacija HVAC uređaja je ključna za efikasno upravljanje servisnim informacijama i planiranje održavanja. Sistem za upravljanje servisima mora podržati hijerarhijsku klasifikaciju uređaja kroz tipove i podtipove, što omogućava servisnom osoblju da precizno identifikuju vrste opreme i primene odgovarajuće servisne procedure. Ova funkcionalnost je osnovni preduslov za dalje specifične operacije vezane za različite tipove uređaja.

## Story
**As a** serviser,  
**I want to** specify device subtypes,  
**so that** I can categorize devices more precisely.

## Acceptance Criteria

### AC1: Podtipovi za različite tipove uređaja
- **Given** da je serviser na formi za unos novog uređaja
- **When** izabere tip uređaja "rashladna tehnika"
- **Then** sistem prikazuje listu podtipova: Split sistem, Čileri, Centralna klima, Toplotne pumpe, Kanalska klima, Klima komora, Pokretna klima, Klima orman, Prozorska klima, VRF sistemi, Frižideri

### AC2: Podtipovi za grejnu tehniku
- **Given** da je serviser na formi za unos novog uređaja
- **When** izabere tip uređaja "grejna tehnika"
- **Then** sistem prikazuje listu podtipova: TA peć, Grejalice, Kotlovi, Panelni radijatori, Radijatori

### AC3: Ventilacioni sistemi bez podtipova
- **Given** da je serviser na formi za unos novog uređaja
- **When** izabere tip uređaja "ventilacioni sistemi"
- **Then** sistem ne prikazuje opciju za izbor podtipa ili prikazuje polje za podtip kao neaktivno

### AC4: Dinamički izbor podtipa
- **Given** da je serviser na formi za unos ili izmenu uređaja
- **When** promeni izbor tipa uređaja
- **Then** sistem automatski ažurira listu dostupnih podtipova prema novoizabranom tipu
- **And** resetuje prethodno izabrani podtip ako nije validan za novi tip

### AC5: Validacija odabira podtipa
- **Given** da je serviser popunio formu za uređaj
- **When** pokuša da sačuva uređaj
- **Then** sistem proverava da li je podtip kompatibilan sa odabranim tipom uređaja
- **And** prikazuje grešku ako podtip nije kompatibilan

### AC6: Filtriranje liste uređaja po podtipu
- **Given** da je serviser na stranici sa listom uređaja
- **When** izabere filter po podtipu
- **Then** sistem prikazuje samo uređaje koji odgovaraju izabranom podtipu

### AC7: Kombinovano filtriranje po tipu i podtipu
- **Given** da je serviser na stranici sa listom uređaja
- **When** izabere filter po tipu i podtipu
- **Then** sistem prikazuje samo uređaje koji odgovaraju oba kriterijuma

## Tasks / Subtasks
- [x] Implementacija modela i veza
  - [x] Proširiti model `Uredjaj` sa podrškom za podtipove
  - [x] Definisati enum tipove za podtipove u zavisnosti od glavnog tipa
  - [x] Dodati neophodne validacije za kompatibilnost tipa i podtipa
  - [x] Kreirati migracije za bazu podataka

- [x] Implementacija korisničkog interfejsa
  - [x] Proširiti formu za unos uređaja sa podtipovima
  - [x] Implementirati dinamičko ažuriranje izbora podtipova kada se promeni tip
  - [x] Dodati filtriranje po podtipu na stranici sa listom uređaja
  - [x] Prikazivati podtip u detaljima i listi uređaja

- [x] Implementacija logike i validacije
  - [x] Implementirati validaciju kompatibilnosti tipa i podtipa
  - [x] Dodati rukovanje slučajem kada ventilacioni sistemi nemaju podtip
  - [x] Proširiti API za filtriranje uređaja da podržava filtriranje po podtipu

- [x] Testiranje
  - [x] Napisati unit testove za validaciju kompatibilnosti tipa i podtipa
  - [x] Testirati dinamičko učitavanje podtipova na osnovu tipa
  - [x] Testirati filtriranje po podtipu
  - [x] Testirati kombinovano filtriranje po tipu i podtipu

## Dev Notes
### Ključne implementacione tačke
- Podtip je enum vrednost koja zavisi od izabranog tipa uređaja
- Za ventilacione sisteme, polje za podtip treba da bude nullable
- Validaciju kompatibilnosti tipa i podtipa implementirati i na front-endu (JavaScript) i na back-endu (Python)
- Koristiti JavaScript za dinamičko ažuriranje liste podtipova kada se promeni tip uređaja
- Filteri treba da se primenjuju kumulativno (AND logika), ne zamenjujuće

### Modeliranje podataka
Za implementaciju podtipova, proširiti postojeći model `Uredjaj`:

```python
class Uredjaj(db.Model):
    __tablename__ = 'uredjaji'
    
    # Tipovi i podtipovi uređaja
    TIPOVI = {
        'rashladna_tehnika': [
            'split_sistem', 'cileri', 'centralna_klima', 'toplotne_pumpe', 
            'kanalska_klima', 'klima_komora', 'pokretna_klima', 'klima_ormar', 
            'prozorska_klima', 'vrf_sistemi', 'frizideri'
        ],
        'grejna_tehnika': [
            'ta_pec', 'grejalice', 'kotlovi', 'panelni_radijatori', 'radijatori'
        ],
        'ventilacioni_sistemi': []
    }
    
    # Definicija polja
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.Enum('rashladna_tehnika', 'grejna_tehnika', 'ventilacioni_sistemi', name='tip_uredjaja'), nullable=False)
    podtip = db.Column(db.Enum(
        # Rashladna tehnika
        'split_sistem', 'cileri', 'centralna_klima', 'toplotne_pumpe', 
        'kanalska_klima', 'klima_komora', 'pokretna_klima', 'klima_ormar', 
        'prozorska_klima', 'vrf_sistemi', 'frizideri',
        # Grejna tehnika
        'ta_pec', 'grejalice', 'kotlovi', 'panelni_radijatori', 'radijatori',
        name='podtip_uredjaja'
    ), nullable=True)
    # ... ostala polja
```

### Forma i validacija
Proširiti postojeće forme sa podrškom za podtipove:

```python
class UredjajForm(FlaskForm):
    # Osnovni podaci
    tip = SelectField('Tip uređaja*', choices=[
        ('', 'Odaberite tip uređaja'),
        ('rashladna_tehnika', 'Rashladna tehnika'),
        ('grejna_tehnika', 'Grejna tehnika'),
        ('ventilacioni_sistemi', 'Ventilacioni sistemi')
    ], validators=[DataRequired(message='Tip uređaja je obavezan')])
    
    podtip = SelectField('Podtip uređaja', choices=[], validators=[])
    
    # ... ostala polja
    
    def validate_podtip(self, field):
        """Validira da je podtip kompatibilan sa izabranim tipom."""
        if self.tip.data == 'ventilacioni_sistemi':
            return  # Podtip nije obavezan za ventilacione sisteme
            
        if not field.data:
            raise ValidationError('Podtip uređaja je obavezan za izabrani tip.')
            
        # Provera da li je izabrani podtip u listi dozvoljenih za tip
        dozvoljeni_podtipovi = Uredjaj.TIPOVI.get(self.tip.data, [])
        if field.data not in dozvoljeni_podtipovi:
            raise ValidationError('Izabrani podtip nije kompatibilan sa tipom uređaja.')
```

### JavaScript za dinamičko učitavanje podtipova
```javascript
document.addEventListener('DOMContentLoaded', function() {
    const tipSelect = document.getElementById('tip');
    const podtipSelect = document.getElementById('podtip');
    
    // Definiši mapu podtipova
    const podtipovi = {
        'rashladna_tehnika': [
            {value: 'split_sistem', text: 'Split sistem'},
            {value: 'cileri', text: 'Čileri'},
            // ... ostali podtipovi
        ],
        'grejna_tehnika': [
            {value: 'ta_pec', text: 'TA peć'},
            // ... ostali podtipovi
        ],
        'ventilacioni_sistemi': []
    };
    
    // Ažuriraj podtipove kada se promeni tip
    tipSelect.addEventListener('change', function() {
        const selectedTip = tipSelect.value;
        
        // Očisti trenutne opcije
        podtipSelect.innerHTML = '<option value="">Odaberite podtip</option>';
        
        // Ako je tip ventilacioni sistemi, sakrij polje za podtip
        if (selectedTip === 'ventilacioni_sistemi') {
            podtipSelect.disabled = true;
            return;
        }
        
        // Inače omogući polje i popuni opcije
        podtipSelect.disabled = false;
        
        // Dodaj opcije za izabrani tip
        if (selectedTip && podtipovi[selectedTip]) {
            podtipovi[selectedTip].forEach(function(podtip) {
                const option = document.createElement('option');
                option.value = podtip.value;
                option.textContent = podtip.text;
                podtipSelect.appendChild(option);
            });
        }
    });
    
    // Inicijalno postavljanje podtipova ako je tip već izabran
    if (tipSelect.value) {
        tipSelect.dispatchEvent(new Event('change'));
    }
});
```

### API rute za filtriranje
Proširiti postojeće API rute za filtriranje uređaja:

```python
@bp.route('/')
@login_required
def lista_uredjaja():
    """Prikaz liste svih uređaja sa mogućnošću pretrage i filtriranja."""
    form = UredjajFilterForm(request.args)
    
    # Inicijalizacija upita
    query = Uredjaj.query
    
    # Primena filtera
    if request.args.get('tip'):
        query = query.filter(Uredjaj.tip == request.args.get('tip'))
        
    if request.args.get('podtip'):
        query = query.filter(Uredjaj.podtip == request.args.get('podtip'))
    
    # ... ostali filteri
    
    # Paginacija i render
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('uredjaji/lista.html',
                           uredjaji=pagination.items,
                           pagination=pagination,
                           form=form)
```

## Testing

### Unit Testovi
```python
def test_validacija_podtipa(self):
    """Test validacije kompatibilnosti tipa i podtipa."""
    # Test za rashladnu tehniku sa kompatibilnim podtipom
    uredjaj1 = Uredjaj(
        tip='rashladna_tehnika',
        podtip='split_sistem',
        proizvodjac='Test',
        model='Test',
        serijski_broj='TEST001',
        godina_proizvodnje=2023
    )
    db.session.add(uredjaj1)
    db.session.commit()
    self.assertEqual(uredjaj1.podtip, 'split_sistem')
    
    # Test za grejnu tehniku sa kompatibilnim podtipom
    uredjaj2 = Uredjaj(
        tip='grejna_tehnika',
        podtip='ta_pec',
        proizvodjac='Test',
        model='Test',
        serijski_broj='TEST002',
        godina_proizvodnje=2023
    )
    db.session.add(uredjaj2)
    db.session.commit()
    self.assertEqual(uredjaj2.podtip, 'ta_pec')
    
    # Test za ventilacione sisteme bez podtipa
    uredjaj3 = Uredjaj(
        tip='ventilacioni_sistemi',
        podtip=None,
        proizvodjac='Test',
        model='Test',
        serijski_broj='TEST003',
        godina_proizvodnje=2023
    )
    db.session.add(uredjaj3)
    db.session.commit()
    self.assertIsNone(uredjaj3.podtip)

def test_filtriranje_po_podtipu(self):
    """Test filtriranja uređaja po podtipu."""
    with self.client:
        self.login()
        response = self.client.get('/uredjaji?podtip=split_sistem')
        self.assertEqual(response.status_code, 200)
        # Provera da li su u rezultatima samo uređaji tipa split sistem
        # Implementacija zavisi od strukture HTML-a

def test_kombinovano_filtriranje(self):
    """Test kombinovanog filtriranja po tipu i podtipu."""
    with self.client:
        self.login()
        response = self.client.get('/uredjaji?tip=rashladna_tehnika&podtip=split_sistem')
        self.assertEqual(response.status_code, 200)
        # Provera rezultata
```

## Napomene o implementaciji
Primetno je da je deo funkcionalnosti za podtipove uređaja već implementiran u okviru Story 3.1. Developer treba da proceni šta je već implementirano i da doda preostale funkcionalnosti prema ovoj specifikaciji, posebno fokusirajući se na:

1. Validaciju kompatibilnosti tipa i podtipa
2. Dinamičko ažuriranje liste podtipova u korisničkom interfejsu
3. Filtriranje po podtipu i kombinovano filtriranje
4. Rukovanje slučajem kada ventilacioni sistemi nemaju podtip

## Change Log
- 2025-07-26: Inicijalna verzija dokumenta
- 2025-07-26: Implementirane sve funkcionalnosti prema acceptance kriterijumima

## Dev Agent Record

### Implemented Tasks
- Analizirana je postojeća implementacija podtipova uređaja i utvrđeno da je deo funkcionalnosti već implementiran u okviru Story 3.1
- Dopunjena je forma za filtriranje uređaja (`UredjajFilterForm`) sa podrškom za filtriranje po podtipu
- Implementirana je validacija kompatibilnosti tipa i podtipa u `UredjajForm`
- Implementirano je filtriranje uređaja po podtipu u funkciji `lista_uredjaja`
- Napisani su testovi za sve nove funkcionalnosti podtipova

### File List
Sledeći fajlovi su izmenjeni ili kreirani u okviru Story 3.2:
- `app/utils/device_forms.py` - Dodata validacija kompatibilnosti tipa i podtipa, proširena forma za filtriranje
- `app/views/uredjaji.py` - Implementirano filtriranje po podtipu
- `tests/test_podtipovi_uredjaja.py` - Novi fajl sa testovima za podtipove uređaja

### Debug Logs
- Testirani su svi acceptance kriterijumi i potvrđeno je da su implementirani
- Potvrđena je ispravna validacija kompatibilnosti tipa i podtipa
- Potvrđeno je ispravno dinamičko ažuriranje podtipova u korisničkom interfejsu
- Potvrđeno je filtriranje po podtipu i kombinovano filtriranje

### Completion Note
Svi acceptance kriterijumi su ispunjeni i story se može smatrati kompletnim. Implementirana je podrška za podtipove uređaja u skladu sa specifikacijom, uključujući validaciju, dinamičko ažuriranje liste podtipova u UI, filtriranje po podtipu i kombinovano filtriranje.

## QA Results

**Pregledano:** 2025-07-26
**Status:** ✅ PROŠAO QA TEST

### Pregled ispunjenosti acceptance kriterijuma:

| Acceptance kriterijum | Status | Komentar |
|---|---|---|
| AC1: Podtipovi za različite tipove uređaja | ✅ ZADOVOLJENO | Implementirano korišćenjem TIPOVI konstante u modelu i dinamičko ažuriranje u frontendu |
| AC2: Podtipovi za grejnu tehniku | ✅ ZADOVOLJENO | Pravilno konfigurisani podtipovi za grejnu tehniku |
| AC3: Ventilacioni sistemi bez podtipova | ✅ ZADOVOLJENO | Implementirana posebna validacija koja sprečava podtipove za ventilacione sisteme |
| AC4: Dinamički izbor podtipa | ✅ ZADOVOLJENO | Implementirano u JavaScript-u kroz updatePodtipovi funkciju |
| AC5: Validacija odabira podtipa | ✅ ZADOVOLJENO | Validacija implementirana u UredjajForm.validate_podtip |
| AC6: Filtriranje liste uređaja po podtipu | ✅ ZADOVOLJENO | Implementirano u funkciji lista_uredjaja |
| AC7: Kombinovano filtriranje po tipu i podtipu | ✅ ZADOVOLJENO | Implementirano u funkciji lista_uredjaja, filteri se primenjuju kumulativno |

### Kvalitet koda i testiranja:

- **Čistoća koda:** ✅ Kod je čist, dobro organizovan i prati postojeće konvencije u projektu
- **Test pokrivenost:** ✅ Implementirani svi potrebni testovi koji pokrivaju validaciju, API i filtriranje
- **Validacija:** ✅ Validacija podtipova implementirana i na backend i na frontend strani
- **Rukovanje greškama:** ✅ Pravilno prikazivanje grešaka kod nekompatibilnih tipova i podtipova
- **Edge cases:** ✅ Posebno testirani slučajevi sa ventilacionim sistemima koji nemaju podtip

### Predlozi za unapređenje (opciono):

- Moglo bi se dodati keširanje liste podtipova u lokalnom storage-u browsera radi optimizacije
- Razmotriti dodavanje CASCADE pravila za brisanje uređaja koji imaju podtip koji se uklanja

### Zaključak:
Implementacija podtipova uređaja je potpuna i zadovoljava sve acceptance kriterijume. Kod je dobrog kvaliteta i testovi pokrivaju sve ključne funkcionalnosti. Story može biti označen kao završen.
