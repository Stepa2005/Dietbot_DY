from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

token = "8102143668:AAEjPGyP1TvNTPdBj_mXuDtuigbrnAdX4Vc"
GigaChatKey = 'MTljZDYyMTUtYmZlYy00Y2NlLWI3NzItNTA2ODA0ZGM0ZTNmOmQ2OWE3MTVhLWU5YjQtNDAwMS05MWM0LTA4MTc5ODBjZTkyMg=='


bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))