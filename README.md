# Task Manager API

A production-style REST API built with **FastAPI and PostgreSQL** that demonstrates modern backend engineering practices including **JWT authentication, refresh token rotation, rate limiting, and layered architecture**.

The project focuses on building a **secure, scalable backend service** with authentication, task management, pagination, filtering, and clean separation of business logic.

---

## Features

### Authentication & Security
- JWT Authentication
- Refresh Token Rotation
- Secure Password Hashing (bcrypt)
- Rate Limiting
- Protection against IDOR (user-scoped queries)

### Task Management
- User Registration and Login
- Task CRUD Operations

### Query Features
- Pagination
- Search and Filtering
- Sorting

### Architecture
- Layered architecture (routers → services → models)
---

## Tech Stack

- **FastAPI** – Web framework
- **PostgreSQL** – Relational database
- **SQLAlchemy** – ORM
- **JWT (PyJWT)** – Authentication tokens
- **Passlib (bcrypt)** – Password hashing
- **SlowAPI** – Rate limiting
- **Pydantic** – Data validation

---

## Project Architecture

The project follows a **layered architecture** that separates routing, business logic, and data models to improve maintainability and scalability.

```
task-manager-api
│
├── auth
│   ├── deps.py
│   ├── jwt_handler.py
│   └── security.py
│
├── routers
│   ├── auth.py
│   └── tasks.py
│
├── services
│   ├── auth_service.py
│   ├── task_service.py
│   └── user_service.py
│
├── config.py
├── database.py
├── main.py
├── models.py
├── rate_limiter.py
└── schemas.py

---
```

## Architecture Overview

- **Routers** handle HTTP requests and responses.
- **Services** contain business logic and application rules.
- **Models** define database structure using SQLAlchemy.
- **Schemas** define request and response validation using Pydantic.
- **Auth module** manages authentication, JWT tokens, and security utilities.

This separation ensures that the API remains modular, testable, and easier to scale.

---

## Security Implementations

- Password hashing using **bcrypt**
- **JWT access tokens** for authentication
- **Refresh token rotation** for session security
- Protection against **IDOR (Insecure Direct Object Reference)**
- **Rate limiting** to prevent abuse
- Request validation using **Pydantic schemas**

---

## Run the Project

### Clone the repository
```bash
git clone https://github.com/deepthiyekkanti/task-manager-api.git
```

### Navigate to project folder
```bash
cd task-manager-api
```

### Create virtual environment
```bash
python -m venv venv
```

### Activate virtual environment

Mac / Linux

```bash
source venv/bin/activate
```

Windows
```bash
venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run server
```bash
uvicorn main:app --reload
```

---

## API Documentation

Once the server is running, open:

```
http://127.0.0.1:8000/docs
```

FastAPI provides interactive Swagger documentation.

---


## Example Endpoints

| Method | Endpoint | Description |
|------|------|------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT tokens |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Revoke refresh token |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Retrieve user tasks |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

---

## Future Improvements

- Docker containerization
- CI/CD pipeline (GitHub Actions)
- Automated API tests (Pytest)
- Cloud deployment (AWS / GCP)
- Logging and monitoring (Prometheus / Grafana)

---

## API Demo

FastAPI automatically generates interactive API documentation.

Visit: http://127.0.0.1:8000/docs

You can test endpoints directly from the Swagger UI.

## API Test Scenarios

The API was tested with multiple scenarios including:

### Authentication
- Successful user registration and login
- Login with invalid credentials
- Access with expired JWT tokens
- Access with missing or malformed tokens

### Authorization & Security
- Unauthorized access attempts
- IDOR prevention (user-scoped data access)
- Refresh token rotation security
- Revoked refresh token usage
- Expired refresh token handling

### Task Operations
- Task creation, retrieval, update, and deletion
- Access control ensuring users can only access their own tasks

### Query Features
- Pagination boundary validation
- Sorting with valid and invalid fields
- Search filtering functionality

### Validation & Error Handling
- Input validation errors
- Invalid query parameter handling
- Large pagination values rejected

### Abuse Protection
- Rate limiting validation

## Author

**Deepthi Yekkanti**

GitHub: https://github.com/deepthiyekkanti

