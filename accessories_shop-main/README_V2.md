# Accessories Shop — Version 2.0

This is a cleaned and production-ready refactor of the original Django inventory/accessories shop project.

## What changed in Version 2.0

### Security
- Removed hardcoded production-style secret key from settings.
- Added environment variable based settings via `.env.example`.
- Added safer production defaults for cookies, CSRF, HSTS, referrer policy, and clickjacking protection.
- Added `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` environment support.
- Removed the bundled local SQLite database from the repo.
- Removed virtual environment files from the project zip.

### Performance
- Added `select_related()` on product/sale/history queries to reduce N+1 database queries.
- Replaced manual Python loops with database aggregation where safe.
- Optimized dashboard totals and report calculations.
- Improved brand/model/product search queries.

### Critical bug fixes
- Fixed invalid foreign-key search: `model__icontains` → `model__name__icontains`.
- Fixed product filtering bug where brand filter incorrectly used model id.
- Fixed sale flow to block selling more items than available stock.
- Wrapped stock update and sale creation in `transaction.atomic()`.
- Fixed profile signal behavior to avoid missing profile crashes.
- Fixed form initialization so model dropdown loads based on selected brand.
- Fixed repeated duplicate object fetches with `get_object_or_404()`.
- Fixed service total calculation using database aggregation.
- Fixed unsafe update-status endpoint to require POST.

### Architecture and code quality
- Cleaned duplicate imports and unused imports.
- Added helper functions for repeated dashboard logic.
- Added PEP 8 style formatting across updated files.
- Added `requirements.txt` with clean UTF-8 text.
- Added `.gitignore`.
- Added `.env.example`.
- Added Whitenoise static file support for production deployment.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```

## Production notes

Set these in your server environment:

```env
DJANGO_SECRET_KEY=your-real-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DJANGO_SECURE_SSL_REDIRECT=True
```

For production, PostgreSQL is recommended. SQLite is kept only for local development.

## Validation performed

- Python syntax compilation passed for all project files.
- Removed generated `__pycache__` files after validation.
- Removed local virtual environment and database files from final zip.

## Notes

The original database file was removed intentionally because databases should not be committed or shipped in production source code. If you need to preserve old data, export/import it separately using Django fixtures or database backup tools.
