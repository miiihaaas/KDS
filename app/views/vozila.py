from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required
from sqlalchemy import or_

from app import db
from app.models.vehicle import Vehicle
from app.utils.forms import VehicleForm
from app.utils.decorators import admin_required

# Kreiranje Blueprint-a
vozila_bp = Blueprint('vozila', __name__, url_prefix='/vozila')

@vozila_bp.route('/')
@login_required
@admin_required
def lista():
    """Prikaz liste vozila sa opcijom pretrage i paginacijom."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    
    # Osnovni query, sortiran po registarskoj oznaci
    query = Vehicle.query.order_by(Vehicle.registracija)
    
    # Pretraga ako je uneta
    if search_query:
        query = query.filter(
            or_(
                Vehicle.marka.ilike(f'%{search_query}%'),
                Vehicle.model.ilike(f'%{search_query}%'),
                Vehicle.registracija.ilike(f'%{search_query}%')
            )
        )
    
    # Paginacija - 10 vozila po stranici
    vozila = query.paginate(page=page, per_page=10)
    
    # AJAX zahtev vraća samo podatke o vozilima
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_template('vozila/_lista_partial.html', vozila=vozila)
        return jsonify({'html': html})
    
    # Redovan zahtev vraća kompletnu stranicu
    return render_template('vozila/lista.html', vozila=vozila, search_query=search_query)

@vozila_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo():
    """Kreiranje novog vozila."""
    forma = VehicleForm()
    
    if forma.validate_on_submit():
        # Kreiranje novog vozila
        vozilo = Vehicle(
            marka=forma.marka.data,
            model=forma.model.data,
            registracija=forma.registracija.data.upper(),  # Uvek čuvamo registraciju velikim slovima
            active=forma.active.data
        )
        
        # Čuvanje u bazi podataka
        db.session.add(vozilo)
        db.session.commit()
        
        flash('Vozilo je uspešno kreirano.', 'success')
        return redirect(url_for('vozila.lista'))
    
    # Prikazivanje forme za kreiranje
    return render_template('vozila/form.html', forma=forma, title='Novo vozilo')

@vozila_bp.route('/<int:id>/izmeni', methods=['GET', 'POST'])
@login_required
@admin_required
def izmeni(id):
    """Izmena postojećeg vozila."""
    vozilo = Vehicle.query.get_or_404(id)
    forma = VehicleForm(original_reg=vozilo.registracija)
    
    if forma.validate_on_submit():
        # Ažuriranje podataka o vozilu
        vozilo.marka = forma.marka.data
        vozilo.model = forma.model.data
        vozilo.registracija = forma.registracija.data.upper()  # Uvek čuvamo registraciju velikim slovima
        vozilo.active = forma.active.data
        
        # Čuvanje izmena u bazi podataka
        db.session.commit()
        
        flash('Podaci o vozilu su uspešno ažurirani.', 'success')
        return redirect(url_for('vozila.lista'))
    
    # Popunjavanje forme postojećim podacima
    if request.method == 'GET':
        forma.marka.data = vozilo.marka
        forma.model.data = vozilo.model
        forma.registracija.data = vozilo.registracija
        forma.active.data = vozilo.active
    
    # Prikazivanje forme za izmenu
    return render_template('vozila/form.html', forma=forma, title='Izmena vozila')

@vozila_bp.route('/<int:id>/status', methods=['POST'])
@login_required
@admin_required
def status(id):
    """Promena statusa vozila (aktivno/neaktivno)."""
    vozilo = Vehicle.query.get_or_404(id)
    
    # Menjanje statusa vozila
    novi_status = vozilo.toggle_status()
    db.session.commit()
    
    # Poruka o uspehu
    poruka = 'Vozilo je uspešno aktivirano.' if novi_status else 'Vozilo je uspešno deaktivirano.'
    kategorija = 'success'
    
    # Ako je AJAX zahtev
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True, 
            'active': novi_status, 
            'message': poruka,
            'category': kategorija
        })
    
    # Standardni zahtev
    flash(poruka, kategorija)
    return redirect(url_for('vozila.lista'))

@vozila_bp.route('/api/aktivna')
@login_required
def api_aktivna_vozila():
    """API endpoint za dohvatanje samo aktivnih vozila."""
    aktivna_vozila = Vehicle.query.filter_by(active=True).order_by(Vehicle.registracija).all()
    
    rezultat = [
        {
            'id': vozilo.id,
            'marka': vozilo.marka,
            'model': vozilo.model,
            'registracija': vozilo.registracija,
            'naziv': vozilo.get_vehicle_info()
        }
        for vozilo in aktivna_vozila
    ]
    
    return jsonify(rezultat)
