# Story 3.3: QR kod generisanje

## Metadata
- **Story ID**: 3.3
- **Epic**: Epic 3 - Upravljanje uređajima i QR kodovima
- **Priority**: Medium
- **Story Points**: 3
- **Status**: Ready for Development
- **Created**: 2025-07-26
- **Assigned To**: AI Developer


## Business Context
Efikasna identifikacija HVAC uređaja na terenu je ključna za servise i održavanje. QR kodovi omogućavaju brzu identifikaciju uređaja korišćenjem mobilnih uređaja bez potrebe za manuelnim unosom serijskih brojeva ili drugih identifikatora. Ova funkcionalnost je važna za optimizaciju procesa servisiranja, smanjenje mogućnosti greške pri identifikaciji uređaja i poboljšanje produktivnosti servisera na terenu. Automatsko generisanje QR kodova pri registraciji uređaja osigurava da svaki uređaj ima jedinstven kod koji se može koristiti tokom njegovog životnog ciklusa.

## Story
**As a** serviser,  
**I want to** generate QR codes for devices,  
**so that** I can quickly identify devices in the field.

## Acceptance Criteria

### AC1: Automatsko generisanje QR koda
- **Given** da je serviser kreirao novi uređaj u sistemu
- **When** uspešno sačuva informacije o uređaju
- **Then** sistem automatski generiše QR kod koji sadrži jedinstveni ID uređaja

### AC2: Sadržaj QR koda
- **Given** da je QR kod generisan
- **When** serviser pregleda informacije o QR kodu
- **Then** QR kod sadrži jedinstveni ID uređaja koji se može skenirati standardnim QR čitačima

### AC3: Opcija štampanja QR kodova
- **Given** da je serviser na stranici detalja uređaja
- **When** klikne na opciju "Štampaj QR kod"
- **Then** sistem prikazuje dijalog za izbor broja kopija QR kodova za štampanje
- **And** nakon potvrde, generiše se PDF za štampanje sa odabranim brojem kopija QR koda

### AC4: Printable format QR koda
- **Given** da je serviser izabrao štampanje QR koda
- **When** se generiše PDF za štampanje
- **Then** QR kod je prikazan u formatu pogodnom za štampanje
- **And** PDF sadrži osnovne informacije o uređaju pored QR koda (proizvođač, model, serijski broj)

### AC5: Ponovno štampanje QR kodova
- **Given** da je serviser na stranici postojećeg uređaja
- **When** klikne na opciju "Štampaj QR kod"
- **Then** sistem omogućava ponovno štampanje istog QR koda bez kreiranja novog jedinstvenog identifikatora

## Tasks / Subtasks
- [ ] Implementacija generisanja QR koda
  - [ ] Istražiti biblioteke za generisanje QR koda u Python-u (npr. qrcode, pyqrcode)
  - [ ] Implementirati servis za generisanje QR koda sa jedinstvenim ID-jem uređaja
  - [ ] Sačuvati generisani QR kod uz model uređaja ili generisati ga dinamički po potrebi

- [ ] Implementacija korisničkog interfejsa
  - [ ] Dodati prikaz QR koda na stranici detalja uređaja
  - [ ] Implementirati dijalog za izbor broja kopija za štampanje
  - [ ] Kreirati UI komponentu za prikaz QR koda

- [ ] Implementacija PDF generisanja za štampanje
  - [ ] Implementirati funkcionalnost za generisanje PDF-a sa QR kodom
  - [ ] Dodati osnovne informacije o uređaju na PDF
  - [ ] Obezbediti da se više kopija istog QR koda može štampati na jednom PDF-u
  - [ ] Optimizovati format za štampanje na standardnim nalepnicama

- [ ] Testiranje
  - [ ] Testirati automatsko generisanje QR koda pri kreiranju uređaja
  - [ ] Testirati čitljivost generisanih QR kodova sa različitim QR čitačima
  - [ ] Testirati generisanje PDF-a sa različitim brojem kopija
  - [ ] Testirati ponovno štampanje QR kodova za postojeće uređaje

## Dev Notes
### Ključne implementacione tačke
- Koristiti pouzdanu biblioteku za generisanje QR kodova, poželjno `qrcode` biblioteku za Python
- QR kod treba da sadrži samo jedinstveni ID uređaja, ne sve podatke (radi optimalne veličine i čitljivosti)
- Primeniti odgovarajuće formatiranje za štampanje QR kodova na standardnim nalepnicama
- PDF dokument treba da bude generisan korišćenjem `fpdf2` biblioteke sa podešenim dimenzijama za standardne nalepnice
- Razmotriti opciju za štampanje više različitih QR kodova odjednom (batch štampanje)

### Modeliranje podataka
Razmotrite sledeće promene u modelu `Uredjaj`:

