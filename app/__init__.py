from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import config
from datetime import timedelta
import os

# Inicijalizacija ekstenzija
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    """Flask app factory."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicijalizacija ekstenzija
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Morate se prijaviti da biste pristupili ovoj stranici.'
    login_manager.login_message_category = 'info'
    login_manager.remember_cookie_duration = timedelta(days=30)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Registracija blueprint-a
    from app.views.auth import auth_bp
    from app.views.dashboard import dashboard_bp
    from app.views.korisnici import korisnici_bp
    from app.views.vozila import vozila_bp
    from app.views.materijali import materijali_bp
    from app.views.api import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(korisnici_bp)
    app.register_blueprint(vozila_bp)
    app.register_blueprint(materijali_bp)
    app.register_blueprint(api_bp)
    
    # Glavna ruta
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    # Test konekcije sa bazom pri pokretanju
    def test_database_connection():
        try:
            with app.app_context():
                db.session.execute(db.text('SELECT 1'))
                app.logger.info('Konekcija sa bazom podataka je uspešno uspostavljena.')
        except Exception as e:
            app.logger.error(f'Greška pri konekciji sa bazom: {str(e)}')
    
    # Pozovi test konekcije
    test_database_connection()
    
    # Kreiranje tabela
    with app.app_context():
        try:
            db.create_all()
            app.logger.info('Tabele su uspešno kreirane.')
        except Exception as e:
            app.logger.error(f'Greška pri kreiranju tabela: {str(e)}')
    
    return app
