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

@bot.callback_query_handler(func=lambda call: call.data == "requisitos-materia")
def callback_requisitos_materia(call):
    resposta = "Para puxar uma matéria, você precisa ter cursado e sido aprovado em todas as matérias pré-requisitos listadas no SIGAA. Além disso, é necessário que haja vagas disponíveis na turma que deseja se matricular."
    bot.send_message(call.message.chat.id, resposta)

@bot.callback_query_handler(func=lambda call: call.data == "calendario-matricula")
def callback_calendario_matricula(call):

    resposta = (
        "📅 O calendário de matrícula do SIGAA é divulgado periodicamente."
        "Algumas datas importantes de *2026.2* são:\n\n"
        "• Cadastro de Turmas: 13/05 até 06/07\n"
        "• Matrícula OnLine (Pré-Matrícula): 17/07 até 26/07\n"
        "• Ajustes das Matrículas (1ª fase): 27/07\n"
        "• Re-Matrícula (2ª fase): 30/07 até 05/08\n\n"
        "➡️ Confira o calendário completo abaixo:"
    )
    
    # envia a mensagem de texto separada
    bot.send_message(call.message.chat.id, resposta)
    
    # envia o PDF logo em seguida
    caminho_pdf = "data/calendario-matriculas-2026-2.pdf" 
    
    try: # vai tentar abrir o arquivo PDF, se não encontrar, envia uma mensagem de erro para o usuario
        with open(caminho_pdf, 'rb') as pdf: # 'rb' = read binary 
            bot.send_document(
                call.message.chat.id, # envia o pdf para o mesmo chat onde o usuario clicou no botao
                pdf, # o arquivo pdf em si
                caption="Calendário Acadêmico 2026.2 - UFRRJ"
            )
    except FileNotFoundError:# exceção caso o pdf nao seja encontrado no caminho especificado
        bot.send_message(call.message.chat.id, "Erro: Desculpe, arquivo .pdf não disponível.")



print("Bot rodando...")
bot.infinity_polling() 