# Story 3.3: QR kod generisanje

## Metadata
- **Story ID**: 3.3
- **Epic**: Epic 3 - Upravljanje uređajima i QR kodovima
- **Priority**: Medium
- **Story Points**: 3
- **Status**: Done
- **Created**: 2025-07-27
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
- [x] Implementacija generisanja QR koda
  - [x] Istražiti biblioteke za generisanje QR koda u Python-u (npr. qrcode, pyqrcode)
  - [x] Implementirati pomoćnu funkciju za dinamičko generisanje QR koda sa jedinstvenim ID-jem uređaja
  - [x] Podesiti generisanje QR koda direktno u memoriji bez čuvanja na disk

- [x] Implementacija korisničkog interfejsa
  - [x] Dodati prikaz QR koda na stranici detalja uređaja
  - [x] Implementirati dijalog za izbor broja kopija za štampanje
  - [x] Kreirati UI komponentu za prikaz QR koda

- [x] Implementacija PDF generisanja za štampanje
  - [x] Implementirati funkcionalnost za generisanje PDF-a sa QR kodom koristeći fpdf2
  - [x] Optimizovati format za štampanje na portabl štampačima i nalepnicama (57mm x 32mm)
  - [x] Dodati osnovne informacije o uređaju na PDF uz optimalan raspored za male nalepnice
  - [x] Obezbediti da se više kopija istog QR koda može štampati na jednom PDF-u
  - [x] Implementirati čišćenje privremenih fajlova nakon slanja
  - [x] Dodati podršku za Unicode fontove (čćžšđ) u PDF-u
  - [x] Izmeniti generisanje PDF-a da se otvara u novom tabu (stream iz memorije, bez čuvanja na disku)

- [x] Testiranje
  - [x] Testirati automatsko generisanje QR koda pri kreiranju uređaja
  - [x] Testirati čitljivost generisanih QR kodova sa različitim QR čitačima
  - [x] Testirati generisanje PDF-a sa različitim brojem kopija
  - [x] Testirati ponovno štampanje QR kodova za postojeće uređaje

## Dev Notes
### Ključne implementacione tačke
- Koristiti biblioteku `qrcode` za dinamičko generisanje QR kodova bez čuvanja na disku
- QR kod treba da sadrži samo jedinstveni ID uređaja, ne sve podatke (radi optimalne veličine i čitljivosti)
- PDF dokument mora biti optimizovan za štampu na portabl štampačima koristeći `fpdf2` biblioteku
- Podesiti dimenzije PDF-a prema standardnim dimenzijama nalepnica koje se koriste na portabl štampačima (tipično 57mm x 32mm)
- Koristiti privremene fajlove (`tempfile`) za međukorak pri generisanju PDF-a umesto čuvanja trajnih fajlova
- Izbrisati privremene fajlove nakon slanja PDF-a korisniku

### Generisanje QR koda (dinamičko)
Pošto ne čuvamo QR kodove u aplikaciji, već ih generišemo po potrebi, implementiraćemo pomoćne funkcije za generisanje QR koda:

```python
def generisi_qr_kod_za_uredjaj(uredjaj_id):
    """
    Dinamički generiše QR kod za uređaj bez čuvanja slike na disku.
    Vraća QR kod kao BytesIO objekat koji se može koristiti za prikaz ili generisanje PDF-a.
    """
    import qrcode
    from io import BytesIO
    
    # Generisanje QR koda sa ID-jem uređaja
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(uredjaj_id))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Čuvanje QR koda u memoriji umesto na disku
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer
```

### Generisanje PDF-a za štampanje na portabl štampačima
Za generisanje PDF-a sa QR kodom koristiti fpdf2 biblioteku, optimizovano za portabl štampače:

```python
def generisi_pdf_sa_qr_kodom(uredjaj, broj_kopija=1):
    """
    Generiše PDF sa određenim brojem kopija QR koda za dati uređaj,
    optimizovan za štampu na portabl štampačima.
    """
    from fpdf import FPDF
    import tempfile
    
    # Kreiranje instance PDF-a sa dimenzijama za standardne nalepnice
    # Tipična nalepnica je 57mm x 32mm
    # Pretvaramo mm u tačke (1mm = 2.83 tačke)
    nalepnica_sirina_mm = 57
    nalepnica_visina_mm = 32
    
    pdf = FPDF(orientation='P', unit='mm', format=(nalepnica_sirina_mm, nalepnica_visina_mm))
    pdf.set_auto_page_break(auto=False)
    pdf.set_margins(2, 2, 2)  # mali margine za maksimalno iskorišćenje prostora
    
    # Za svaku kopiju kreiramo QR kod na novoj stranici
    for _ in range(broj_kopija):
        pdf.add_page()
        
        # Generisanje QR koda direktno - bez čuvanja na disk
        qr_buffer = generisi_qr_kod_za_uredjaj(uredjaj.id)
        
        # Koristimo tempfile za privremeno čuvanje QR koda
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_filename = temp_file.name
            temp_file.write(qr_buffer.getvalue())
        
        # Dodaj informacije o uređaju - optimizovano za malu nalepnicu
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(0, 3, f"ID: {uredjaj.id}", new_x="LMARGIN", new_y="NEXT", align='C')
        
        pdf.set_font('Arial', '', 6)
        pdf.cell(0, 2, f"{uredjaj.proizvodjac} {uredjaj.model}", new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.cell(0, 2, f"S/N: {uredjaj.serijski_broj}", new_x="LMARGIN", new_y="NEXT", align='C')
        
        # Dodaj QR kod centriran
        pdf.image(temp_filename, x=(nalepnica_sirina_mm-20)/2, y=8, w=20, h=20)
        
        # Obrisati privremeni fajl
        import os
        os.unlink(temp_filename)
            
    # Sačuvaj PDF u privremeni fajl
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
        output_path = pdf_file.name
        pdf.output(output_path)
    
    return output_path
```

