from flask import flash
from flask_login import login_user, logout_user, current_user
from app.models.user import User
from app.utils.logging_utils import log_failed_login_attempt, log_successful_login, log_logout
from app import db

class AuthService:
    """Servis za autentifikaciju korisnika."""
    
    @staticmethod
    def authenticate_user(email, password, remember_me=False):
        """
        Autentifikuje korisnika na osnovu email-a i lozinke.
        
        Args:
            email (str): Email adresa korisnika
            password (str): Lozinka korisnika
            remember_me (bool): Da li da zapamti korisnika
            
        Returns:
            bool: True ako je autentifikacija uspešna, False inače
        """
        try:
            # Pronađi korisnika po email-u
            user = User.query.filter_by(email=email.lower().strip()).first()
            
            if not user:
                log_failed_login_attempt(email, "Korisnik ne postoji")
                flash('Neispravni kredencijali.', 'error')
                return False
            
            # Proveri da li je nalog aktivan
            if not user.aktivan:
                log_failed_login_attempt(email, "Nalog je deaktiviran")
                flash('Vaš nalog je deaktiviran. Kontaktirajte administratora.', 'error')
                return False
            
            # Proveri lozinku
            if not user.check_password(password):
                log_failed_login_attempt(email, "Neispravna lozinka")
                flash('Neispravni kredencijali.', 'error')
                return False
            
            # Prijavi korisnika
            login_user(user, remember=remember_me, duration=None if not remember_me else None)
            log_successful_login(email)
            flash(f'Dobrodošli, {user.get_full_name()}!', 'success')
            return True
            
        except Exception as e:
            log_failed_login_attempt(email, f"Sistemska greška: {str(e)}")
            flash('Došlo je do greške pri prijavljivanju. Pokušajte ponovo.', 'error')
            return False
    
    @staticmethod
    def logout_user_session():
        """Odjavljuje korisnika iz sistema."""
        try:
            # Loguj odjavljivanje pre nego što se korisnik odjavi
            if current_user.is_authenticated:
                log_logout(current_user.email)
            
            logout_user()
            flash('Uspešno ste se odjavili.', 'info')
            return True
        except Exception as e:
            flash('Došlo je do greške pri odjavljivanju.', 'error')
            return False
    
    @staticmethod
    def create_user(ime, prezime, email, password, tip='serviser'):
        """
        Kreira novog korisnika.
        
        Args:
            ime (str): Ime korisnika
            prezime (str): Prezime korisnika
            email (str): Email adresa
            password (str): Lozinka
            tip (str): Tip korisnika ('administrator' ili 'serviser')
            
        Returns:
            User: Kreiran korisnik ili None ako je došlo do greške
        """
        try:
            # Proveri da li već postoji korisnik sa istim email-om
            existing_user = User.query.filter_by(email=email.lower().strip()).first()
            if existing_user:
                flash('Korisnik sa ovom email adresom već postoji.', 'error')
                return None
            
            # Kreiraj novog korisnika
            user = User(
                ime=ime.strip(),
                prezime=prezime.strip(),
                email=email.lower().strip(),
                tip=tip,
                aktivan=True
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'Korisnik {user.get_full_name()} je uspešno kreiran.', 'success')
            return user
            
        except Exception as e:
            db.session.rollback()
            flash('Došlo je do greške pri kreiranju korisnika.', 'error')
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """Pronalazi korisnika po email adresi."""
        return User.query.filter_by(email=email.lower().strip()).first()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Pronalazi korisnika po ID-u."""
        return User.query.get(user_id)
