# Story 4.1: Kreiranje radnog naloga

## Metadata
- **Story ID**: 4.1
- **Epic**: Epic 4 - Radni nalozi i workflow
- **Priority**: High
- **Story Points**: 5
- **Status**: Draft
- **Created**: 2025-07-28
- **Assigned To**: AI Developer

## Business Context
Kreiranje radnih naloga predstavlja osnovu sistema za praćenje i dokumentovanje servisnih aktivnosti. Serviseri moraju imati mogućnost da brzo i jednostavno dokumentuju svoje radne aktivnosti na terenu. Dobro implementiran sistem za kreiranje radnih naloga omogućava efikasno praćenje servisnih aktivnosti, preciznu evidenciju o izvršenim radovima i transparentnost prema klijentima. Standardizovani format radnog naloga olakšava administrativne procese i obezbeđuje konzistentnost u dokumentaciji servisnih aktivnosti. Automatsko generisanje jedinstvenih brojeva naloga pomaže u organizaciji i pretraživanju dokumentacije, dok statusni sistem omogućava praćenje napretka posla od otvaranja do fakturisanja.

## Story
**As a** serviser,  
**I want to** create work orders,  
**so that** I can document service activities.

## Acceptance Criteria

### AC1: Kreiranje radnog naloga sa osnovnim podacima
- **Given** da je serviser prijavljen u sistem
- **When** navigira na stranicu za kreiranje radnog naloga
- **Then** može popuniti osnovne podatke radnog naloga
- **And** sistem prikazuje formu sa svim potrebnim poljima

### AC2: Obavezna polja radnog naloga
- **Given** da je serviser na formi za kreiranje radnog naloga
- **When** popunjava podatke
- **Then** mora odabrati sledeća polja: tip (servis/popravka/montaža), klijent, lokacija
- **And** opcionalno može odabrati servisere i vozilo
- **And** može uneti dodatne napomene

### AC3: Automatsko generisanje broja naloga
- **Given** da je serviser kreirao novi radni nalog
- **When** se nalog sačuva u sistem
- **Then** sistem automatski generiše jedinstveni broj naloga
- **And** format broja je prefiks (RNS/RNP/RNM) + godina-broj (npr. RNS-2025-0001)
- **And** prefiks zavisi od tipa naloga (Servis/Popravka/Montaža)

### AC4: Automatsko beleženje datuma i vremena
- **Given** da je serviser kreirao novi radni nalog
- **When** se nalog sačuva u sistem
- **Then** sistem automatski beleži datum i vreme otvaranja naloga
- **And** ti podaci su vidljivi u detaljima naloga

### AC5: Inicijalni status radnog naloga
- **Given** da je serviser kreirao novi radni nalog
- **When** se nalog sačuva u sistem
- **Then** sistem automatski postavlja status naloga na "U radu"
- **And** status se prikazuje na detaljima naloga

## Tasks / Subtasks
- [ ] Implementacija modela za radne naloge
  - [ ] Kreiranje RadniNalog modela sa potrebnim poljima
  - [ ] Implementacija relacija sa drugim modelima (Korisnik, Klijent, Lokacija, Vozilo)
  - [ ] Implementacija statusa radnog naloga sa enumeracijom
  - [ ] Definisanje validacija za obavezna polja

- [ ] Implementacija forme za kreiranje radnog naloga
  - [ ] Kreiranje KreirajRadniNalogForm klase sa validacijom polja
  - [ ] Implementacija dinamičkog odabira lokacija na osnovu izabranog klijenta
  - [ ] Implementacija odabira serviserskog tima i vozila

- [ ] Implementacija generisanja jedinstvenog broja naloga
  - [ ] Kreiranje funkcije za generisanje prefiksa na osnovu tipa naloga
  - [ ] Implementacija logike za redni broj naloga u tekućoj godini
  - [ ] Testiranje jedinstvenosti generisanih brojeva naloga

- [ ] Implementacija backend ruta
  - [ ] Implementacija GET rute za prikaz forme radnog naloga
  - [ ] Implementacija POST rute za prihvatanje i kreiranje novog naloga
  - [ ] Implementacija rute za pregled detalja kreiranog naloga

- [ ] Implementacija frontend interfejsa
  - [ ] Kreiranje UI komponenti za formu radnog naloga
  - [ ] Implementacija validacija na frontend-u
  - [ ] Implementacija prikaza detalja kreiranog naloga

- [ ] Testiranje
  - [ ] Testiranje kreiranje radnog naloga sa različitim tipovima
  - [ ] Testiranje generisanja jedinstvenih brojeva naloga
  - [ ] Testiranje obaveznih polja i validacija
  - [ ] Testiranje automatskog postavljanja statusa

