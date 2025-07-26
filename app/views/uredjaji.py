from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.device import Uredjaj
from app.models.client import Prostorija, Objekat, RadnaJedinica, LokacijaKuce, PravnoLice, FizickoLice
from app.models.device import Uredjaj
from app.utils.device_forms import UredjajForm, UredjajFilterForm, DodelaUredjajaForm
from sqlalchemy import or_
import traceback

bp = Blueprint('uredjaji', __name__, url_prefix='/uredjaji')

@bp.route('/')
@login_required
def lista_uredjaja():
    """Prikaz liste svih uređaja sa mogućnošću pretrage i filtriranja."""
    form = UredjajFilterForm(request.args)
    
    # Inicijalizacija upita
    query = Uredjaj.query
    
    # Primena filtera
    if request.args.get('tip'):
        query = query.filter(Uredjaj.tip == request.args.get('tip'))
        
    if request.args.get('proizvodjac'):
        query = query.filter(Uredjaj.proizvodjac.like(f"%{request.args.get('proizvodjac')}%"))
    
    # Pretraga po različitim poljima
    if request.args.get('pretraga'):
        search_term = f"%{request.args.get('pretraga')}%"
        query = query.filter(or_(
            Uredjaj.proizvodjac.like(search_term),
            Uredjaj.model.like(search_term),
            Uredjaj.serijski_broj.like(search_term),
            Uredjaj.inventarski_broj.like(search_term)
        ))
    
    # Paginacija
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Uredjaj.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template(
        'uredjaji/lista.html',
        uredjaji=pagination.items,
        pagination=pagination,
        form=form
    )

@bp.route('/novi', methods=['GET', 'POST'])
@login_required
def novi_uredjaj():
    """Kreiranje novog uređaja."""
    form = UredjajForm()
    
    # Ako je POST zahtev, moramo dinamički ažurirati choices za sve select elemente
    # pre validacije forme
    if request.method == 'POST':
        # Ažuriranje za prostoriju_id
        if request.form.get('prostorija_id'):
            prostorija_id = request.form.get('prostorija_id')
            prostorija = Prostorija.query.get(prostorija_id)
            if prostorija:
                form.prostorija_id.choices = [('', 'Odaberite prostoriju'), (str(prostorija.id), prostorija.naziv)]
        
        # Ažuriranje za objekat_id
        if request.form.get('objekat_id'):
            objekat_id = request.form.get('objekat_id')
            objekat = Objekat.query.get(objekat_id)
            if objekat:
                form.objekat_id.choices = [('', 'Odaberite objekat'), (str(objekat.id), objekat.naziv)]
        
        # Ažuriranje za lokacija_id
        if request.form.get('lokacija_id'):
            lokacija_id = request.form.get('lokacija_id')
            # Pošto lokacija može biti RadnaJedinica ili LokacijaKuce
            rj = RadnaJedinica.query.get(lokacija_id)
            lk = None if rj else LokacijaKuce.query.get(lokacija_id)
            
            if rj:
                form.lokacija_id.choices = [('', 'Odaberite lokaciju'), (str(rj.id), rj.naziv)]
            elif lk:
                form.lokacija_id.choices = [('', 'Odaberite lokaciju'), (str(lk.id), lk.naziv)]
    
    if form.validate_on_submit():
        uredjaj = Uredjaj(
            tip=form.tip.data,
            podtip=form.podtip.data,
            proizvodjac=form.proizvodjac.data,
            model=form.model.data,
            serijski_broj=form.serijski_broj.data,
            inventarski_broj=form.inventarski_broj.data,
            godina_proizvodnje=form.godina_proizvodnje.data
        )
        
        db.session.add(uredjaj)
        
        # Ako je odabrana prostorija, dodeljujemo uređaj toj prostoriji
        if form.prostorija_id.data and form.prostorija_id.data != '':
            prostorija = Prostorija.query.get(form.prostorija_id.data)
            if prostorija:
                uredjaj.dodeli_prostoriju(prostorija, current_user.id)
        
        db.session.commit()
        flash('Uređaj je uspešno kreiran.', 'success')
        return redirect(url_for('uredjaji.detalji_uredjaja', id=uredjaj.id))
    
    return render_template('uredjaji/forma.html', form=form, title="Novi uređaj")

