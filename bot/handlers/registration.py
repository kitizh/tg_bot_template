from __future__ import annotations

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.types import Message

from bot.common.handlers import BaseHandlers
from bot.states.registration import RegistrationSG


class RegistrationHandlers(BaseHandlers):
    """Хендлеры регистрации пользователя."""

    def register(self) -> None:
        @self.router.message(Command("reg"))
        async def reg_start(message: Message, state: FSMContext) -> None:
            await state.clear()
            await state.set_state(RegistrationSG.name)
            await message.answer("Введите имя:")

        @self.router.message(Command("cancel"))
        async def reg_cancel(message: Message, state: FSMContext) -> None:
            await state.clear()
            await message.answer("Ок, отменил. Состояние очищено ✅")

        @self.router.message(StateFilter(RegistrationSG.name))
        async def reg_name(message: Message, state: FSMContext) -> None:
            name = (message.text or "").strip()
            if not name:
                await message.answer("Имя не может быть пустым. Введите имя:")
                return

            await state.update_data(name=name)
            await state.set_state(RegistrationSG.phone)
            await message.answer("Теперь отправьте номер телефона (текстом) или контакт:")

        @self.router.message(StateFilter(RegistrationSG.phone))
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

            await message.answer(
                "Готово ✅\n"
                f"Имя: {data.get('name')}\n"
                f"Телефон: {data.get('phone')}"
            )


# экспортируем router как раньше, чтобы main.py был простым
router = RegistrationHandlers().router
