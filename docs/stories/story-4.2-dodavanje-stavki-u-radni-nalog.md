# Story 4.2: Dodavanje stavki u radni nalog

## Metadata
- **Story ID**: 4.2
- **Epic**: Epic 4 - Radni nalozi i workflow
- **Priority**: High
- **Story Points**: 8
- **Status**: Draft
- **Created**: 2025-07-28
- **Assigned To**: AI Developer
- **Dependencies**: Story 4.1

## Business Context
Nakon što je implementirano kreiranje osnovnog radnog naloga, potrebno je omogućiti serviserima da u radni nalog dodaju konkretne stavke koje predstavljaju obavljene aktivnosti i rad na uređajima. Ova funkcionalnost je ključna za detaljno dokumentovanje svih aktivnosti koje su serviseri obavili na terenu. Stavke radnog naloga omogućavaju precizno praćenje koji uređaji su servisirani, koji tipovi aktivnosti su izvršeni i koje napomene su relevantne za svaku aktivnost. Mogućnost dodavanja stavki preko QR koda ili manuelno pruža fleksibilnost serviserima u različitim situacijama na terenu. Povezivanje uređaja sa stavkama radnog naloga omogućava praćenje istorije servisa za svaki uređaj, što je važno za buduće održavanje i servisne aktivnosti.

## Story
**As a** serviser,  
**I want to** add service items to work orders,  
**so that** I can document all performed activities.

## Acceptance Criteria

### AC1: Dodavanje stavki različitih tipova
- **Given** da je serviser kreirao radni nalog
- **When** pristupa stranici za dodavanje stavki
- **Then** može odabrati tip stavke: servis, popravka, ili montaža
- **And** tip stavke određuje dostupne opcije i polja za unos

### AC2: Dodavanje stavke preko QR koda
- **Given** da je serviser na stranici za dodavanje stavki
- **When** odabere opciju "Skeniraj QR kod"
- **Then** sistem aktivira kameru za skeniranje
- **And** nakon uspešnog skeniranja, automatski popunjava podatke o uređaju
- **And** serviser može dopuniti ostale informacije o stavci

### AC3: Manuelni odabir uređaja
- **Given** da je serviser na stranici za dodavanje stavki
- **When** odabere opciju za manuelni unos
- **Then** može pretražiti i odabrati postojeći uređaj iz sistema
- **And** može odabrati opciju "Novi uređaj" za dodavanje uređaja koji nije u sistemu

### AC4: Dodavanje napomene za stavku
- **Given** da serviser dodaje stavku u radni nalog
- **When** popunjava podatke stavke
- **Then** može uneti napomenu koja opisuje obavljene aktivnosti
- **And** napomena se čuva uz stavku i vidljiva je u detaljima radnog naloga

### AC5: Dodavanje materijala za popravke i montaže
- **Given** da serviser dodaje stavku tipa popravka ili montaža
- **When** popunjava podatke stavke
- **Then** može dodati jedan ili više materijala korišćenih tokom rada
- **And** za svaki materijal može uneti naziv, jedinicu mere, količinu i serijski broj
- **And** lista dodatih materijala se prikazuje u okviru stavke

## Tasks / Subtasks
- [ ] Implementacija modela za stavke radnog naloga
  - [ ] Kreiranje StavkaRadnogNaloga modela sa potrebnim poljima
  - [ ] Implementacija relacija sa RadniNalog i Uredjaj modelima
  - [ ] Implementacija enumeracije za tip stavke

- [ ] Implementacija modela za materijale
  - [ ] Kreiranje Materijal modela sa potrebnim poljima
  - [ ] Implementacija relacije sa StavkaRadnogNaloga modelom
  - [ ] Definisanje validacija za obavezna polja

- [ ] Implementacija forme za dodavanje stavki
  - [ ] Kreiranje DodajStavkuForm klase sa dinamičkim poljima u zavisnosti od tipa stavke
  - [ ] Implementacija validacije u zavisnosti od tipa stavke
  - [ ] Implementacija dinamičkog UI-a koji se prilagođava tipu stavke

- [ ] Implementacija QR kod integracije za dodavanje stavki
  - [ ] Integracija postojeće QR kod funkcionalnosti sa formom za dodavanje stavki
  - [ ] Implementacija automatskog popunjavanja podataka o uređaju nakon skeniranja
  - [ ] Implementacija opcije za manuelni unos ako QR skeniranje nije moguće

