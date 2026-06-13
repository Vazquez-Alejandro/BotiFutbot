import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config import get_settings
from api.routes import auth, leagues, users, monetization, mundial
from shared.database import engine, Base

settings = get_settings()

app = FastAPI(title="BotiFutbol API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(leagues.router)
app.include_router(users.router)
app.include_router(monetization.router)
app.include_router(mundial.router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "BotiFutbol API"}
