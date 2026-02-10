from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


def build_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Inline 1", callback_data="kb:inline:1"),
                InlineKeyboardButton(text="Inline 2", callback_data="kb:inline:2"),
            ],
            [InlineKeyboardButton(text="Menu", callback_data="kb:menu:main")],
            [InlineKeyboardButton(text="Open site", url="https://example.com")],
        ]
    )


def build_inline_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Option A", callback_data="kb:menu:a")],
            [InlineKeyboardButton(text="Option B", callback_data="kb:menu:b")],
            [InlineKeyboardButton(text="Back", callback_data="kb:menu:back")],
        ]
    )


def build_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Reply 1"),
                KeyboardButton(text="Reply 2"),
            ],
            [
                KeyboardButton(text="Send contact", request_contact=True),
                KeyboardButton(text="Hide keyboard"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите кнопку",
    )


def remove_reply_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
