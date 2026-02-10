from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from bot.common.handlers import BaseHandlers
from bot.core.config import settings
from bot.filters.text_prefix import TextPrefix
from bot.services.user import UserService
from bot.ui import (
    build_inline_keyboard,
    build_inline_menu,
    build_reply_keyboard,
    remove_reply_keyboard,
)


class UserHandlers(BaseHandlers):
    """Хендлеры для базовых пользовательских команд."""

    def register(self) -> None:
        @self.router.message(CommandStart())
        async def start(message: Message, user_service: UserService) -> None:
            await message.answer(user_service.get_welcome_text())

        @self.router.message(Command("help"))
        async def help_command(message: Message) -> None:
            user_id = message.from_user.id if message.from_user else 0
            is_admin = user_id in settings.admin_ids
            lines = [
                "Доступные команды:",
                "/start — старт",
                "/help — помощь",
                "/reg — регистрация",
                "/cancel — отменить регистрацию",
                "/kb_inline — пример inline‑клавиатуры",
                "/kb_reply — пример reply‑клавиатуры",
                "/kb_hide — скрыть reply‑клавиатуру",
            ]
            if is_admin:
                lines += [
                    "",
                    "Админские команды:",
                    "/admin — админ‑панель",
                    "/stats — статистика",
                    "/broadcast — рассылка",
                ]
            await message.answer("\n".join(lines))

        @self.router.message(Command("kb_inline"))
        async def show_inline_keyboard(message: Message) -> None:
            await message.answer(
                "Пример inline‑клавиатуры:",
                reply_markup=build_inline_keyboard(),
            )

        @self.router.message(Command("kb_reply"))
        async def show_reply_keyboard(message: Message) -> None:
            await message.answer(
                "Пример reply‑клавиатуры:",
                reply_markup=build_reply_keyboard(),
            )

        @self.router.message(Command("kb_hide"))
        async def hide_reply_keyboard(message: Message) -> None:
            await message.answer("Скрываю клавиатуру.", reply_markup=remove_reply_keyboard())

        @self.router.message(F.text.casefold() == "ping")
        async def magicfilter_ping(message: Message) -> None:
            await message.answer("pong")

        @self.router.message(TextPrefix("say "))
        async def custom_filter_echo(message: Message) -> None:
            text = (message.text or "")[len("say "):].strip()
            await message.answer(text or "Пусто.")

        @self.router.callback_query(F.data.startswith("kb:inline:"))
        async def inline_choice(callback: CallbackQuery) -> None:
            await callback.answer()
            await callback.message.answer(f"Вы выбрали: {callback.data}")

        @self.router.callback_query(F.data.startswith("kb:menu:"))
        async def inline_menu(callback: CallbackQuery) -> None:
            await callback.answer()
            if callback.data == "kb:menu:main":
                await callback.message.edit_text(
                    "Inline меню:",
                    reply_markup=build_inline_menu(),
                )
                return
            if callback.data == "kb:menu:back":
                await callback.message.edit_text(
                    "Пример inline‑клавиатуры:",
                    reply_markup=build_inline_keyboard(),
                )
                return

            if callback.data == "kb:menu:a":
                label = "A"
            else:
                label = "B"

            new_text = f"Вы выбрали {label}"
            if callback.message.text == new_text:
                return

            await callback.message.edit_text(
                new_text,
                reply_markup=build_inline_menu(),
            )

        @self.router.message(F.text == "Hide keyboard")
        async def hide_keyboard_on_reply(message: Message) -> None:
            await message.answer("Скрываю клавиатуру.", reply_markup=remove_reply_keyboard())


router = UserHandlers().router
