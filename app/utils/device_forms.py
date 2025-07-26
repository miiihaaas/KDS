from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional
from datetime import datetime
from app.models.device import Uredjaj
from app.models.client import Client
from app import db

class UredjajForm(FlaskForm):
    """Forma za kreiranje i ažuriranje uređaja."""
    tip = SelectField('Tip uređaja*', choices=[
        ('', 'Odaberite tip uređaja'),
        ('rashladna_tehnika', 'Rashladna tehnika'),
        ('grejna_tehnika', 'Grejna tehnika'),
        ('ventilacioni_sistemi', 'Ventilacioni sistemi')
    ], validators=[DataRequired(message='Tip uređaja je obavezan.')])
    
    podtip = SelectField('Podtip uređaja', choices=[], validators=[
        Optional(),
        Length(max=100, message='Podtip može imati najviše 100 karaktera.')
    ])
    
    proizvodjac = StringField('Proizvođač*', validators=[
        DataRequired(message='Proizvođač je obavezan.'),
        Length(min=2, max=255, message='Proizvođač mora imati između 2 i 255 karaktera.')
    ])
    
    model = StringField('Model*', validators=[
        DataRequired(message='Model je obavezan.'),
        Length(min=2, max=255, message='Model mora imati između 2 i 255 karaktera.')
    ])
    
    serijski_broj = StringField('Serijski broj*', validators=[
        DataRequired(message='Serijski broj je obavezan.'),
        Length(min=2, max=100, message='Serijski broj mora imati između 2 i 100 karaktera.')
    ])
    
    inventarski_broj = StringField('Inventarski broj', validators=[
        Optional(),
        Length(max=100, message='Inventarski broj može imati najviše 100 karaktera.')
    ])
    
    godina_proizvodnje = IntegerField('Godina proizvodnje*', validators=[
        DataRequired(message='Godina proizvodnje je obavezna.'),
        NumberRange(min=1900, max=datetime.now().year, 
                   message=f'Godina mora biti između 1900 i {datetime.now().year}.')
    ])
    
    # Hijerarhijski odabir prostorije
    klijent_id = SelectField('Klijent', choices=[], validators=[Optional()])
    lokacija_id = SelectField('Lokacija', choices=[], validators=[Optional()])
    objekat_id = SelectField('Objekat', choices=[], validators=[Optional()])
    prostorija_id = SelectField('Prostorija', choices=[], validators=[Optional()])
    
    submit = SubmitField('Sačuvaj')
    
    def __init__(self, original_sn=None, *args, **kwargs):
        from app.models.device import Uredjaj
        super(UredjajForm, self).__init__(*args, **kwargs)
        self.original_sn = original_sn
        
        # Dinamički popunimo izbor klijenata
        self.klijent_id.choices = [('', 'Odaberite klijenta')] + [
            (str(k.id), k.naziv if hasattr(k, 'naziv') else k.puno_ime)
            for k in db.session.query(Client).all()
        ]
        
        # Postavimo podtipove na osnovu tipa ako postoji
        if 'tip' in self.data and self.data['tip'] in Uredjaj.TIPOVI:
            podtipovi = Uredjaj.TIPOVI[self.data['tip']]
            self.podtip.choices = [('', 'Nije primenljivo')] if not podtipovi else [('', 'Odaberite podtip')] + [(p, p.replace('_', ' ').title()) for p in podtipovi]
        else:
            self.podtip.choices = [('', 'Prvo izaberite tip uređaja')]
    
    def validate_serijski_broj(self, field):
        """Validacija jedinstvenosti serijskog broja."""
        # Proveravamo da li postoji uređaj sa istim serijskim brojem
        if field.data != self.original_sn:
            uredjaj = Uredjaj.query.filter_by(serijski_broj=field.data).first()
            if uredjaj:
                raise ValidationError('Uređaj sa ovim serijskim brojem već postoji.')
    
    def validate_godina_proizvodnje(self, field):
        """Dodatna validacija godine proizvodnje."""
        if field.data > datetime.now().year:
            raise ValidationError('Godina ne može biti u budućnosti.')


class UredjajFilterForm(FlaskForm):
    """Forma za filtriranje uređaja."""
    tip = SelectField('Tip uređaja', choices=[
        ('', 'Svi tipovi'),
        ('rashladna_tehnika', 'Rashladna tehnika'),
        ('grejna_tehnika', 'Grejna tehnika'),
        ('ventilacioni_sistemi', 'Ventilacioni sistemi')
    ], validators=[Optional()])
    
    proizvodjac = StringField('Proizvođač', validators=[Optional()])
    pretraga = StringField('Pretraga', validators=[Optional()])
    
    submit = SubmitField('Filtriraj')


class DodelaUredjajaForm(FlaskForm):
    """Forma za dodelu uređaja prostoriji."""
    uredjaj_id = HiddenField('ID uređaja', validators=[DataRequired()])
    prostorija_id = HiddenField('ID prostorije', validators=[DataRequired()])
    submit = SubmitField('Dodeli uređaj')
