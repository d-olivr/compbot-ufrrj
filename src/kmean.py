import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# matérias usadas na análise
FEATURES = ["IM885", "IM853", "TN707", "TN705", "TN706", "TN703"]


def analisar_historico(historico_csv):

    # ---------------- BASE DE REFERÊNCIA ----------------

    alunos = pd.read_csv("data/ate-2-periodo.csv")

    # remove linhas incompletas
    alunos = alunos.dropna(subset=FEATURES)
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
            "📊 Resultado da análise:\n\n"
            "Você se encaixa no grupo com melhor desempenho acadêmico."
        )

    elif cluster == pior_cluster:
        return (
            "📊 Resultado da análise:\n\n"
            "Você se encaixa no grupo com maiores dificuldades nas disciplinas iniciais."
        )

    else:
        return (
            "📊 Resultado da análise:\n\n"
            "Você se encaixa no grupo intermediário de desempenho."
        )