- [ ] Implementacija pretrage i odabira postojećih uređaja
  - [ ] Kreiranje API endpointa za pretragu uređaja
  - [ ] Implementacija autocomplete komponente za odabir uređaja
  - [ ] Implementacija opcije za dodavanje novog uređaja direktno iz forme za stavke

- [ ] Implementacija dodavanja materijala
  - [ ] Kreiranje komponente za dinamičko dodavanje materijala
  - [ ] Implementacija validacije za materijale
  - [ ] Implementacija prikaza liste dodatih materijala sa opcijom brisanja

- [ ] Implementacija backend ruta
  - [ ] Implementacija rute za dodavanje nove stavke u radni nalog
  - [ ] Implementacija rute za dodavanje materijala u stavku
  - [ ] Implementacija rute za brisanje stavke ili materijala

- [ ] Implementacija prikaza dodanih stavki
  - [ ] Implementacija tabelarnog prikaza stavki u radnom nalogu
  - [ ] Implementacija detaljnog pregleda pojedinačne stavke
  - [ ] Implementacija prikaza materijala za svaku stavku

- [ ] Testiranje
  - [ ] Testiranje dodavanja stavki različitih tipova
  - [ ] Testiranje QR kod integracije
  - [ ] Testiranje pretrage i odabira uređaja
  - [ ] Testiranje dodavanja i brisanja materijala

## Dev Notes
### Ključne implementacione tačke
- Tip stavke (servis/popravka/montaža) određuje dostupna polja i validacije
- Za stavke tipa "servis" nije potrebno dodavanje materijala
- Za stavke tipa "popravka" i "montaža" dodavanje materijala je opciono
- Integracija sa QR kod sistemom iz Story 3.4 mora biti besprekorna

### Tehnička implementacija
#### Modeli za stavke i materijale
```python
class TipStavke(enum.Enum):
    SERVIS = 'servis'
    POPRAVKA = 'popravka'
    MONTAZA = 'montaža'

class StavkaRadnogNaloga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.Enum(TipStavke), nullable=False)
    opis = db.Column(db.Text, nullable=False)
    napomena = db.Column(db.Text)
    datum_kreiranja = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Reference
    radni_nalog_id = db.Column(db.Integer, db.ForeignKey('radni_nalog.id'), nullable=False)
    uredjaj_id = db.Column(db.Integer, db.ForeignKey('uredjaj.id'), nullable=False)
    kreirao_id = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)
    
    # Relacije
    radni_nalog = db.relationship('RadniNalog', backref=db.backref('stavke', lazy='dynamic'))
    uredjaj = db.relationship('Uredjaj', backref=db.backref('stavke_radnih_naloga', lazy='dynamic'))
    kreirao = db.relationship('Korisnik', backref=db.backref('kreirane_stavke', lazy='dynamic'))
    materijali = db.relationship('Materijal', backref='stavka', lazy='dynamic', cascade='all, delete-orphan')

class Materijal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(100), nullable=False)
    jedinica_mere = db.Column(db.String(20), nullable=False)
    kolicina = db.Column(db.Float, nullable=False)
    serijski_broj = db.Column(db.String(50))
    cena = db.Column(db.Numeric(10, 2))
    
    # Reference
    stavka_id = db.Column(db.Integer, db.ForeignKey('stavka_radnog_naloga.id'), nullable=False)
```

