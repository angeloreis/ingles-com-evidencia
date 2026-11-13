import csv
import io

import pytest

from scripts.validar import Erro, validar_arquivo, validar_pasta

CAB = ["id", "en", "pt", "silaba", "situacao", "fonte", "licenca", "autor"]
BASE = {"id": "reuniao-01", "en": "Can we schedule a call for Monday?",
        "pt": "Podemos marcar uma ligação para segunda?", "silaba": "SCHED·ule",
        "situacao": "6", "fonte": "projeto", "licenca": "CC BY-SA 4.0", "autor": ""}


def montar(*linhas, cab=CAB):
    s = io.StringIO()
    w = csv.writer(s, lineterminator="\n")
    w.writerow(cab)
    for linha in linhas:
        w.writerow([linha.get(c, "") for c in cab])
    return s.getvalue()


def gravar(tmp_path, texto, nome="teste.csv", codificacao="utf-8"):
    p = tmp_path / nome
    p.write_bytes(texto.encode(codificacao))
    return p


def erros(tmp_path, texto, **kw):
    return validar_arquivo(gravar(tmp_path, texto, **kw), {}).erros


def test_erro_formata_arquivo_linha_mensagem():
    assert str(Erro("kit/dados/a.csv", 3, "falta en")) == "kit/dados/a.csv:3: falta en"


def test_arquivo_valido(tmp_path):
    ids = {}
    r = validar_arquivo(gravar(tmp_path, montar(BASE)), ids)
    assert (r.arquivos, r.linhas, r.erros) == (1, 1, [])
    assert ids["reuniao-01"] == (str(tmp_path / "teste.csv"), 2)


@pytest.mark.parametrize("texto", [
    "﻿" + montar(BASE).replace("\n", "\r\n") + "\r\n\r\n",
    montar(BASE) + ",,,,,,,\n,  ,,,,,,\n",
    montar({**BASE, "fonte": "tatoeba:123", "licenca": "CC BY 2.0 FR", "autor": "CK"}),
    montar({**BASE, "fonte": "tatoeba:123", "licenca": "CC0"}),
    montar({"id": "ngsl-0001", "en": "time", "pt": "tempo", "faixa": "1",
            "fonte": "ngsl", "licenca": "CC BY-SA 4.0"},
           cab=["id", "en", "pt", "faixa", "fonte", "licenca"]),
])
def test_casos_validos(tmp_path, texto):
    assert erros(tmp_path, texto) == []


@pytest.mark.parametrize("texto, trecho", [
    (montar({**BASE, "en": "   "}), "en"),
    (montar({**BASE, "id": "Reuniao 01"}), "id"),
    (montar({**BASE, "situacao": "9"}), "situacao"),
    (montar({**BASE, "situacao": "seis"}), "situacao"),
    (montar({**BASE, "fonte": "tatoeba:"}), "fonte"),
    (montar({**BASE, "fonte": "wikipedia"}), "fonte"),
    (montar({**BASE, "licenca": "CC BY-NC 4.0"}), "não permitida"),
    (montar({**BASE, "fonte": "ngsl", "licenca": "CC0"}), "ngsl"),
    (montar({**BASE, "fonte": "tatoeba:123", "licenca": "CC BY 2.0 FR"}), "autor"),
    (montar({**BASE, "silaba": "va·CA·tion"}), "silaba"),
    (montar({**BASE, "silaba": "schedule"}), "·"),
    (",".join(CAB) + "\nreuniao-02,Hi, how are you?,Oi, tudo bem?,,6,projeto,CC BY-SA 4.0,\n", "aspas"),
    (",".join(CAB) + "\nreuniao-02,Hi\n", "menos colunas"),
    (",".join(CAB) + "\nreuniao-02,Hi\n", "campo vazio também"),
    # vírgula sem aspas e, ao mesmo tempo, sem a vírgula final do autor vazio:
    # a contagem bate, mas os valores caem nas colunas erradas
    (",".join(CAB) + "\nreuniao-02,Hi, how are you?,Oi tudo bem?,,6,projeto,CC BY-SA 4.0\n", "deslocadas"),
    (",".join(CAB[:-1]) + "\nreuniao-02,Hello,Olá,,6,projeto,CC BY-SA 4.0,\n", "sobrando"),
    (",".join(CAB) + '\nreuniao-02,"Hi there,Oi,,6,projeto,CC BY-SA 4.0,\n'
     "reuniao-03,Hello,Olá,,6,projeto,CC BY-SA 4.0,\n", "sem fechar"),
])
def test_um_erro_na_linha_2(tmp_path, texto, trecho):
    e = erros(tmp_path, texto)
    assert len(e) == 1 and e[0].linha == 2 and trecho in e[0].mensagem


@pytest.mark.parametrize("texto, trecho", [
    ("id;en;pt;situacao;fonte;licenca\n", "vírgula"),
    # o Excel em português grava ; mesmo em "CSV (delimitado por vírgulas)"
    ("id;en;pt;situacao;fonte;licenca\n", "Google Planilhas"),
    (montar(BASE, cab=["id", "en", "pt", "situacao", "fonte"]), "licenca"),
    (montar(BASE, cab=[c.replace("licenca", "licença") for c in CAB]), "licença"),
    (montar(BASE, cab=CAB + ["faixa"]), "situacao ou faixa"),
    (montar(BASE, cab=[c for c in CAB if c != "situacao"]), "situacao ou faixa"),
])
def test_erro_no_cabecalho(tmp_path, texto, trecho):
    e = erros(tmp_path, texto)
    assert e and all(x.linha == 1 for x in e) and any(trecho in x.mensagem for x in e)


