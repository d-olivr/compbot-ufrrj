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
            texto = pagina.extract_text() or ""
            semestres = re.findall(r"\d{4}\.\d", texto)
            
            tabelas = pagina.extract_tables()
            for i, tabela in enumerate(tabelas):
                if not tabela or len(tabela) < 2:
                    continue
                try:
                    cabecalho = tabela[0]
                    contagem = {}
                    colunas = []
                    for c in cabecalho:
                        nome = c if c else "col_vazia"
                        contagem[nome] = contagem.get(nome, -1) + 1
                        colunas.append(f"{nome}_{contagem[nome]}" if contagem[nome] > 0 else nome)

                    df = pd.DataFrame(tabela[1:], columns=colunas)
                    df["pagina"] = num_pagina + 1

                    if i < len(semestres):
                        df["semestre"] = semestres[i]
                    else:
                        df["semestre"] = "desconhecido"

                    todos_dfs.append(df)
                except Exception as e:
                    print(f"Erro na página {num_pagina+1}, tabela {i+1}: {e}")

    if not todos_dfs:
        return None, None

    df_final = pd.concat(todos_dfs, ignore_index=True)

    nome_base = caminho_pdf.replace(".pdf", "")
    arquivo_csv = f"{nome_base}_completo.csv"
    arquivo_xlsx = f"{nome_base}_completo.xlsx"

    df_final.to_csv(arquivo_csv, index=False)
    df_final.to_excel(arquivo_xlsx, index=False)

    return arquivo_csv, arquivo_xlsx