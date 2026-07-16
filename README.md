# Django E-Commerce Store (Algeria Localized)

A comprehensive, full-featured E-Commerce Platform built with Django 5, optimized for the Algerian market with localized shipping (wilayas/communes), real-time updates, and a powerful management dashboard.

---

## Features

### Customer Frontend
- Product Discovery: Browse by category (Clothing, Electronics, Health, etc.) with a responsive, modern UI.
- Product Details: Detailed views with descriptions, pricing, and stock status.
- Localized Ordering: Optimized checkout flow for Algeria, including wilaya and commune selection.
- Feedback System: Customers can submit feedback with image uploads.

### Management Dashboard
- Stock Management: Comprehensive CRUD operations for products, including SKU/UUID tracking and category management.
- Order Tracking: Real-time order management with status updates (Pending, Confirmed, Shipped, Delivered, Cancelled).
- Real-time Analytics: Instant metrics on revenue, total sales, and low-stock alerts.
- User Notifications: In-app notifications for administrative actions and system updates.
- Site Configuration: Manage site-wide settings (Logo, Contact Info, Social Links) and dynamic SMTP configuration directly from the dashboard.

### Technical Highlights
- Real-time Updates: Integrated with django-eventstream for live SSE notifications.
- Dynamic Email: Custom DynamicSMTPBackend allowing SMTP settings to be configured via the database.
- Clean Architecture: Decoupled frontend, dashboard, and authentication modules.
- Localization: Full Arabic translation support for models and status choices.

---

## Docker Setup (Recommended)

The easiest way to run the project with all its dependencies (PostgreSQL, Redis).

### 1. Environment Setup
Create a .env file in the root directory and configure it based on .env.example:
```bash
cp .env.example .env
# Edit .env with your secrets, DB credentials, and site settings
```

### 2. Launch
```bash
# Default (Development)
docker compose up --build

# Production
docker compose -f docker-compose.prod.yml up --build -d
# Note: In production, Nginx is expected to be configured at the host level. 
# See nginx/django_store.host.conf for a sample configuration.
```

---

## Manual Setup (Alternative)

### 1. Prerequisites
- Python >= 3.10
- PostgreSQL & Redis (for full feature support)

### 2. Installation
```bash
git clone https://github.com/amraoui-mo7amed/inventory-management.git
cd inventory-management
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Initialization
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000 to view the store.
"# dj-store" 
