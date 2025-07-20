from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from collections import defaultdict
from app import db
from app.models.client import Client, PravnoLice, FizickoLice, RadnaJedinica, LokacijaKuce, Objekat, Prostorija
from app.utils.client_forms import ClientTypeForm, PravnoLiceForm, FizickoLiceForm, RadnaJedinicaForm, ObjekatForm, ProstorijaForm
from app.utils.decorators import admin_required
from app.utils.helpers import sanitize_search_term
from sqlalchemy import or_

klijenti_bp = Blueprint('klijenti', __name__, url_prefix='/klijenti')

# Pomoćne funkcije za hijerarhiju i breadcrumbs
def generate_hierarchy_tree(pravno_lice_id=None, radna_jedinica_id=None, objekat_id=None, prostorija_id=None):
    """
    Generiše hijerarhijsko stablo entiteta za prikaz u tree-view komponenti.
    Parametri omogućavaju označavanje aktivnog elementa u hijerarhiji.
    """
    tree = []
    
    # Dohvatamo sva pravna lica
    pravna_lica = PravnoLice.query.all()
    
    for pl in pravna_lica:
        pl_node = {
            'id': pl.id,
            'name': pl.naziv,
            'icon': 'bi bi-building',
            'url': url_for('klijenti.detalji_klijenta', id=pl.id),
            'children': []
        }
        
        # Ako je trenutno pravno lice aktivno ili je neki njegov potomak aktivan, popunjavamo hijerarhiju
        is_active = (pl.id == pravno_lice_id) or (pravno_lice_id is None)
        
        # Ako je pravno lice aktivno ili imamo aktivan neki njegov element, učitaj radne jedinice
        if is_active or radna_jedinica_id or objekat_id or prostorija_id:
            for rj in pl.radne_jedinice:
                rj_node = {
                    'id': rj.id,
                    'name': rj.naziv,
                    'icon': 'bi bi-building-gear',
                    'url': url_for('klijenti.detalji_radne_jedinice', id=rj.id),
                    'children': []
                }
                
                # Ako je radna jedinica aktivna ili je neki njen potomak aktivan
                is_rj_active = (rj.id == radna_jedinica_id) or (radna_jedinica_id is None and is_active)
                
                # Ako je radna jedinica aktivna ili imamo aktivan neki njen element, učitaj objekte
                if is_rj_active or objekat_id or prostorija_id:
                    for obj in rj.objekti:
                        obj_node = {
                            'id': obj.id,
                            'name': obj.naziv,
                            'icon': 'bi bi-house-door',
                            'url': url_for('klijenti.detalji_objekta', id=obj.id),
                            'children': []
                        }
                        
                        # Ako je objekat aktivan ili je neka njegova prostorija aktivna
                        is_obj_active = (obj.id == objekat_id) or (objekat_id is None and is_rj_active)
                        
                        # Ako je objekat aktivan ili je neka njegova prostorija aktivna, učitaj prostorije
                        if is_obj_active or prostorija_id:
                            for prostorija in obj.prostorije:
                                prostorija_node = {
                                    'id': prostorija.id,
                                    'name': prostorija.naziv,
                                    'icon': 'bi bi-door-open',
                                    'url': url_for('klijenti.detalji_prostorije', id=prostorija.id),
                                    'children': []
                                }
                                obj_node['children'].append(prostorija_node)
                        
                        rj_node['children'].append(obj_node)
                
                pl_node['children'].append(rj_node)
        
        tree.append(pl_node)
    
    return tree

