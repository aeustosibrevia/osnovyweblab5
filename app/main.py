from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.apartment import router as apartment_router
from app.core.config import settings
from app.db.database import Base, engine
from app.db import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description="REST API для керування квартирами, призначеними для продажу",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API працює"}

@app.get("/")
def root():
    return {
        "message": "Apartment Sales API is running",
        "docs": "/docs",
        "apartments": "/api/apartments"
    }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": ".".join(str(part) for part in error["loc"]),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Помилка валідації даних",
            "errors": errors,
        },
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Помилка під час роботи з базою даних",
        },
    )


app.include_router(apartment_router)
