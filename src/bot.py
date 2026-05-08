import telebot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(['/start'])
def start(msg:telebot.types.Message):
  bot.reply_to(msg, 'Hello, World!!!')


@bot.message_handler(['trancar'])
def trancar(msg:telebot.types.Message):
  bot.reply_to(msg, 'hoje!')