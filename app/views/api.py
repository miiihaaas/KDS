from flask import Blueprint, jsonify
from flask_login import login_required

from app.models.material import Material

# Kreiranje Blueprint-a
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/materijali')
@login_required
def aktivni_materijali():
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
