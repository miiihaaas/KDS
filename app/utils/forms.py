from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from app.models.vehicle import Vehicle
from app.models.material import Material

class VehicleForm(FlaskForm):
    """Forma za kreiranje i ažuriranje vozila."""
    marka = StringField('Marka vozila', validators=[
        DataRequired(message='Marka vozila je obavezna.'), 
        Length(min=2, max=100, message='Marka vozila mora imati između 2 i 100 karaktera.')
    ])
    model = StringField('Model vozila', validators=[
        DataRequired(message='Model vozila je obavezan.'), 
        Length(min=2, max=100, message='Model vozila mora imati između 2 i 100 karaktera.')
    ])
    registracija = StringField('Registarska oznaka', validators=[
        DataRequired(message='Registarska oznaka je obavezna.'), 
        Length(min=2, max=20, message='Registarska oznaka mora imati između 2 i 20 karaktera.'),
        Regexp(r'^[A-ZŠĐČĆŽ0-9\-\s]+$', message='Registarska oznaka može sadržati samo velika slova, brojeve, crtice i razmake.')
    ])
    active = BooleanField('Aktivno', default=True)
    submit = SubmitField('Sačuvaj')
    
    def __init__(self, original_reg=None, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.original_reg = original_reg
    
    def validate_registracija(self, field):
        """Validacija jedinstvenosti registarske oznake."""
        # Ako se radi o izmeni vozila, a registracija se nije promenila, preskačemo validaciju
        if self.original_reg and field.data.upper() == self.original_reg.upper():
            return
        
        # Provera da li već postoji vozilo sa istom registarskom oznakom (ne osetljivo na velika/mala slova)
        existing = Vehicle.query.filter(Vehicle.registracija.ilike(field.data)).first()
        if existing:
            raise ValidationError('Vozilo sa ovom registarskom oznakom već postoji u sistemu.')


class MaterialForm(FlaskForm):
    """Forma za kreiranje i ažuriranje potrošnog materijala."""
    naziv = StringField('Naziv materijala', validators=[
        DataRequired(message='Naziv materijala je obavezan.'), 
        Length(min=2, max=100, message='Naziv materijala mora imati između 2 i 100 karaktera.')
    ])
    jedinica_mere = SelectField('Jedinica mere', 
        choices=[
            ('kg', 'kg'), 
            ('g', 'g'), 
            ('l', 'l'), 
            ('ml', 'ml'), 
            ('kom', 'kom'), 
            ('m', 'm'), 
            ('m²', 'm²')
        ],
        validators=[DataRequired(message='Jedinica mere je obavezna.')]
    )
    active = BooleanField('Aktivno', default=True)
    submit = SubmitField('Sačuvaj')
    
    def __init__(self, original_naziv=None, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.original_naziv = original_naziv
    
    def validate_naziv(self, field):
        """Validacija jedinstvenosti naziva materijala."""
        # Ako se radi o izmeni materijala, a naziv se nije promenio, preskačemo validaciju
        if self.original_naziv and field.data.lower() == self.original_naziv.lower():
            return
        
        # Provera da li već postoji materijal sa istim nazivom (ne osetljivo na velika/mala slova)
        existing = Material.query.filter(Material.naziv.ilike(field.data)).first()
        if existing:
            raise ValidationError('Materijal sa ovim nazivom već postoji u sistemu.')
