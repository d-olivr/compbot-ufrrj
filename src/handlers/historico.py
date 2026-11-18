"""Análise via histórico acadêmico (PDF do SIGAA)."""
import os

import pandas as pd

from instancia import bot
from leitura_tabela import extrair_tabelas_sigaa
from kmean import analisar_historico


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
        with open(caminho_local, 'wb' ) as f:
            f.write(downloaded_file)
        
        # Chama a função lá do leitura_tabela.py
        arquivo_csv, arquivo_xlsx = extrair_tabelas_sigaa(caminho_local)

        if arquivo_csv and arquivo_xlsx:
            # Lê o CSV gerado e joga no KMeans
            df_historico = pd.read_csv(arquivo_csv)
            resultado_analise = analisar_historico(df_historico)

            # Envia as respostas para o Telegram
            bot.send_message(message.chat.id, "✅ **Histórico extraído com sucesso!** Aqui estão os seus arquivos:")
            bot.send_message(message.chat.id, resultado_analise, parse_mode="Markdown")
            
            # Envia o Excel
            with open(arquivo_xlsx, 'rb') as doc_xlsx:
                bot.send_document(message.chat.id, doc_xlsx)
                
            # Envia o CSV
            with open(arquivo_csv, 'rb') as doc_csv:
                bot.send_document(message.chat.id, doc_csv)
            
            # Faxina! LIMPA ARQUIVOS DA MÁQUINA
            os.remove(caminho_local)
            os.remove(arquivo_csv)
            os.remove(arquivo_xlsx)
            
        else:
            bot.send_message(message.chat.id, "⚠️ Não consegui encontrar nenhuma tabela reconhecível neste PDF.")
            os.remove(caminho_local)
            
    except Exception as e:
        print(f"ERRO NO PROCESSAMENTO DO PDF: {e}")
        bot.send_message(message.chat.id, "❌ Ocorreu um erro interno ao tentar ler o histórico.")
