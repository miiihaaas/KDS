# Coding Standards

## Critical Fullstack Rules

- **Konzistentnost JavaScript-a**: Koristi vanilla ES6+ JavaScript kroz ceo frontend bez mešanja framework-ova
- **Flask Blueprint organizacija**: Svaki funkcionalni domen ima svoj blueprint (auth, clients, devices, work_orders, admin)
- **Template nasleđivanje**: Svi template-i naslеđuju base.html i koriste block strukture
- **API response format**: Svi API endpoint-i vraćaju konzistentne JSON structure sa standardnim error handling-om
- **Database transaction handling**: Koristi try/except/rollback pattern za sve database operacije
- **QR kod standard**: Svi QR kodovi koriste isti format (jedinstveni_id) i generation/scanning library
- **Session management**: Koristi Flask-Login za sve authentication/authorization potrebe

## Naming Conventions

| Element | Frontend | Backend | Example |
|---------|----------|---------|---------|
| CSS Classes | kebab-case | N/A | `.client-card`, `.qr-scanner-btn` |
| JavaScript Functions | camelCase | N/A | `scanQRCode()`, `createWorkOrder()` |
| JavaScript Variables | camelCase | N/A | `currentClient`, `workOrderData` |
| Python Functions | snake_case | snake_case | `get_client_by_id()`, `create_work_order()` |
| Python Classes | PascalCase | PascalCase | `ClientService`, `WorkOrderForm` |
| Database Tables | snake_case | snake_case | `work_orders`, `material_usage` |
| Flask Routes | kebab-case | kebab-case | `/work-orders/new`, `/api/qr-scan` |
| Template Files | kebab-case | snake_case | `work-order-detail.html` |
