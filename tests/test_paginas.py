import shutil

import pytest

from scripts import RAIZ
from scripts.paginas import gerar_tudo, nome_audio, silaba_html, trecho_dialogo, trecho_frases, trecho_semanas

FRASE = {"id": "x-01", "en": 'I\'m "fine" & you?', "pt": "Estou bem, e você?", "silaba": "",
         "situacao": "6", "fonte": "projeto", "licenca": "CC BY-SA 4.0", "autor": ""}


def test_nome_audio():
    assert nome_audio("telefonar-01") == "ice-telefonar-01.mp3"


def test_trecho_frases_escapa_e_marca_ingles():
    html = trecho_frases([FRASE])
    assert 'lang="en"' in html and "&quot;fine&quot; &amp; you?" in html
    assert 'data-audio="ice-x-01.mp3"' in html and "<script" not in html
    assert "pp-frase__silaba" not in html
    assert "\n\n" not in html  # bloco HTML contínuo para o Markdown


def test_silaba_html():
    assert silaba_html("va·CA·tion") == '<span lang="en">va·<b>CA</b>·tion</span>'
    assert 'Sílaba forte: <span lang="en"><b>SCHED</b>·ule</span>' in trecho_frases([{**FRASE, "silaba": "SCHED·ule"}])


def test_trecho_dialogo_em_ordem_com_sequencia():
    falas = [
        {"id": "d-02", "ordem": "2", "falante": "B", "en": "Sure.", "pt": "Claro."},
        {"id": "d-01", "ordem": "1", "falante": "A", "en": "Got a minute?", "pt": "Tem um minuto?"},
    ]
    html = trecho_dialogo(falas)
    assert html.index("Got a minute?") < html.index("Sure.")
    assert 'data-audio-sequencia="ice-d-01.mp3 ice-d-02.mp3"' in html
    assert "Pessoa A" in html and "Pessoa B" in html and "Ouvir o diálogo inteiro" in html


def test_trecho_semanas():
    dados = {"trilha": "destravar", "titulo": "Destravar a fala", "semanas": 12, "passos": [
        {"semana": 1, "dia": 1, "ordem": 1, "passo": "Ouvir e repetir as frases", "minutos": 10,
         "link": "situacoes/telefonar/"},
        {"semana": 1, "dia": 1, "ordem": 2, "passo": "Conversa real", "minutos": 15, "link": ""},
        {"semana": 1, "dia": 3, "ordem": 1, "passo": "Treinar as cartas", "minutos": 20, "link": "treinar/"},
    ]}
    md = trecho_semanas(dados)
    assert "### Semana 1" in md and "Dia 1 — 25 min" in md and "Dia 3 — 20 min" in md
    assert "[Ouvir e repetir as frases](../../situacoes/telefonar/)" in md
    assert "- Conversa real — 15 min" in md
    assert "semanas 2 a 12" in md


def test_gerados_do_repositorio_em_dia(tmp_path):
    for pasta in ("kit", "conteudo"):
        shutil.copytree(RAIZ / pasta, tmp_path / pasta)
    for gerado in gerar_tudo(tmp_path):
        relativo = gerado.relative_to(tmp_path)
        assert (RAIZ / relativo).read_text(encoding="utf-8") == gerado.read_text(encoding="utf-8"), relativo


def test_trilha_sem_plano_ganha_trecho_de_aviso(tmp_path):
    (tmp_path / "kit" / "dados").mkdir(parents=True)
    gerados = gerar_tudo(tmp_path)
    semanas = tmp_path / "kit" / "gerado" / "semanas-destravar.md"
    assert semanas in gerados
    assert "ainda não foi publicado" in semanas.read_text(encoding="utf-8")


# O texto e o link dos passos vêm de um CSV que pode chegar por contribuição:
# nada nele vira HTML ou formatação Markdown na página (achado I2 da revisão final).
def _semana_com(passo, link):
    return {"trilha": "destravar", "titulo": "Destravar a fala", "semanas": 1, "passos": [
        {"semana": 1, "dia": 1, "ordem": 1, "passo": passo, "minutos": 20, "link": link}]}


def test_trecho_semanas_escapa_o_texto_do_passo():
    import markdown
    passo = "Ouvir <img src=x onerror=alert(1)> e *repetir* [a](b) _junto_ & `gravar` {: .x} \\fim"
    for link in ["treinar/?situacao=6", ""]:
        html = markdown.markdown(trecho_semanas(_semana_com(passo, link)), extensions=["attr_list", "md_in_html"])
        assert "<img" not in html and "<em>" not in html and "<code>" not in html and 'href="b"' not in html
        assert "Ouvir &lt;img src=x onerror=alert(1)&gt; e *repetir* [a](b) _junto_ &amp; `gravar` {: .x} \\fim" in html
        assert html.count("<a ") == (1 if link else 0)
    assert 'href="../../treinar/?situacao=6"' in markdown.markdown(trecho_semanas(_semana_com("A", "treinar/?situacao=6")))


def test_trecho_semanas_recusa_link_fora_do_formato():
    with pytest.raises(ValueError, match="link"):
        trecho_semanas(_semana_com("Treinar", "treinar/?situacao=6) [clique](javascript:alert(1)"))


# --- Fase 1B, Tarefa 2: títulos das situações no treino ------------------

def test_titulos_das_situacoes_com_cartas(tmp_path):
    import json

    from scripts.situacoes import SITUACOES

    (tmp_path / "kit" / "dados").mkdir(parents=True)
    (tmp_path / "kit" / "dados" / "s.csv").write_text(
        "id,en,pt,situacao,fonte,licenca\n"
        "e-01,Tell me about yourself.,Fale de você.,8,projeto,CC BY-SA 4.0\n"
        "t-01,Hello,Olá,6,projeto,CC BY-SA 4.0\n", encoding="utf-8")
    gravados = gerar_tudo(tmp_path)
    caminho = tmp_path / "conteudo" / "dados" / "situacoes.json"
    assert caminho in gravados
    texto = caminho.read_text(encoding="utf-8")
    assert json.loads(texto) == {"6": SITUACOES[6][1], "8": SITUACOES[8][1]}
    assert list(json.loads(texto)) == ["6", "8"]


# --- Fase 1B, Tarefa 4 (M8): sem JavaScript ou antes do manifesto, "Ouvir" fica desabilitado ---

def test_ouvir_nasce_desabilitado():
    import re

    falas = [{"id": "d-01", "ordem": "1", "falante": "A", "en": "Hi.", "pt": "Oi."}]
    for html in (trecho_frases([FRASE]), trecho_dialogo(falas)):
        botoes = re.findall(r"<button[^>]*>", html)
        assert botoes
        for b in botoes:
            assert "data-audio" in b and " disabled" in b, b
