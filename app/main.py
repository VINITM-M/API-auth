from fastapi import FastAPI
from database import init_db
from routes.router import api_router

init_db()

app = FastAPI(
    title="FastAPI Application",
    description="Weather app using FastAPI",
)

app.include_router(api_router, prefix="/api")