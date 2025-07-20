from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required
from sqlalchemy import or_

from app import db
from app.models.material import Material
from app.utils.forms import MaterialForm
from app.utils.decorators import admin_required

# Kreiranje Blueprint-a
materijali_bp = Blueprint('materijali', __name__, url_prefix='/materijali')

@materijali_bp.route('/')
@login_required
@admin_required
def lista():
    """Prikaz liste materijala sa opcijom pretrage i paginacijom."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    
    # Osnovni query, sortiran po nazivu materijala
    query = Material.query.order_by(Material.naziv)
    
    # Pretraga ako je uneta
    if search_query:
        query = query.filter(
            or_(
                Material.naziv.ilike(f'%{search_query}%'),
                Material.jedinica_mere.ilike(f'%{search_query}%')
            )
        )
    
    # Paginacija - 10 materijala po stranici
    materijali = query.paginate(page=page, per_page=10)
    
    # AJAX zahtev vraća samo podatke o materijalima
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_template('materijali/_lista_partial.html', materijali=materijali)
        return jsonify({'html': html})
    
    # Redovan zahtev vraća kompletnu stranicu
    return render_template('materijali/lista.html', materijali=materijali, search_query=search_query)

@materijali_bp.route('/novi', methods=['GET', 'POST'])
@login_required
@admin_required
def novi():
    """Kreiranje novog materijala."""
    forma = MaterialForm()
    
    if forma.validate_on_submit():
        # Kreiranje novog materijala
        materijal = Material(
            naziv=forma.naziv.data,
            jedinica_mere=forma.jedinica_mere.data,
            active=forma.active.data
        )
        
        # Čuvanje u bazi podataka
        db.session.add(materijal)
        db.session.commit()
        
        flash('Materijal je uspešno kreiran.', 'success')
        return redirect(url_for('materijali.lista'))
    
    # Prikazivanje forme za kreiranje
    return render_template('materijali/form.html', forma=forma, title='Novi materijal')

@materijali_bp.route('/<int:id>/izmeni', methods=['GET', 'POST'])
@login_required
@admin_required
def izmeni(id):
    """Izmena postojećeg materijala."""
    materijal = Material.query.get_or_404(id)
    forma = MaterialForm(original_naziv=materijal.naziv)
    
    if forma.validate_on_submit():
        # Ažuriranje podataka o materijalu
        materijal.naziv = forma.naziv.data
        materijal.jedinica_mere = forma.jedinica_mere.data
        materijal.active = forma.active.data
        
        # Čuvanje izmena u bazi podataka
        db.session.commit()
        
        flash('Podaci o materijalu su uspešno ažurirani.', 'success')
        return redirect(url_for('materijali.lista'))
    
    # Popunjavanje forme postojećim podacima
    if request.method == 'GET':
        forma.naziv.data = materijal.naziv
        forma.jedinica_mere.data = materijal.jedinica_mere
        forma.active.data = materijal.active
    
    # Prikazivanje forme za izmenu
    return render_template('materijali/form.html', forma=forma, title='Izmena materijala')

@materijali_bp.route('/<int:id>/status', methods=['POST'])
@login_required
@admin_required
def status(id):
    """Promena statusa materijala (aktivno/neaktivno)."""
    materijal = Material.query.get_or_404(id)
    
    # Menjanje statusa materijala
    novi_status = materijal.toggle_status()
    db.session.commit()
    
    # Poruka o uspehu
    poruka = 'Materijal je uspešno aktiviran.' if novi_status else 'Materijal je uspešno deaktiviran.'
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
    return redirect(url_for('materijali.lista'))

@materijali_bp.route('/api')
@login_required
def api_aktivni_materijali():
    """API endpoint za dohvatanje samo aktivnih materijala."""
    aktivni_materijali = Material.query.filter_by(active=True).order_by(Material.naziv).all()
    
    rezultat = [
        {
            'id': materijal.id,
            'naziv': materijal.naziv,
            'jedinica_mere': materijal.jedinica_mere,
            'naziv_sa_jedinicom': materijal.get_material_info()
        }
        for materijal in aktivni_materijali
    ]
    
    return jsonify(rezultat)
