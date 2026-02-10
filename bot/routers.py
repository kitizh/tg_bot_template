"""Единая точка подключения роутеров."""

from bot.handlers.admin import router as admin_router
from bot.handlers.fallback import router as fallback_router
from bot.handlers.registration import router as registration_router
from bot.handlers.user import router as user_router

ROUTERS = [
    user_router,
    admin_router,
    registration_router,
    fallback_router,
]
