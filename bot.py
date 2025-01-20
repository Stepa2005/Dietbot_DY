from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TELEGRAM_API_TOKEN = "8089225129:AAFBcRLeAXEZZJvu_f9Z9f9DsJSGYJThsvM"
GigaChatKey = "MTljZDYyMTUtYmZlYy00Y2NlLWI3NzItNTA2ODA0ZGM0ZTNmOmQ2OWE3MTVhLWU5YjQtNDAwMS05MWM0LTA4MTc5ODBjZTkyMg=="

bot = Bot(
    token=TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