```python
class Uredjaj(db.Model):
    __tablename__ = 'uredjaji'
    
    # Postojeća polja...
    
    # Opciono: ako želite da čuvate generisani QR kod
    qr_kod_path = db.Column(db.String(255), nullable=True)
    
    # Metoda za generisanje QR koda
    def generisi_qr_kod(self):
        """Generiše QR kod za uređaj i vraća putanju do sačuvanog QR koda."""
        import qrcode
        import os
        from flask import current_app
        
        # Generisanje QR koda sa ID-jem uređaja
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(self.id))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Čuvanje QR koda
        qr_path = f"qr_codes/uredjaj_{self.id}.png"
        full_path = os.path.join(current_app.static_folder, qr_path)
        
        # Osigurati da direktorijum postoji
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Sačuvaj sliku
        img.save(full_path)
        
        # Ažuriraj putanju u bazi
        self.qr_kod_path = qr_path
        
        return qr_path
```

### Generisanje PDF-a za štampanje
Za generisanje PDF-a sa QR kodom koristiti fpdf2 biblioteku:

```python
def generisi_pdf_sa_qr_kodom(uredjaj, broj_kopija=1):
    """
    Generiše PDF sa određenim brojem kopija QR koda za dati uređaj.
    """
    from fpdf import FPDF
    import os
    from flask import current_app
    
    # Kreiranje instance PDF-a
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=0)
    
    # Za svaku kopiju kreiramo QR kod na stranici
    for _ in range(broj_kopija):
        pdf.add_page()
        
        # Dodaj naslov
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f"QR kod za uređaj #{uredjaj.id}", new_x="LMARGIN", new_y="NEXT", align='C')
        
        # Dodaj informacije o uređaju
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 7, f"Proizvođač: {uredjaj.proizvodjac}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, f"Model: {uredjaj.model}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, f"Serijski broj: {uredjaj.serijski_broj}", new_x="LMARGIN", new_y="NEXT")
        
        # Ako QR kod već postoji, dodaj ga u PDF
        qr_path = uredjaj.qr_kod_path
        if not qr_path:
            qr_path = uredjaj.generisi_qr_kod()
            
        full_path = os.path.join(current_app.static_folder, qr_path)
        if os.path.exists(full_path):
            pdf.image(full_path, x=70, y=50, w=70)
            
    # Sacuvaj PDF u privremeni fajl
    output_path = os.path.join(current_app.static_folder, f"qr_codes/uredjaj_{uredjaj.id}_qr_print.pdf")
    pdf.output(output_path)
    
    return output_path
```

### Rute za QR kodove
Dodajte nove rute u `uredjaji.py`:

```python
@bp.route('/<int:id>/qr_kod')
@login_required
def prikazi_qr_kod(id):
    """Prikazuje QR kod za uređaj."""
    uredjaj = Uredjaj.query.get_or_404(id)
    
    # Generiši QR kod ako ne postoji
    if not uredjaj.qr_kod_path:
        uredjaj.generisi_qr_kod()
        db.session.commit()
        
    return render_template('uredjaji/qr_kod.html', uredjaj=uredjaj)

@bp.route('/<int:id>/stampa_qr_kod', methods=['GET', 'POST'])
@login_required
def stampa_qr_kod(id):
    """Prikazuje formu za štampanje QR koda i generiše PDF."""
    uredjaj = Uredjaj.query.get_or_404(id)
    
    if request.method == 'POST':
        broj_kopija = int(request.form.get('broj_kopija', 1))
        pdf_path = generisi_pdf_sa_qr_kodom(uredjaj, broj_kopija)
        
        # Vrati PDF kao download
        return send_file(pdf_path, as_attachment=True, 
                         download_name=f"qr_kod_uredjaj_{id}.pdf")
        
    return render_template('uredjaji/stampa_qr_kod.html', uredjaj=uredjaj)
```

## Testing
### Unit testovi
```python
def test_generisanje_qr_koda(self):
    """Test generisanja QR koda za uređaj."""
    uredjaj = Uredjaj(
        tip='rashladna_tehnika',
        podtip='split_sistem',
        proizvodjac='Test',
        model='Test Model',
        serijski_broj='TEST001'
    )
    db.session.add(uredjaj)
    db.session.commit()
    
    # Testiramo generisanje QR koda
    qr_path = uredjaj.generisi_qr_kod()
    self.assertIsNotNone(qr_path)
    
    # Proverimo da li je QR kod sačuvan na disku
    import os
    from flask import current_app
    full_path = os.path.join(current_app.static_folder, qr_path)
    self.assertTrue(os.path.exists(full_path))

def test_pdf_sa_qr_kodom(self):
    """Test generisanja PDF-a sa QR kodom."""
    # Kreiranje test uređaja
    uredjaj = Uredjaj(
        tip='rashladna_tehnika',
        podtip='split_sistem',
        proizvodjac='Test',
        model='Test Model',
        serijski_broj='TEST002'
    )
    db.session.add(uredjaj)
    db.session.commit()
    
    # Generisanje PDF-a
    pdf_path = generisi_pdf_sa_qr_kodom(uredjaj, 2)
    
    # Provera da li je PDF kreiran
    import os
    self.assertTrue(os.path.exists(pdf_path))
    self.assertTrue(pdf_path.endswith('.pdf'))
```

## Change Log
- 2025-07-26: Inicijalna verzija dokumenta
