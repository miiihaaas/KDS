# Deployment Architecture

## Deployment Strategy

**Frontend Deployment:**
- **Platform:** Same server as backend (integrated Flask app)
- **Build Command:** N/A (static files served directly)
- **Output Directory:** app/static/
- **CDN/Edge:** Optional Nginx caching for static assets

**Backend Deployment:**
- **Platform:** Ubuntu/CentOS VPS or cloud instance
- **Build Command:** pip install -r requirements.txt
- **Deployment Method:** Gunicorn + Nginx reverse proxy

## CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml (GitHub Actions example)
name: Deploy KDS Sistem

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /var/www/kds-sistem
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          flask db upgrade
          sudo systemctl restart kds-sistem
          sudo systemctl reload nginx
```

## Environments

| Environment | Frontend URL | Backend URL | Purpose |
|-------------|--------------|-------------|---------|
| Development | http://localhost:5000 | http://localhost:5000 | Lokalni development |
| Staging | https://staging.kds-sistem.com | https://staging.kds-sistem.com | Pre-production testing |
| Production | https://kds-sistem.com | https://kds-sistem.com | Live environment |
