"""Единая точка подключения роутеров."""

from bot.admin.handlers import router as admin_router
from bot.handlers.registration import router as registration_router
from bot.handlers.user import router as user_router

ROUTERS = [
    user_router,
    admin_router,
    registration_router,
]