@bp.route('/<int:id>')
@login_required
def detalji_uredjaja(id):
    """Prikaz detalja uređaja."""
    uredjaj = Uredjaj.query.get_or_404(id)
    return render_template('uredjaji/detalji.html', uredjaj=uredjaj)

@bp.route('/<int:id>/izmeni', methods=['GET', 'POST'])
@login_required
def izmeni_uredjaj(id):
    """Izmena postojećeg uređaja."""
    uredjaj = Uredjaj.query.get_or_404(id)
    form = UredjajForm(original_sn=uredjaj.serijski_broj, obj=uredjaj)
    
    # Ako je POST zahtev, moramo dinamički ažurirati choices za sve select elemente
    # pre validacije forme
    if request.method == 'POST':
        # Ažuriranje za prostoriju_id
        if request.form.get('prostorija_id'):
            prostorija_id = request.form.get('prostorija_id')
            prostorija = Prostorija.query.get(prostorija_id)
            if prostorija:
                form.prostorija_id.choices = [('', 'Odaberite prostoriju'), (str(prostorija.id), prostorija.naziv)]
        
        # Ažuriranje za objekat_id
        if request.form.get('objekat_id'):
            objekat_id = request.form.get('objekat_id')
            objekat = Objekat.query.get(objekat_id)
            if objekat:
                form.objekat_id.choices = [('', 'Odaberite objekat'), (str(objekat.id), objekat.naziv)]
        
        # Ažuriranje za lokacija_id
        if request.form.get('lokacija_id'):
            lokacija_id = request.form.get('lokacija_id')
            # Pošto lokacija može biti RadnaJedinica ili LokacijaKuce
            rj = RadnaJedinica.query.get(lokacija_id)
            lk = None if rj else LokacijaKuce.query.get(lokacija_id)
            
            if rj:
                form.lokacija_id.choices = [('', 'Odaberite lokaciju'), (str(rj.id), rj.naziv)]
            elif lk:
                form.lokacija_id.choices = [('', 'Odaberite lokaciju'), (str(lk.id), lk.naziv)]
    
    if form.validate_on_submit():
        uredjaj.tip = form.tip.data
        uredjaj.podtip = form.podtip.data
        uredjaj.proizvodjac = form.proizvodjac.data
        uredjaj.model = form.model.data
        uredjaj.serijski_broj = form.serijski_broj.data
        uredjaj.inventarski_broj = form.inventarski_broj.data
        uredjaj.godina_proizvodnje = form.godina_proizvodnje.data
        
        # Ako je odabrana nova prostorija
        if form.prostorija_id.data and form.prostorija_id.data != '':
            prostorija = Prostorija.query.get(form.prostorija_id.data)
            if prostorija and prostorija not in uredjaj.prostorije:
                uredjaj.dodeli_prostoriju(prostorija, current_user.id)
        
        db.session.commit()
        flash('Uređaj je uspešno ažuriran.', 'success')
        return redirect(url_for('uredjaji.detalji_uredjaja', id=uredjaj.id))
    
    # Preselect postojećih vrednosti za hijerarhijski odabir prostorije
    if uredjaj.prostorije.count() > 0:
        prva_prostorija = uredjaj.prostorije.first()
        objekat = prva_prostorija.objekat
        
        if objekat:
            form.objekat_id.data = str(objekat.id)
            form.prostorija_id.data = str(prva_prostorija.id)
            
            if objekat.radna_jedinica_id:
                form.lokacija_id.data = str(objekat.radna_jedinica_id)
                pravno_lice = objekat.radna_jedinica.pravno_lice
                form.klijent_id.data = str(pravno_lice.id)
            elif objekat.lokacija_kuce_id:
                form.lokacija_id.data = str(objekat.lokacija_kuce_id)
                fizicko_lice = objekat.lokacija_kuce.fizicko_lice
                form.klijent_id.data = str(fizicko_lice.id)
    
    return render_template('uredjaji/forma.html', form=form, uredjaj=uredjaj, title="Izmena uređaja")

