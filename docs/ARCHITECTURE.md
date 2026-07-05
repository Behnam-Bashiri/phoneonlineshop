# PhonyShop Architecture

## System Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────▶│    Nginx    │────▶│  Next.js    │
│  (React 19) │     │  (Reverse   │     │  Frontend   │
└─────────────┘     │   Proxy)    │     └─────────────┘
                    │             │
                    │             │────▶┌─────────────┐
                    └─────────────┘     │   Django    │
                                        │   REST API  │
                                        └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
              ┌─────▼─────┐           ┌───────▼───────┐          ┌───────▼───────┐
              │ PostgreSQL │           │    Redis      │          │    Celery     │
              │  Database  │           │ Cache/Queue   │          │   Workers     │
              └───────────┘           └───────────────┘          └───────────────┘
```

## Backend Architecture (Clean Architecture)

```
apps/
├── accounts/     # User domain — auth, wallet, membership
├── catalog/      # Product domain — products, variants, brands
├── cart/         # Cart domain — cart management
├── orders/       # Order domain — checkout, fulfillment
├── payments/     # Payment domain — gateway integration
├── promotions/   # Promotion domain — coupons, flash sales
├── reviews/      # Review domain — reviews, Q&A
├── blog/         # Content domain — blog posts
├── cms/          # CMS domain — pages, banners, settings
├── support/      # Support domain — tickets
├── notifications/# Notification domain — in-app, email, SMS ready
├── inventory/    # Inventory domain — warehouses, stock
├── search/       # Search domain — instant search
└── analytics/    # Analytics domain — dashboard stats

Each app follows:
  models.py      → Data layer (Django ORM)
  serializers.py → API contract layer
  views.py       → Presentation layer (DRF ViewSets)
  services.py    → Business logic layer
  admin.py       → Admin interface
  urls.py        → Route definitions
```

## Frontend Architecture

```
src/
├── app/[locale]/          # App Router pages (i18n)
├── components/
│   ├── ui/                # Shadcn/UI primitives
│   ├── layout/            # Header, Footer, Navigation
│   ├── home/              # Homepage sections
│   ├── product/           # Product catalog & detail
│   ├── cart/              # Cart components
│   ├── checkout/          # Checkout flow
│   ├── account/           # User dashboard
│   └── common/            # Shared components
├── services/              # API service layer (Axios)
├── stores/                # Zustand state management
├── hooks/                 # Custom React hooks
├── lib/                   # Utilities, validations, i18n
├── types/                 # TypeScript interfaces
└── locales/               # en.json, fa.json translations
```

## Authentication Flow

```
Client                    API                     Database
  │                        │                         │
  │── POST /auth/login/ ──▶│                         │
  │                        │── Validate credentials ─▶│
  │                        │◀── User record ──────────│
  │◀── access + refresh ───│                         │
  │                        │                         │
  │── GET /catalog/ ──────▶│ (Bearer access token)   │
  │                        │── Verify JWT ───────────▶│
  │◀── Product list ───────│                         │
  │                        │                         │
  │── POST /auth/refresh/ ─▶│ (on 401)               │
  │◀── new access token ───│                         │
```

## Deployment

- **Development**: `docker compose up` — all services with hot reload
- **Production**: `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`
- **CI/CD**: GitHub Actions — test, lint, build on push to main/develop

## Security

- JWT with refresh token rotation and blacklisting
- CSRF protection on session endpoints
- Rate limiting via DRF throttling + Nginx
- Security headers (XSS, clickjacking, MIME sniffing)
- SQL injection protection via Django ORM
- Input validation via DRF serializers + Zod (frontend)
