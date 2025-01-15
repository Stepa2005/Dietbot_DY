from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.types import CallbackQuery
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from html import escape
import asyncio
import logging
from bot import bot

import app.keyboards as kb

#Определим состояния:
class Register(StatesGroup):
    name = State()
    t_id = State()
    sex = State()
    weight = State()
    ph_condition = State() # Физическая активность
    ch_illnesses = State() # Хронические заболевания (любые отклонения)

listuser = {}    
router = Router()
@router.message(CommandStart(), State(None))
async def cmd_start(message: Message, state: FSMContext):
    await message.reply(f'Привет', reply_markup=kb.register_keyboard)  #{message.from_user.last_name} {message.from_user.first_name}! Ваш id={message.from_user.id}\n
    #await message.answer(f'Введите Вашу Фамилию и Имя', show_alert=True)
    #await state.update_data(lastfirstname=f'{message.from_user.last_name} {message.from_user.first_name}')
    #await state.set_state(Register.name)
    await message.answer(f'Пройдите регистрацию!')

@router.message(F.text == "Зарегистрироваться")
async def register(message: Message, state:FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.t_id)
    await message.answer('Для продолжения регистрации отправьте любое сообщение')

@router.message(Register.t_id)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(t_id=message.from_user.id)
    await message.answer('Для составления точного плана тренировок и питания ответайте и честно)')
    await state.set_state(Register.sex)
    await message.answer('Введите ваш пол ♂/♀')

@router.message(Register.sex)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(sex=message.text)
    await state.set_state(Register.weight)
    await message.answer('Введите ваш вес')

@router.message(Register.weight)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await state.set_state(Register.ph_condition)
    await message.answer('Напишите насколько вы активны, каким спортом занимаетесь и т.д.')

@router.message(Register.ph_condition)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(ph_condition=message.text)
    await state.set_state(Register.ch_illnesses)
    await message.answer('Есть ли у вас какие-то хронические заболевания, травмы (если нет, то напишите "нет")')

@router.message(Register.ch_illnesses)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(ch_illnesses=message.text)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data.name}\nВаш пол: {data.sex}\nВаш вес: {data.weight}\n')
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=kb.main_keyboard)
    await state.clear()

'''@router.message(Register.name)
async def inputfio(message: Message, state: FSMContext):
    if len(message.text.split()) != 2:
      await message.answer(f'Данные введены некорректно. Повторите ввод')
      return
    await message.answer(f'Данные приняты!', show_allert=True)
    #await state.set_state(Register.t_number)
    data = await state.get_data()
    listuser[message.from_user.id] = data['lastfirstname']
    print(listuser[message.from_user.id])
    await state.clear()'''

'''
@router.message(Register.t_number)
async def inputfio(message: Message, state: FSMContext):
    await message.answer(f'Введите номер телефона')
    data = await state.get_data()
    listuser[message.from_user.id] = data['lastfirstname']
    await state.clear()
'''
@router.message(Command("com1"), State(None))
async def cmd_com1(message: Message, state: FSMContext):
    await message.answer(f'Напишите продукт или блюдо, БЖУ которого вы хотите узнать.')
    if message.text.LowerCase == "курица":
        await message.answer(f'Б Ж У')
    #resize_keyboard=True: клавиатура будет автоматически изменять размер.
    #one_time_keyboard=True: клавиатура скрывается после одного использования.
    #input_field_placeholder: заменяет стандартную подпись «Написать сообщение...» на пользовательскую.

@router.message(Command("com2"), State(None))
async def cmd_com2(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Вывести содержание', callback_data='content')
    builder.button(text='Вывести информацию о справочнике', callback_data='about')
    builder.button(text="Мой Telegram", url='https://t.me/varn_alex/')
    builder.button(text="Веб приложение", web_app=WebAppInfo(url="https://tgbot.ru/app"))
    builder.adjust(1, 1, 2)
    await message.answer('Выберите действие:\nКлавиатура построена с использованием билдера.', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'content')
async def send_content(call: CallbackQuery):
    await call.answer('Отображаю содержание', show_alert=True)
    await call.message.answer("Содержание:\n1. Раздел 1.\n2. Раздел 2. \n3. Раздел 3.")

@router.message((F.text == "📖 О справочнике") | (F.text.lower() == 'о справочнике'))
@router.callback_query(F.data == 'about')
async def send_about(call_or_message):
    print(type(call_or_message))
    if type(call_or_message) == Message:
      objectmes = call_or_message
    else:
      objectmes = call_or_message.message
      await objectmes.answer('Отображаю содержание', show_alert=True)
    await objectmes.answer("Содержание:\n1. Раздел 1.\n2. Раздел 2. \n3. Раздел 3.")

@router.message(F.text.lower().in_({'справочник', 'раздел'}))
async def cmd_mes(message: Message):
    await message.answer("Это справочник!", reply_markup=ReplyKeyboardRemove())

'''@dp.message()
async def prtext(message: Message, state: FSMContext):
    await message.answer("Нельзя писать произвольный текст)")
'''
@router.message(F.text == "Узнать БЖУ")
async def PFC(message: Message):
    await message.answer("Выберите нужный продукт", reply_markup=kb.PFC)

@router.callback_query(F.data == 'Chicken')
async def chicken(call: CallbackQuery):
    await call.answer('Отображаю БЖУ', show_alert=True)
    await call.message.answer('1 10 15')