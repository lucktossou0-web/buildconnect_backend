from fastapi import APIRouter
from app.api.v1.endpoints import auth, feed, messages, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentification"])
api_router.include_router(feed.router, prefix="/feed", tags=["Le Feed"])
api_router.include_router(messages.router, prefix="/messages", tags=["Messagerie"])
api_router.include_router(users.router, prefix="/users", tags=["Utilisateurs"])