@bp.route('/obrisi/<int:id>', methods=['POST'])
@login_required
def obrisi_uredjaj(id):
    """Brisanje uređaja."""
    try:
        uredjaj = Uredjaj.query.get_or_404(id)
        
        # Provera da li je uređaj već dodeljen nekoj prostoriji
        if uredjaj.prostorije.count() > 0:
            # Uklanjamo sve veze sa prostorijama pre brisanja
            for prostorija in uredjaj.prostorije.all():
                uredjaj.ukloni_iz_prostorije(prostorija)
        
        # Brisanje uređaja
        naziv = uredjaj.get_display_name()
        db.session.delete(uredjaj)
        db.session.commit()
        flash(f'Uređaj {naziv} je uspešno obrisan.', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Greška prilikom brisanja uređaja: {str(e)}\n{traceback.format_exc()}')
        flash(f'Došlo je do greške prilikom brisanja uređaja.', 'danger')
    
    return redirect(url_for('uredjaji.lista_uredjaja'))

@bp.route('/ukloni-iz-prostorije/<int:id>/<int:prostorija_id>', methods=['POST'])
@login_required
def ukloni_iz_prostorije(id, prostorija_id):
    """Uklanjanje uređaja iz prostorije."""
    try:
        uredjaj = Uredjaj.query.get_or_404(id)
        prostorija = Prostorija.query.get_or_404(prostorija_id)
        
        if uredjaj.ukloni_iz_prostorije(prostorija):
            db.session.commit()
            flash('Uređaj je uspešno uklonjen iz prostorije.', 'success')
        else:
            flash('Uređaj nije dodeljen ovoj prostoriji.', 'warning')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Greška prilikom uklanjanja uređaja iz prostorije: {str(e)}\n{traceback.format_exc()}')
        flash(f'Došlo je do greške prilikom uklanjanja uređaja iz prostorije.', 'danger')
    
    return redirect(url_for('uredjaji.detalji_uredjaja', id=id))

# API rute za dinamičko učitavanje hijerarhijskih podataka
@bp.route('/api/klijenti')
@login_required
def api_klijenti():
    """API za vraćanje liste klijenata."""
    pravna_lica = PravnoLice.query.all()
    fizicka_lica = FizickoLice.query.all()
    
    rezultat = []
    
    for pl in pravna_lica:
        rezultat.append({
            'id': pl.id,
            'naziv': pl.naziv,
            'tip': 'pravno_lice'
        })
    
    for fl in fizicka_lica:
        rezultat.append({
            'id': fl.id,
            'naziv': fl.puno_ime,
            'tip': 'fizicko_lice'
        })
    
    return jsonify(rezultat)

@bp.route('/api/lokacije/<int:klijent_id>')
@login_required
def api_lokacije_auto(klijent_id):
    """API za vraćanje lokacija za određenog klijenta automatski određujući tip."""
    # Prvo proverimo da li je pravno lice
    pl = PravnoLice.query.filter_by(id=klijent_id).first()
    if pl:
        return api_lokacije(klijent_id, 'pravno_lice')
    
    # Ako nije pravno lice, proverimo da li je fizičko lice
    fl = FizickoLice.query.filter_by(id=klijent_id).first()
    if fl:
        return api_lokacije(klijent_id, 'fizicko_lice')
    
    # Ako nije ni jedno ni drugo, vraćamo praznu listu
    return jsonify([]), 404

@bp.route('/api/lokacije/<int:klijent_id>/<tip>')
@login_required
def api_lokacije(klijent_id, tip):
    """API za vraćanje lokacija za određenog klijenta."""
    rezultat = []
    
    if tip == 'pravno_lice':
        lokacije = RadnaJedinica.query.filter_by(pravno_lice_id=klijent_id).all()
        for lok in lokacije:
            rezultat.append({
                'id': lok.id,
                'naziv': lok.naziv,
                'tip': 'radna_jedinica'
            })
    else:  # fizicko_lice
        lokacije = LokacijaKuce.query.filter_by(fizicko_lice_id=klijent_id).all()
        for lok in lokacije:
            rezultat.append({
                'id': lok.id,
                'naziv': lok.naziv,
                'tip': 'lokacija_kuce'
            })
    
    return jsonify(rezultat)

@bp.route('/api/objekti/<int:lokacija_id>/<tip>')
@login_required
def api_objekti(lokacija_id, tip):
    """API za vraćanje objekata za određenu lokaciju."""
    rezultat = []
    
    if tip == 'radna_jedinica':
        objekti = Objekat.query.filter_by(radna_jedinica_id=lokacija_id).all()
    else:  # lokacija_kuce
        objekti = Objekat.query.filter_by(lokacija_kuce_id=lokacija_id).all()
    
    for obj in objekti:
        rezultat.append({
            'id': obj.id,
            'naziv': obj.naziv
        })
    
    return jsonify(rezultat)

@bp.route('/api/prostorije/<int:objekat_id>')
@login_required
def api_prostorije(objekat_id):
    """API za vraćanje prostorija za određeni objekat."""
    prostorije = Prostorija.query.filter_by(objekat_id=objekat_id).all()
    rezultat = []
    
    for p in prostorije:
        rezultat.append({
            'id': p.id,
            'naziv': p.get_display_name()
        })
    
    return jsonify(rezultat)

@bp.route('/api/podtipovi-uredjaja/<tip>', methods=['GET'])
@login_required
def api_podtipovi_uredjaja(tip):
    """API za vraćanje podtipova uređaja za određeni tip."""
    if tip not in Uredjaj.TIPOVI:
        return jsonify({'error': 'Nepoznat tip uređaja'}), 400
    
    podtipovi = Uredjaj.TIPOVI[tip]
    rezultat = [{'id': p, 'naziv': p.replace('_', ' ').title()} for p in podtipovi]
    
    return jsonify(rezultat)

# Rute za dodelu uređaja preko prostorije
@bp.route('/dodeli-prostoriji/<int:prostorija_id>', methods=['GET'])
@login_required
def dodeli_prostoriji(prostorija_id):
    """Prikazuje listu uređaja koji se mogu dodeliti prostoriji."""
    prostorija = Prostorija.query.get_or_404(prostorija_id)
    
    # Pronađi uređaje koji nisu dodeljeni nijednoj prostoriji
    nedodeljeni_uredjaji = Uredjaj.query.filter(
        ~Uredjaj.prostorije.any()
    ).all()
    
    return render_template(
        'uredjaji/dodeli_prostoriji.html',
        prostorija=prostorija,
        nedodeljeni_uredjaji=nedodeljeni_uredjaji
    )

@bp.route('/dodeli-prostoriji', methods=['POST'])
@login_required
def dodeli_prostoriji_post():
    """Dodeljuje uređaj prostoriji."""
    form = DodelaUredjajaForm()
    
    try:
        if form.validate_on_submit():
            uredjaj = Uredjaj.query.get_or_404(form.uredjaj_id.data)
            prostorija = Prostorija.query.get_or_404(form.prostorija_id.data)
            
            if uredjaj.dodeli_prostoriju(prostorija, current_user.id):
                db.session.commit()
                flash('Uređaj je uspešno dodeljen prostoriji.', 'success')
            else:
                flash('Uređaj je već dodeljen ovoj prostoriji.', 'warning')
            
            return redirect(url_for('uredjaji.detalji_uredjaja', id=uredjaj.id))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Greška u polju {getattr(form, field).label.text}: {error}', 'danger')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Greška prilikom dodele uređaja prostoriji: {str(e)}\n{traceback.format_exc()}')
        flash(f'Došlo je do greške prilikom dodele uređaja prostoriji.', 'danger')
    
    return redirect(url_for('uredjaji.lista_uredjaja'))
