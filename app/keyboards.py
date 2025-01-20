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
        [
            KeyboardButton(text="Узнать БЖУ"),
            KeyboardButton(text="Составить диетный план"),
        ],
        [KeyboardButton(text="Составить план тренировок")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите нужную команду",
)

contacts = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Стасяныч", url="https://t.me/phantom2107/")],
        [InlineKeyboardButton(text="Степс", url="https://t.me/stakez0/")],
    ]
)
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
    input_field_placeholder="Выберите нужную команду",
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Узнать БЖУ"),
            KeyboardButton(text="Составить диетный план"),
        ],
        [KeyboardButton(text="Составить план тренировок")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите нужную команду",
)

contacts = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Стасяныч", url="https://t.me/phantom2107/")],
        [InlineKeyboardButton(text="Степс", url="https://t.me/stakez0/")],
    ]
)
