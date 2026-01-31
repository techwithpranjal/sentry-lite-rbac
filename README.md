# Sentry Lite RBAC

A lightweight, production-inspired Role-Based Access Control (RBAC) system built to demonstrate how modern teams manage applications, roles, memberships, and access requests at scale.

This project is intentionally designed as a realistic internal tool, not a toy CRUD app. It mirrors how RBAC actually works inside SaaS companies.


## Live Demo

- **Frontend (GitHub Pages)**  
  https://techwithpranjal.github.io/sentry-lite-rbac/

- **Backend API (Railway)**  
  https://sentry-lite-rbac-production.up.railway.app

- **Swagger Docs**
  https://sentry-lite-rbac-production.up.railway.app/docs#/

> The frontend is deployed using hash-based routing on GitHub Pages.  
> The backend is deployed on Railway with JWT-based authentication.




### Demo Login Credentials

**Super Admin**
- Email: `admin@sentry.io`
- Password: `admin123`

**Standard Users**
- Email: `alice@corp.com`
- Email: `bob@corp.com`
- Email: `charlie@corp.com`
- Password (all users): `password`

> The super admin has access to the Admin Dashboard and global system controls.


## Overview

Sentry Lite RBAC answers one core question:

Who can access what, and why?

The system allows:
- Users to authenticate
- Applications to define roles
- Users to be assigned roles via memberships
- Users to request access
- Admins to review, approve, or reject access

It is split into:
- Backend: FastAPI + SQLModel + JWT
- Frontend: Angular (Standalone API) + Tailwind CSS
- Database: SQLite (dev/demo, easily swappable)

The project is deployed as:
- Frontend → GitHub Pages
- Backend → Railway


## Core Concepts (RBAC Model)

### Users
- Identified by email
- Can be normal users or super admins

### Applications
- Logical internal tools (e.g. Revenue Analysis, Design Factory)
- Each application has a point-of-contact (POC)

### Roles
- Defined per application
- Examples:
  - Admin
  - Analyst
  - Editor
  - Auditor
  - Designer
  - Viewer

### Memberships
- Mapping of user → application → role
- Created by an admin or application owner

### Requests
- Users can request access to a role in an application
- Requests follow a lifecycle:
  - pending
  - approved
  - rejected

This structure closely matches how tools like Okta, AWS IAM, and internal enterprise RBAC systems work.


## Database Design

The database uses SQLModel (SQLAlchemy + Pydantic).

### Tables
- user
- app
- role
- membership
- request

### Key Relationships
- app.poc_user_email → user.email
- role.app_id → app.id
- membership.user_email → user.email
- membership.role_id → role.id
- request.role_id → role.id

Foreign keys are intentionally explicit to surface real-world constraints.


## Backend Architecture

### Technology Stack
- FastAPI
- SQLModel
- JWT authentication (python-jose)
- Passlib + bcrypt for password hashing

### Authentication Flow
1. User logs in with email and password
2. Backend validates credentials
3. JWT access token is issued
4. Token is sent via Authorization header
5. Protected routes validate the token

### Backend Design
- Router-based separation (auth, apps, roles, memberships, requests, admin)
- Dependency-based authentication
- Explicit read/write schemas
- Deterministic seed data for demos


## Frontend Architecture

### Technology Stack
- Angular (Standalone API)
- Angular Router (hash-based routing)
- Tailwind CSS
- TypeScript

### Routing
- Public routes:
  - /login
  - /register
- Protected routes:
  - /dashboard
  - /apps
  - /roles
  - /members
  - /access
  - /admin

All protected routes are wrapped by AuthenticatedLayoutComponent.

### Guards
- CanActivateChild guard protects authenticated routes
- Unauthenticated users are redirected to login

### State Management
- JWT stored in browser storage
- AuthService acts as the single source of truth


## Demo Seed Data

### Demo Users
- admin@sentry.io (super admin)
- alice@corp.com
- bob@corp.com
- charlie@corp.com
- david@corp.com
- emma@corp.com
- frank@corp.com
- grace@corp.com
- henry@corp.com
- ivy@corp.com


### Demo Applications
- Revenue Analysis
- Customer Insights
- Design Factory
- Access Audit Tool
- Operations Console

### Example Roles
- Admin
- Analyst
- Editor
- Auditor
- Designer
- Support
- Viewer


## Admin Dashboard

The admin section provides:
- System-wide statistics
- Pending access requests
- Role and membership visibility
- Operational metrics

## End-to-End Workflow

1. User registers or logs in
2. User views available applications
3. User browses roles within an application
4. User submits an access request with justification
5. Request appears as `pending`
6. Admin or App Owner reviews the request
7. Request is approved or rejected
8. On approval, a membership is created
9. User gains access to the role

This mirrors real-world RBAC flows used in internal enterprise tools.

## Screenshots

> Screenshots are intentionally listed in workflow order.

- Login & Authentication

![Login page.](/frontend/assets/asset1.png)

- Register New User

![Register page.](/frontend/assets/asset2.png)
  
- Dashboard Overview

![Dashboard page.](/frontend/assets/asset3.png)

- My Applications List

![My Apps page.](/frontend/assets/asset4.png)

- All Applications List

![All Apps page.](/frontend/assets/asset5.png)

- Roles per Application

![Roles page.](/frontend/assets/asset6.png)

- Members per Role

![Members page.](/frontend/assets/asset7.png)

- Access Requests 

![Requests page.](/frontend/assets/asset8.png)

- Approvals

![Approvals page.](/frontend/assets/asset9.png)

- Memberships

![Memberships page.](/frontend/assets/asset10.png)

- Admin Overview Dashboard

![Admin Overview page.](/frontend/assets/asset11.png)

- Admin View Applications
  
![Admin Apps page.](/frontend/assets/asset12.png)

- Admin View Roles

![Admin Roles page.](/frontend/assets/asset13.png)

- Admin View Requests

![Admin Requests page.](/frontend/assets/asset14.png)

- Admin View Memberships

![Admin Memberships page.](/frontend/assets/asset15.png)



## Local Development Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git

### Clone Repository
```
git clone https://github.com/techwithpranjal/sentry-lite-rbac.git
cd sentry-lite-rbac
```

### Backend Setup
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:
http://localhost:8000

### Frontend Setup
```
cd frontend
npm install
ng serve
```

Frontend runs at:
http://localhost:4200


## Deployment

### Frontend (GitHub Pages)
- Hash-based routing
- Environment-specific base href
- Production build:
```
ng build --configuration production
```

### Backend (Railway)
- Docker-based deployment
- SQLite for demo
- Environment variables for JWT configuration


## Why This Project Exists

This project was built to:
- Demonstrate real RBAC modeling
- Show full-stack architectural thinking
- Mirror internal enterprise tooling
- Act as a strong portfolio artifact
