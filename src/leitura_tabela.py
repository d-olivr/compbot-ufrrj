import pdfplumber
import pandas as pd
import logging
import re
import os

# Remove warnings chatos do pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)

def extrair_tabelas_sigaa(caminho_pdf):
    todos_dfs = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for num_pagina, pagina in enumerate(pdf.pages):
            # Adiciona um 'or ""' para evitar erro se a página não tiver texto
            texto = pagina.extract_text() or ""
            
            # Procura algo tipo 2024.1 / 2025.2
            semestres = re.findall(r"\d{4}\.\d", texto)
            
            tabelas = pagina.extract_tables()
            for i, tabela in enumerate(tabelas):
                # ignora tabelas vazias
                if not tabela or len(tabela) < 2:
                    continue
                try:
                    df = pd.DataFrame(tabela[1:], columns=tabela[0])
                    # adiciona metadados
                    df["pagina"] = num_pagina + 1

                    if i < len(semestres):
                        df["semestre"] = semestres[i]
                    else:
                        df["semestre"] = "desconhecido"

                    todos_dfs.append(df)
                except Exception as e:
                    print(f"Erro na página {num_pagina+1}, tabela {i+1}: {e}")

    # Se não achou nenhuma tabela, retorna vazio
    if not todos_dfs:
        return None, None

    # Junta tudo
    df_final = pd.concat(todos_dfs, ignore_index=True)

    # Cria nomes de arquivos baseados no nome original pra não dar conflito
    nome_base = caminho_pdf.replace(".pdf", "")
    arquivo_csv = f"{nome_base}_completo.csv"
    arquivo_xlsx = f"{nome_base}_completo.xlsx"

    # Salva CSV e Excel
    df_final.to_csv(arquivo_csv, index=False)
    df_final.to_excel(arquivo_xlsx, index=False)

    # Devolve o caminho dos arquivos gerados para o bot
    return arquivo_csv, arquivo_xlsx