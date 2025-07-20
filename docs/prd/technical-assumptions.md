# Technical Assumptions

## Repository Structure: Monorepo
Jednostavna monorepo struktura sa Flask backend-om i frontend template-ima u istom projektu.

## Service Architecture
Monolitna aplikacija za MVP sa jasno definisanim modulima za buduće skaliranje.

## Testing Requirements
- Unit testiranje za kritične business logike
- Integration testiranje za email i QR kod funkcionalnosti
- Manual testiranje za korisničko iskustvo

## Additional Technical Assumptions and Requests
- **Backend Framework**: Flask (Python) za REST API
- **Database**: MySQL za perzistentnu storage
- **Frontend**: HTML, CSS, Bootstrap za responsive design
- **QR Code Library**: Python QR kod biblioteka za generisanje
- **Email Service**: SMTP konfiguracija za slanje email-ova
- **Image Processing**: Podrška za QR kod skeniranje preko web kamera
- **Authentication**: Session-based autentifikacija sa sigurnim password handling
- **File Storage**: Lokalno storage za QR kod slike
- **Printing Integration**: Podrška za portabilne štampače