@pytest.mark.parametrize("texto, codificacao, trecho", [
    (montar(BASE), "latin-1", "UTF-8"),
    ("", "utf-8", "vazio"),
])
def test_erro_no_arquivo_inteiro(tmp_path, texto, codificacao, trecho):
    e = erros(tmp_path, texto, codificacao=codificacao)
    assert len(e) == 1 and e[0].linha == 0 and trecho in e[0].mensagem


def test_aspa_sem_fechar_em_arquivo_grande(tmp_path):
    # o csv engole o resto do arquivo e estoura o limite de tamanho do campo
    linhas = [",".join(CAB), 'reuniao-0000,"Hi there,Oi,,6,projeto,CC BY-SA 4.0,']
    linhas += [f"reuniao-{n:04d},Hello there my friend,Olá meu amigo,,6,projeto,CC BY-SA 4.0,"
               for n in range(1, 3001)]
    e = erros(tmp_path, "\n".join(linhas) + "\n")
    assert len(e) == 1 and e[0].linha == 2 and "sem fechar" in e[0].mensagem


def test_id_repetido_entre_arquivos(tmp_path):
    gravar(tmp_path, montar(BASE), "a.csv")
    gravar(tmp_path, montar(BASE), "b.csv")
    r = validar_pasta(tmp_path)
    assert r.arquivos == 2 and len(r.erros) == 1
    assert r.erros[0].arquivo.endswith("b.csv") and r.erros[0].linha == 2
    assert "a.csv:2" in r.erros[0].mensagem


def test_pasta_conta_linhas(tmp_path):
    gravar(tmp_path, montar(BASE, {**BASE, "id": "reuniao-02"}))
    r = validar_pasta(tmp_path)
    assert (r.arquivos, r.linhas, r.erros) == (1, 2, [])


def test_pasta_sem_csv(tmp_path):
    r = validar_pasta(tmp_path)
    assert len(r.erros) == 1 and r.erros[0].linha == 0 and "nenhum CSV" in r.erros[0].mensagem


# --- Fase 1A, Tarefa 1: diálogos e ajustes do cabeçalho -------------------

from scripts.validar import DIALOGO  # noqa: E402

CAB_DIALOGO = ["id", "situacao", "ordem", "falante", "en", "pt", "fonte", "licenca", "autor"]
FALA = {"id": "telefonar-d01", "situacao": "6", "ordem": "1", "falante": "A",
        "en": "Hi, it's Ana from the data team.", "pt": "Oi, é a Ana do time de dados.",
        "fonte": "projeto", "licenca": "CC BY-SA 4.0", "autor": ""}


def erros_dialogo(tmp_path, texto):
    return validar_arquivo(gravar(tmp_path, texto), {}, DIALOGO).erros


def test_dialogo_valido(tmp_path):
    texto = montar(FALA, {**FALA, "id": "telefonar-d02", "ordem": "2", "falante": "B"}, cab=CAB_DIALOGO)
    assert erros_dialogo(tmp_path, texto) == []


@pytest.mark.parametrize("linhas, trecho", [
    ([{**FALA, "falante": "C"}], "falante"),
    ([FALA, {**FALA, "id": "telefonar-d02"}], "ordem"),
    ([{**FALA, "ordem": "0"}], "ordem"),
])
def test_dialogo_erros(tmp_path, linhas, trecho):
    e = erros_dialogo(tmp_path, montar(*linhas, cab=CAB_DIALOGO))
    assert len(e) == 1 and trecho in e[0].mensagem


def test_id_repetido_entre_baralho_e_dialogo(tmp_path):
    (tmp_path / "dados").mkdir()
    (tmp_path / "dialogos").mkdir()
    gravar(tmp_path / "dados", montar(BASE), "a.csv")
    gravar(tmp_path / "dialogos", montar({**FALA, "id": "reuniao-01"}, cab=CAB_DIALOGO), "b.csv")
    ids = {}
    assert validar_pasta(tmp_path / "dados", ids_vistos=ids).erros == []
    e = validar_pasta(tmp_path / "dialogos", DIALOGO, ids_vistos=ids).erros
    assert len(e) == 1 and "id repetido" in e[0].mensagem


@pytest.mark.parametrize("cab, trecho", [
    (CAB + [""], "sem nome"),
    (CAB + ["en"], "repetida"),
])
def test_cabecalho_coluna_sem_nome_e_repetida(tmp_path, cab, trecho):
    e = erros(tmp_path, montar(BASE, cab=cab))
    assert e and all(x.linha == 1 for x in e) and any(trecho in x.mensagem for x in e)


def test_digito_de_outro_alfabeto_nao_vale(tmp_path):
    e = erros(tmp_path, montar({**BASE, "situacao": "６"}))
    assert len(e) == 1 and "situacao" in e[0].mensagem


# --- Fase 1B, Tarefa 1: texto de leitura para a voz ----------------------

def test_leitura_e_coluna_opcional(tmp_path):
    cab = CAB + ["leitura"]
    baralho = montar({**BASE, "leitura": "Can we schedule a call for Monday?"},
                     {**BASE, "id": "reuniao-02"}, cab=cab)
    assert erros(tmp_path, baralho) == []
    dialogo = montar({**FALA, "leitura": "Hi, it's Ana."},
                     {**FALA, "id": "telefonar-d02", "ordem": "2", "falante": "B"}, cab=CAB_DIALOGO + ["leitura"])
    assert erros_dialogo(tmp_path, dialogo) == []
