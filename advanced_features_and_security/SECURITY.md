# Security Best Practices Applied

1. **DEBUG=False** in production to avoid info leaks.
2. **Browser XSS & Clickjacking protections**:
   - `SECURE_BROWSER_XSS_FILTER = True`
   - `X_FRAME_OPTIONS = 'DENY'`
   - `SECURE_CONTENT_TYPE_NOSNIFF = True`
3. **Secure cookies**:
   - `CSRF_COOKIE_SECURE = True`
   - `SESSION_COOKIE_SECURE = True`
4. **HSTS enforced**:
   - `SECURE_HSTS_SECONDS = 31536000`, etc.
5. **CSRF tokens** added to all forms (`{% csrf_token %}`).
6. **ORM filtering** used instead of raw SQL.
7. **CSP** enabled via [django-csp] to restrict external scripts/styles.

_Testing: log in and submit each form, and verify cookies are `Secure` and CSP header appears in the response._
