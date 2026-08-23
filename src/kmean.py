import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import re

# matérias usadas na análise
FEATURES = ["IM885", "IM853", "TN707", "TN705", "TN706", "TN703"]

def analisar_historico(df_hist):
    # ---------------- BASE DE REFERÊNCIA ----------------
    alunos = pd.read_csv("data/ate-2-periodo.csv")
    alunos = alunos.dropna(subset=FEATURES)

    # df_hist já chega pronto, direto do bot.py — não precisa ler de novo

    # Inicializa o dicionário de matérias do aluno com 0.0
    materias = {feat: 0.0 for feat in FEATURES}

    # Varre as linhas do histórico para extrair as notas
    for _, row in df_hist.iterrows():
        texto_linha = " ".join([str(x) for x in row.values])
        texto_linha = texto_linha.replace(",", ".")
        for codigo in FEATURES:
            if codigo in texto_linha:
                numeros = re.findall(r"\d+\.\d+|\d+", texto_linha)
                notas = []
                for n in numeros:
                    try:
                        val = float(n)
                        if 0 <= val <= 10:
                            notas.append(val)
                    except:
                        pass
                if notas:
                    materias[codigo] = max(notas)

    # Cria o DataFrame no formato esperado pelo KMeans
    historico_csv = pd.DataFrame([materias])
    historico_csv = historico_csv.dropna(subset=FEATURES)

    # ---------------- NORMALIZAÇÃO ----------------
    scaler = MinMaxScaler(feature_range=(1, 10))
    X_alunos = scaler.fit_transform(alunos[FEATURES])
    X_historico = scaler.transform(historico_csv[FEATURES])

    # ---------------- KMEANS ----------------
    kmeans = KMeans(
        n_clusters=3,
        random_state=0,
        n_init=10
    )

    kmeans.fit(X_alunos)
    cluster = kmeans.predict(X_historico)[0]

    # -------------------------------------------
    medias_clusters = kmeans.cluster_centers_.mean(axis=1)

    melhor_cluster = medias_clusters.argmax()
    pior_cluster = medias_clusters.argmin()

    clusters_restantes = [
        i for i in range(len(medias_clusters))
        if i not in [melhor_cluster, pior_cluster]
    ]

    medio_cluster = clusters_restantes[0]

    # ---------------- RESPOSTAS ----------------
    if cluster == melhor_cluster:
        return (
            "📊 **Resultado da análise via KMeans:**\n\n"
            "Você se encaixa no grupo com melhor desempenho acadêmico nas disciplinas iniciais! 🚀"
        )
    elif cluster == pior_cluster:
        return (
            "📊 **Resultado da análise via KMeans:**\n\n"
            "Você se encaixa no grupo com maiores dificuldades nas disciplinas iniciais. 💪"
        )
    else:
        return (
            "📊 **Resultado da análise via KMeans:**\n\n"
            "Você se encaixa no grupo intermediário de desempenho nas disciplinas iniciais. 📈"
        )