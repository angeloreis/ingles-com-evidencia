import json
import sqlite3
import zipfile

import genanki
import pytest

from scripts.baralhos import gerar_baralho

LINHAS = [
    {"id": "telefonar-01", "en": "Can we talk?", "pt": "Podemos conversar?", "silaba": "",
     "situacao": "6", "fonte": "projeto", "licenca": "CC BY-SA 4.0", "autor": ""},
    {"id": "telefonar-02", "en": "Does that work for you?", "pt": "Funciona para você?", "silaba": "",
     "situacao": "6", "fonte": "tatoeba:123", "licenca": "CC BY 2.0 FR", "autor": "CK"},
]


@pytest.fixture
def audio(tmp_path):
    pasta = tmp_path / "audio"
    pasta.mkdir()
    for l in LINHAS:
        (pasta / f"ice-{l['id']}.mp3").write_bytes(b"mp3 falso")
    return pasta


def abrir(apkg, pasta):
    with zipfile.ZipFile(apkg) as z:
        z.extractall(pasta)
        midia = json.loads(z.read("media"))
    return sqlite3.connect(pasta / "collection.anki2"), midia


def test_apkg_tem_notas_com_guid_estavel(tmp_path, audio):
    apkg = gerar_baralho(6, LINHAS, audio, tmp_path / "dist")
    con, _ = abrir(apkg, tmp_path / "x")
    notas = dict(con.execute("select guid, flds from notes").fetchall())
    assert set(notas) == {genanki.guid_for("telefonar-01"), genanki.guid_for("telefonar-02")}
    assert "Podemos conversar?" in notas[genanki.guid_for("telefonar-01")]


def test_apkg_leva_os_audios(tmp_path, audio):
    apkg = gerar_baralho(6, LINHAS, audio, tmp_path / "dist")
    _, midia = abrir(apkg, tmp_path / "x")
    assert sorted(midia.values()) == ["ice-telefonar-01.mp3", "ice-telefonar-02.mp3"]


def test_nome_do_baralho(tmp_path, audio):
    apkg = gerar_baralho(6, LINHAS, audio, tmp_path / "dist")
    assert apkg.name == "ice-destravar-situacao-06.apkg"
    con, _ = abrir(apkg, tmp_path / "x")
    nomes = [d["name"] for d in json.loads(con.execute("select decks from col").fetchone()[0]).values()]
    assert "Inglês com Evidência::Destravar a fala::06 Telefonar para colegas e marcar reunião" in nomes


def test_frase_sem_audio_e_erro(tmp_path, audio):
    (audio / "ice-telefonar-02.mp3").unlink()
    with pytest.raises(RuntimeError, match="sem áudio: telefonar-02"):
        gerar_baralho(6, LINHAS, audio, tmp_path / "dist")


# Fase 1B, Tarefa 4 (M17): quem abre o baralho no Anki sabe de onde veio e sob qual licença.
def test_baralho_tem_descricao(tmp_path, audio):
    apkg = gerar_baralho(6, LINHAS, audio, tmp_path / "dist")
    con, _ = abrir(apkg, tmp_path / "x")
    decks = json.loads(con.execute("select decks from col").fetchone()[0]).values()
    desc = next(d["desc"] for d in decks if d["name"].startswith("Inglês com Evidência::"))
    for parte in ("Inglês com Evidência", "https://angeloreis.github.io/ingles-com-evidencia/", "CC BY-SA 4.0"):
        assert parte in desc


def test_credito_da_carta_do_tatoeba():
    from scripts.baralhos import _credito
    linha = {**LINHAS[1], "fonte": "tatoeba:21098"}
    assert _credito(linha) == ("Tatoeba nº 21098, de CK, CC BY 2.0 FR "
                               "(https://creativecommons.org/licenses/by/2.0/fr/). Tradução do projeto.")
    cc0 = {**linha, "licenca": "CC0"}
    assert _credito(cc0) == ("Tatoeba nº 21098, de CK, CC0 "
                             "(https://creativecommons.org/publicdomain/zero/1.0/). Tradução do projeto.")
    assert _credito(LINHAS[0]) == "projeto · CC BY-SA 4.0"


def test_descricao_do_baralho_ressalva_o_tatoeba():
    # O texto em inglês do Tatoeba não está sob CC BY-SA 4.0 (revisão final da 2A, I1).
    from scripts.baralhos import DESCRICAO
    assert "exceto o texto em inglês das frases do Tatoeba" in DESCRICAO
    assert "CC BY 2.0 FR" in DESCRICAO and "CC0" in DESCRICAO
