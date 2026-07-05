# PhonyShop - Enterprise Mobile Phone E-Commerce Platform

[![CI](https://github.com/phonyshop/phonyshop/actions/workflows/ci.yml/badge.svg)](https://github.com/phonyshop/phonyshop/actions)

PhonyShop is a production-ready, enterprise-level e-commerce platform for selling mobile phones. Built with Django 5 + Next.js 15, featuring a modern Apple-inspired UI, full RTL/LTR bilingual support, and comprehensive e-commerce functionality.

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python, Django 5, DRF, PostgreSQL, Redis, Celery, JWT |
| **Frontend** | Next.js 15, React 19, TypeScript, TailwindCSS, Shadcn/UI |
| **Infrastructure** | Docker, Docker Compose, Nginx, GitHub Actions |

## Features

- Complete product catalog with variants (color, storage, RAM)
- Multi-step checkout with mock payment gateway
- User wallet, customer club (Bronze → VIP), loyalty points
- Support ticket system, blog, CMS, landing page builder
- Advanced search, filters, compare, wishlist
- Dark/light theme, Persian/English i18n, RTL support
- Admin dashboard with analytics
- OpenAPI/Swagger documentation
- JWT authentication with refresh tokens

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Docker (Recommended)

```bash
# Clone and start all services
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
docker compose up -d --build

# Run migrations and seed data
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_data
```

**Access:**
- Frontend: http://localhost:3000
- API: http://localhost:8000/api/v1/
- Swagger: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

**Default credentials (after seed):**
- Admin: `admin@phonyshop.com` / `admin123`
- Customer: `customer@phonyshop.com` / `customer123`

### Local Development

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver

# Frontend (separate terminal)
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Project Structure

```
phonyshop/
├── backend/                 # Django REST API
│   ├── config/              # Settings, URLs, Celery
│   ├── core/                # Shared utilities, middleware
│   ├── apps/                # Domain apps (14 modules)
│   └── tests/               # Pytest suite
├── frontend/                # Next.js 15 App Router
│   └── src/
│       ├── app/             # Pages (en/fa locales)
│       ├── components/      # UI components
│       ├── services/        # API layer
│       └── stores/          # Zustand state
├── nginx/                   # Reverse proxy config
├── docker/                  # Dockerfiles
├── docs/                    # ER diagram, architecture
└── docker-compose.yml
```

## API Documentation

Interactive OpenAPI docs available at `/api/docs/` when the backend is running.

Key endpoint groups:
- `/api/v1/auth/` — Authentication, profile, wallet
- `/api/v1/catalog/` — Products, brands, categories
- `/api/v1/cart/` — Shopping cart
- `/api/v1/orders/` — Checkout, orders
- `/api/v1/cms/home/` — Homepage data

## Testing

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm run lint && npm run build
```

## Production Deployment

1. Set production environment variables (see `.env.example`)
2. Configure SSL certificates in `nginx/ssl/`
3. Run `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`
4. Enable HTTPS in Nginx config

## License

Proprietary — PhonyShop © 2026
