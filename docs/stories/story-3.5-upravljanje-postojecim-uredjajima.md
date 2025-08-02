# Story 3.5: Upravljanje postojećim uređajima

## Metadata
- **Story ID**: 3.5
- **Epic**: Epic 3 - Upravljanje uređajima i QR kodovima
- **Priority**: Medium
- **Story Points**: 3
- **Status**: Draft
- **Created**: 2025-07-28
- **Assigned To**: AI Developer
- **Dependencies**: Story 4.1, Story 4.2, Story 3.4

## Business Context
Nakon što je implementirana registracija uređaja i QR kod funkcionalnost, potrebno je omogućiti serviserima da ažuriraju podatke o postojećim uređajima. Ova funkcionalnost je važna jer se tokom životnog veka HVAC uređaja mogu promeniti različiti parametri, lokacije i karakteristike. Efikasno upravljanje ažuriranjem podataka o uređajima osigurava da servisni tehničari uvek imaju pristup tačnim i ažurnim informacijama, što je ključno za kvalitetno održavanje i servisiranje. Takođe, omogućavanje premeštanja uređaja između prostorija prati realnu situaciju na terenu gde se HVAC oprema može relocirati prema potrebama klijenata.

## Story
**As a** serviser,  
**I want to** edit device information,  
**so that** I can keep device records up to date.

## Acceptance Criteria

### AC1: Editovanje osnovnih podataka uređaja
- **Given** da je serviser prijavljen u sistem
- **When** pristupa stranici sa detaljima uređaja
- **Then** može da klikne na dugme za izmenu podataka
- **And** uredi bilo koje od polja uređaja (proizvođač, model, serijski broj, itd.)
- **And** sačuva izmene

### AC2: Čuvanje istorije izmena
- **Given** da je serviser izmenio podatke o uređaju
- **When** sačuva izmene
- **Then** sistem beleži ko je i kada izvršio izmenu
- **And** kreira zapis u istoriji izmena
- **And** administratori mogu videti istoriju svih izmena

### AC3: Očuvanje QR koda
- **Given** da je serviser izmenio podatke o uređaju
- **When** sačuva izmene
- **Then** jedinstveni ID uređaja ostaje nepromenjen
- **And** QR kod nastavlja da funkcioniše kao i pre izmena

### AC4: Očuvanje istorije servisa
- **Given** da je serviser izmenio podatke o uređaju
- **When** pregleda detalje tog uređaja nakon izmena
- **Then** sva prethodna istorija servisa ostaje povezana sa uređajem
- **And** radni nalozi zadržavaju sve reference ka tom uređaju

### AC5: Premeštanje uređaja u drugu prostoriju
- **Given** da je serviser prijavljen u sistem
- **When** pristupa stranici sa detaljima uređaja
- **Then** može da promeni prostoriju kojoj uređaj pripada
- **And** nakon promene, uređaj se prikazuje u novoj prostoriji
- **And** breadcrumb navigacija se ažurira sa novom putanjom

## Tasks / Subtasks
- [ ] Implementacija forme za editovanje podataka o uređaju (AC1)
  - [ ] Kreirati EditUredjajForm klasu sa validacijom polja
  - [ ] Implementirati rutu za prikaz forme sa popunjenim vrednostima
  - [ ] Implementirati rutu za prihvatanje izmenjenih podataka (POST)
  - [ ] Dodati kontrole za validaciju podataka pre čuvanja

- [ ] Implementacija sistema za praćenje istorije izmena (AC2)
  - [ ] Kreirati model IstorijaIzmenaUredjaja
  - [ ] Implementirati logiku za beleženje promena
  - [ ] Implementirati prikaz istorije izmena za administratore

- [ ] Očuvanje integriteta QR kodova (AC3)
  - [ ] Osigurati da se ID uređaja ne menja pri editovanju
  - [ ] Testirati funkcionalnost QR koda nakon izmena podataka

- [ ] Očuvanje relacija sa istorijom servisa (AC4)
  - [ ] Osigurati da sve relacije sa radnim nalozima ostaju validne
  - [ ] Testirati prikaz istorije servisa nakon izmena podataka

- [ ] Implementacija premeštanja uređaja (AC5)
  - [ ] Proširiti formu sa opcijom za odabir prostorije
  - [ ] Implementirati logiku za ažuriranje relacija prostorija-uređaj
  - [ ] Ažurirati prikaz breadcrumb navigacije nakon promene prostorije

- [ ] Testiranje
  - [ ] Implementirati unit testove za editovanje uređaja
  - [ ] Testirati integritet podataka nakon različitih scenarija izmena
  - [ ] Testirati očuvanje relacija sa istorijom servisa
  - [ ] Testirati premeštanje uređaja između prostorija

## Dev Notes
### Ključne implementacione tačke
- Dizajn forme za editovanje treba da bude sličan formi za dodavanje novog uređaja
- Istorija izmena treba da prati pattern korišćen u drugim delovima sistema
- Prilikom premeštanja uređaja, treba voditi računa o validaciji dozvola i pripadnosti objektima

