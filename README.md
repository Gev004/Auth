# Auth System — Django REST Framework + PostgreSQL

## Overview

Custom authentication and authorization backend without relying on Django's built-in `auth` framework for access control logic.

---

## Architecture

### Authentication

- Passwords hashed with **bcrypt**
- After login, a **JWT token** is issued (via `PyJWT`)
- Token is sent in `Authorization: Bearer <token>` header
- Custom **Django Middleware** reads the header, decodes the token, and sets `request.user` before view processing

### Authorization (RBAC — Role-Based Access Control)

#### Database Schema

```
users
  id, first_name, last_name, middle_name, email, password_hash,
  is_active, created_at, updated_at, role_id (FK → roles)

roles
  id, name (admin | manager | user | guest), description

business_elements
  id, name, description
  Examples: users, products, shops, orders, access_rules

access_roles_rules
  id, role_id (FK → roles), element_id (FK → business_elements),
  read_permission         BOOL,
  read_all_permission     BOOL,
  create_permission       BOOL,
  update_permission       BOOL,
  update_all_permission   BOOL,
  delete_permission       BOOL,
  delete_all_permission   BOOL
```

#### Permission logic

- `read_permission` — can read **own** objects (where `owner_id = request.user.id`)
- `read_all_permission` — can read **all** objects
- `update_permission` / `delete_permission` — own objects only
- `update_all_permission` / `delete_all_permission` — all objects
- `create_permission` — can create new objects

#### Default Roles (seed data)

| Role    | Description                                      |
|---------|--------------------------------------------------|
| admin   | Full access to everything including rules API    |
| manager | CRUD on products/shops/orders, read users        |
| user    | CRUD own objects, read public resources          |
| guest   | Read-only access to products and shops           |

---

## Modules

### 1. User Management (`/api/users/`)

| Method | Endpoint               | Description            | Auth required |
|--------|------------------------|------------------------|---------------|
| POST   | `/api/auth/register/`  | Register new user      | No            |
| POST   | `/api/auth/login/`     | Login → returns JWT    | No            |
| POST   | `/api/auth/logout/`    | Logout (token blacklist) | Yes         |
| GET    | `/api/users/me/`       | Get own profile        | Yes           |
| PATCH  | `/api/users/me/`       | Update own profile     | Yes           |
| DELETE | `/api/users/me/`       | Soft-delete account    | Yes           |

### 2. Access Rules Admin (`/api/admin/`)

| Method | Endpoint                     | Description                  | Role  |
|--------|------------------------------|------------------------------|-------|
| GET    | `/api/admin/roles/`          | List all roles               | admin |
| GET    | `/api/admin/elements/`       | List business elements       | admin |
| GET    | `/api/admin/rules/`          | List all access rules        | admin |
| POST   | `/api/admin/rules/`          | Create rule                  | admin |
| PATCH  | `/api/admin/rules/<id>/`     | Update rule                  | admin |
| DELETE | `/api/admin/rules/<id>/`     | Delete rule                  | admin |

### 3. Mock Business Views (`/api/mock/`)

| Method | Endpoint             | Description         |
|--------|----------------------|---------------------|
| GET    | `/api/mock/products/`| List products       |
| GET    | `/api/mock/shops/`   | List shops          |
| GET    | `/api/mock/orders/`  | List own orders     |

---

## Setup

```bash
# 1. Clone / enter project
cd auth_project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure .env 
# Edit DB credentials

# 5. Make migrations
python manage.py makemigrations

# 6. Apply migrations
python manage.py migrate

# 7. Seed initial data
python manage.py seed_data

# 8. Run server
python manage.py runserver
```

---

## Environment Variables

```
SECRET_KEY=your-django-secret-key
JWT_SECRET=your-jwt-secret
DB_NAME=auth_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
```
