import fitz  # PyMuPDF

def extrair_texto_pdf(caminho_arquivo):
    
    # essa funçao apenas abre o PDF e extrai o texto.
    texto_completo = ""
    try:
        doc = fitz.open(caminho_arquivo)
        for pagina in doc:
            texto_completo += pagina.get_text()
        doc.close()
        return texto_completo
    except Exception as e:
        print(f"Erro ao processar PDF: {e}")
        return None