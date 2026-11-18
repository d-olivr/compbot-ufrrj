"""navegação: matriz -> período -> disciplina.

callback_data usado aqui (separador "|", limite do Telegram é 64 bytes):
    dicas-disciplina      entrada (pula a escolha de matriz se só existir uma)
    mz|<matriz>           lista de períodos da matriz
    pd|<matriz>|<n>       disciplinas do período n
    mt|<matriz>|<id>      tela da disciplina
"""
from telebot import types

from instancia import bot
import dados


# ----------------- MENUS -----------------

def menu_matrizes():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for matriz_id, nome in dados.listar_matrizes():
        markup.add(types.InlineKeyboardButton(nome, callback_data=f"mz|{matriz_id}"))
    markup.add(types.InlineKeyboardButton("⬅️ Voltar ao Menu Principal", callback_data="ajuda"))
    return markup


def menu_periodos(matriz_id):
    markup = types.InlineKeyboardMarkup(row_width=4)
    botoes = [
        types.InlineKeyboardButton(f"{i}º Período", callback_data=f"pd|{matriz_id}|{i}")
        for i in range(1, dados.total_periodos(matriz_id) + 1)
    ]
    markup.add(*botoes)
    if len(dados.listar_matrizes()) == 1:
        markup.add(types.InlineKeyboardButton("⬅️ Voltar ao Menu Principal", callback_data="ajuda"))
    else:
        markup.add(types.InlineKeyboardButton("⬅️ Voltar às Matrizes", callback_data="dicas-disciplina"))
    return markup


def menu_materias(matriz_id, periodo):
    markup = types.InlineKeyboardMarkup(row_width=2)
    botoes = [
        types.InlineKeyboardButton(d["nome"], callback_data=f"mt|{matriz_id}|{d['id']}")
        for d in dados.disciplinas_do_periodo(matriz_id, periodo)
    ]
    if botoes:
        markup.add(*botoes)
    markup.add(types.InlineKeyboardButton("⬅️ Voltar aos Períodos", callback_data=f"mz|{matriz_id}"))
    return markup


"""----------------- TELA GENÉRICA DA DISCIPLINA -----------------
essa "interface" é a base pra tela de todas as disciplinas. ela é montada a partir do catálogo + dados da matriz.
caso a disciplina não exista na matriz, o usuário é informado e pode voltar ao menu de ajuda.
para alterar o conteúdo de uma disciplina, basta editar o arquivo `data/disciplinas.json`. 
não altere o arquivo da matriz, pois ele é apenas um "mapa" de ids de disciplinas.
"""

def montar_texto(matriz_id, disc):
    linhas = [f"{disc.get('emoji', '📘')} **{disc['nome']}**", ""]

    if disc.get("descricao"):
        linhas += [disc["descricao"], ""]
    else:
        linhas += ["O conteúdo desta disciplina ainda está sendo configurado! ⏳", ""]

    if disc.get("professor"):
        linhas.append(f"**Professor(a):** {disc['professor']}")
    if disc.get("contato"):
        linhas.append(f"**Contato:** {disc['contato']}")

    # TODO : mostrar carga_horaria, oferta, e usar dados.pre_requisitos(...) e dados.dependentes(...) e tal

    return "\n".join(linhas)


def montar_botoes(matriz_id, disc):
    markup = types.InlineKeyboardMarkup()
    if disc.get("playlist"):
        markup.add(types.InlineKeyboardButton("📺 Playlist Recomendada", url=disc["playlist"]))
    markup.add(types.InlineKeyboardButton("⬅️ Voltar", callback_data=f"pd|{matriz_id}|{disc['periodo']}"))
    return markup


# ----------------- HANDLERS -----------------

def _mostrar_periodos(call, matriz_id):
    bot.edit_message_text(
        "Navegue pelos períodos para acessar as matérias:",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_periodos(matriz_id),
    )


@bot.callback_query_handler(func=lambda call: call.data == "dicas-disciplina")
def callback_dicas_disciplina(call):
    bot.answer_callback_query(call.id)
    matrizes = dados.listar_matrizes()
    if len(matrizes) == 1:
        _mostrar_periodos(call, matrizes[0][0])
    else:
        bot.edit_message_text(
            "Escolha a matriz curricular:",
            call.message.chat.id, call.message.message_id,
            reply_markup=menu_matrizes(),
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("mz|"))
def callback_selecao_matriz(call):
    bot.answer_callback_query(call.id)
    matriz_id = call.data.split("|")[1]
    _mostrar_periodos(call, matriz_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("pd|"))
def callback_selecao_periodo(call):
    bot.answer_callback_query(call.id)
    _, matriz_id, periodo = call.data.split("|")
    periodo = int(periodo)
    bot.edit_message_text(
        f"Você selecionou o {periodo}º período. Escolha uma matéria:",
        call.message.chat.id, call.message.message_id,
        reply_markup=menu_materias(matriz_id, periodo),
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("mt|"))
def callback_detalhe_materia(call):
    bot.answer_callback_query(call.id)
    _, matriz_id, disc_id = call.data.split("|")
    disc = dados.get_disciplina(matriz_id, disc_id)

    if disc is None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Voltar", callback_data="dicas-disciplina"))
        bot.edit_message_text("Não encontrei essa disciplina 😕", call.message.chat.id,
                              call.message.message_id, reply_markup=markup)
        return

    bot.edit_message_text(
        montar_texto(matriz_id, disc),
        call.message.chat.id, call.message.message_id,
        reply_markup=montar_botoes(matriz_id, disc),
        parse_mode="Markdown",
    )