#### Backend rute za upravljanje stavkama
```python
@bp.route('/<int:id>/stavke/nova', methods=['GET', 'POST'])
@login_required
def nova_stavka(id):
    """Dodavanje nove stavke u radni nalog."""
    radni_nalog = RadniNalog.query.get_or_404(id)
    form = NovaStavkaForm()
    
    # Inicijalizacija forme za QR skeniranje
    qr_form = None
    if request.args.get('qr_mode') == '1':
        qr_form = QRScanForm()
    
    if form.validate_on_submit():
        # Kreiranje nove stavke
        stavka = StavkaRadnogNaloga(
            tip=form.tip.data,
            opis=form.opis.data,
            napomena=form.napomena.data,
            radni_nalog_id=radni_nalog.id,
            uredjaj_id=form.uredjaj_id.data,
            kreirao_id=current_user.id
        )
        
        db.session.add(stavka)
        
        # Dodavanje materijala ako su prosleđeni
        if form.materijali.data:
            for mat_data in form.materijali.data:
                materijal = Materijal(
                    naziv=mat_data['naziv'],
                    jedinica_mere=mat_data['jedinica_mere'],
                    kolicina=float(mat_data['kolicina']),
                    serijski_broj=mat_data.get('serijski_broj', ''),
                    cena=float(mat_data.get('cena', 0)),
                    stavka_id=stavka.id
                )
                db.session.add(materijal)
        
        db.session.commit()
        flash('Stavka je uspešno dodata u radni nalog.', 'success')
        return redirect(url_for('radni_nalozi.detalji', id=radni_nalog.id))
    
    return render_template('radni_nalozi/nova_stavka.html', 
                          form=form,
                          qr_form=qr_form,
                          radni_nalog=radni_nalog)

@bp.route('/api/uredjaji/pretraga')
@login_required
def pretrazi_uredjaje():
    """API za pretragu uređaja za autocomplete."""
    q = request.args.get('q', '')
    if len(q) < 2:
        return jsonify([])
    
    uredjaji = Uredjaj.query.filter(
        or_(
            Uredjaj.naziv.ilike(f'%{q}%'),
            Uredjaj.serijski_broj.ilike(f'%{q}%'),
            Uredjaj.inventarski_broj.ilike(f'%{q}%')
        )
    ).limit(10).all()
    
    rezultati = [
        {
            'id': u.id,
            'text': f"{u.naziv} (S/N: {u.serijski_broj})",
            'tip': u.tip.value,
            'proizvodjac': u.proizvodjac,
            'model': u.model
        }
        for u in uredjaji
    ]
    
    return jsonify(rezultati)

@bp.route('/<int:id>/stavke/<int:stavka_id>/materijali', methods=['POST'])
@login_required
def dodaj_materijal(id, stavka_id):
    """Dodavanje materijala u postojeću stavku."""
    stavka = StavkaRadnogNaloga.query.get_or_404(stavka_id)
    
    # Provera da li stavka pripada radnom nalogu
    if stavka.radni_nalog_id != id:
        abort(404)
    
    form = DodajMaterijalForm()
    
    if form.validate_on_submit():
        materijal = Materijal(
            naziv=form.naziv.data,
            jedinica_mere=form.jedinica_mere.data,
            kolicina=form.kolicina.data,
            serijski_broj=form.serijski_broj.data,
            cena=form.cena.data if form.cena.data else None,
            stavka_id=stavka.id
        )
        
        db.session.add(materijal)
        db.session.commit()
        
        flash('Materijal je uspešno dodat.', 'success')
    
    return redirect(url_for('radni_nalozi.detalji_stavke', id=id, stavka_id=stavka_id))
```