## Dev Notes
### Ključne implementacione tačke
- Radni nalog je centralni entitet sistema za upravljanje servisnim aktivnostima
- Format broja naloga mora biti konzistentan i pažljivo implementiran
- Status radnog naloga će biti kasnije proširen u Story 4.4

### Tehnička implementacija
#### Model radnog naloga
```python
class TipRadnogNaloga(enum.Enum):
    SERVIS = 'servis'
    POPRAVKA = 'popravka'
    MONTAZA = 'montaža'

class StatusRadnogNaloga(enum.Enum):
    U_RADU = 'u_radu'
    ZAVRSEN = 'završen'
    FAKTURISAN = 'fakturisan'
    OTKAZAN = 'otkazan'

class RadniNalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    broj_naloga = db.Column(db.String(20), unique=True, nullable=False)
    tip = db.Column(db.Enum(TipRadnogNaloga), nullable=False)
    status = db.Column(db.Enum(StatusRadnogNaloga), nullable=False, default=StatusRadnogNaloga.U_RADU)
    
    # Osnovni podaci
    datum_kreiranja = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    datum_zatvaranja = db.Column(db.DateTime)
    napomena = db.Column(db.Text)
    
    # Reference
    klijent_id = db.Column(db.Integer, db.ForeignKey('klijent.id'), nullable=False)
    lokacija_id = db.Column(db.Integer, db.ForeignKey('lokacija.id'), nullable=False)
    vozilo_id = db.Column(db.Integer, db.ForeignKey('vozilo.id'))
    kreirao_id = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)
    
    # Relacije
    klijent = db.relationship('Klijent', backref=db.backref('radni_nalozi', lazy='dynamic'))
    lokacija = db.relationship('Lokacija', backref=db.backref('radni_nalozi', lazy='dynamic'))
    vozilo = db.relationship('Vozilo', backref=db.backref('radni_nalozi', lazy='dynamic'))
    kreirao = db.relationship('Korisnik', backref=db.backref('kreirani_nalozi', lazy='dynamic'))
    serviseri = db.relationship('Korisnik', secondary='radni_nalog_serviser', backref=db.backref('nalozi', lazy='dynamic'))
    
    def __init__(self, **kwargs):
        super(RadniNalog, self).__init__(**kwargs)
        if not self.broj_naloga:
            self.generisi_broj_naloga()
    
    def generisi_broj_naloga(self):
        prefiks = self._odredi_prefiks()
        godina = datetime.now().year
        poslednji_nalog = RadniNalog.query.filter(
            RadniNalog.broj_naloga.like(f"{prefiks}-{godina}-%")
        ).order_by(RadniNalog.broj_naloga.desc()).first()
        
        if poslednji_nalog:
            poslednji_broj = int(poslednji_nalog.broj_naloga.split('-')[-1])
            novi_broj = poslednji_broj + 1
        else:
            novi_broj = 1
        
        self.broj_naloga = f"{prefiks}-{godina}-{novi_broj:04d}"
    
    def _odredi_prefiks(self):
        if self.tip == TipRadnogNaloga.SERVIS:
            return "RNS"
        elif self.tip == TipRadnogNaloga.POPRAVKA:
            return "RNP"
        elif self.tip == TipRadnogNaloga.MONTAZA:
            return "RNM"
        return "RN"

# Asocijativna tabela za vezu više-na-više između radnih naloga i servisera
radni_nalog_serviser = db.Table('radni_nalog_serviser',
    db.Column('radni_nalog_id', db.Integer, db.ForeignKey('radni_nalog.id'), primary_key=True),
    db.Column('korisnik_id', db.Integer, db.ForeignKey('korisnik.id'), primary_key=True)
)
```

#### Backend ruta za kreiranje radnog naloga
```python
@bp.route('/novi', methods=['GET', 'POST'])
@login_required
def novi_radni_nalog():
    """Kreiranje novog radnog naloga"""
    form = KreirajRadniNalogForm()
    
    # Dinamičko učitavanje lokacija na osnovu klijenta
    if request.method == 'GET' and request.args.get('klijent_id'):
        klijent_id = request.args.get('klijent_id', type=int)
        lokacije = Lokacija.query.filter_by(klijent_id=klijent_id).all()
        return jsonify([(l.id, l.naziv) for l in lokacije])
    
    if form.validate_on_submit():
        radni_nalog = RadniNalog(
            tip=form.tip.data,
            klijent_id=form.klijent_id.data,
            lokacija_id=form.lokacija_id.data,
            vozilo_id=form.vozilo_id.data if form.vozilo_id.data else None,
            napomena=form.napomena.data,
            kreirao_id=current_user.id
        )
        
        # Dodavanje servisera ako su izabrani
        if form.serviseri.data:
            for serviser_id in form.serviseri.data:
                serviser = Korisnik.query.get(serviser_id)
                if serviser:
                    radni_nalog.serviseri.append(serviser)
        
        db.session.add(radni_nalog)
        db.session.commit()
        
        flash('Radni nalog je uspešno kreiran.', 'success')
        return redirect(url_for('radni_nalozi.detalji', id=radni_nalog.id))
    
    return render_template('radni_nalozi/novi.html', form=form)
```

