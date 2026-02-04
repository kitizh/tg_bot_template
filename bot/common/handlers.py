from __future__ import annotations

from aiogram import Router


class BaseHandlers:
    """Базовый класс для группировки хендлеров в Router."""
    def __init__(self, *, name: str | None = None) -> None:
        """Создает Router и вызывает регистрацию обработчиков."""
        self.router = Router(name=name)
        self.register()

    def register(self) -> None:
        """Регистрирует обработчики на self.router."""
        raise NotImplementedError
