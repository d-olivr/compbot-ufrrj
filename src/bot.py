"""pra rodar o bot, rode da raiz do repositório: python src/bot.py"""
from instancia import bot

# importa módulos
from handlers import menu, disciplinas, historico 

print("Bot rodando...")
bot.infinity_polling()
