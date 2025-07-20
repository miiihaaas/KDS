# Requirements

## Functional
1. **FR1**: Sistem omogućava autentifikaciju sa dva nivoa korisnika (administrator, serviser) sa standardnom opcijom za reset lozinke
2. **FR2**: Administrator može kreirati, editovati i upravljati nalozima servisera
3. **FR3**: Sistem podržava upravljanje podacima o službenim vozilima (marka, model, registracija)
4. **FR4**: Sistem omogućava upravljanje potrošnim materijalima sa karakteristikama (naziv, jedinica mere)
5. **FR5**: Sistem podržava kreiranje i upravljanje klijentima - pravna lica (kompanija > lokacija > objekat > prostorija) i fizička lica (kuća > lokacija > objekat > prostorija)
6. **FR6**: Sistem omogućava registraciju tri tipa HVAC uređaja: rashladna tehnika, grejna tehnika i ventilacioni sistemi sa podtipovima
7. **FR7**: Sistem generiše jedinstvene ID-jeve za uređaje koji se koriste za QR kod funkcionalnnost
8. **FR8**: Sistem omogućava generisanje, štampanje i skeniranje QR kodova za uređaje
9. **FR9**: Skeniranje QR koda prikazuje putanju: Kompanija/Kuća - Lokacija - Objekat - Prostorija - Uređaj
10. **FR10**: Sistem omogućava kreiranje radnih naloga sa tri tipa: servis, popravka, montaža
11. **FR11**: Sistem automatski generiše oznake radnih naloga (RNS, RNP, RNM + godina-broj)
12. **FR12**: Sistem omogućava dodavanje materijala u radne naloge za popravke i montaže
13. **FR13**: Sistem generiše i šalje radne naloge klijentima preko email-a
14. **FR14**: Sistem omogućava praćenje statusa radnih naloga (U radu, Završen, Fakturisan, Otkazan)
15. **FR15**: Sistem omogućava pregled radnih naloga po periodu i klijentima
16. **FR16**: Sistem automatski beleži datum i vreme svake intervencije na uređaju

## Non Functional
1. **NFR1**: Sistem mora biti responzivan i optimizovan za mobilne uređaje (primarno za servisere)
2. **NFR2**: Sistem mora biti kompatibilan sa Chrome, Firefox, Safari, Edge (poslednje 2 verzije)
3. **NFR3**: Vreme odziva sistema mora biti manje od 3 sekunde za osnovne operacije
4. **NFR4**: Sistem mora podržavati kamersku funkcionalnost za QR kod skeniranje
5. **NFR5**: Sistem mora biti dostupan 99.5% vremena tokom radnih sati
6. **NFR6**: Podaci klijenata moraju biti sigurno čuvani u skladu sa GDPR regulations
7. **NFR7**: Sistem mora podržavati paralelno korišćenje od strane više servisera
8. **NFR8**: Email funkcionalnost mora biti pouzdana za slanje radnih naloga