### Tehnička implementacija
#### Backend model za istoriju izmena
```python
class IstorijaIzmenaUredjaja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uredjaj_id = db.Column(db.Integer, db.ForeignKey('uredjaj.id'), nullable=False)
    korisnik_id = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)
    datum_izmene = db.Column(db.DateTime, default=datetime.utcnow)
    opis_izmene = db.Column(db.Text, nullable=False)
    stare_vrednosti = db.Column(db.JSON)
    nove_vrednosti = db.Column(db.JSON)
    
    uredjaj = db.relationship('Uredjaj', backref=db.backref('istorija_izmena', lazy='dynamic'))
    korisnik = db.relationship('Korisnik', backref=db.backref('izmene_uredjaja', lazy='dynamic'))
```

#### Backend rute
```python
@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_uredjaj(id):
    """Prikazuje formu za editovanje i prihvata izmene uređaja."""
    uredjaj = Uredjaj.query.get_or_404(id)
    form = EditUredjajForm(obj=uredjaj)
    
    if form.validate_on_submit():
        # Čuvanje starih vrednosti za istoriju
        stare_vrednosti = {
            'naziv': uredjaj.naziv,
            'proizvodjac': uredjaj.proizvodjac,
            'model': uredjaj.model,
            'serijski_broj': uredjaj.serijski_broj,
            'godina_proizvodnje': uredjaj.godina_proizvodnje,
            'prostorija_id': uredjaj.prostorija_id
        }
        
        # Ažuriranje vrednosti iz forme
        form.populate_obj(uredjaj)
        
        # Kreiranje zapisa u istoriji izmena
        nove_vrednosti = {
            'naziv': uredjaj.naziv,
            'proizvodjac': uredjaj.proizvodjac,
            'model': uredjaj.model,
            'serijski_broj': uredjaj.serijski_broj,
            'godina_proizvodnje': uredjaj.godina_proizvodnje,
            'prostorija_id': uredjaj.prostorija_id
        }
        
        izmena = IstorijaIzmenaUredjaja(
            uredjaj_id=uredjaj.id,
            korisnik_id=current_user.id,
            opis_izmene='Ažuriranje podataka o uređaju',
            stare_vrednosti=stare_vrednosti,
            nove_vrednosti=nove_vrednosti
        )
        
        db.session.add(izmena)
        db.session.commit()
        
        flash('Uređaj je uspešno ažuriran.', 'success')
        return redirect(url_for('uredjaji.detalji_uredjaja', id=uredjaj.id))
        
    return render_template('uredjaji/edit.html', form=form, uredjaj=uredjaj)
```

#### Frontend forma za editovanje
```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{{ url_for('main.index') }}">Početna</a></li>
            <li class="breadcrumb-item"><a href="{{ url_for('uredjaji.lista') }}">Uređaji</a></li>
            <li class="breadcrumb-item"><a href="{{ url_for('uredjaji.detalji_uredjaja', id=uredjaj.id) }}">{{ uredjaj.naziv }}</a></li>
            <li class="breadcrumb-item active">Izmena</li>
        </ol>
    </nav>
    
    <h2>Izmena uređaja: {{ uredjaj.naziv }}</h2>
    
    <form method="POST" class="mt-4">
        {{ form.hidden_tag() }}
        
        <div class="row mb-3">
            <div class="col-md-6">
                <div class="form-group mb-3">
                    {{ form.naziv.label(class="form-label") }}
                    {{ form.naziv(class="form-control") }}
                    {% if form.naziv.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.naziv.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
            
            <!-- Ostala polja forme -->
            
            <div class="col-md-6">
                <div class="form-group mb-3">
                    {{ form.prostorija_id.label(class="form-label") }}
                    {{ form.prostorija_id(class="form-select") }}
                    {% if form.prostorija_id.errors %}
                        <div class="invalid-feedback d-block">
                            {% for error in form.prostorija_id.errors %}
                                {{ error }}
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mt-4">
            <a href="{{ url_for('uredjaji.detalji_uredjaja', id=uredjaj.id) }}" class="btn btn-secondary">Otkaži</a>
            <button type="submit" class="btn btn-primary">Sačuvaj izmene</button>
        </div>
    </form>
</div>
{% endblock %}
```

### Zavisnosti i implementacioni redosled
**Važna napomena**: Preporučuje se da se pre implementacije ove story implementiraju:
1. Story 4.1 - Kreiranje radnog naloga
2. Story 4.2 - Dodavanje stavki u radni nalog
3. Zatim završiti Story 3.4 - QR kod skeniranje

Tek nakon što su ove priče implementirane, preći na implementaciju Story 3.5, jer je neophodno da postoji kompletan model radnih naloga kako bi se pravilno održavale relacije između uređaja i radnih naloga tokom editovanja i premeštanja uređaja.

### Potrebne biblioteke
- Flask-WTF: Za obradu formi i validaciju
- SQLAlchemy: Za upravljanje modelima i relacionim vezama

## Testing
### Unit i integracija testovi
- Testirati validaciju forme za editovanje
- Testirati kreiranje zapisa u istoriji izmena
- Testirati održavanje relacija nakon premeštanja uređaja
- Testirati prikaz breadcrumb navigacije nakon premeštanja

### Testiranje korisničkog interfejsa
- Testirati responzivnost forme za editovanje
- Testirati workflow editovanja i premeštanja

## Change Log
| Datum | Verzija | Opis | Autor |
|-------|---------|------|-------|
| 2025-07-28 | 1.0 | Inicijalni draft story-ja | Scrum Master Bob |
