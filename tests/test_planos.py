import json
import re

import pytest

from scripts import RAIZ
from scripts.planos import dados_do_plano, validar_plano

CAB = "semana,dia,ordem,passo,minutos,link\n"


@pytest.fixture
def conteudo(tmp_path):
    pasta = tmp_path / "conteudo"
    (pasta / "situacoes").mkdir(parents=True)
    (pasta / "situacoes" / "telefonar.md").write_text("# Telefonar\n", encoding="utf-8")
    (pasta / "treinar.md").write_text("# Treinar\n", encoding="utf-8")
    return pasta


def plano(tmp_path, linhas):
    p = tmp_path / "destravar.csv"
    p.write_text(CAB + "".join(l + "\n" for l in linhas), encoding="utf-8")
    return p


def test_plano_valido_gera_dados(tmp_path, conteudo):
    p = plano(tmp_path, [
        "1,1,2,Treinar as cartas,15,treinar/?situacao=6",
        "1,1,1,Ouvir e repetir as frases,10,situacoes/telefonar/",
    ])
    assert validar_plano(p, "destravar", conteudo) == []
    dados = dados_do_plano(p, "destravar")
    assert dados["trilha"] == "destravar" and dados["titulo"] == "Destravar a fala" and dados["semanas"] == 12
    assert [x["ordem"] for x in dados["passos"]] == [1, 2]
    assert dados["passos"][0] == {"semana": 1, "dia": 1, "ordem": 1, "passo": "Ouvir e repetir as frases",
                                  "minutos": 10, "link": "situacoes/telefonar/"}


@pytest.mark.parametrize("linhas, trecho", [
    (["1,1,1,A,20,", "1,1,2,B,15,"], "minutos"),
    (["1,1,1,A,15,"], "minutos"),
    (["1,8,1,A,20,"], "dia"),
    (["1,1,1,A,10,", "1,1,1,B,10,"], "ordem"),
    (["1,1,1,A,20,/situacoes/telefonar/"], "link"),
    (["1,1,1,A,20,https://exemplo.com"], "link"),
    (["1,1,1,A,20,situacoes/nao-existe/"], "não existe"),
])
def test_plano_erros(tmp_path, conteudo, linhas, trecho):
    erros = validar_plano(plano(tmp_path, linhas), "destravar", conteudo)
    assert erros and any(trecho in e.mensagem for e in erros)


def test_dados_do_plano_do_repositorio_em_dia():
    csv = RAIZ / "kit/planos/destravar.csv"
    if not csv.exists():
        pytest.skip("plano ainda não escrito")
    gravado = json.loads((RAIZ / "conteudo/dados/destravar.json").read_text(encoding="utf-8"))
    assert gravado == dados_do_plano(csv, "destravar")


@pytest.mark.parametrize("link", [
    "treinar/?situacao=6) [clique](javascript:alert(1)",
    "treinar/?situacao=6 x",
    'treinar/?a="b"',
    "treinar/#<x>",
    "treinar/(x)",
    "Situacoes/telefonar/",
])
def test_link_do_plano_so_aceita_caminho_simples(tmp_path, conteudo, link):
    import csv
    p = tmp_path / "destravar.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["semana", "dia", "ordem", "passo", "minutos", "link"])
        escritor.writerow([1, 1, 1, "Treinar", 20, link])
    erros = validar_plano(p, "destravar", conteudo)
    assert len(erros) == 1 and "o link só pode ter" in erros[0].mensagem


# Semanas 2 a 6 da trilha Destravar a fala (plano da 1B, Tarefa 15).
LEITURAS = {2: {"guia/como-usar/", "guia/shadowing/"}, 3: {"guia/fluencia/"}, 4: {"guia/frases-chave/"},
            5: {"guia/medo-de-falar/"}, 6: {"guia/ia-modo-de-voz/"}}


def test_semanas_1_a_6_do_destravar():
    passos = dados_do_plano(RAIZ / "kit/planos/destravar.csv", "destravar")["passos"]
    assert {p["semana"] for p in passos} == set(range(1, 7))
    for semana in range(1, 7):
        da_semana = [p for p in passos if p["semana"] == semana]
        assert {p["dia"] for p in da_semana} == set(range(1, 7)), semana

        def com(trecho):
            return [p for p in da_semana if trecho in p["passo"]]

        assert len(com("Conversa real")) == 1, semana
        gravar = com("Gravar a sua voz")
        assert len(gravar) == 1 and gravar[0]["link"] == "trilhas/destravar/ficha/", semana
        assert com("4/3/2") and com("Shadowing"), semana
        if semana >= 2:
            assert len(com("Roteiro de IA")) >= 2, semana
            assert LEITURAS[semana] <= {p["link"] for p in da_semana}, semana
    for p in passos:
        for n in re.findall(r"situacao=([0-9]+)", p["link"]):
            assert n in {"6", "7", "8"}, p
        if p["link"].startswith("situacoes/"):
            assert p["link"].split("/")[1] in {"telefonar", "tecnologia", "entrevista"}, p
