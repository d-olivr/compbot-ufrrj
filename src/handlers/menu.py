"""Menu principal: /start, ajuda, requisitos e calendário acadêmico."""
from datetime import datetime

from telebot import types
import telebot

from instancia import bot

# TODO : adicionar aqui o botão "Extensão" no menu de ajuda
# e lembra de criar o handler em handlers/extensao.py


@bot.message_handler(commands=['start'])
def start(msg: telebot.types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2) 
    btn_ajuda = types.InlineKeyboardButton("🤔 Quero ajuda", callback_data="ajuda")
    btn_github = types.InlineKeyboardButton("💻 Ver no GitHub", url="https://github.com/d-olivr/compbot-ufrrj")
    markup.add(btn_ajuda, btn_github)
    bot.send_message(msg.chat.id, 'Bem vindo ao CompBot UFRRJ! Escolha uma opção:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "ajuda")
def callback_ajuda(call):
    bot.answer_callback_query(call.id)
    markup_ajuda = types.InlineKeyboardMarkup(row_width=1)
    markup_ajuda.add(
        types.InlineKeyboardButton("🔬 Requisitos para puxar uma disciplina", callback_data="requisitos-materia"),
        types.InlineKeyboardButton("📚 Dicas das disciplinas", callback_data="dicas-disciplina"),
        types.InlineKeyboardButton("📅 Calendário Acadêmico", callback_data="calendario-academico"),
        types.InlineKeyboardButton("📄 Análise via Histórico", callback_data="analise-historico")
    )
    bot.edit_message_text('Em que posso te ajudar?', call.message.chat.id, call.message.message_id, reply_markup=markup_ajuda)

# REQUISITOS PARA PUXAR UMA DISCIPLINA
@bot.callback_query_handler(func=lambda call: call.data == "requisitos-materia")
def callback_requisitos_materia(call):
    bot.answer_callback_query(call.id)
    resposta = "Para puxar uma matéria, você precisa ter sido aprovado nos pré-requisitos do SIGAA e haver vagas disponíveis."
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="ajuda"))
    bot.edit_message_text(resposta, call.message.chat.id, call.message.message_id, reply_markup=markup)

# CALENDÁRIO ACADEMICO
@bot.callback_query_handler(func=lambda call: call.data == "calendario-academico")
def callback_calendario_academico(call):
    bot.answer_callback_query(call.id)
    data_fim, dias = calcular_dados_semestre()
    
    texto = (
        "📅 O calendário de matrícula do SIGAA é divulgado periodicamente.\n"
        "Algumas datas importantes de **2026.2** são:\n\n"
        "• Cadastro de Turmas: 13/05 até 06/07\n"
        "• Matrícula OnLine (Pré-Matrícula): 17/07 até 26/07\n"
        "• Ajustes das Matrículas (1ª fase): 27/07\n"
        "• Re-Matrícula (2ª fase): 30/07 até 05/08\n"
        f"• Fim do Semestre: {data_fim}\n"
        f"🤩 Faltam {dias} dias para o fim do semestre!\n\n"
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


def calcular_dados_semestre():
    #A alteração da data do fim do semestre deve ser aplicada manualmente, logo caso tenhamos alguma aleração ela deve ser feita na linha abaixo.
    ano, mes, dia = 2026, 12, 19
    
    data_destino = datetime(ano, mes, dia)
    data_formatada = data_destino.strftime("%d/%m/%Y")
    
    # Cálculo dos dias que faltam
    hoje = datetime.now()
    dias_restantes = (data_destino - hoje).days
    
    return data_formatada, dias_restantes
