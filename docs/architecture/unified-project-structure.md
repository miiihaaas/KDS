# Unified Project Structure

```
kds-sistem/
├── app/                              # Flask application
│   ├── __init__.py                   # App factory
│   ├── models/                       # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── device.py
│   │   ├── work_order.py
│   │   ├── material.py
│   │   └── vehicle.py
│   ├── views/                        # Flask blueprints
│   │   ├── __init__.py
│   │   ├── auth.py                   # Authentication routes
│   │   ├── dashboard.py              # Dashboard routes
│   │   ├── clients.py                # Client management
│   │   ├── devices.py                # Device management
│   │   ├── work_orders.py            # Work order management
│   │   ├── admin.py                  # Admin routes
│   │   └── api.py                    # REST API endpoints
│   ├── services/                     # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── client_service.py
│   │   ├── device_service.py
│   │   ├── work_order_service.py
│   │   ├── qr_service.py
│   │   └── email_service.py
│   ├── forms/                        # WTForms form classes
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── client_forms.py
│   │   ├── device_forms.py
│   │   └── work_order_forms.py
│   ├── utils/                        # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── decorators.py
│   ├── static/                       # Static files
│   │   ├── css/
│   │   │   ├── bootstrap.min.css
│   │   │   ├── custom.css
│   │   │   └── mobile.css
│   │   ├── js/
│   │   │   ├── bootstrap.bundle.min.js
│   │   │   ├── app.js               # Main app logic
│   │   │   ├── qr-scanner.js        # QR functionality
│   │   │   ├── work-orders.js       # Work order management
│   │   │   ├── client-management.js # Client management
│   │   │   └── utils.js             # Utility functions
│   │   ├── images/
│   │   │   ├── icons/
│   │   │   └── qr-codes/            # Generated QR codes
│   │   └── fonts/
│   └── templates/                    # Jinja2 templates
│       ├── base.html                 # Base template
│       ├── partials/                 # Reusable template parts
│       │   ├── navigation.html
│       │   ├── breadcrumb.html
│       │   └── notifications.html
│       ├── auth/
│       │   ├── login.html
│       │   └── reset-password.html
│       ├── dashboard/
│       │   ├── serviser.html
│       │   └── administrator.html
│       ├── clients/
│       │   ├── list.html
│       │   ├── detail.html
│       │   ├── form.html
│       │   └── hierarchy.html
│       ├── devices/
│       │   ├── list.html
│       │   ├── detail.html
│       │   ├── form.html
│       │   └── qr-scanner.html
│       ├── work-orders/
│       │   ├── list.html
│       │   ├── create.html
│       │   ├── detail.html
│       │   ├── edit.html
│       │   └── email-template.html
│       ├── admin/
│       │   ├── users.html
│       │   ├── vehicles.html
│       │   ├── materials.html
│       │   └── reports.html
│       └── errors/
│           ├── 404.html
│           └── 500.html
├── migrations/                       # Database migrations
│   ├── versions/
│   └── alembic.ini
├── tests/                           # Test files
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── test_api.py
│   │   ├── test_auth.py
│   │   └── test_workflows.py
│   └── fixtures/
│       ├── test_data.sql
│       └── sample_qr_codes.py
├── scripts/                         # Utility scripts
│   ├── init_db.py                   # Database initialization
│   ├── create_admin.py              # Create admin user
│   └── generate_sample_data.py      # Sample data for testing
├── docs/                           # Project documentation
│   ├── project-brief.md
│   ├── prd.md
│   ├── front-end-spec.md
│   └── fullstack-architecture.md
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project readme
└── run.py                          # Application entry point
```
