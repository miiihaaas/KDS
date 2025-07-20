from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    """
    Dekorator koji zahteva da korisnik ima određenu ulogu.
    
    Args:
        *roles: Lista uloga koje su dozvoljene ('administrator', 'serviser')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Morate se prijaviti da biste pristupili ovoj stranici.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.tip not in roles:
                flash('Nemate dozvolu za pristup ovoj stranici.', 'error')
                abort(403)
            
            if not current_user.aktivan:
                flash('Vaš nalog je deaktiviran. Kontaktirajte administratora.', 'error')
                return redirect(url_for('auth.login'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Dekorator koji zahteva administrator ulogu."""
    return role_required('administrator')(f)

def serviser_required(f):
    """Dekorator koji zahteva serviser ulogu."""
    return role_required('serviser')(f)

def admin_or_serviser_required(f):
    """Dekorator koji zahteva administrator ili serviser ulogu."""
    return role_required('administrator', 'serviser')(f)
