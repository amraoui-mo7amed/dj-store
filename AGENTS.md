# Agent Guide: django-store (E-Commerce Platform)

## Developer Workflow
- Environment: Uses python-decouple. You must have a .env file in the root. Refer to .env.example for required keys (APP_SECRET, APP_ENV, DOCKERFILE, DB_*, REDIS_*, DJANGO_SUPERUSER_*, CSRF_TRUSTED_ORIGINS).
- Docker:
  - All configurations are centralized in .env.
  - The DOCKERFILE variable in .env determines the startup behavior (Dev vs Prod).
  - Includes Postgres and Redis services.
- Dev: docker compose up
- Prod: docker compose -f docker-compose.prod.yml up --build (Note: Nginx is now expected to be configured at the host level).

## Architecture High-Signals
- Localization: Localized for Algeria with wilaya/commune choices in dashboard/models.py.
- Notifications: Uses django-eventstream for SSE (Server-Sent Events). Client connects to /dashboard/sse/?channel=user:<id>. Events are pushed via send_event() in dashboard/utils.py (createNotification function). Also polls /dashboard/api/notifications/unread/<id>/ on load.
- Frontend: Vanilla JS and SweetAlert2. Static files are in /static/.
- Context Processors: frontend.context_processors.site_data injects global site data from SiteSettings into templates.

## Testing
- Tests are currently minimal/placeholders in */tests.py.
- Run tests via python manage.py test.

## Operational Gotchas
- APP_ALLOWED_HOSTS in .env should be comma-separated (e.g., localhost,127.0.0.1).
- DEBUG is automatically set to False if APP_ENV is production.

