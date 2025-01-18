from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


register = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Войти'),
                                      KeyboardButton(text = 'Зарегистрироваться')],
                                     ],resize_keyboard=True,
                                     input_field_placeholder = 'Выберите нужную команду')

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = 'Узнать БЖУ'),
                                      KeyboardButton(text = 'Составить диетный план')],
                                     [KeyboardButton(text = 'Составить план тренировок')]],
                                       resize_keyboard=True,
                                       input_field_placeholder = 'Выберите нужную команду')

contacts = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Стасяныч', url='https://t.me/phantom2107/')],
                                           [InlineKeyboardButton(text='Степс', url='https://t.me/stakez0/')]])   

'''refresh_data = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Имя', callback_data = 'name')],
                                           [InlineKeyboardButton(text='Пол', callback_data = 'sex')],
                                           [InlineKeyboardButton(text='Возраст', callback_data = 'age')],
                                           [InlineKeyboardButton(text='Рост', callback_data = 'height')],
                                           [InlineKeyboardButton(text='Вес', callback_data = 'weight')],
                                           [InlineKeyboardButton(text='Физическая активность', callback_data = 'ph_condition')],
                                           [InlineKeyboardButton(text='Хронические заболевания (любые отклонения)', callback_data = 'ch_illnesses')],
                                           [InlineKeyboardButton(text='Цель', callback_data = 'goal')]])   

'''