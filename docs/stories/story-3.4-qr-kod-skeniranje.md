# Story 3.4: QR kod skeniranje

## Metadata
- **Story ID**: 3.4
- **Epic**: Epic 3 - Upravljanje uređajima i QR kodovima
- **Priority**: High
- **Story Points**: 5
- **Status**: Draft
- **Created**: 2025-07-27
- **Assigned To**: AI Developer


## Business Context
Nakon što je implementirano generisanje QR kodova za uređaje u Story 3.3, potrebno je omogućiti serviserima da te kodove skeniraju na terenu. Ova funkcionalnost je ključna za efikasno izvođenje servisnih aktivnosti, jer omogućava brz pristup svim relevantnim informacijama o uređaju bez potrebe za ručnom pretragom ili unošenjem identifikatora. Skeniranje QR koda treba da omogući direktno učitavanje stranice sa detaljima uređaja, istorijom servisa i mogućnošću kreiranja novog radnog naloga za taj uređaj, što značajno ubrzava radne procese na terenu.

## Story
**As a** serviser,  
**I want to** scan QR codes,  
**so that** I can quickly access device information.

## Acceptance Criteria

### AC1: Dostupnost Camera interface-a
- **Given** da je serviser prijavljen u sistem
- **When** navigira na stranicu za skeniranje QR koda
- **Then** sistem prikazuje pristupačan Camera interface za skeniranje
- **And** traži dozvolu za pristup kameri ako nije prethodno odobrena

### AC2: Učitavanje podataka o uređaju
- **Given** da je serviser aktivirao camera interface
- **When** skenira QR kod postavljen na uređaju
- **Then** sistem identifikuje uređaj na osnovu skeniranog koda
- **And** učitava stranicu sa detaljima tog uređaja

### AC3: Prikaz putanje navigacije
- **Given** da je serviser skenirao QR kod uređaja
- **When** sistem učita stranicu uređaja
- **Then** breadcrumb navigacija prikazuje punu putanju do uređaja (Objekat > Prostorija > Uređaj)

### AC4: Prikaz istorije servisa
- **Given** da je serviser skenirao QR kod uređaja
- **When** sistem učita stranicu uređaja
- **Then** stranica prikazuje prethodnu istoriju servisa za taj uređaj
- **And** serviser može videti detalje prethodnih servisa

### AC5: Kreiranje novog radnog naloga
- **Given** da je serviser pregledao podatke o uređaju nakon skeniranja QR koda
- **When** klikne na opciju "Kreiraj radni nalog"
- **Then** sistem otvara formu za kreiranje novog radnog naloga
- **And** automatski povezuje nalog sa tim uređajem

## Tasks / Subtasks
- [ ] Implementacija Camera interface-a (AC1)
  - [ ] Istražiti biblioteke za pristup kameri putem web browsera (npr. MediaDevices API)
  - [ ] Implementirati komponentu za pristup i prikaz video streama sa kamere
  - [ ] Implementirati proveru i traženje dozvole za pristup kameri
  - [ ] Implementirati fallback opciju ako kamera nije dostupna ili dozvoljena

- [ ] Implementacija QR kod skeniranja (AC2)
  - [ ] Istražiti JavaScript biblioteke za dekodiranje QR kodova (npr. jsQR, ZXing)
  - [ ] Implementirati funkcionalnost za prepoznavanje i dekodiranje QR koda iz video streama
  - [ ] Implementirati ekstrakciju ID-a uređaja iz skeniranog QR koda
  - [ ] Implementirati redirekciju na stranicu uređaja nakon uspešnog skeniranja

- [ ] Unapređenje prikaza detalja uređaja (AC3, AC4)
  - [ ] Implementirati breadcrumb navigaciju koja prikazuje hijerarhiju (Objekat > Prostorija > Uređaj)
  - [ ] Optimizovati prikaz istorije servisa za brzo učitavanje nakon skeniranja
  - [ ] Implementirati sortiranje i filtriranje istorije servisa

