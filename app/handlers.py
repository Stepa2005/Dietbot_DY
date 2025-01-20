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
from aiogram.enums import ParseMode
import asyncio
from asyncio import run
import logging
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot import bot
from config import GigaChatKey
import app.keyboards as kb
import database.requests as rq
import database.models as models


# Определим состояния:
class Register(StatesGroup):
    name = State()
    tg_id = State()
    sex = State()
    age = State()
    height = State()
    weight = State()
    ph_condition = State()
    ch_illnesses = State()
    goal = State()


class Write(StatesGroup):
    can = State()


reminder_tasks = {}
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
router = Router()


def is_alpha(input_text: str) -> bool:
    cleaned_input = "".join([char for char in input_text if char.isalpha()])
    return len(cleaned_input) == len(input_text)


def is_digit(input_text: str) -> bool:
    cleaned_input = "".join([char for char in input_text if char.isdigit()])
    return len(cleaned_input) == len(input_text)


@router.message(CommandStart(), State(None))
async def cmd_start(message: Message, state: FSMContext):
    await message.reply(f"Привет", reply_markup=kb.register)
    await message.answer(f"Пройдите регистрацию!")


@router.message(F.text == "Зарегистрироваться")
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("Введите ваше имя")


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    if not is_alpha(message.text):
        await message.answer("Пожалуйста, введите только буквы для имени.")
        return
    await state.update_data(name=message.text)
    print("Данные после обновления имени:", await state.get_data())
    await state.set_state(Register.tg_id)
    await message.answer("Для продолжения регистрации отправьте любое сообщение")


@router.message(Register.tg_id)
async def register_tg_id(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.from_user.id)
    await message.answer(
        "Для составления точного плана тренировок и питания ответайте и честно)"
    )
    await state.set_state(Register.sex)
    await message.answer("Введите ваш пол мужской/женский")


@router.message(Register.sex)
async def register_sex(message: Message, state: FSMContext):
    if message.text not in ["мужской", "женский"]:
        await message.answer(
            "Пожалуйста, введите ваш пол как 'мужской' или 'женский' без кавычек."
        )
        return
    await state.update_data(sex=message.text)
    await state.set_state(Register.age)
    await message.answer("Введите ваш возраст")


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    if not is_digit(message.text):
        await message.answer(
            "Пожалуйста, введите только числовое значение для возраста (например, 25)."
        )
        return
    await state.update_data(age=message.text)
    await state.set_state(Register.height)
    await message.answer("Введите ваш рост")


@router.message(Register.height)
async def register_height(message: Message, state: FSMContext):
    if not is_digit(message.text):
        await message.answer(
            "Пожалуйста, введите только числовое значение для роста (например, 175)."
        )
        return
    await state.update_data(height=message.text)
    await state.set_state(Register.weight)
    await message.answer("Введите ваш вес")


@router.message(Register.weight)
async def register_weight(message: Message, state: FSMContext):
    if not is_digit(message.text):
        await message.answer(
            "Пожалуйста, введите только числовое значение для веса (например, 70)."
        )
        return
    await state.update_data(weight=message.text)
    await state.set_state(Register.ph_condition)
    await message.answer(
        "Напишите насколько вы активны, каким спортом занимаетесь и т.д."
    )


@router.message(Register.ph_condition)
async def register_ph_condition(message: Message, state: FSMContext):
    await state.update_data(ph_condition=message.text)
    await state.set_state(Register.ch_illnesses)
    await message.answer(
        'Есть ли у вас какие-то хронические заболевания, травмы, аллергии (если нет, то напишите "нет")'
    )


@router.message(Register.ch_illnesses)
async def register_ch_illnesses(message: Message, state: FSMContext):
    await state.update_data(ch_illnesses=message.text)
    await state.set_state(Register.goal)
    await message.answer(
        "Какие у вас цели (набрать мышечную массу, похудеть, исправить проблемы со здоровьем)?"
    )


async def send_reminder(tg_id: int):
    await bot.send_message(tg_id, "Пользуйтесь ботом побольше!")


@router.message(Register.goal)
async def register_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    data = await state.get_data()
    await rq.set_user(
        tg_id=message.from_user.id,
        name=data.get("name"),
        sex=data.get("sex"),
        age=int(data.get("age")),
        height=int(data.get("height")),
        weight=int(data.get("weight")),
        ph_condition=data.get("ph_condition"),
        ch_illnesses=data.get("ch_illnesses"),
        goal=data.get("goal"),
        is_registered=True,
    )
    await message.answer(
        f'Ваше имя: {data.get("name")}\nВаш пол: {data.get("sex")}\nВаш возраст: {data.get("age")}\nВаш рост: {data.get("height")}\nВаш вес: {data.get("weight")}\n',
        reply_markup=kb.register,
    )
    await message.answer("Теперь выберите действие:", reply_markup=kb.main)
    await state.clear()
    await state.clear()
    task = scheduler.add_job(
        send_reminder, "interval", seconds=180, args=[message.from_user.id]
    )
    reminder_tasks[message.from_user.id] = task
    await message.answer(
        "Напоминания включены! Я буду присылать уведомления каждые три минуты."
    )
    if not scheduler.running:
        scheduler.start()


