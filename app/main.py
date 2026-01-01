from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.api.v1.endpoints import auth, feed, messages, users # 1. Ajout de users

# Création automatique des tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BuildConnect API", version="1.0.0")

# CORS - Configuration robuste
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://buildconnect-nine.vercel.app"
    ],
    # CETTE LIGNE autorise toutes tes URL de test Vercel d'un coup :
    allow_origin_regex=r"https://buildconnect-.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes avec le préfixe /v1 pour correspondre au Frontend
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(feed.router, prefix="/api/v1/feed", tags=["Feed"])
app.include_router(messages.router, prefix="/api/v1/messages", tags=["Messages"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
def home():
    return {
        "status": "BuildConnect Backend is Live",
        "version": "1.0.0",
        "docs": "/docs"
    }