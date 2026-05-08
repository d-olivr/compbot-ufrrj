import os
import telebot
from telebot import types  # botões
from dotenv import load_dotenv

# carrega as configurações do arquivo .env
load_dotenv()

# pega a variável do .env 
TOKEN_DO_BOT = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN_DO_BOT)


# ------ START ------
@bot.message_handler(commands=['start'])
def start(msg: telebot.types.Message):
    # criação do teclado de opcoes (chamei de markup porque ví que é convenção)
    markup = types.InlineKeyboardMarkup(row_width=5) 

    # botao de ajuda
    btn_ajuda = types.InlineKeyboardButton("🤔 Quero ajuda", callback_data="ajuda")
    
    # botao github
    btn_github = types.InlineKeyboardButton("Ver no GitHub", url="https://github.com/d-olivr/compbot-ufrrj")

    # botao sigaa
    btn_grade = types.InlineKeyboardButton(" SIGAA", url="https://sigaa.ufrrj.br/sigaa/verTelaLogin.do")
    
    # adiciona botões ao teclado
    markup.add(btn_ajuda, btn_grade, btn_github)

    # envia a mensagem com o teclado acoplado
    bot.send_message(msg.chat.id, 'Bem vindo ao CompBot! Escolha uma opção:', reply_markup=markup)

# ---- CLIQUE NO BOTÃO "AJUDA" ----
@bot.callback_query_handler(func=lambda call: call.data == "ajuda")
def callback_ajuda(call):
    
    markup_ajuda = types.InlineKeyboardMarkup(row_width=5) # teclado para opções de ajuda

    btn_requisitos_materia = types.InlineKeyboardButton("Requisitos para puxar matéria", callback_data="requisitos-materia")
    btn_calendario_matricula = types.InlineKeyboardButton("Calendário de matrícula", callback_data="calendario-matricula")

    markup_ajuda.add(btn_requisitos_materia, btn_calendario_matricula)

    bot.send_message(call.message.chat.id, 'Em que posso te ajudar?', reply_markup=markup_ajuda)


print("Bot rodando...")
bot.polling()