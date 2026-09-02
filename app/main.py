from fastapi import FastAPI 

from app.routes.router import api_router 

app = FastAPI(
    title = "FastAPI Application",
    description="Weather app using FastAPI"
) 

app.include_router(api_router, prefix="/api") 