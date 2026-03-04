# Task Manager API

A production-style REST API built using **FastAPI** that supports authentication, secure task management, and modern backend architecture practices.

This project demonstrates how to design a clean backend service with authentication, pagination, search, sorting, and rate limiting.

---

# Features

- JWT Authentication
- Refresh Token Rotation
- Secure Password Hashing (bcrypt)
- User Registration and Login
- Task CRUD Operations
- Pagination
- Search and Filtering
- Sorting
- Rate Limiting
- User-scoped data access (IDOR protection)
- Layered architecture (routers → services → models)

---

# Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- JWT (JSON Web Tokens)
- Passlib (bcrypt)
- SlowAPI (Rate Limiting)
- Pydantic (Data validation)

---

# Project Architecture

The project follows a layered architecture separating routing, business logic, and data models to keep the code maintainable and scalable.

task-manager-api
│
├── auth
│ ├── deps.py
│ ├── jwt_handler.py
│ └── security.py
│
├── routers
│ ├── auth.py
│ └── tasks.py
│
├── services
│ ├── auth_service.py
│ ├── task_service.py
│ └── user_service.py
│
├── config.py
├── database.py
├── main.py
├── models.py
├── rate_limiter.py
└── schemas.py


---

# Security Implementations

- Password hashing using bcrypt
- JWT access tokens for authentication
- Refresh token rotation with revocation
- Protection against IDOR (user-scoped queries)
- Rate limiting to prevent abuse
- Input validation using Pydantic schemas

---

# Run the Project Locally

### Clone the repository
git clone https://github.com/deepthiyekkanti/task-manager-api.git


### Navigate to project folder
cd task-manager-api

### Create virtual environment
python -m venv venv

### Activate virtual environment
Mac / Linux
source venv/bin/activate
Windows
venv\Scripts\activate


### Install dependencies
pip install -r requirements.txt

### Run server
uvicorn main:app --reload

---

# API Documentation

Once the server is running, open:
http://127.0.0.1:8000/docs


FastAPI provides interactive Swagger documentation.

---

# Example Endpoints

Authentication

- POST `/auth/register`
- POST `/auth/login`
- POST `/auth/refresh`
- POST `/auth/logout`

Tasks

- POST `/tasks`
- GET `/tasks`
- PUT `/tasks/{task_id}`
- DELETE `/tasks/{task_id}`

---

# Future Improvements

- Docker containerization
- CI/CD pipeline
- Automated tests
- Cloud deployment
- Monitoring and logging

---

# Author

**Deepthi Yekkanti**

