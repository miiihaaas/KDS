from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.client import Client, PravnoLice, FizickoLice, RadnaJedinica, LokacijaKuce
from app.utils.client_forms import ClientTypeForm, PravnoLiceForm, FizickoLiceForm
from app.utils.decorators import admin_required
from app.utils.helpers import sanitize_search_term
from sqlalchemy import or_

klijenti_bp = Blueprint('klijenti', __name__, url_prefix='/klijenti')

@klijenti_bp.route('/')
@login_required
def lista():
    """Prikaz liste svih klijenata sa paginacijom i pretragom."""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Inicijalne query za pravna i fizička lica
    pravna_lica_query = PravnoLice.query
    fizicka_lica_query = FizickoLice.query
    
    # Pretraga
    search_term = sanitize_search_term(request.args.get('search', ''))
    if search_term:
        # Pretraga pravnih lica
        pravna_lica_query = pravna_lica_query.filter(
            or_(
                PravnoLice.naziv.ilike(f'%{search_term}%'),
                PravnoLice.adresa.ilike(f'%{search_term}%'),
                PravnoLice.telefon.ilike(f'%{search_term}%'),
                PravnoLice.email.ilike(f'%{search_term}%')
            )
        )
        
        # Pretraga fizičkih lica
        fizicka_lica_query = fizicka_lica_query.filter(
            or_(
                FizickoLice.ime.ilike(f'%{search_term}%'),
                FizickoLice.prezime.ilike(f'%{search_term}%'),
                FizickoLice.adresa.ilike(f'%{search_term}%'),
                FizickoLice.telefon.ilike(f'%{search_term}%'),
                FizickoLice.email.ilike(f'%{search_term}%')
            )
        )
    
    # Dohvatanje rezultata i kombinovanje u jedinstvenu listu
    pravna_lica = pravna_lica_query.all()
    fizicka_lica = fizicka_lica_query.all()
    
    # Kombinovanje pravnih i fizičkih lica u jednu listu
    svi_klijenti = pravna_lica + fizicka_lica
    
    # Sortiranje po nazivu/imenu
    svi_klijenti.sort(key=lambda x: x.naziv if hasattr(x, 'naziv') else x.ime + x.prezime)
    
    # Ručna paginacija
    start = (page - 1) * per_page
    end = start + per_page
    paginated_klijenti = svi_klijenti[start:end]
    
    # Ukupan broj stranica
    total_pages = (len(svi_klijenti) + per_page - 1) // per_page
    
    # Ako je AJAX zahtev, vraćamo samo parcijalni template
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('klijenti/_lista_partial.html', 
                               klijenti=paginated_klijenti,
                               page=page, 
                               total_pages=total_pages,
                               search_term=search_term)
    
    return render_template('klijenti/lista.html', 
                           title='Lista klijenata',
                           klijenti=paginated_klijenti,
                           page=page, 
                           total_pages=total_pages,
                           search_term=search_term)

@klijenti_bp.route('/novi', methods=['GET', 'POST'])
@login_required
def novi_klijent():
    """Kreiranje novog klijenta - prvi korak, izbor tipa klijenta."""
    form = ClientTypeForm()
    
    if form.validate_on_submit():
        tip_klijenta = form.tip_klijenta.data
        # Preusmeravanje na odgovarajuću formu za unos podataka
        return redirect(url_for('klijenti.novi_klijent_podaci', tip=tip_klijenta))
    
    return render_template('klijenti/tip_klijenta.html', 
                           title='Novi klijent - Izbor tipa',
                           form=form)

