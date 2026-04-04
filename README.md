# Fuel Management System – Rwanda

A scalable, secure, and user-friendly **multi-branch fuel management system** for a company operating in Rwanda that trades diesel and petrol/premium fuel across multiple stations.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [User Roles](#user-roles)
- [Running Tests](#running-tests)

---

## Features

- **Role-Based Access Control (RBAC)** – Five roles: Pompiste, Branch Manager, Accountant, HQ Manager, Admin
- **Fuel Tank Monitoring** – Real-time tank levels, low-fuel alerts, status tracking
- **Pump Meter Tracking** – Start/end shift readings, auto-calculated fuel sold and revenue
- **Sales Management** – Cash and credit sales, auto-amount calculation
- **Credit Customer Management** – Customer records, outstanding balances, payment tracking
- **Fuel Restocking** – Restocking requests with approval workflow
- **Pricing & Discounts** – Admin-managed fuel prices, per-sale discounts
- **Reporting** – Daily reports, monthly reports, HQ dashboard, financial reports
- **Audit Logging** – All write operations are logged with user, timestamp, and IP
- **JWT Authentication** – Secure token-based auth with refresh and blacklist support

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 + Django REST Framework |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | PostgreSQL (SQLite for development/tests) |
| API Docs | drf-spectacular (Swagger + ReDoc) |
| Filtering | django-filter |
| CORS | django-cors-headers |
| Static Files | WhiteNoise |

---

## Project Structure

```
fuel_management_rwanda/
├── manage.py
├── requirements.txt
├── .env.example
├── core/
│   ├── settings.py
│   ├── test_settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── api/urls.py           # Central API router
│   ├── users/                # User model, roles, RBAC permissions
│   ├── branches/             # Branch (station) management
│   ├── tanks/                # Fuel tank monitoring & restocking
│   ├── pumps/                # Pump management & shift records
│   ├── sales/                # Sales, fuel prices, discounts
│   ├── customers/            # Credit customers, transactions, payments
│   ├── reports/              # Daily/monthly/HQ dashboard reports
│   └── audit/                # Audit log middleware
└── tests/
    ├── conftest.py
    └── test_api.py
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL 13+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/komezusenge/fuel_management_rwanda.git
cd fuel_management_rwanda

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials and secret key

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (Admin)
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (required in production) |
| `DEBUG` | Debug mode | `True` |
| `DB_NAME` | PostgreSQL database name | `fuel_management_db` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | (required) |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login (returns JWT tokens) |
| POST | `/api/auth/refresh/` | Refresh access token |
| POST | `/api/auth/logout/` | Logout (blacklist refresh token) |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/users/` | List / create users |
| GET/PUT/PATCH/DELETE | `/api/users/{id}/` | Retrieve / update / deactivate user |
| GET | `/api/users/me/` | Current user profile |
| POST | `/api/users/change-password/` | Change password |

### Branches
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/branches/` | List / create branches |
| GET/PUT/PATCH/DELETE | `/api/branches/{id}/` | Branch details |

### Tanks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/tanks/` | List / create tanks |
| GET/PUT/PATCH | `/api/tanks/{id}/` | Tank details |
| POST | `/api/tanks/{id}/add-fuel/` | Add fuel to tank |
| GET/POST | `/api/tanks/restocking/` | List / create restocking requests |
| POST | `/api/tanks/restocking/{id}/approve/` | Approve/reject request |

### Pumps & Shifts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/pumps/` | List / create pumps |
| GET/POST | `/api/pumps/shifts/` | List / create shift records |
| GET/PUT | `/api/pumps/shifts/{id}/` | Shift details |
| POST | `/api/pumps/shifts/{id}/close/` | Close shift (enter end reading) |

### Sales
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/sales/` | List / create sales |
| GET/POST | `/api/sales/prices/` | Fuel prices |
| GET/POST | `/api/sales/discounts/` | Discounts |

### Customers & Credit
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/customers/` | List / create credit customers |
| GET | `/api/customers/{id}/balance/` | Customer balance |
| GET/POST | `/api/customers/transactions/` | Credit transactions |
| GET/POST | `/api/customers/payments/` | Payments |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reports/daily/?date=YYYY-MM-DD` | Daily report |
| GET | `/api/reports/monthly/?year=YYYY&month=M` | Monthly report |
| GET | `/api/reports/dashboard/` | HQ dashboard |
| GET | `/api/reports/financial/` | Financial report (accountants) |

### API Documentation
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

---

## User Roles

| Role | Key | Permissions |
|------|-----|-------------|
| Pump Attendant | `pompiste` | Record shifts, cash/credit sales, register customers |
| Branch Manager | `branch_manager` | All pompiste access + reports, restocking, approvals |
| Accountant | `accountant` | Financial reports, payment tracking |
| HQ Manager | `hq_manager` | All branches oversight, approve requests |
| Admin | `admin` | Full system access |

---

## Running Tests

```bash
# Run all tests (uses SQLite in-memory DB)
python manage.py test --settings=core.test_settings

# Run specific app tests
python manage.py test --settings=core.test_settings apps.users
python manage.py test --settings=core.test_settings apps.tanks
python manage.py test --settings=core.test_settings tests
```

---

## Security Features

- JWT authentication with token rotation and blacklisting
- Role-based access control on every endpoint
- Audit log records all write operations (POST/PUT/PATCH/DELETE)
- Password validation via Django's built-in validators
- CORS headers configured
- WhiteNoise for secure static file serving