#### Frontend forma za dodavanje stavki
```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{{ url_for('main.index') }}">Početna</a></li>
            <li class="breadcrumb-item"><a href="{{ url_for('radni_nalozi.lista') }}">Radni nalozi</a></li>
            <li class="breadcrumb-item"><a href="{{ url_for('radni_nalozi.detalji', id=radni_nalog.id) }}">{{ radni_nalog.broj_naloga }}</a></li>
            <li class="breadcrumb-item active">Nova stavka</li>
        </ol>
    </nav>
    
    <h2>Nova stavka - {{ radni_nalog.broj_naloga }}</h2>
    
    <!-- QR Skeniranje opcija -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    Način unosa uređaja
                </div>
                <div class="card-body">
                    <div class="d-flex gap-2">
                        {% if qr_form %}
                            <a href="{{ url_for('radni_nalozi.nova_stavka', id=radni_nalog.id) }}" class="btn btn-outline-primary">
                                <i class="bi bi-keyboard"></i> Manuelni unos
                            </a>
                            <div class="alert alert-info">
                                Skenirajte QR kod uređaja kamerom da automatski popunite podatke.
                            </div>
                            <div id="qr-scanner-container">
                                <!-- QR skener komponenta -->
                            </div>
                        {% else %}
                            <a href="{{ url_for('radni_nalozi.nova_stavka', id=radni_nalog.id, qr_mode=1) }}" class="btn btn-outline-primary">
                                <i class="bi bi-qr-code-scan"></i> Skeniraj QR kod
                            </a>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Forma za novu stavku -->
    <form method="POST" id="nova-stavka-form" class="mt-4">
        {{ form.hidden_tag() }}
        
        <div class="row mb-3">
            <div class="col-md-4">
                <div class="form-group mb-3">
                    {{ form.tip.label(class="form-label") }}
                    {{ form.tip(class="form-select", id="tip-stavke") }}
                    {% if form.tip.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.tip.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
            
            <div class="col-md-8">
                <div class="form-group mb-3">
                    {{ form.uredjaj_id.label(class="form-label") }}
                    <select name="uredjaj_id" id="uredjaj-select" class="form-control select2" required>
                        <option value="">Izaberite uređaj</option>
                        <option value="new">+ Dodaj novi uređaj</option>
                    </select>
                    {% if form.uredjaj_id.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.uredjaj_id.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <!-- Detalji o izabranom uređaju -->
        <div id="uredjaj-detalji" class="card mb-3 d-none">
            <div class="card-header">
                Detalji uređaja
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        <p><strong>Proizvođač:</strong> <span id="uredjaj-proizvodjac"></span></p>
                    </div>
                    <div class="col-md-3">
                        <p><strong>Model:</strong> <span id="uredjaj-model"></span></p>
                    </div>
                    <div class="col-md-3">
                        <p><strong>Tip:</strong> <span id="uredjaj-tip"></span></p>
                    </div>
                    <div class="col-md-3">
                        <p><strong>Serijski broj:</strong> <span id="uredjaj-serijski-broj"></span></p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="form-group mb-3">
            {{ form.opis.label(class="form-label") }}
            {{ form.opis(class="form-control") }}
            {% if form.opis.errors %}
                <div class="invalid-feedback d-block">
                    {% for error in form.opis.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <div class="form-group mb-3">
            {{ form.napomena.label(class="form-label") }}
            {{ form.napomena(class="form-control", rows=3) }}
            {% if form.napomena.errors %}
                <div class="invalid-feedback d-block">
                    {% for error in form.napomena.errors %}
                        {{ error }}
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <!-- Sekcija za materijale - prikazuje se samo za popravku i montažu -->
        <div id="materijali-sekcija" class="card mb-3 d-none">
            <div class="card-header d-flex justify-content-between align-items-center">
                <span>Materijali</span>
                <button type="button" class="btn btn-sm btn-outline-primary" id="dodaj-materijal-btn">
                    <i class="bi bi-plus"></i> Dodaj materijal
                </button>
            </div>
            <div class="card-body">
                <div id="materijali-container">
                    <!-- Ovde će se dinamički dodavati materijali -->
                </div>
                <div id="nema-materijala-poruka" class="alert alert-info">
                    Nema dodatih materijala. Kliknite na dugme "Dodaj materijal" za dodavanje.
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mt-4">
            <a href="{{ url_for('radni_nalozi.detalji', id=radni_nalog.id) }}" class="btn btn-secondary">Otkaži</a>
            <button type="submit" class="btn btn-primary">Dodaj stavku</button>
        </div>
    </form>
</div>

{% block scripts %}
<script>
$(document).ready(function() {
    // Inicijalizacija Select2 za pretragu uređaja
    $('#uredjaj-select').select2({
        ajax: {
            url: "{{ url_for('radni_nalozi.pretrazi_uredjaje') }}",
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        },
        placeholder: 'Pretražite uređaje po nazivu, serijskom broju ili inventarskom broju',
        minimumInputLength: 2
    });
    
    // Prikazivanje detalja o izabranom uređaju
    $('#uredjaj-select').on('select2:select', function (e) {
        const data = e.params.data;
        
        if (data.id === 'new') {
            // Redirekcija na formu za dodavanje novog uređaja
            window.location.href = "{{ url_for('uredjaji.novi') }}?redirect={{ url_for('radni_nalozi.nova_stavka', id=radni_nalog.id) | urlencode }}";
            return;
        }
        
        // Prikazivanje detalja o izabranom uređaju
        $('#uredjaj-proizvodjac').text(data.proizvodjac);
        $('#uredjaj-model').text(data.model);
        $('#uredjaj-tip').text(data.tip);
        $('#uredjaj-serijski-broj').text(data.serijski_broj || 'Nije definisan');
        $('#uredjaj-detalji').removeClass('d-none');
    });
    
    // Prikaz/sakrivanje sekcije za materijale u zavisnosti od tipa stavke
    $('#tip-stavke').change(function() {
        const tip = $(this).val();
        if (tip === 'popravka' || tip === 'montaža') {
            $('#materijali-sekcija').removeClass('d-none');
        } else {
            $('#materijali-sekcija').addClass('d-none');
        }
    });
    
    // Dinamičko dodavanje materijala
    let materijalCounter = 0;
    
    $('#dodaj-materijal-btn').click(function() {
        const materijalHtml = `
            <div class="materijal-item mb-3 p-3 border rounded">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h6>Materijal #${materijalCounter + 1}</h6>
                    <button type="button" class="btn btn-sm btn-outline-danger ukloni-materijal-btn">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
                <div class="row mb-2">
                    <div class="col-md-6">
                        <label class="form-label">Naziv</label>
                        <input type="text" name="materijali[${materijalCounter}][naziv]" class="form-control" required>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Jedinica mere</label>
                        <input type="text" name="materijali[${materijalCounter}][jedinica_mere]" class="form-control" required>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Količina</label>
                        <input type="number" name="materijali[${materijalCounter}][kolicina]" class="form-control" step="0.01" min="0.01" required>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <label class="form-label">Serijski broj</label>
                        <input type="text" name="materijali[${materijalCounter}][serijski_broj]" class="form-control">
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Cena (opciono)</label>
                        <input type="number" name="materijali[${materijalCounter}][cena]" class="form-control" step="0.01" min="0">
                    </div>
                </div>
            </div>
        `;
        
        $('#materijali-container').append(materijalHtml);
        materijalCounter++;
        
        if (materijalCounter > 0) {
            $('#nema-materijala-poruka').addClass('d-none');
        }
    });
    
    // Uklanjanje materijala
    $(document).on('click', '.ukloni-materijal-btn', function() {
        $(this).closest('.materijal-item').remove();
        materijalCounter--;
        
        if (materijalCounter === 0) {
            $('#nema-materijala-poruka').removeClass('d-none');
        }
        
        // Ažuriranje brojeva materijala
        $('.materijal-item h6').each(function(index) {
            $(this).text(`Materijal #${index + 1}`);
        });
    });
    
    // QR skener inicijalizacija ako je u QR modu
    {% if qr_form %}
    initQRScanner();
    {% endif %}
});

