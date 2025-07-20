# Development Workflow

## Local Development Setup

### Prerequisites
```bash
# Python 3.9+ installation
python --version  # Should be 3.9 or higher

# MySQL installation and setup
mysql --version   # Should be 8.0 or higher

# Virtual environment creation
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### Initial Setup
```bash
# Clone/create project directory
mkdir kds-sistem
cd kds-sistem

# Install dependencies
pip install -r requirements.txt

# Database setup
mysql -u root -p
CREATE DATABASE kds_sistem CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'kds_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON kds_sistem.* TO 'kds_user'@'localhost';
FLUSH PRIVILEGES;
exit

# Environment configuration
cp .env.example .env
# Edit .env with your database credentials and other settings

# Initialize database
python scripts/init_db.py

# Create admin user
python scripts/create_admin.py

# Generate sample data (optional)
python scripts/generate_sample_data.py
```

### Dev Commands
```bash
# Start development server
python run.py

# Run with debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py

# Database migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run tests
pytest
pytest --coverage

# Code formatting
black app/
flake8 app/
```

## Environment Configuration

### Required Environment Variables
```bash
# Database configuration (.env)
DATABASE_URL=mysql://kds_user:your_password@localhost/kds_sistem

# Flask configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1

# Email configuration (SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# File upload settings
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# QR Code settings
QR_CODE_FOLDER=app/static/images/qr-codes
QR_CODE_SIZE=200

# Security settings
SESSION_TIMEOUT=3600  # 1 hour
PASSWORD_MIN_LENGTH=8
LOGIN_ATTEMPTS_LIMIT=5
```