def generate_breadcrumbs(entity_type, entity=None, parent_ids=None):
    """
    Generiše breadcrumbs za navigaciju.
    entity_type može biti: 'pravno_lice', 'radna_jedinica', 'objekat', 'prostorija'
    entity je instanca odgovarajućeg modela
    parent_ids je rečnik sa id-jevima roditelja kada entitet nije direktno dostupan
    """
    breadcrumbs = [
        {'name': 'Klijenti', 'url': url_for('klijenti.lista')}
    ]
    
    # Za svaki tip entiteta, dodajemo odgovarajuće breadcrumbs
    if entity_type == 'pravno_lice':
        if entity:
            breadcrumbs.append({'name': entity.naziv, 'url': url_for('klijenti.detalji_klijenta', id=entity.id)})
    
    elif entity_type == 'radna_jedinica':
        if entity:
            # Dodajemo pravno lice
            pravno_lice = entity.pravno_lice
            breadcrumbs.append({'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)})
            # Dodajemo radnu jedinicu
            breadcrumbs.append({'name': entity.naziv, 'url': url_for('klijenti.detalji_radne_jedinice', id=entity.id)})
        elif parent_ids and 'pravno_lice_id' in parent_ids:
            pravno_lice = PravnoLice.query.get_or_404(parent_ids['pravno_lice_id'])
            breadcrumbs.append({'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)})
            breadcrumbs.append({'name': 'Radne jedinice', 'url': url_for('klijenti.lista_radnih_jedinica', id=pravno_lice.id)})
    
    elif entity_type == 'objekat':
        if entity:
            # Dodajemo pravno lice
            radna_jedinica = entity.radna_jedinica
            pravno_lice = radna_jedinica.pravno_lice
            breadcrumbs.append({'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)})
            # Dodajemo radnu jedinicu
            breadcrumbs.append({'name': radna_jedinica.naziv, 'url': url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id)})
            # Dodajemo objekat
            breadcrumbs.append({'name': entity.naziv, 'url': url_for('klijenti.detalji_objekta', id=entity.id)})
        elif parent_ids and 'radna_jedinica_id' in parent_ids:
            radna_jedinica = RadnaJedinica.query.get_or_404(parent_ids['radna_jedinica_id'])
            pravno_lice = radna_jedinica.pravno_lice
            breadcrumbs.append({'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)})
            breadcrumbs.append({'name': radna_jedinica.naziv, 'url': url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id)})
            breadcrumbs.append({'name': 'Objekti', 'url': url_for('klijenti.lista_objekata', id=radna_jedinica.id)})
    
    elif entity_type == 'prostorija':
        if entity:
            # Dodajemo pravno lice
            objekat = entity.objekat
            radna_jedinica = objekat.radna_jedinica
            pravno_lice = radna_jedinica.pravno_lice
            breadcrumbs.append({'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)})
            # Dodajemo radnu jedinicu
            breadcrumbs.append({'name': radna_jedinica.naziv, 'url': url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id)})
            # Dodajemo objekat
            breadcrumbs.append({'name': objekat.naziv, 'url': url_for('klijenti.detalji_objekta', id=objekat.id)})
            # Dodajemo prostoriju
            breadcrumbs.append({'name': entity.naziv, 'url': url_for('klijenti.detalji_prostorije', id=entity.id)})
        elif parent_ids and 'objekat_id' in parent_ids:
            objekat = Objekat.query.get_or_404(parent_ids['objekat_id'])
            radna_jedinica = objekat.radna_jedinica
            pravno_lice = radna_jedinica.pravno_lice
            breadcrumbs.append({'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)})
            breadcrumbs.append({'name': radna_jedinica.naziv, 'url': url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id)})
            breadcrumbs.append({'name': objekat.naziv, 'url': url_for('klijenti.detalji_objekta', id=objekat.id)})
            breadcrumbs.append({'name': 'Prostorije', 'url': url_for('klijenti.lista_prostorija', id=objekat.id)})
    
    return breadcrumbs

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
                
                # Dodajemo klijenta u bazu i izvršavamo flush da dobijemo ID
                db.session.add(klijent)
                db.session.flush()  # Dobijamo ID bez komitovanja transakcije
                
                # Automatsko kreiranje radne jedinice "Centrala"
                centrala = RadnaJedinica(
                    naziv='Centrala',
                    adresa=form.adresa.data,
                    mesto=form.mesto.data,
                    postanski_broj=form.postanski_broj.data,
                    drzava=form.drzava.data,
                    telefon=form.telefon.data,
                    email=form.email.data,
                    pravno_lice_id=klijent.id
                )
                db.session.add(centrala)
                
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
            
            # Komitujemo sve promene
            db.session.commit()
            
            if tip == 'pravno_lice':
                flash('Pravno lice je uspešno kreirano sa automatski dodeljenom radnom jedinicom "Centrala".', 'success')
            else:
                flash('Fizičko lice je uspešno kreirano.', 'success')
                
            return redirect(url_for('klijenti.detalji_klijenta', id=klijent.id))
            
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
    
    # Koristimo novu funkciju za breadcrumbs
    if isinstance(klijent, PravnoLice):
        # Gradimo breadcrumb navigaciju
        breadcrumbs = generate_breadcrumbs('pravno_lice', entity=klijent)
        
        # Dohvatamo hijerarhiju za pravno lice
        hierarchy = generate_hierarchy_tree(pravno_lice_id=klijent.id)
        
        # Dohvatamo radne jedinice za prikaz u detaljima
        radne_jedinice = klijent.radne_jedinice
        
        return render_template('klijenti/detalji_pravno_lice.html',
                              title='Detalji klijenta',
                              klijent=klijent,
                              radne_jedinice=radne_jedinice,
                              breadcrumbs=breadcrumbs,
                              hierarchy=hierarchy,
                              active_id=klijent.id)
    else:
        # Gradimo breadcrumb navigaciju
        breadcrumbs = generate_breadcrumbs('fizicko_lice', entity=klijent)
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

@klijenti_bp.route('/pravno-lice/<int:id>/radne-jedinice')
@login_required
def lista_radnih_jedinica(id):
    """Prikaz liste radnih jedinica za pravno lice."""
    pravno_lice = PravnoLice.query.get_or_404(id)
    radne_jedinice = RadnaJedinica.query.filter_by(pravno_lice_id=id).all()
    
    # Koristimo funkciju za generisanje breadcrumbs
    breadcrumbs = generate_breadcrumbs('radna_jedinica', parent_ids={'pravno_lice_id': id})
    
    # Generišemo hijerarhijsko stablo
    hierarchy = generate_hierarchy_tree(pravno_lice_id=id)
    
    return render_template('klijenti/lista_radnih_jedinica.html',
                           title=f'Radne jedinice - {pravno_lice.naziv}',
                           pravno_lice=pravno_lice,
                           radne_jedinice=radne_jedinice,
                           breadcrumbs=breadcrumbs,
                           hierarchy=hierarchy,
                           active_id=id)

@klijenti_bp.route('/pravno-lice/<int:id>/radne-jedinice/novi', methods=['GET', 'POST'])
@login_required
def nova_radna_jedinica(id):
    """Dodavanje nove radne jedinice za pravno lice."""
    pravno_lice = PravnoLice.query.get_or_404(id)
    form = RadnaJedinicaForm()
    
    # Koristimo funkciju za generisanje breadcrumbs
    breadcrumbs = generate_breadcrumbs('radna_jedinica', parent_ids={'pravno_lice_id': id})
    # Dodajemo informaciju o novoj radnoj jedinici
    breadcrumbs.append({'name': 'Nova', 'url': None})
    
    # Generišemo hijerarhijsko stablo
    hierarchy = generate_hierarchy_tree(pravno_lice_id=id)
    
    if form.validate_on_submit():
        try:
            radna_jedinica = RadnaJedinica(
                pravno_lice_id=pravno_lice.id,
                naziv=form.naziv.data,
                adresa=form.adresa.data,
                mesto=form.mesto.data,
                postanski_broj=form.postanski_broj.data,
                drzava=form.drzava.data,
                kontakt_osoba=form.kontakt_osoba.data,
                telefon=form.telefon.data,
                email=form.email.data,
                napomena=form.napomena.data
            )
            
            db.session.add(radna_jedinica)
            db.session.commit()
            
            flash('Nova radna jedinica je uspešno dodata.', 'success')
            return redirect(url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri kreiranju radne jedinice: {str(e)}', 'error')
    
    return render_template('klijenti/radna_jedinica_form.html',
                          title=f'Nova radna jedinica - {pravno_lice.naziv}',
                          form=form,
                          pravno_lice=pravno_lice,
                          breadcrumbs=breadcrumbs,
                          hierarchy=hierarchy,
                          active_id=id)

@klijenti_bp.route('/radna-jedinica/<int:id>', methods=['GET'])
@login_required
def detalji_radne_jedinice(id):
    """Prikaz detalja radne jedinice."""
    radna_jedinica = RadnaJedinica.query.get_or_404(id)
    pravno_lice = radna_jedinica.pravno_lice
    objekti = Objekat.query.filter_by(radna_jedinica_id=id).all()
    
    # Koristimo funkciju za generisanje breadcrumbs
    breadcrumbs = generate_breadcrumbs('radna_jedinica', entity=radna_jedinica)
    
    # Generišemo hijerarhijsko stablo
    hierarchy = generate_hierarchy_tree(pravno_lice_id=pravno_lice.id, radna_jedinica_id=id)
    
    return render_template('klijenti/radna_jedinica_detalji.html',
                          title=f'Detalji radne jedinice - {radna_jedinica.naziv}',
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          objekti=objekti,
                          breadcrumbs=breadcrumbs,
                          hierarchy=hierarchy,
                          active_id=id)

@klijenti_bp.route('/radna-jedinica/<int:id>/izmeni', methods=['GET', 'POST'])
@login_required
def izmeni_radnu_jedinicu(id):
    """Izmena postojeće radne jedinice."""
    radna_jedinica = RadnaJedinica.query.get_or_404(id)
    pravno_lice = radna_jedinica.pravno_lice
    form = RadnaJedinicaForm(obj=radna_jedinica)
    
    # Koristimo funkciju za generisanje breadcrumbs
    breadcrumbs = generate_breadcrumbs('radna_jedinica', entity=radna_jedinica)
    # Dodajemo informaciju o izmeni
    breadcrumbs.append({'name': 'Izmena', 'url': None})
    
    # Generišemo hijerarhijsko stablo
    hierarchy = generate_hierarchy_tree(pravno_lice_id=pravno_lice.id, radna_jedinica_id=id)
    
    if form.validate_on_submit():
        try:
            radna_jedinica.naziv = form.naziv.data
            radna_jedinica.adresa = form.adresa.data
            radna_jedinica.mesto = form.mesto.data
            radna_jedinica.postanski_broj = form.postanski_broj.data
            radna_jedinica.drzava = form.drzava.data
            radna_jedinica.kontakt_osoba = form.kontakt_osoba.data
            radna_jedinica.telefon = form.telefon.data
            radna_jedinica.email = form.email.data
            radna_jedinica.napomena = form.napomena.data
            
            db.session.commit()
            
            flash('Radna jedinica je uspešno ažurirana.', 'success')
            return redirect(url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri ažuriranju radne jedinice: {str(e)}', 'error')
    
    return render_template('klijenti/radna_jedinica_form.html',
                          title=f'Izmena radne jedinice - {radna_jedinica.naziv}',
                          form=form,
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          izmena=True,
                          breadcrumbs=breadcrumbs,
                          hierarchy=hierarchy,
                          active_id=id)

@klijenti_bp.route('/radna-jedinica/<int:id>/obrisi', methods=['POST'])
@login_required
def obrisi_radnu_jedinicu(id):
    """Brisanje radne jedinice."""
    
# Rute za objekte
@klijenti_bp.route('/radna-jedinica/<int:id>/objekti')
@login_required
def lista_objekata(id):
    """Prikaz liste objekata za radnu jedinicu."""
    radna_jedinica = RadnaJedinica.query.get_or_404(id)
    pravno_lice = radna_jedinica.pravno_lice
    objekti = Objekat.query.filter_by(radna_jedinica_id=id).all()
    
    # Koristimo funkciju za generisanje breadcrumbs
    breadcrumbs = generate_breadcrumbs('objekat', parent_ids={'radna_jedinica_id': id})
    
    # Generišemo hijerarhijsko stablo
    hierarchy = generate_hierarchy_tree(pravno_lice_id=pravno_lice.id, radna_jedinica_id=id)
    
    return render_template('klijenti/lista_objekata.html',
                          title=f'Objekti - {radna_jedinica.naziv}',
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          objekti=objekti,
                          breadcrumbs=breadcrumbs,
                          hierarchy=hierarchy,
                          active_id=id)

@klijenti_bp.route('/radna-jedinica/<int:id>/objekti/novi', methods=['GET', 'POST'])
@login_required
def novi_objekat(id):
    """Dodavanje novog objekta za radnu jedinicu."""
    radna_jedinica = RadnaJedinica.query.get_or_404(id)
    pravno_lice = radna_jedinica.pravno_lice
    form = ObjekatForm()
    
    # Koristimo funkciju za generisanje breadcrumbs
    breadcrumbs = generate_breadcrumbs('objekat', parent_ids={'radna_jedinica_id': id})
    # Dodajemo informaciju o novom objektu
    breadcrumbs.append({'name': 'Novi', 'url': None})
    
    # Generišemo hijerarhijsko stablo
    hierarchy = generate_hierarchy_tree(pravno_lice_id=pravno_lice.id, radna_jedinica_id=id)
    
    if form.validate_on_submit():
        try:
            objekat = Objekat(
                radna_jedinica_id=radna_jedinica.id,
                naziv=form.naziv.data,
                opis=form.opis.data
            )
            
            db.session.add(objekat)
            db.session.commit()
            
            flash('Novi objekat je uspešno dodat.', 'success')
            return redirect(url_for('klijenti.detalji_objekta', id=objekat.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri kreiranju objekta: {str(e)}', 'error')
    
    return render_template('klijenti/objekat_form.html',
                          title=f'Novi objekat - {radna_jedinica.naziv}',
                          form=form,
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          breadcrumbs=breadcrumbs,
                          hierarchy=hierarchy,
                          active_id=id)

@klijenti_bp.route('/objekat/<int:id>', methods=['GET'])
@login_required
def detalji_objekta(id):
    """Prikaz detalja objekta."""
    objekat = Objekat.query.get_or_404(id)
    radna_jedinica = objekat.radna_jedinica
    pravno_lice = radna_jedinica.pravno_lice
    prostorije = Prostorija.query.filter_by(objekat_id=id).all()
    
    # Koristimo funkciju za generisanje breadcrumbs
    breadcrumbs = generate_breadcrumbs('objekat', entity=objekat)
    
    # Generišemo hijerarhijsko stablo
    hierarchy = generate_hierarchy_tree(pravno_lice_id=pravno_lice.id, radna_jedinica_id=radna_jedinica.id, objekat_id=id)
    
    return render_template('klijenti/objekat_detalji.html',
                          title=f'Detalji objekta - {objekat.naziv}',
                          objekat=objekat,
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          prostorije=prostorije,
                          breadcrumbs=breadcrumbs,
                          hierarchy=hierarchy,
                          active_id=id)

@klijenti_bp.route('/objekat/<int:id>/izmeni', methods=['GET', 'POST'])
@login_required
def izmeni_objekat(id):
    """Izmena postojećeg objekta."""
    objekat = Objekat.query.get_or_404(id)
    radna_jedinica = objekat.radna_jedinica
    pravno_lice = radna_jedinica.pravno_lice
    form = ObjekatForm(obj=objekat)
    
    # Koristimo funkciju za generisanje breadcrumbs
    breadcrumbs = generate_breadcrumbs('objekat', entity=objekat)
    # Dodajemo informaciju o izmeni
    breadcrumbs.append({'name': 'Izmena', 'url': None})
    
    # Generišemo hijerarhijsko stablo
    hierarchy = generate_hierarchy_tree(pravno_lice_id=pravno_lice.id, radna_jedinica_id=radna_jedinica.id, objekat_id=id)
    
    if form.validate_on_submit():
        try:
            objekat.naziv = form.naziv.data
            objekat.opis = form.opis.data
            
            db.session.commit()
            flash('Objekat je uspešno ažuriran.', 'success')
            return redirect(url_for('klijenti.detalji_objekta', id=objekat.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri ažuriranju objekta: {str(e)}', 'error')
    
    return render_template('klijenti/objekat_form.html',
                          title=f'Izmena objekta - {objekat.naziv}',
                          form=form,
                          objekat=objekat,
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          izmena=True,
                          breadcrumbs=breadcrumbs,
                          hierarchy=hierarchy,
                          active_id=id)



@klijenti_bp.route('/objekat/<int:id>/obrisi', methods=['POST'])
@login_required
def obrisi_objekat(id):
    """Brisanje objekta."""
    objekat = Objekat.query.get_or_404(id)
    radna_jedinica_id = objekat.radna_jedinica_id
    naziv = objekat.naziv
    
    try:
        db.session.delete(objekat)
        db.session.commit()
        flash(f'Objekat "{naziv}" je uspešno obrisan.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Došlo je do greške pri brisanju objekta: {str(e)}', 'error')
    
    return redirect(url_for('klijenti.lista_objekata', id=radna_jedinica_id))

@klijenti_bp.route('/objekat/<int:id>/prostorije')
@login_required
def lista_prostorija(id):
    """Prikaz liste prostorija za objekat."""
    objekat = Objekat.query.get_or_404(id)
    radna_jedinica = objekat.radna_jedinica
    pravno_lice = radna_jedinica.pravno_lice
    prostorije = Prostorija.query.filter_by(objekat_id=id).all()
    
    breadcrumbs = [
        {'name': 'Klijenti', 'url': url_for('klijenti.lista')},
        {'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)},
        {'name': radna_jedinica.naziv, 'url': url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id)},
        {'name': objekat.naziv, 'url': url_for('klijenti.detalji_objekta', id=objekat.id)},
        {'name': 'Prostorije', 'url': None}
    ]
    
    return render_template('klijenti/lista_prostorija.html',
                          title=f'Prostorije - {objekat.naziv}',
                          objekat=objekat,
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          prostorije=prostorije,
                          breadcrumbs=breadcrumbs)

@klijenti_bp.route('/objekat/<int:id>/prostorije/nova', methods=['GET', 'POST'])
@login_required
def nova_prostorija(id):
    """Dodavanje nove prostorije za objekat."""
    objekat = Objekat.query.get_or_404(id)
    radna_jedinica = objekat.radna_jedinica
    pravno_lice = radna_jedinica.pravno_lice
    form = ProstorijaForm()
    
    breadcrumbs = [
        {'name': 'Klijenti', 'url': url_for('klijenti.lista')},
        {'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)},
        {'name': radna_jedinica.naziv, 'url': url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id)},
        {'name': objekat.naziv, 'url': url_for('klijenti.detalji_objekta', id=objekat.id)},
        {'name': 'Prostorije', 'url': url_for('klijenti.lista_prostorija', id=objekat.id)},
        {'name': 'Nova', 'url': None}
    ]
    
    if form.validate_on_submit():
        try:
            prostorija = Prostorija(
                objekat_id=objekat.id,
                naziv=form.naziv.data,
                sprat=form.sprat.data,
                broj=form.broj.data,
                namena=form.namena.data,
            )
            
            db.session.add(prostorija)
            db.session.commit()
            
            flash('Nova prostorija je uspešno dodata.', 'success')
            return redirect(url_for('klijenti.detalji_prostorije', id=prostorija.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri kreiranju prostorije: {str(e)}', 'error')
    
    return render_template('klijenti/prostorija_form.html',
                          title=f'Nova prostorija - {objekat.naziv}',
                          form=form,
                          objekat=objekat,
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          breadcrumbs=breadcrumbs)

@klijenti_bp.route('/prostorija/<int:id>', methods=['GET'])
@login_required
def detalji_prostorije(id):
    """Prikaz detalja prostorije."""
    prostorija = Prostorija.query.get_or_404(id)
    objekat = prostorija.objekat
    radna_jedinica = objekat.radna_jedinica
    pravno_lice = radna_jedinica.pravno_lice
    
    breadcrumbs = [
        {'name': 'Klijenti', 'url': url_for('klijenti.lista')},
        {'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)},
        {'name': radna_jedinica.naziv, 'url': url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id)},
        {'name': objekat.naziv, 'url': url_for('klijenti.detalji_objekta', id=objekat.id)},
        {'name': 'Prostorije', 'url': url_for('klijenti.lista_prostorija', id=objekat.id)},
        {'name': prostorija.naziv, 'url': None}
    ]
    
    return render_template('klijenti/prostorija_detalji.html',
                          title=f'Detalji prostorije - {prostorija.naziv}',
                          prostorija=prostorija,
                          objekat=objekat,
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          breadcrumbs=breadcrumbs)

@klijenti_bp.route('/prostorija/<int:id>/izmeni', methods=['GET', 'POST'])
@login_required
def izmeni_prostoriju(id):
    """Izmena postojeće prostorije."""
    prostorija = Prostorija.query.get_or_404(id)
    objekat = prostorija.objekat
    radna_jedinica = objekat.radna_jedinica
    pravno_lice = radna_jedinica.pravno_lice
    form = ProstorijaForm(obj=prostorija)
    
    breadcrumbs = [
        {'name': 'Klijenti', 'url': url_for('klijenti.lista')},
        {'name': pravno_lice.naziv, 'url': url_for('klijenti.detalji_klijenta', id=pravno_lice.id)},
        {'name': radna_jedinica.naziv, 'url': url_for('klijenti.detalji_radne_jedinice', id=radna_jedinica.id)},
        {'name': objekat.naziv, 'url': url_for('klijenti.detalji_objekta', id=objekat.id)},
        {'name': 'Prostorije', 'url': url_for('klijenti.lista_prostorija', id=objekat.id)},
        {'name': prostorija.naziv, 'url': url_for('klijenti.detalji_prostorije', id=prostorija.id)},
        {'name': 'Izmena', 'url': None}
    ]
    
    if form.validate_on_submit():
        try:
            prostorija.naziv = form.naziv.data
            prostorija.sprat = form.sprat.data
            prostorija.broj = form.broj.data
            prostorija.namena = form.namena.data
            
            db.session.commit()
            
            flash('Prostorija je uspešno ažurirana.', 'success')
            return redirect(url_for('klijenti.detalji_prostorije', id=prostorija.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Došlo je do greške pri ažuriranju prostorije: {str(e)}', 'error')
    
    return render_template('klijenti/prostorija_form.html',
                          title=f'Izmena prostorije - {prostorija.naziv}',
                          form=form,
                          prostorija=prostorija,
                          objekat=objekat,
                          radna_jedinica=radna_jedinica,
                          pravno_lice=pravno_lice,
                          izmena=True,
                          breadcrumbs=breadcrumbs)

@klijenti_bp.route('/prostorija/<int:id>/obrisi', methods=['POST'])
@login_required
def obrisi_prostoriju(id):
    """Brisanje prostorije."""
    prostorija = Prostorija.query.get_or_404(id)
    objekat_id = prostorija.objekat_id
    naziv = prostorija.naziv
    
    try:
        db.session.delete(prostorija)
        db.session.commit()
        flash(f'Prostorija "{naziv}" je uspešno obrisana.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Došlo je do greške pri brisanju prostorije: {str(e)}', 'error')
    
    return redirect(url_for('klijenti.lista_prostorija', id=objekat_id))

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
