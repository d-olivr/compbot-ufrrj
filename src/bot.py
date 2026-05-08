import os
import telebot
from telebot import types
from dotenv import load_dotenv

# carrega token do .env
load_dotenv()

#passa o token para a variavel do bot
TOKEN_DO_BOT = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN_DO_BOT)

# ----------------- DADOS ------------------
MATERIAS_POR_PERIODO = {
    "1": ["Circuitos Digitais", 
          "Computadores e Sociedade", 
          "Geometria Analítica", 
          "ICC", "Matemática Discreta", 
          "Programação Estruturada"],
    "2": ["Álgebra Linear", 
          "Cálculo I", 
          "Estruturas de Dados I", 
          "Arquitetura de Computadores", 
          "Lógica"],
}

# ------------------ FUNÇÕES AUXILIARES -----------------

def menu_periodos():
    markup = types.InlineKeyboardMarkup(row_width=4) 
    botoes = [types.InlineKeyboardButton(f"{i}º Período", callback_data=f"periodo-{i}") for i in range(1, 9)]
    markup.add(*botoes)
    markup.add(types.InlineKeyboardButton("⬅️ Voltar ao Menu Principal", callback_data="ajuda"))
    return markup

def menu_materias(periodo_num):
    markup = types.InlineKeyboardMarkup(row_width=2)
    lista_materias = MATERIAS_POR_PERIODO.get(periodo_num, [])
    botoes = [types.InlineKeyboardButton(materia, callback_data=f"materia-{materia}") for materia in lista_materias]
    markup.add(*botoes)
    markup.add(types.InlineKeyboardButton("⬅️ Voltar aos Períodos", callback_data="dicas-disciplina"))
    return markup

# ------------------ CONTEÚDO DAS MATÉRIAS -----------------

def detalhe_ga(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="periodo-1"))
    
    texto = (
        "📐 **Geometria Analítica**\n\n"
        "Nesta disciplina você estudará vetores, retas, planos e cônicas. "
        "É essencial para entender Álgebra Linear e Computação Gráfica.\n\n"
        "**Professora:** Vânia Machado\n"
        "**Contato:** machadovc@gmail.com"
    )
    
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

def detalhe_circuitos(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📺 Playlist Recomendada", url="https://www.youtube.com/playlist?list=PLN-6t07cgV6mvR_VUjQCUzOHGmdHPE_Uz"))
    markup.add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="periodo-1"))
    
    texto = (
        "🔌 **Circuitos Digitais**\n\n"
        "Aqui você aprenderá sobre portas lógicas, flip-flops e circuitos lógicos. "
        "Essa matéria é fundamental para entender Arquitetura de Computadores e Sistemas Operacionais.\n\n"
        "**Professor:** Marcel Silva\n"
        "**Contato:** marcelsilva@ufrrj.br"
    )

    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")


# ----------------- MAPA DE MATERIAS -----------------
MAPA_MATERIAS = {
    "Geometria Analítica": detalhe_ga,
    "Circuitos Digitais": detalhe_circuitos,
}

# ----------------- HANDLERS DE NAVEGAÇÃO -----------------

@bot.callback_query_handler(func=lambda call: call.data.startswith("periodo-"))
def callback_selecao_periodo(call):
    bot.answer_callback_query(call.id)
    periodo_selecionado = call.data.split("-")[1]
    texto = f"Você selecionou o {periodo_selecionado}º período. Escolha uma matéria:"
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=menu_materias(periodo_selecionado))

@bot.callback_query_handler(func=lambda call: call.data.startswith("materia-"))
def callback_detalhe_materia(call):
    bot.answer_callback_query(call.id)
    materia_nome = call.data.split("-")[1]
    funcao_conteudo = MAPA_MATERIAS.get(materia_nome)
    
    if funcao_conteudo:
        funcao_conteudo(call)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="dicas-disciplina"))
        bot.edit_message_text(f"O conteúdo de **{materia_nome}** está sendo configurado! ⏳", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# ----------------- MENUS PRINCIPAIS ----------------------

@bot.message_handler(commands=['start'])
def start(msg: telebot.types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2) 
    btn_ajuda = types.InlineKeyboardButton("🤔 Quero ajuda", callback_data="ajuda")
    btn_github = types.InlineKeyboardButton("💻 Ver no GitHub", url="https://github.com/d-olivr/compbot-ufrrj")
    markup.add(btn_ajuda, btn_github)
    bot.send_message(msg.chat.id, 'Bem vindo ao CompBot! Escolha uma opção:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "ajuda")
def callback_ajuda(call):
    bot.answer_callback_query(call.id)
    markup_ajuda = types.InlineKeyboardMarkup(row_width=1)
    markup_ajuda.add(
        types.InlineKeyboardButton("🔬 Requisitos para puxar uma disciplina", callback_data="requisitos-materia"),
        types.InlineKeyboardButton("📚 Dicas das disciplinas", callback_data="dicas-disciplina"),
        types.InlineKeyboardButton("📅 Calendário de matrícula", callback_data="calendario-matricula")
    )
    bot.edit_message_text('Em que posso te ajudar?', call.message.chat.id, call.message.message_id, reply_markup=markup_ajuda)

@bot.callback_query_handler(func=lambda call: call.data == "requisitos-materia")
def callback_requisitos_materia(call):
    bot.answer_callback_query(call.id)
    resposta = "Para puxar uma matéria, você precisa ter sido aprovado nos pré-requisitos do SIGAA e haver vagas disponíveis."
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="ajuda"))
    bot.edit_message_text(resposta, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "calendario-matricula")
def callback_calendario_matricula(call):
    bot.answer_callback_query(call.id)
    
    texto = (
        "📅 O calendário de matrícula do SIGAA é divulgado periodicamente.\n"
        "Algumas datas importantes de **2026.2** são:\n\n"
        "• Cadastro de Turmas: 13/05 até 06/07\n"
        "• Matrícula OnLine (Pré-Matrícula): 17/07 até 26/07\n"
        "• Ajustes das Matrículas (1ª fase): 27/07\n"
        "• Re-Matrícula (2ª fase): 30/07 até 05/08\n\n"
        "➡️ Confira o calendário completo abaixo:"
    )
    
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="ajuda"))
    
    bot.edit_message_text(texto, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
 
    caminho_pdf = "data/calendario-matriculas-2026-2.pdf" 
    try:
        with open(caminho_pdf, 'rb') as pdf:
            bot.send_document(call.message.chat.id, pdf, caption="Calendário Acadêmico 2026.2")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "⚠️ PDF não disponível no momento.")

@bot.callback_query_handler(func=lambda call: call.data == "dicas-disciplina")
def callback_dicas_disciplina(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text("Navegue pelos períodos para acessar as matérias:", call.message.chat.id, call.message.message_id, reply_markup=menu_periodos())



print("Bot rodando...")
bot.infinity_polling()