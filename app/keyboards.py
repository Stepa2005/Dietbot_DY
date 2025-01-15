from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


register_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Войти'),
                                      KeyboardButton(text = 'Зарегистрироваться')],
                                     ],resize_keyboard=True)

main_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Руководство пользователя')],
                                     [KeyboardButton(text = 'Узнать БЖУ'),
                                      KeyboardButton(text = 'Составить диетный план')],
                                     [KeyboardButton(text = 'Контакты'),
                                       KeyboardButton(text = 'О нас')]],
                                       resize_keyboard=True)

PFC = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Курица', callback_data ='Chicken')],
                                           [InlineKeyboardButton(text='Рис', callback_data = 'Rice')]])   #БЖУ

