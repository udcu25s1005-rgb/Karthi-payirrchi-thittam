from fastapi import FastAPI

from app.database import init_db
from app.routes import api, router


app = FastAPI(
    title="FitBuddy API",
    version="1.0.0",
    description=(
        "AI Fitness Plan Generator using "
        "FastAPI, Gemini and SQLite."
    ),
)


# Static files.


# Web routes.
app.include_router(
    router
)


# API routes.
app.include_router(
    api
)


@app.on_event("startup")
def startup():
    """
    Initialize the database when the application starts.
    """

    init_db()