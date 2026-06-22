from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import api_router
from .core.config import APP_NAME
from .core.database import SessionLocal
from .db.init_db import create_tables, seed_database


app = FastAPI(title=APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    create_tables()
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


app.include_router(api_router)
