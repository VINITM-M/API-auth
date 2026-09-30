from fastapi import FastAPI
from routes import router
from db import init_db

init_db()

app = FastAPI(
    title="FastAPI Application",
    description="Weather app using FastAPI",
)

app.include_router(router.api_router, prefix="/api")