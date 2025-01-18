from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TELEGRAM_API_TOKEN = "8089225129:AAFBcRLeAXEZZJvu_f9Z9f9DsJSGYJThsvM"
GigaChatKey = "M2Y1Mjk0NGMtNGNiMC00NjllLTgwMDYtYmNiMzNlOGI5MWJjOjllY2Q0MzIyLTJlNjItNGRjNC1iNGExLTA4ZWNhMDEzOGYyMQ=="

bot = Bot(
    token=TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
