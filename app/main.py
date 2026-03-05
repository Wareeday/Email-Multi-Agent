from fastapi import FastAPI
from app.api import router
from app.database.session import engine
from app.database import models
from app.utils.logger import logger

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Agent Email AI System", version="1.0.0")
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Email AI System...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")