#### Frontend forma za kreiranje radnog naloga
```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{{ url_for('main.index') }}">Početna</a></li>
            <li class="breadcrumb-item"><a href="{{ url_for('radni_nalozi.lista') }}">Radni nalozi</a></li>
            <li class="breadcrumb-item active">Novi radni nalog</li>
        </ol>
    </nav>
    
    <h2>Novi radni nalog</h2>
    
    <form method="POST" class="mt-4">
        {{ form.hidden_tag() }}
        
        <div class="row mb-3">
            <div class="col-md-4">
                <div class="form-group mb-3">
                    {{ form.tip.label(class="form-label") }}
                    {{ form.tip(class="form-select") }}
                    {% if form.tip.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.tip.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="form-group mb-3">
                    {{ form.klijent_id.label(class="form-label") }}
                    {{ form.klijent_id(class="form-select", id="klijent_select") }}
                    {% if form.klijent_id.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.klijent_id.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="form-group mb-3">
                    {{ form.lokacija_id.label(class="form-label") }}
                    {{ form.lokacija_id(class="form-select", id="lokacija_select") }}
                    {% if form.lokacija_id.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.lokacija_id.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="form-group mb-3">
                    {{ form.serviseri.label(class="form-label") }}
                    {{ form.serviseri(class="form-select", multiple=true, size=5) }}
                    <div class="form-text">Držite CTRL za odabir više servisera</div>
                    {% if form.serviseri.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.serviseri.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="form-group mb-3">
                    {{ form.vozilo_id.label(class="form-label") }}
                    {{ form.vozilo_id(class="form-select") }}
                    {% if form.vozilo_id.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.vozilo_id.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
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
        
        <div class="d-flex justify-content-between mt-4">
            <a href="{{ url_for('radni_nalozi.lista') }}" class="btn btn-secondary">Otkaži</a>
            <button type="submit" class="btn btn-primary">Kreiraj radni nalog</button>
        </div>
    </form>
</div>

{% block scripts %}
<script>
$(document).ready(function() {
    // Dinamičko učitavanje lokacija na osnovu izabranog klijenta
    $('#klijent_select').change(function() {
        const klijentId = $(this).val();
        if (klijentId) {
            $.get("{{ url_for('radni_nalozi.novi_radni_nalog') }}", {
                klijent_id: klijentId
            }).done(function(data) {
                const lokacijeSelect = $('#lokacija_select');
                lokacijeSelect.empty();
                
                // Dodavanje opcije "Izaberite lokaciju"
                lokacijeSelect.append($('<option></option>').attr('value', '').text('Izaberite lokaciju'));
                
                // Dodavanje lokacija iz odgovora servera
                $.each(data, function(index, lokacija) {
                    lokacijeSelect.append($('<option></option>').attr('value', lokacija[0]).text(lokacija[1]));
                });
                
                lokacijeSelect.prop('disabled', false);
            });
        } else {
            $('#lokacija_select').empty().prop('disabled', true);
            $('#lokacija_select').append($('<option></option>').attr('value', '').text('Prvo izaberite klijenta'));
        }
    });
    
    // Inicijalno stanje za lokacije
    if (!$('#klijent_select').val()) {
        $('#lokacija_select').empty().prop('disabled', true);
        $('#lokacija_select').append($('<option></option>').attr('value', '').text('Prvo izaberite klijenta'));
    }
});
</script>
{% endblock %}
{% endblock %}
```

### Potrebne biblioteke
- Flask-WTF: Za obradu formi i validaciju
- SQLAlchemy: Za upravljanje modelima i relacionim vezama
- jQuery: Za dinamički prikaz lokacija na osnovu izabranog klijenta

## Testing
### Unit i integracija testovi
- Testirati generisanje jedinstvenih brojeva naloga
- Testirati validaciju obaveznih polja forme
- Testirati dinamičko učitavanje lokacija
- Testirati kreiranje radnog naloga za različite tipove

### Testiranje korisničkog interfejsa
- Testirati responzivnost forme za kreiranje naloga
- Testirati validacije na strani klijenta
- Testirati dinamičko ponašanje forme (npr. učitavanje lokacija)

## Change Log
| Datum | Verzija | Opis | Autor |
|-------|---------|------|-------|
| 2025-07-28 | 1.0 | Inicijalni draft story-ja | Scrum Master Bob |
