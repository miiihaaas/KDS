import re
from wtforms.validators import ValidationError

def validate_email(form, field):
    """Validacija email adrese."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, field.data):
        raise ValidationError('Unesite validnu email adresu.')

def validate_password_strength(form, field):
    """Validacija jačine lozinke."""
    password = field.data
    if len(password) < 8:
        raise ValidationError('Lozinka mora imati najmanje 8 karaktera.')
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Lozinka mora sadržavati najmanje jedno veliko slovo.')
    
    if not re.search(r'[a-z]', password):
        raise ValidationError('Lozinka mora sadržavati najmanje jedno malo slovo.')
    
    if not re.search(r'\d', password):
        raise ValidationError('Lozinka mora sadržavati najmanje jedan broj.')

def validate_serbian_name(form, field):
    """Validacija srpskih imena (dozvoljava ćirilicu i latinicu)."""
    name_pattern = r'^[a-zA-ZčćžšđČĆŽŠĐ\s]+$'
    if not re.match(name_pattern, field.data):
        raise ValidationError('Ime može sadržavati samo slova i razmake.')