// Funkcija za inicijalizaciju QR skenera
function initQRScanner() {
    // Implementacija QR skenera iz Story 3.4
    // Ova funkcija će koristiti postojeću QR kod funkcionalnost
    // i automatski popuniti polja forme kada se detektuje uređaj
}
</script>
{% endblock %}
{% endblock %}
```

### Integracija sa QR kod sistemom
Integracija sa QR kod sistemom iz Story 3.4 zahteva:

1. Korišćenje postojeće funkcionalnosti za skeniranje QR koda
2. Prilagođavanje QR koda za korišćenje u kontekstu dodavanja stavki u radni nalog
3. Implementaciju automatskog popunjavanja forme sa podacima o uređaju nakon skeniranja

### Potrebne biblioteke
- Flask-WTF: Za obradu formi i validaciju
- SQLAlchemy: Za upravljanje modelima i relacionim vezama
- Select2.js: Za naprednu pretragu i odabir uređaja
- jsQR: Za skeniranje QR kodova (rekorišćena iz Story 3.4)

## Testing
### Unit i integracija testovi
- Testirati dodavanje stavki različitih tipova
- Testirati validaciju obaveznih polja forme
- Testirati dinamičko ponašanje forme u zavisnosti od tipa stavke
- Testirati dodavanje i brisanje materijala
- Testirati integraciju sa QR kod sistemom

### Testiranje korisničkog interfejsa
- Testirati responzivnost forme za dodavanje stavki
- Testirati pretragu i odabir uređaja
- Testirati dinamičko dodavanje i brisanje materijala
- Testirati QR kod skeniranje u različitim uslovima

## Change Log
| Datum | Verzija | Opis | Autor |
|-------|---------|------|-------|
| 2025-07-28 | 1.0 | Inicijalni draft story-ja | Scrum Master Bob |
