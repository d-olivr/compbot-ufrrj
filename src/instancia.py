# objeto bot isolado de tudo com token vindo de .env
import os

import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
