from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
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
from config import TELEGRAM_API_TOKEN
from app.handlers import router
from database.models import async_main


logging.basicConfig(
    force=True,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

dp = Dispatcher(storage=MemoryStorage())


async def start_bot():
    commands = [
        BotCommand(command="instruction", description="Руководство пользователя"),
        BotCommand(command="start", description="Перезайти"),
        BotCommand(command="contacts", description="Контакты разработчиков"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    await async_main()
    dp.include_router(router)
    dp.startup.register(start_bot)
    try:
        print("Бот запущен...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        print("Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())
