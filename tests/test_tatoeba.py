from scripts.tatoeba import LICENCAS, conferir_linhas

LINHA = {"id": "imigracao-03", "en": "Check, please.", "fonte": "tatoeba:21098",
         "licenca": "CC BY 2.0 FR", "autor": "CK"}
API = {"id": 21098, "text": "Check, please.", "lang": "eng", "license": "CC BY 2.0 FR",
       "owner": "CK", "is_unapproved": False}


def falso(**mudancas):
    pedidos = []

    def buscar(numero):
        pedidos.append(numero)
        return None if mudancas.get("sumiu") else {**API, **mudancas}
    buscar.pedidos = pedidos
    return buscar


def test_licencas_da_api_e_do_csv():
    assert LICENCAS == {"CC BY 2.0 FR": "CC BY 2.0 FR", "CC0 1.0": "CC0"}


def test_frase_igual_sem_problemas():
    buscar = falso()
    assert conferir_linhas([LINHA], buscar) == []
    assert buscar.pedidos == [21098]


def test_cc0_da_api_bate_com_cc0_do_csv():
    assert conferir_linhas([{**LINHA, "licenca": "CC0"}], falso(license="CC0 1.0")) == []


def test_licenca_diferente():
    assert conferir_linhas([LINHA], falso(license="CC0 1.0")) == [
        "imigracao-03: licença diferente (CSV CC BY 2.0 FR, Tatoeba CC0)"]


def test_texto_diferente():
    assert conferir_linhas([LINHA], falso(text="Check please.")) == [
        'imigracao-03: texto diferente do Tatoeba ("Check, please." × "Check please.")']


def test_autor_diferente():
    assert conferir_linhas([LINHA], falso(owner="outra")) == [
        "imigracao-03: autor diferente (CSV CK, Tatoeba outra)"]


def test_frase_que_sumiu():
    assert conferir_linhas([LINHA], falso(sumiu=True)) == ["imigracao-03: não existe mais no Tatoeba"]


def test_frase_nao_aprovada():
    assert conferir_linhas([LINHA], falso(is_unapproved=True)) == [
        "imigracao-03: frase ainda não aprovada no Tatoeba"]


def test_frase_sem_dono():
    problemas = conferir_linhas([LINHA], falso(owner=None))
    assert "imigracao-03: frase sem dono no Tatoeba" in problemas


def test_linha_do_projeto_nao_e_buscada():
    def buscar(numero):
        raise AssertionError("não devia buscar")
    assert conferir_linhas([{**LINHA, "fonte": "projeto", "licenca": "CC BY-SA 4.0", "autor": ""}], buscar) == []


def test_main_sem_frases_do_tatoeba(tmp_path, monkeypatch, capsys):
    from scripts import tatoeba
    monkeypatch.setattr(tatoeba, "RAIZ", tmp_path)
    monkeypatch.setattr(tatoeba, "buscar_frase", lambda n: (_ for _ in ()).throw(AssertionError()))
    assert tatoeba.main([]) == 0
    assert "Frases do Tatoeba conferidas: 0." in capsys.readouterr().out
