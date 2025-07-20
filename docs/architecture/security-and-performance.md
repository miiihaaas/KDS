# Security and Performance

## Security Requirements

**Frontend Security:**
- CSP Headers: `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';`
- XSS Prevention: Jinja2 auto-escaping enabled, input sanitization
- Secure Storage: Session cookies with secure flags

**Backend Security:**
- Input Validation: WTForms validation za sve forme
- Rate Limiting: Flask-Limiter za login endpoint-e
- CORS Policy: Restricted to same origin

**Authentication Security:**
- Token Storage: Server-side sessions sa Flask-Login
- Session Management: Secure session cookies, auto logout
- Password Policy: Minimum 8 karaktera, hash sa werkzeug

## Performance Optimization

**Frontend Performance:**
- Bundle Size Target: < 500KB total JavaScript
- Loading Strategy: Lazy loading za QR scanner komponente
- Caching Strategy: Browser caching za static assets (1 mesec)

**Backend Performance:**
- Response Time Target: < 500ms za API pozive
- Database Optimization: Proper indexing, query optimization
- Caching Strategy: Flask-Caching za često pristupane podatke