- [ ] Integracija sa sistemom radnih naloga (AC5)
  - [ ] Dodati dugme "Kreiraj radni nalog" na stranicu detalja uređaja
  - [ ] Implementirati automatsko popunjavanje reference na uređaj u formi za kreiranje radnog naloga
  - [ ] Implementirati brzi workflow za kreiranje radnog naloga iz konteksta skeniranog uređaja

- [ ] Testiranje
  - [ ] Testirati kompatibilnost Camera interface-a sa različitim browserima
  - [ ] Testirati prepoznavanje QR kodova u različitim svetlosnim uslovima
  - [ ] Testirati ceo workflow od skeniranja do kreiranja radnog naloga
  - [ ] Implementirati unit i integracija testove

## Dev Notes
### Ključne implementacione tačke
- QR kod skeniranje će se implementirati na klijentskoj strani koristeći JavaScript biblioteke
- Za pristup kameri koristiti MediaDevices API i getUserMedia() funkciju
- Za dekodiranje QR kodova iz video streama koristiti jsQR biblioteku
- Skeniranje treba da radi i na mobilnim uređajima za terenski rad

### Tehnička implementacija
#### Frontend
```javascript
// Primer implementacije Camera interface-a
async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
    const videoElement = document.getElementById('qr-video');
    videoElement.srcObject = stream;
    videoElement.play();
    startScanningQR(videoElement);
  } catch (error) {
    console.error("Greška pri pristupu kameri:", error);
    showFallbackOptions();
  }
}

// Primer implementacije QR skener funkcije
function startScanningQR(videoElement) {
  const canvas = document.createElement('canvas');
  const canvasContext = canvas.getContext('2d');
  
  setInterval(() => {
    if (videoElement.readyState === videoElement.HAVE_ENOUGH_DATA) {
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      canvasContext.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
      
      const imageData = canvasContext.getImageData(0, 0, canvas.width, canvas.height);
      const code = jsQR(imageData.data, imageData.width, imageData.height);
      
      if (code) {
        // QR kod je pronađen, ekstraktuj ID uređaja
        const deviceId = code.data;
        window.location.href = `/uredjaji/${deviceId}?source=qr_scan`;
      }
    }
  }, 100); // Proveravaj svakih 100ms
}
```

#### Backend rute
```python
@bp.route('/skeniraj', methods=['GET'])
@login_required
def skeniraj_qr_kod():
    """Prikazuje interfejs za skeniranje QR koda."""
    return render_template('uredjaji/skeniraj_qr.html')

@bp.route('/<int:id>', methods=['GET'])
@login_required
def detalji_uredjaja(id):
    """Prikazuje detalje uređaja, uključujući istoriju servisa."""
    uredjaj = Uredjaj.query.get_or_404(id)
    
    # Učitaj istoriju servisa
    servisi = RadniNalog.query.filter_by(uredjaj_id=id).order_by(RadniNalog.datum_kreiranja.desc()).all()
    
    # Dobavi informacije za breadcrumb navigaciju
    prostorija = uredjaj.prostorija
    objekat = prostorija.objekat if prostorija else None
    
    return render_template('uredjaji/detalji.html',
                          uredjaj=uredjaj,
                          servisi=servisi,
                          prostorija=prostorija,
                          objekat=objekat,
                          skenirano=request.args.get('source') == 'qr_scan')
```

### Potrebne biblioteke
- jsQR: JavaScript biblioteka za dekodiranje QR kodova
- Flask-WTF: Za obradu formi i CSRF zaštitu
- Potrebne izmene u postojećim Flask rutama za rad sa uređajima

## Testing
### Unit i integracija testovi
- Implementirati pytest testove za backend rute
- Implementirati JavaScript testove za frontend QR skeniranje
- Testirati ceo workflow od skeniranja do prikaza detalja uređaja

### Testiranje korisničkog interfejsa
- Testirati kompatibilnost sa različitim browserima (Chrome, Firefox, Safari)
- Testirati responsivnost na desktop i mobilnim uređajima
- Testirati brzinu i tačnost prepoznavanja QR kodova

## Change Log
| Datum | Verzija | Opis | Autor |
|-------|---------|------|-------|
| 2025-07-27 | 1.0 | Inicijalni draft story-ja | Scrum Master Bob |
