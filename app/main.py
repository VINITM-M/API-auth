from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from database import init_db
from database.db import ScopedSession
from routes.router import api_router

# Initialize database schema and migrate missing columns
try:
    init_db()
except Exception as e:
    print(f"Warning: Database connection on startup: {e}")

app = FastAPI(
    title="API Authentication & Key Management Service",
    description="Authentication and encrypted API key management system using FastAPI and PostgreSQL",
    version="1.0.0"
)

# Enable CORS for React frontend (runs on http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ensure database session is cleanly closed and removed after each request
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    finally:
        ScopedSession.remove()


# Global database exception handler
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    ScopedSession.remove()
    print(f"SQLAlchemy Database Error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database transaction error occurred. Please try again."}
    )


# Register routes with prefix /api
app.include_router(api_router, prefix="/api")
