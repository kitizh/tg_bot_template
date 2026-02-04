from __future__ import annotations

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.types import Message

from bot.common.handlers import BaseHandlers
from bot.states.registration import RegistrationSG

import logging

log = logging.getLogger(__name__)


async def reg_start(message: Message, state: FSMContext) -> None:
    log.info("Registration start: %s", message.from_user.id if message.from_user else None)
    await state.clear()
    await state.set_state(RegistrationSG.name)
    await message.answer("Введите имя:")


async def reg_cancel(message: Message, state: FSMContext) -> None:
    log.info("Registration cancelled: %s", message.from_user.id if message.from_user else None)
    await state.clear()
    await message.answer("Ок, отменил. Состояние очищено ✅")


async def reg_name(message: Message, state: FSMContext) -> None:
    name = (message.text or "").strip()
    if not name:
        await message.answer("Имя не может быть пустым. Введите имя:")
        return

    await state.update_data(name=name)
    await state.set_state(RegistrationSG.phone)
    await message.answer("Теперь отправьте номер телефона (текстом) или контакт:")


async def reg_phone(message: Message, state: FSMContext) -> None:
    if message.contact and message.contact.phone_number:
        phone = message.contact.phone_number
    else:
        phone = (message.text or "").strip()

    if not phone:
        await message.answer("Не вижу номер. Отправьте телефон текстом или контакт.")
        return

    await state.update_data(phone=phone)
    data = await state.get_data()
    await state.clear()
    log.info("Registration completed: %s", message.from_user.id if message.from_user else None)

    await message.answer(
        "Готово ✅\n"
        f"Имя: {data.get('name')}\n"
        f"Телефон: {data.get('phone')}"
    )


class RegistrationHandlers(BaseHandlers):
    """Хендлеры регистрации пользователя."""

    def register(self) -> None:
        self.router.message.register(reg_start, Command("reg"))
        self.router.message.register(reg_cancel, Command("cancel"))
        self.router.message.register(reg_name, StateFilter(RegistrationSG.name))
        self.router.message.register(reg_phone, StateFilter(RegistrationSG.phone))


# экспортируем router как раньше, чтобы main.py был простым
router = RegistrationHandlers().router
