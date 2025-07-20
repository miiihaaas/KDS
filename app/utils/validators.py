import re
from wtforms.validators import ValidationError, Optional

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

def optional_length(max=-1, min=-1, message=None):
    """Validacija dužine polja koje može biti prazno.
    
    Kombinuje Optional i Length validacije na način koji pravilno validira dužinu
    samo kada polje nije prazno.
    """
    def _optional_length(form, field):
        # Ako je polje prazno, preskači validaciju
        if not field.data or field.data.strip() == '':
            return
            
        # Validacija maksimalne dužine
        if max != -1 and len(field.data) > max:
            msg = message or f'Polje ne može biti duže od {max} karaktera.'
            raise ValidationError(msg)
            
        # Validacija minimalne dužine
        if min != -1 and len(field.data) < min:
            msg = message or f'Polje mora imati najmanje {min} karaktera.'
            raise ValidationError(msg)
            
    return _optional_length

def optional_email(message=None):
    """Validacija email adrese za polje koje može biti prazno.
    
    Kombinuje Optional i Email validacije tako da validira format emaila
    samo kada polje nije prazno.
    """
    def _optional_email(form, field):
        # Ako je polje prazno, preskači validaciju
        if not field.data or field.data.strip() == '':
            return
            
        # Validacija email formata
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, field.data):
            msg = message or 'Unesite ispravnu email adresu.'
            raise ValidationError(msg)
            
    return _optional_email