@klijenti_bp.route('/novi/<tip>', methods=['GET', 'POST'])
@login_required
def novi_klijent_podaci(tip):
    """Kreiranje novog klijenta - drugi korak, unos podataka."""
    breadcrumbs = [
        {'name': 'Klijenti', 'url': url_for('klijenti.lista')},
        {'name': 'Novi klijent', 'url': url_for('klijenti.novi_klijent')},
        {'name': 'Podaci', 'url': None}
    ]
    
    if tip == 'pravno_lice':
        form = PravnoLiceForm()
        template = 'klijenti/form_pravno_lice.html'
        title = 'Novi klijent - Pravno lice'
    elif tip == 'fizicko_lice':
        form = FizickoLiceForm()
        template = 'klijenti/form_fizicko_lice.html'
        title = 'Novi klijent - Fizičko lice'
    else:
        flash('Nepoznat tip klijenta.', 'error')
        return redirect(url_for('klijenti.novi_klijent'))
    
    if form.validate_on_submit():
        try:
            if tip == 'pravno_lice':
                klijent = PravnoLice(
                    tip=tip,
                    naziv=form.naziv.data,
                    pib=form.pib.data,
                    mb=form.mb.data,
                    adresa=form.adresa.data,
                    mesto=form.mesto.data,
                    postanski_broj=form.postanski_broj.data,
                    drzava=form.drzava.data,
                    telefon=form.telefon.data,
                    email=form.email.data
                )
            else:  # fizicko_lice
                klijent = FizickoLice(
                    tip=tip,
                    ime=form.ime.data,
                    prezime=form.prezime.data,
                    adresa=form.adresa.data,
                    mesto=form.mesto.data,
                    postanski_broj=form.postanski_broj.data,
                    drzava=form.drzava.data,
                    telefon=form.telefon.data,
                    email=form.email.data
                )
            
            db.session.add(klijent)
            db.session.commit()
            
            flash('Klijent je uspešno kreiran.', 'success')
            return redirect(url_for('klijenti.lista'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri kreiranju klijenta: {str(e)}', 'error')
    
    return render_template(template, 
                           title=title,
                           form=form,
                           breadcrumbs=breadcrumbs)

@klijenti_bp.route('/<int:id>', methods=['GET'])
@login_required
def detalji_klijenta(id):
    """Prikaz detalja klijenta."""
    # Pokušaj da nađemo klijenta - prvo u pravnim licima, pa u fizičkim licima
    klijent = PravnoLice.query.get(id)
    if not klijent:
        klijent = FizickoLice.query.get(id)
        if not klijent:
            flash('Klijent nije pronađen.', 'error')
            return redirect(url_for('klijenti.lista'))
    
    # Gradimo breadcrumb navigaciju
    breadcrumbs = [
        {'name': 'Klijenti', 'url': url_for('klijenti.lista')},
        {'name': klijent.naziv if hasattr(klijent, 'naziv') else klijent.get_full_name(), 'url': None}
    ]
    
    if isinstance(klijent, PravnoLice):
        return render_template('klijenti/detalji_pravno_lice.html',
                              title='Detalji klijenta',
                              klijent=klijent,
                              breadcrumbs=breadcrumbs)
    else:
        return render_template('klijenti/detalji_fizicko_lice.html',
                              title='Detalji klijenta',
                              klijent=klijent,
                              breadcrumbs=breadcrumbs)

@klijenti_bp.route('/<int:id>/izmeni', methods=['GET', 'POST'])
@login_required
def izmeni_klijenta(id):
    """Izmena postojećeg klijenta."""
    # Pokušaj da nađemo klijenta - prvo u pravnim licima, pa u fizičkim licima
    klijent = PravnoLice.query.get(id)
    if klijent:
        tip = 'pravno_lice'
        form = PravnoLiceForm(original_pib=klijent.pib, original_mb=klijent.mb, original_email=klijent.email)
        template = 'klijenti/form_pravno_lice.html'
    else:
        klijent = FizickoLice.query.get(id)
        if klijent:
            tip = 'fizicko_lice'
            form = FizickoLiceForm()
            template = 'klijenti/form_fizicko_lice.html'
        else:
            flash('Klijent nije pronađen.', 'error')
            return redirect(url_for('klijenti.lista'))
    
    # Breadcrumb navigacija
    breadcrumbs = [
        {'name': 'Klijenti', 'url': url_for('klijenti.lista')},
        {'name': klijent.naziv if hasattr(klijent, 'naziv') else klijent.get_full_name(), 
         'url': url_for('klijenti.detalji_klijenta', id=klijent.id)},
        {'name': 'Izmena', 'url': None}
    ]
    
    if request.method == 'GET':
        # Popunjavamo formu sa postojećim podacima
        if tip == 'pravno_lice':
            form.naziv.data = klijent.naziv
            form.pib.data = klijent.pib
            form.mb.data = klijent.mb
        else:  # fizicko_lice
            form.ime.data = klijent.ime
            form.prezime.data = klijent.prezime
        
        # Zajednička polja za oba tipa klijenta
        form.adresa.data = klijent.adresa
        form.mesto.data = klijent.mesto
        form.postanski_broj.data = klijent.postanski_broj
        form.drzava.data = klijent.drzava
        form.telefon.data = klijent.telefon
        form.email.data = klijent.email
    
    if form.validate_on_submit():
        try:
            if tip == 'pravno_lice':
                klijent.naziv = form.naziv.data
                klijent.pib = form.pib.data
                klijent.mb = form.mb.data
            else:  # fizicko_lice
                klijent.ime = form.ime.data
                klijent.prezime = form.prezime.data
            
            # Ažuriranje zajedničkih polja
            klijent.adresa = form.adresa.data
            klijent.mesto = form.mesto.data
            klijent.postanski_broj = form.postanski_broj.data
            klijent.drzava = form.drzava.data
            klijent.telefon = form.telefon.data
            klijent.email = form.email.data
            
            db.session.commit()
            flash('Podaci o klijentu su uspešno ažurirani.', 'success')
            return redirect(url_for('klijenti.detalji_klijenta', id=klijent.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri ažuriranju klijenta: {str(e)}', 'error')
    
    title = f'Izmena klijenta - {klijent.naziv if hasattr(klijent, "naziv") else klijent.get_full_name()}'
    return render_template(template, 
                           title=title,
                           form=form,
                           klijent=klijent,
                           izmena=True,
                           breadcrumbs=breadcrumbs)

@klijenti_bp.route('/pretraga')
@login_required
def pretraga():
    """AJAX endpoint za pretragu klijenata."""
    search_term = sanitize_search_term(request.args.get('term', ''))
    
    # Ako je prazan upit, vraćamo prazan rezultat
    if not search_term:
        return jsonify([])
    
    # Pretraga pravnih lica
    pravna_lica = PravnoLice.query.filter(
        or_(
            PravnoLice.naziv.ilike(f'%{search_term}%'),
            PravnoLice.adresa.ilike(f'%{search_term}%'),
            PravnoLice.mesto.ilike(f'%{search_term}%'),
            PravnoLice.telefon.ilike(f'%{search_term}%'),
            PravnoLice.email.ilike(f'%{search_term}%')
        )
    ).all()
    
    # Pretraga fizičkih lica
    fizicka_lica = FizickoLice.query.filter(
        or_(
            FizickoLice.ime.ilike(f'%{search_term}%'),
            FizickoLice.prezime.ilike(f'%{search_term}%'),
            FizickoLice.adresa.ilike(f'%{search_term}%'),
            FizickoLice.mesto.ilike(f'%{search_term}%'),
            FizickoLice.telefon.ilike(f'%{search_term}%'),
            FizickoLice.email.ilike(f'%{search_term}%')
        )
    ).all()
    
    # Formatiranje rezultata za JSON odgovor
    rezultati = []
    
    for klijent in pravna_lica:
        rezultati.append({
            'id': klijent.id,
            'naziv': klijent.naziv,
            'tip': 'pravno_lice',
            'adresa': klijent.adresa,
            'telefon': klijent.telefon,
            'email': klijent.email
        })
    
    for klijent in fizicka_lica:
        rezultati.append({
            'id': klijent.id,
            'naziv': f"{klijent.ime} {klijent.prezime}",
            'tip': 'fizicko_lice',
            'adresa': klijent.adresa,
            'telefon': klijent.telefon,
            'email': klijent.email
        })
    
    return jsonify(rezultati)
