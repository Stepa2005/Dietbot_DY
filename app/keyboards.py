from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


register = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Войти"), KeyboardButton(text="Зарегистрироваться")],
    ],
    resize_keyboard=True,
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Руководство пользователя")],
        [
            KeyboardButton(text="Узнать БЖУ"),
            KeyboardButton(text="Составить диетный план"),
        ],
        [KeyboardButton(text="Контакты"), KeyboardButton(text="О нас")],
    ],
    resize_keyboard=True,
)

contacts = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Стасяныч", url="https://t.me/phantom2107/")],
        [InlineKeyboardButton(text="Степс", url="https://t.me/stakez0/")],
    ]
)
