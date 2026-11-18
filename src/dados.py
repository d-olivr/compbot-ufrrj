"""carrega o catálogo/modulos de disciplinas e as matrizes curriculares.

data/disciplinas.json     catálogo único: o que a disciplina É (nome, descrição,
                          professor, playlist, carga horária, quando costuma ser oferecida)
data/matrizes/*.json      cada matriz só diz ONDE a disciplina entra: período e
                          pré-requisitos (que podem mudar de uma matriz pra outra)

explicando como funciona:
handlers nao leem os jsons direto, eles usam as funções daqui, que devolvem
a disciplina já "juntada" (catálogo + dados da matriz). 

qualquer campo do catálogo pode ser sobrescrito dentro da matriz, se for diferente naquela matriz
(ex.: se carga_horaria não é a mesma na matriz de 2020 e de 2023, é só sobrescrever no respectivo json).

se algum json estiver com erro, bot nem sobe. assim dá pra ver qual é o problema
"""
import json
from pathlib import Path

PASTA_DADOS = Path(__file__).resolve().parent.parent / "data"
PASTA_MATRIZES = PASTA_DADOS / "matrizes"


def _ler_json(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def _carregar_catalogo():
    lista = _ler_json(PASTA_DADOS / "disciplinas.json")["disciplinas"]
    ids = [d["id"] for d in lista]
    repetidos = {i for i in ids if ids.count(i) > 1}
    if repetidos:
        raise ValueError(f"[disciplinas.json] ids repetidos: {repetidos}")
    return {d["id"]: d for d in lista}


def _carregar_matrizes():
    matrizes = {}
    for caminho in sorted(PASTA_MATRIZES.glob("*.json")):
        matriz = _ler_json(caminho)
        matrizes[matriz["id"]] = matriz
    if not matrizes:
        raise FileNotFoundError(f"nenhuma matriz encontrada em {PASTA_MATRIZES}")
    return matrizes


def _validar(catalogo, matrizes):
    for mid, matriz in matrizes.items():
        ids = [d["id"] for d in matriz["disciplinas"]]
        repetidos = {i for i in ids if ids.count(i) > 1}
        if repetidos:
            raise ValueError(f"[{mid}] ids repetidos: {repetidos}")
        for entrada in matriz["disciplinas"]:
            if entrada["id"] not in catalogo:
                raise ValueError(f"[{mid}] '{entrada['id']}' não existe em disciplinas.json")
            for pre in entrada.get("pre_requisitos", []):
                if pre not in ids:
                    raise ValueError(f"[{mid}] '{entrada['id']}' tem pré-requisito que não está na matriz: '{pre}'")


CATALOGO = _carregar_catalogo()
MATRIZES = _carregar_matrizes()
_validar(CATALOGO, MATRIZES)


# ---------------- CONSULTAS ----------------

def _juntar(entrada):
    """Catálogo + dados da matriz (a matriz tem prioridade)."""
    return {**CATALOGO[entrada["id"]], **entrada}


def listar_matrizes():
    """[(id, nome), ...]"""
    return [(m["id"], m["nome"]) for m in MATRIZES.values()]


def total_periodos(matriz_id):
    return MATRIZES[matriz_id].get("total_periodos", 8)


def disciplinas_da_matriz(matriz_id):
    return [_juntar(e) for e in MATRIZES[matriz_id]["disciplinas"]]


def disciplinas_do_periodo(matriz_id, periodo):
    return [d for d in disciplinas_da_matriz(matriz_id) if d["periodo"] == periodo]


def get_disciplina(matriz_id, disc_id):
    """None se a disciplina não faz parte dessa matriz."""
    for entrada in MATRIZES[matriz_id]["disciplinas"]:
        if entrada["id"] == disc_id:
            return _juntar(entrada)
    return None


def pre_requisitos(matriz_id, disc_id):
    """disciplinas que precisam ser cursadas antes, nessa matriz"""
    disc = get_disciplina(matriz_id, disc_id)
    return [get_disciplina(matriz_id, p) for p in disc.get("pre_requisitos", [])]


def dependentes(matriz_id, disc_id):
    """disciplinas que têm essa materia como pré-requisito, nessa matriz"""
    return [d for d in disciplinas_da_matriz(matriz_id)
            if disc_id in d.get("pre_requisitos", [])]
