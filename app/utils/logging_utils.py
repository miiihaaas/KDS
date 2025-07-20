import logging
from datetime import datetime
from flask import request
import os

# Konfiguracija logging-a
def setup_auth_logger():
    """Postavlja logger za autentifikaciju."""
    logger = logging.getLogger('auth')
    logger.setLevel(logging.INFO)
    
    # Kreiraj direktorijum za logove ako ne postoji
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # File handler za auth logove
    log_file = os.path.join(log_dir, 'auth.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Format za logove
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Dodaj handler samo ako već nije dodat
    if not logger.handlers:
        logger.addHandler(file_handler)
    
    return logger

def log_failed_login_attempt(email, reason="Neispravni kredencijali"):
    """
    Loguje neuspešan pokušaj prijavljivanja.
    
    Args:
        email (str): Email adresa korisnika
        reason (str): Razlog neuspešnog pokušaja
    """
    logger = setup_auth_logger()
    
    # Dobij IP adresu korisnika
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'Unknown'))
    
    # Loguj neuspešan pokušaj
    logger.warning(
        f"Neuspešan pokušaj prijavljivanja - Email: {email} | IP: {ip_address} | Razlog: {reason}"
    )

def log_successful_login(email):
    """
    Loguje uspešan pokušaj prijavljivanja.
    
    Args:
        email (str): Email adresa korisnika
    """
    logger = setup_auth_logger()
    
    # Dobij IP adresu korisnika
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'Unknown'))
    
    # Loguj uspešan pokušaj
    logger.info(
        f"Uspešno prijavljivanje - Email: {email} | IP: {ip_address}"
    )

def log_logout(email):
    """
    Loguje odjavljivanje korisnika.
    
    Args:
        email (str): Email adresa korisnika
    """
    logger = setup_auth_logger()
    
    # Dobij IP adresu korisnika
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'Unknown'))
    
    # Loguj odjavljivanje
    logger.info(
        f"Odjavljivanje korisnika - Email: {email} | IP: {ip_address}"
    )
