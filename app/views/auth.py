from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from app.services.auth_service import AuthService
from app.utils.validators import validate_email
from urllib.parse import urlparse, urljoin

auth_bp = Blueprint('auth', __name__)

def is_safe_url(target):
    """Proverava da li je URL bezbedan za redirect."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

class LoginForm(FlaskForm):
    """Forma za prijavljivanje korisnika."""
    email = StringField('Email adresa', validators=[
        DataRequired(message='Email adresa je obavezna.'),
        Email(message='Unesite validnu email adresu.'),
        Length(max=255, message='Email adresa ne može biti duža od 255 karaktera.')
    ])
    password = PasswordField('Lozinka', validators=[
        DataRequired(message='Lozinka je obavezna.'),
        Length(min=1, max=255, message='Lozinka mora biti između 1 i 255 karaktera.')
    ])
    remember_me = BooleanField('Zapamti me')
    submit = SubmitField('Prijaviť se')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Stranica za prijavljivanje korisnika."""
    # Ako je korisnik već prijavljen, preusmeri ga na dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        
        # Pokušaj autentifikacije
        if AuthService.authenticate_user(email, password, remember_me):
            # Uspešna autentifikacija - preusmeri na odgovarajuću stranicu
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
    
    return render_template('auth/login.html', form=form, title='Prijavljivanje')

@auth_bp.route('/logout')
@login_required
def logout():
    """Odjavljivanje korisnika."""
    AuthService.logout_user_session()
    return redirect(url_for('auth.login'))
