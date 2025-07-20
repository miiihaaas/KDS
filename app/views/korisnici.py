from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import or_

from app import db
from app.models.user import User
from app.utils.decorators import admin_required

# Kreiranje Blueprint-a
korisnici_bp = Blueprint('korisnici', __name__, url_prefix='/korisnici')

@korisnici_bp.route('/')
@login_required
@admin_required
def lista():
    """Prikaz liste korisnika sa opcijom pretrage."""
    # Osnovni query za korisnike, sortiran po imenu i prezimenu
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    
    # Osnovni query
    query = User.query.order_by(User.ime, User.prezime)
    
    # Pretraga ako je uneta
    if search_query:
        query = query.filter(
            or_(
                User.ime.ilike(f'%{search_query}%'),
                User.prezime.ilike(f'%{search_query}%'),
                User.email.ilike(f'%{search_query}%')
            )
        )
    
    # Paginacija - 10 korisnika po stranici
    korisnici = query.paginate(page=page, per_page=10)
    
    # AJAX zahtev vraća samo podatke o korisnicima
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_template('korisnici/_lista_partial.html', korisnici=korisnici)
        return jsonify({'html': html})
    
    # Redovan zahtev vraća kompletnu stranicu
    return render_template('korisnici/lista.html', korisnici=korisnici, search_query=search_query)


@korisnici_bp.route('/novi', methods=['GET', 'POST'])
@login_required
@admin_required
def novi():
    """Kreiranje novog korisnika."""
    if request.method == 'POST':
        # Prikupljanje podataka iz forme
        ime = request.form.get('ime')
        prezime = request.form.get('prezime')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        tip = request.form.get('tip')
        aktivan = True if request.form.get('aktivan') else False
        
        # Validacija
        errors = {}
        
        if not ime or len(ime) < 2:
            errors['ime'] = 'Ime mora imati najmanje 2 karaktera.'
            
        if not prezime or len(prezime) < 2:
            errors['prezime'] = 'Prezime mora imati najmanje 2 karaktera.'
            
        if not email:
            errors['email'] = 'Email adresa je obavezna.'
        elif User.query.filter_by(email=email).first():
            errors['email'] = 'Email adresa je već u upotrebi.'
            
        if not password:
            errors['password'] = 'Lozinka je obavezna.'
        elif len(password) < 8:
            errors['password'] = 'Lozinka mora imati najmanje 8 karaktera.'
            
        if password != password_confirm:
            errors['password_confirm'] = 'Potvrda lozinke se ne podudara.'
            
        if not tip or tip not in ['administrator', 'serviser']:
            errors['tip'] = 'Tip korisnika mora biti administrator ili serviser.'
            
        # Ako postoje greške, vraćamo korisnika na formu sa porukama
        if errors:
            for field, message in errors.items():
                flash(message, 'error')
            return render_template(
                'korisnici/novi.html',
                values={
                    'ime': ime,
                    'prezime': prezime,
                    'email': email,
                    'tip': tip,
                    'aktivan': aktivan
                }
            )
        
        # Kreiranje novog korisnika
        novi_korisnik = User(
            ime=ime,
            prezime=prezime,
            email=email,
            tip=tip,
            aktivan=aktivan
        )
        novi_korisnik.set_password(password)
        
        try:
            db.session.add(novi_korisnik)
            db.session.commit()
            flash('Korisnik je uspešno kreiran.', 'success')
            return redirect(url_for('korisnici.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri kreiranju korisnika: {str(e)}', 'error')
            
    return render_template('korisnici/novi.html')


@korisnici_bp.route('/<int:id>/izmeni', methods=['GET', 'POST'])
@login_required
@admin_required
def izmeni(id):
    """Izmena postojećeg korisnika."""
    korisnik = User.query.get_or_404(id)
    
    if request.method == 'POST':
        # Prikupljanje podataka iz forme
        ime = request.form.get('ime')
        prezime = request.form.get('prezime')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        tip = request.form.get('tip')
        aktivan = True if request.form.get('aktivan') else False
        
        # Validacija
        errors = {}
        
        if not ime or len(ime) < 2:
            errors['ime'] = 'Ime mora imati najmanje 2 karaktera.'
            
        if not prezime or len(prezime) < 2:
            errors['prezime'] = 'Prezime mora imati najmanje 2 karaktera.'
            
        if not email:
            errors['email'] = 'Email adresa je obavezna.'
        elif email != korisnik.email and User.query.filter_by(email=email).first():
            errors['email'] = 'Email adresa je već u upotrebi.'
            
        # Lozinka je opcionalna pri izmeni
        if password:
            if len(password) < 8:
                errors['password'] = 'Lozinka mora imati najmanje 8 karaktera.'
            elif password != password_confirm:
                errors['password_confirm'] = 'Potvrda lozinke se ne podudara.'
                
        if not tip or tip not in ['administrator', 'serviser']:
            errors['tip'] = 'Tip korisnika mora biti administrator ili serviser.'
        
        # Provera da li korisnik pokušava da deaktivira svoj nalog
        if current_user.id == korisnik.id and not aktivan:
            errors['aktivan'] = 'Ne možete deaktivirati sopstveni nalog.'
        
        # Ako postoje greške, vraćamo korisnika na formu sa porukama
        if errors:
            for field, message in errors.items():
                flash(message, 'error')
            return render_template(
                'korisnici/izmeni.html',
                korisnik=korisnik,
                values={
                    'ime': ime,
                    'prezime': prezime,
                    'email': email,
                    'tip': tip,
                    'aktivan': aktivan
                }
            )
        
        # Ažuriranje korisnika
        korisnik.ime = ime
        korisnik.prezime = prezime
        korisnik.email = email
        korisnik.tip = tip
        korisnik.aktivan = aktivan
        
        # Ažuriranje lozinke samo ako je nova lozinka uneta
        if password:
            korisnik.set_password(password)
        
        try:
            db.session.commit()
            flash('Podaci o korisniku su uspešno ažurirani.', 'success')
            return redirect(url_for('korisnici.lista'))
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri ažuriranju korisnika: {str(e)}', 'error')
            
    return render_template('korisnici/izmeni.html', korisnik=korisnik)


@korisnici_bp.route('/<int:id>/status', methods=['POST'])
@login_required
@admin_required
def promeni_status(id):
    """Promena statusa korisnika (aktivacija/deaktivacija)."""
    korisnik = User.query.get_or_404(id)
    
    # Provera da korisnik ne pokušava da deaktivira svoj nalog
    if current_user.id == korisnik.id:
        flash('Ne možete promeniti status sopstvenog naloga.', 'error')
        return redirect(url_for('korisnici.lista'))
    
    # Promena statusa
    novi_status = not korisnik.aktivan
    korisnik.aktivan = novi_status
    
    try:
        db.session.commit()
        status_tekst = "aktiviran" if novi_status else "deaktiviran"
        flash(f'Korisnik je uspešno {status_tekst}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Došlo je do greške pri promeni statusa korisnika: {str(e)}', 'error')
        
    return redirect(url_for('korisnici.lista'))