@router.message(Command("contacts"), State(None))
async def contacts(message: Message):
    await message.answer(f"Контакты разработчиков", reply_markup=kb.contacts)


@router.message(F.text == "Войти")
async def abletowrite(message: Message, state: FSMContext):
    try:
        user_data = await rq.get_user_data(message.from_user.id)
        await message.answer(
            f'Добро пожаловать, {user_data["name"]}', reply_markup=kb.register
        )
        await message.answer("Теперь выберите действие:", reply_markup=kb.main)
    except Exception:
        await message.answer("Пройдите регистрацию!")


@router.message(Command("instruction"), State(None))
async def instruction(message: Message):
    instruction_text = """
    🎉 **Добро пожаловать, пройди регистрацию или войди в уже имеющийся аккаунт!** 🎉

    Здесь ты можешь узнать БЖУ любого продукта, составить план тренировок и питания под свои нужды.


    📌 **Как начать?**
    - Просто нажми на любую кнопку ниже.
    
    📝 **Как общаться с ботом?**
    - После нажатия кнопки Узнать БЖУ отправь название продукта в чат с ботом.
    - После нажатия кнопкок Составить диетный план и Составить план тренировок ничего писать боту не надо. Для правильной работы надо внимательно пройти регистрацию.

    ⚙️ **Доступные команды:**
    - `/start` - Начать заново.
    - `/instruction` - прочитать инструкцию.

    👨‍💻 **Использование Reply клавиатуры:**
    - **"Узнать БЖУ"** — После нажатия кнопки напиши название продукта, чтобу узнать его БЖУ.
    - **"Составить диетный план"** — Бот напишет оптимальный диетный план, учитывая твои параметры и цели.
    - **"Составить план тренировок"** — Бот напишет оптимальный план тренировок, Который поможет достичь желаемого результата.

    👩‍💻 **Если у тебя есть вопросы, просто напиши нам! Наши контакты надодятся в меню, также их можно получить по команде `/contacts`**

 

    Наслаждайся использованием нашего бота! 😊
    """
    await message.answer(instruction_text)


llm = GigaChat(
    credentials=GigaChatKey,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False,
    streaming=False,
)

messages = [
    SystemMessage(
        content="Ты профессиональный диетолог с опытом работы в сфере питания и здоровья.Твоя задача — помогать людям составлять сбалансированные диеты, рекомендовать правильное питание для достижения различных целей (например, снижение веса, набор массы, улучшение общего состояния здоровья), а также учитывать индивидуальные потребности каждого клиента, такие как возраст, пол, рост. Ты даешь советы по правильному питанию, учитывая научные данные и практический опыт."
    )
]


async def get_gigachat_response(user_message):

    messages.append(HumanMessage(content=user_message))

    response = llm.invoke(messages)

    messages.append(response)

    return response.content


@router.message(F.text == "Узнать БЖУ")
async def abletowrite(message: Message, state: FSMContext):
    await rq.bju_request(tg_id=message.from_user.id, request=message.text)
    await state.set_state(Write.can)
    await message.reply("Введите продукт, БЖУ которого хотите узнать")


@router.message(Write.can)
async def PFC_message(message: Message, state: FSMContext):
    user_message = (
        message.text
        + "кратко напиши сколько белков, жиров и углеводов у этого продукта"
    )
    response = await get_gigachat_response(user_message)
    await message.reply(response)
    await state.clear()


@router.message(F.text == "Составить диетный план")
async def handle_message(message: Message, state: FSMContext):
    logging.debug("Получена команда: Составить диетный план")
    user_data = await rq.get_user_data(message.from_user.id)
    user_message = f'Пол: {user_data["sex"]}, возраст: {user_data["age"]}, рост: {user_data["height"]}, вес: {user_data["weight"]}, физическая активность: {user_data["ph_condition"]}, хронические заболевания, травмы: {user_data["ch_illnesses"]}, цель: {user_data["goal"]}. Составь для этого человека диетный план на (расписывая несколько дней), который поможет ему достичь желаемого результата, напиши строго меньше 4000 символов'
    response = await get_gigachat_response(user_message)
    await message.reply(response)
    await rq.diet_plan_request(tg_id=message.from_user.id)


@router.message(F.text == "Составить план тренировок")
async def handle_message(message: Message, state: FSMContext):
    logging.debug("Получена команда: Составить план тренировок")
    user_data = await rq.get_user_data(message.from_user.id)
    user_message = f'Пол: {user_data["sex"]}, возраст: {user_data["age"]}, рост: {user_data["height"]}, вес: {user_data["weight"]}, физическая активность: {user_data["ph_condition"]}, хронические заболевания, травмы: {user_data["ch_illnesses"]}, цель: {user_data["goal"]}. Составь для этого человека план тренировок (расписывая несколько дней), который поможет ему достичь желаемого результата, напиши строго меньше 4000 символов'
    print(user_message)
    response = await get_gigachat_response(user_message)
    await message.reply(response)
    await rq.training_plan_request(tg_id=message.from_user.id)


@router.message()
async def without_button(message: Message):
    await message.reply("Нельзя писать произвольный текст)")
    await message.answer("Выберите команду!")
