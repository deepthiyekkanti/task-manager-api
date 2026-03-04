from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from rate_limiter import limiter

from database import engine
from models import Base
from routers import auth, tasks

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="Task management REST API with JWT authentication, refresh token rotation, pagination, search, and rate limiting.",
    docs_url="/docs",
    openapi_tags=[{"name": "Auth"}, {"name": "Tasks"}],
)

# --- Rate limiting ---
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests. Please slow down."})


# --- Create tables (dev) ---
Base.metadata.create_all(bind=engine)


# --- Custom OpenAPI (Authorize button with Bearer JWT) ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    schema = get_openapi(
        title="Task Manager API",
        version="1.0.0",
        description="Task management REST API with JWT authentication, refresh token rotation, pagination, search, and rate limiting.",
        routes=app.routes,
    )

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi


# --- Include routers ---
app.include_router(tasks.router)
app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}