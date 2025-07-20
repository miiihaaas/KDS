from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorators import admin_or_serviser_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
@admin_or_serviser_required
def index():
    """Glavna dashboard stranica."""
    return render_template('dashboard/index.html', 
                         title='Dashboard', 
                         user=current_user)