### Rute za QR kodove
Dodajte nove rute u `uredjaji.py` za dinamičko generisanje QR koda i PDF-a:

```python
@bp.route('/<int:id>/qr_kod')
@login_required
def prikazi_qr_kod(id):
    """Prikazuje QR kod za uređaj."""
    uredjaj = Uredjaj.query.get_or_404(id)
    
    # Dinamički generišemo QR kod
    qr_buffer = generisi_qr_kod_za_uredjaj(uredjaj.id)
    
    # Vraćamo sliku direktno kao response
    return send_file(
        qr_buffer,
        mimetype='image/png',
        download_name=f'qr_kod_uredjaj_{id}.png'
    )

@bp.route('/<int:id>/stampa_qr_kod', methods=['GET', 'POST'])
@login_required
def stampa_qr_kod(id):
    """Prikazuje formu za štampanje QR koda i generiše PDF."""
    uredjaj = Uredjaj.query.get_or_404(id)
    
    if request.method == 'POST':
        broj_kopija = int(request.form.get('broj_kopija', 1))
        pdf_path = generisi_pdf_sa_qr_kodom(uredjaj, broj_kopija)
        
        # Vrati PDF kao download
        response = send_file(
            pdf_path, 
            mimetype='application/pdf',
            as_attachment=True, 
            download_name=f"qr_kod_uredjaj_{id}.pdf"
        )
        
        # Obriši privremeni PDF fajl nakon što je poslat
        @after_this_request
        def remove_file(response):
            try:
                os.unlink(pdf_path)
            except Exception as error:
                app.logger.error(f"Greška pri brisanju privremenog PDF fajla: {error}")
            return response
            
        return response
        
    return render_template('uredjaji/stampa_qr_kod.html', uredjaj=uredjaj)
```

## Testing
### Unit testovi
```python
def test_generisanje_qr_koda(self):
    """Test dinamičkog generisanja QR koda za uređaj."""
    uredjaj = Uredjaj(
        tip='rashladna_tehnika',
        podtip='split_sistem',
        proizvodjac='Test',
        model='Test Model',
        serijski_broj='TEST001'
    )
    db.session.add(uredjaj)
    db.session.commit()
    
    # Testiramo dinamičko generisanje QR koda
    qr_buffer = generisi_qr_kod_za_uredjaj(uredjaj.id)
    self.assertIsNotNone(qr_buffer)
    
    # Proverimo da li je generisan ispravno kao BytesIO objekat
    self.assertTrue(hasattr(qr_buffer, 'getvalue'))
    self.assertGreater(len(qr_buffer.getvalue()), 0)

def test_pdf_sa_qr_kodom(self):
    """Test generisanja PDF-a sa QR kodom za portabl štampu."""
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
    
    # Dodatna provera - veličina PDF-a treba da bude razumna za štampu na portabl štampaču
    file_size = os.path.getsize(pdf_path)
    self.assertLess(file_size, 500 * 1024)  # manje od 500KB
```

## Change Log
- 2025-07-26: Inicijalna verzija dokumenta
- 2025-07-27: Implementacija svih funkcionalnosti
- 2025-07-27: Dodata podrška za Unicode fontove i PDF prikaz u novom tabu
- 2025-07-27: Napisani unit testovi za QR kod funkcionalnost (tests/test_qr_utils.py)

## QA Results
### Status pregleda
- **Datum pregleda**: 2025-07-27
- **Pregledao**: QA Agent Quinn
- **Status**: USPEŠNO ✅

### Testiranje
- Implementirani i uspešno izvršeni pytest testovi u fajlu `tests/test_qr_utils.py`
- Svi testovi prolaze (8 testova, 0 grešaka)
- Testovi pokrivaju sve ključne funkcionalnosti:
  - Generisanje QR koda u memoriji (BytesIO)
  - Generisanje PDF-a sa QR kodom (sa različitim brojem kopija)
  - Rute za prikaz i štampanje QR kodova
  - Mock autentifikacije korisnika

### Kvalitet koda
- Implementacija prati najbolje prakse za rad sa Flask aplikacijom
- Koristi se `BytesIO` za čuvanje podataka u memoriji umesto privremenih fajlova
- Kod je dobro dokumentovan sa docstring komentarima
- Optimizovana veličina i format QR koda za portabl štampače
- Implementirana podrška za srpske karaktere (čćžšđ) kroz DejaVu fontove

### Sigurnost i optimizacija
- PDF se generiše dinamički u memoriji bez trajnog čuvanja na serveru
- Privremeni fajlovi se brišu čak i u slučaju greške (finally blok)
- CSRF zaštita implementirana na formama
- PDF optimizovan za brzo učitavanje i štampanje (mala veličina)

### Preporuke i poboljšanja
- Postoji jedno upozorenje vezano za `uni=True` parametar u `add_font` metodi koji je označen kao zastareo
- Prilagoditi kod da izbegne upozorenja o korišćenju zastarelih API-ja (npr. `Query.get()` -> `Session.get()`)
