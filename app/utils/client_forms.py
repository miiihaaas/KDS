from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Optional, Regexp, ValidationError
from app.utils.validators import optional_length, optional_email
from app.models.client import PravnoLice, FizickoLice, Client, RadnaJedinica, Objekat

class ClientBaseForm(FlaskForm):
    """Osnovna forma za kreiranje i ažuriranje klijenata."""
    adresa = StringField('Adresa', validators=[
        DataRequired(message='Adresa je obavezna.'),
        Length(max=255, message='Adresa ne može biti duža od 255 karaktera.')
    ])
    mesto = StringField('Mesto', validators=[
        DataRequired(message='Mesto je obavezno.'),
        Length(max=100, message='Mesto ne može biti duže od 100 karaktera.')
    ])
    postanski_broj = StringField('Poštanski broj', validators=[
        DataRequired(message='Poštanski broj je obavezan.'),
        Length(max=20, message='Poštanski broj ne može biti duži od 20 karaktera.'),
        Regexp(r'^\d+$', message='Poštanski broj mora sadržati samo brojeve.')
    ])
    drzava = StringField('Država', default='Srbija', validators=[
        DataRequired(message='Država je obavezna.'),
        Length(max=100, message='Država ne može biti duža od 100 karaktera.')
    ])
    telefon = StringField('Telefon', validators=[
        DataRequired(message='Telefon je obavezan.'),
        Length(max=50, message='Telefon ne može biti duži od 50 karaktera.'),
        Regexp(r'^[\d\+\-\s\(\)]+$', message='Telefon može sadržati samo brojeve, +, -, razmake i zagrade.')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email je obavezan.'),
        Email(message='Unesite ispravnu email adresu.'),
        Length(max=255, message='Email ne može biti duži od 255 karaktera.')
    ])
    
    submit = SubmitField('Sačuvaj')
    
    def __init__(self, original_email=None, *args, **kwargs):
        super(ClientBaseForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
    
    def validate_email(self, field):
        """Validacija jedinstvenosti email adrese."""
        # Ako se radi o izmeni klijenta, a email se nije promenio, preskačemo validaciju
        if self.original_email and field.data == self.original_email:
            return
        
        # Provera da li već postoji klijent sa istom email adresom
        existing = Client.query.filter_by(email=field.data).first()
        if existing:
            raise ValidationError('Klijent sa ovom email adresom već postoji u sistemu.')

class PravnoLiceForm(ClientBaseForm):
    """Forma za kreiranje i ažuriranje pravnog lica."""
    naziv = StringField('Naziv firme', validators=[
        DataRequired(message='Naziv firme je obavezan.'),
        Length(min=2, max=255, message='Naziv firme mora imati između 2 i 255 karaktera.')
    ])
    pib = StringField('PIB', validators=[
        DataRequired(message='PIB je obavezan.'),
        Length(min=9, max=9, message='PIB mora imati tačno 9 cifara.'),
        Regexp(r'^\d{9}$', message='PIB mora sadržati tačno 9 cifara.')
    ])
    mb = StringField('Matični broj', validators=[
        DataRequired(message='Matični broj je obavezan.'),
        Length(min=8, max=8, message='Matični broj mora imati tačno 8 cifara.'),
        Regexp(r'^\d{8}$', message='Matični broj mora sadržati tačno 8 cifara.')
    ])
    
    def __init__(self, original_pib=None, original_mb=None, *args, **kwargs):
        super(PravnoLiceForm, self).__init__(*args, **kwargs)
        self.original_pib = original_pib
        self.original_mb = original_mb
    
    def validate_pib(self, field):
        """Validacija jedinstvenosti PIB-a."""
        # Ako se radi o izmeni pravnog lica, a PIB se nije promenio, preskačemo validaciju
        if self.original_pib and field.data == self.original_pib:
            return
        
        # Provera da li već postoji pravno lice sa istim PIB-om
        existing = PravnoLice.query.filter_by(pib=field.data).first()
        if existing:
            raise ValidationError('Pravno lice sa ovim PIB-om već postoji u sistemu.')
    
    def validate_mb(self, field):
        """Validacija jedinstvenosti matičnog broja."""
        # Ako se radi o izmeni pravnog lica, a MB se nije promenio, preskačemo validaciju
        if self.original_mb and field.data == self.original_mb:
            return
        
        # Provera da li već postoji pravno lice sa istim matičnim brojem
        existing = PravnoLice.query.filter_by(mb=field.data).first()
        if existing:
            raise ValidationError('Pravno lice sa ovim matičnim brojem već postoji u sistemu.')

class FizickoLiceForm(ClientBaseForm):
    """Forma za kreiranje i ažuriranje fizičkog lica."""
    ime = StringField('Ime', validators=[
        DataRequired(message='Ime je obavezno.'),
        Length(min=2, max=100, message='Ime mora imati između 2 i 100 karaktera.')
    ])
    prezime = StringField('Prezime', validators=[
        DataRequired(message='Prezime je obavezno.'),
        Length(min=2, max=100, message='Prezime mora imati između 2 i 100 karaktera.')
    ])

class ClientTypeForm(FlaskForm):
    """Forma za izbor tipa klijenta."""
    tip_klijenta = RadioField(
        'Tip klijenta',
        choices=[('pravno_lice', 'Pravno lice'), ('fizicko_lice', 'Fizičko lice')],
        validators=[DataRequired(message='Tip klijenta je obavezan.')]
    )
    submit = SubmitField('Nastavi')


class RadnaJedinicaForm(FlaskForm):
    """Forma za kreiranje i ažuriranje radne jedinice."""
    naziv = StringField('Naziv', validators=[
        DataRequired(message='Naziv radne jedinice je obavezan.'),
        Length(min=2, max=255, message='Naziv mora imati između 2 i 255 karaktera.')
    ])
    adresa = StringField('Adresa', validators=[
        DataRequired(message='Adresa je obavezna.'),
        Length(max=255, message='Adresa ne može biti duža od 255 karaktera.')
    ])
    mesto = StringField('Mesto', validators=[
        DataRequired(message='Mesto je obavezno.'),
        Length(max=100, message='Mesto ne može biti duže od 100 karaktera.')
    ])
    postanski_broj = StringField('Poštanski broj', validators=[
        DataRequired(message='Poštanski broj je obavezan.'),
        Length(max=20, message='Poštanski broj ne može biti duži od 20 karaktera.'),
        Regexp(r'^\d+$', message='Poštanski broj mora sadržati samo brojeve.')
    ])
    drzava = StringField('Država', default='Srbija', validators=[
        DataRequired(message='Država je obavezna.'),
        Length(max=100, message='Država ne može biti duža od 100 karaktera.')
    ])
    kontakt_osoba = StringField('Kontakt osoba', validators=[
        optional_length(max=255, message='Kontakt osoba ne može biti duža od 255 karaktera.')
    ])
    telefon = StringField('Telefon', validators=[
        DataRequired(message='Telefon je obavezan.'),
        Length(max=50, message='Telefon ne može biti duži od 50 karaktera.'),
        Regexp(r'^[\d\+\-\s\(\)]+$', message='Telefon može sadržati samo brojeve, +, -, razmake i zagrade.')
    ])
    email = StringField('Email', validators=[
        optional_email(message='Unesite ispravnu email adresu.'),
        optional_length(max=255, message='Email ne može biti duži od 255 karaktera.')
    ])
    napomena = TextAreaField('Napomena', validators=[Optional()])
    submit = SubmitField('Sačuvaj')


class ObjekatForm(FlaskForm):
    """Forma za kreiranje i ažuriranje objekta."""
    naziv = StringField('Naziv objekta', validators=[
        DataRequired(message='Naziv objekta je obavezan.'),
        Length(min=2, max=255, message='Naziv mora imati između 2 i 255 karaktera.')
    ])
    opis = TextAreaField('Opis', validators=[Optional()])
    
    # Dodajemo polje za tip roditelja samo za informaciju, ne za unos
    parent_type = StringField('Tip roditelja', render_kw={'readonly': True}, validators=[Optional()])
    
    # Polje za skriven ID radne jedinice ili lokacije kuće, koje će se popunjavati kroz hidden field u template-u
    radna_jedinica_id = StringField('ID radne jedinice', render_kw={'type': 'hidden'}, validators=[Optional()])
    lokacija_kuce_id = StringField('ID lokacije kuće', render_kw={'type': 'hidden'}, validators=[Optional()])
    
    submit = SubmitField('Sačuvaj')
    
    def validate(self, extra_validators=None):
        """Prilagođena validacija forme da proveri da je postavljen tačno jedan od tipova roditelja."""
        if not super().validate(extra_validators=extra_validators):
            return False
            
        # # Provera da li je postavljen tačno jedan od roditelja
        # has_radna_jedinica = bool(self.radna_jedinica_id.data and self.radna_jedinica_id.data.strip())
        # has_lokacija_kuce = bool(self.lokacija_kuce_id.data and self.lokacija_kuce_id.data.strip())
        
        # if not (has_radna_jedinica or has_lokacija_kuce):
        #     self.naziv.errors.append('Objekat mora biti povezan sa radnom jedinicom ili lokacijom kuće.')
        #     return False
            
        # if has_radna_jedinica and has_lokacija_kuce:
        #     self.naziv.errors.append('Objekat može biti povezan samo sa jednim roditeljem: radnom jedinicom ILI lokacijom kuće.')
        #     return False
            
        return True


class ProstorijaForm(FlaskForm):
    """Forma za kreiranje i ažuriranje prostorije."""
    naziv = StringField('Naziv prostorije', validators=[
        Optional(),
        Length(max=255, message='Naziv ne može biti duži od 255 karaktera.')
    ])
    numericka_oznaka = StringField('Numerička oznaka', validators=[
        Optional(),
        Length(max=50, message='Numerička oznaka ne može biti duža od 50 karaktera.')
    ])
    sprat = StringField('Sprat', validators=[
        optional_length(max=50, message='Sprat ne može biti duži od 50 karaktera.')
    ])
    namena = StringField('Namena', validators=[
        optional_length(max=100, message='Namena ne može biti duža od 100 karaktera.')
    ])
    submit = SubmitField('Sačuvaj')
    
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        
        if not self.naziv.data and not self.numericka_oznaka.data:
            self.naziv.errors.append('Bar jedno od polja Naziv prostorije ili Numerička oznaka mora biti popunjeno.')
            return False
        
        return True


class LokacijaKuceForm(FlaskForm):
    """Forma za kreiranje i ažuriranje lokacije kuće."""
    naziv = StringField('Naziv', validators=[
        DataRequired(message='Naziv lokacije je obavezan.'),
        Length(min=2, max=255, message='Naziv mora imati između 2 i 255 karaktera.')
    ])
    adresa = StringField('Adresa', validators=[
        DataRequired(message='Adresa je obavezna.'),
        Length(max=255, message='Adresa ne može biti duža od 255 karaktera.')
    ])
    mesto = StringField('Mesto', validators=[
        DataRequired(message='Mesto je obavezno.'),
        Length(max=100, message='Mesto ne može biti duže od 100 karaktera.')
    ])
    postanski_broj = StringField('Poštanski broj', validators=[
        DataRequired(message='Poštanski broj je obavezan.'),
        Length(max=20, message='Poštanski broj ne može biti duži od 20 karaktera.'),
        Regexp(r'^\d+$', message='Poštanski broj mora sadržati samo brojeve.')
    ])
    drzava = StringField('Država', default='Srbija', validators=[
        DataRequired(message='Država je obavezna.'),
        Length(max=100, message='Država ne može biti duža od 100 karaktera.')
    ])
    submit = SubmitField('Sačuvaj')
