from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

#token = "7592817480:AAES9h4YMXb-Qg7H6PfoDNeS8NenC6l1WJ4"
token = "7756409743:AAHekJP4DtANj1BKneWJshBU7Cj7I2sqti8"
GigaChatKey = 'MTljZDYyMTUtYmZlYy00Y2NlLWI3NzItNTA2ODA0ZGM0ZTNmOmQ2OWE3MTVhLWU5YjQtNDAwMS05MWM0LTA4MTc5ODBjZTkyMg=='


bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))