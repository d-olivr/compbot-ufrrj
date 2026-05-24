import os
import telebot
from telebot import types
from dotenv import load_dotenv
from leitura_tabela import extrair_tabelas_sigaa
from datetime import datetime
from kmean import analisar_historico
import pandas as pd

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

# DICAS DAS DISCIPLINAS
@bot.callback_query_handler(func=lambda call: call.data == "dicas-disciplina")
def callback_dicas_disciplina(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text("Navegue pelos períodos para acessar as matérias:", call.message.chat.id, call.message.message_id, reply_markup=menu_periodos())

# ANÁLISE DE HISTÓRICO 
@bot.callback_query_handler(func=lambda call: call.data == "analise-historico")
def callback_analise_historico(call):
    bot.answer_callback_query(call.id)
    
    msg = bot.edit_message_text(
        "📄 **Análise via Histórico**\n\nPor favor, envie o seu arquivo PDF do histórico acadêmico obtido pelo SIGAA.",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown"
    )
    
    bot.register_next_step_handler(msg, processar_upload_historico)


def calcular_dados_semestre():
    #A alteração da data do fim do semestre deve ser aplicada manualmente, logo caso tenhamos alguma aleração ela deve ser feita na linha abaixo.
    ano, mes, dia = 2026, 7, 6
    
    data_destino = datetime(ano, mes, dia)
    data_formatada = data_destino.strftime("%d/%m/%Y")
    
    # Cálculo dos dias que faltam
    hoje = datetime.now()
    dias_restantes = (data_destino - hoje).days
    
    return data_formatada, dias_restantes



def processar_upload_historico(message):
    # VERIFICAÇÃO ARQUIVO
    if message.content_type != 'document' or message.document.mime_type != 'application/pdf':
        bot.reply_to(message, "❌ Isso não parece um arquivo PDF. Operação cancelada.")
        return

    bot.reply_to(message, "📥 Recebi o PDF! Processando as tabelas, isso pode levar alguns segundos...")

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        caminho_local = f"historico_{message.chat.id}.pdf"
        with open(caminho_local, 'wb') as f:
            f.write(downloaded_file)
        
        arquivo_csv, arquivo_xlsx = extrair_tabelas_sigaa(caminho_local)
        
        df_historico = pd.read_csv(arquivo_csv)
        resultado_analise = analisar_historico(df_historico)


        if arquivo_csv and arquivo_xlsx:
            bot.send_message(message.chat.id, "✅ **Histórico extraído com sucesso!** Aqui estão os seus arquivos:")
            bot.send_message(message.chat.id, resultado_analise)
            # EXEL
            with open(arquivo_xlsx, 'rb') as doc_xlsx:
                bot.send_document(message.chat.id, doc_xlsx)
                
            # CSV
            with open(arquivo_csv, 'rb') as doc_csv:
                bot.send_document(message.chat.id, doc_csv)
            
            # Faxina! LIMPA ARQUIVOS DA MAQUINA
            os.remove(caminho_local)
            os.remove(arquivo_csv)
            os.remove(arquivo_xlsx)
            
        else:
            bot.send_message(message.chat.id, "⚠️ Não consegui encontrar nenhuma tabela reconhecível neste PDF.")
            os.remove(caminho_local)
            
    except Exception as e:
        print(f"ERRO NO PROCESSAMENTO DO PDF: {e}")
        bot.send_message(message.chat.id, "❌ Ocorreu um erro interno ao tentar ler o histórico.")

# ------------------ INICIALIZAÇÃO DO BOT -----------------
print("Bot rodando...")
bot.infinity_polling()