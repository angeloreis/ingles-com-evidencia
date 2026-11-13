import re

from scripts.construir import main


def test_dados_do_repositorio_passam(capsys):
    assert main([]) == 0
    # a contagem cresce a cada situação publicada; o que importa é passar sem problemas
    assert re.search(r"Tudo certo: [0-9]+ arquivo\(s\), [0-9]+ linha\(s\)\.", capsys.readouterr().out)


def test_pasta_com_erro_devolve_1(tmp_path, capsys):
    (tmp_path / "ruim.csv").write_text(
        "id,en,pt,situacao,fonte,licenca\nx-1,Hi,Oi,6,projeto,CC BY-NC 4.0\n", encoding="utf-8")
    assert main(["--dados", str(tmp_path)]) == 1
    err = capsys.readouterr().err
    assert "ruim.csv:2:" in err and "1 problema(s) encontrado(s)." in err


def test_dados_apontando_para_arquivo(tmp_path, capsys):
    arquivo = tmp_path / "um.csv"
    arquivo.write_text("id,en,pt,situacao,fonte,licenca\nx-1,Hi,Oi,6,projeto,CC BY-SA 4.0\n", encoding="utf-8")
    assert main(["--dados", str(arquivo), "--dialogos", str(tmp_path / "sem-dialogos")]) == 0
    assert "1 arquivo(s)" in capsys.readouterr().out


def test_dialogo_invalido_reprova(tmp_path, capsys):
    dados = tmp_path / "dados"
    dialogos = tmp_path / "dialogos"
    dados.mkdir()
    dialogos.mkdir()
    (dados / "a.csv").write_text("id,en,pt,situacao,fonte,licenca\nx-1,Hi,Oi,6,projeto,CC BY-SA 4.0\n",
                                 encoding="utf-8")
    (dialogos / "d.csv").write_text(
        "id,situacao,ordem,falante,en,pt,fonte,licenca\nx-d1,6,1,C,Hi,Oi,projeto,CC BY-SA 4.0\n",
        encoding="utf-8")
    assert main(["--dados", str(dados), "--dialogos", str(dialogos)]) == 1
    assert "falante" in capsys.readouterr().err


def test_pasta_de_dialogos_vazia_nao_e_erro(tmp_path, capsys):
    dados = tmp_path / "dados"
    dados.mkdir()
    (dados / "a.csv").write_text("id,en,pt,situacao,fonte,licenca\nx-1,Hi,Oi,6,projeto,CC BY-SA 4.0\n",
                                 encoding="utf-8")
    assert main(["--dados", str(dados), "--dialogos", str(tmp_path / "nao-existe")]) == 0


def _kit_minimo(tmp_path):
    dados = tmp_path / "dados"
    dados.mkdir()
    (dados / "a.csv").write_text("id,en,pt,situacao,fonte,licenca\nx-1,Hi,Oi,6,projeto,CC BY-SA 4.0\n",
                                 encoding="utf-8")
    planos = tmp_path / "planos"
    planos.mkdir()
    conteudo = tmp_path / "conteudo"
    conteudo.mkdir()
    (conteudo / "treinar.md").write_text("# Treinar\n", encoding="utf-8")
    return ["--dados", str(dados), "--dialogos", str(tmp_path / "x"), "--planos", str(planos),
            "--conteudo", str(conteudo)], planos, conteudo


def test_plano_invalido_reprova(tmp_path, capsys):
    args, planos, _ = _kit_minimo(tmp_path)
    (planos / "destravar.csv").write_text("semana,dia,ordem,passo,minutos,link\n1,1,1,A,45,\n", encoding="utf-8")
    assert main(args) == 1
    assert "minutos" in capsys.readouterr().err


def test_plano_valido_grava_os_dados(tmp_path):
    args, planos, conteudo = _kit_minimo(tmp_path)
    (planos / "destravar.csv").write_text("semana,dia,ordem,passo,minutos,link\n1,1,1,Treinar,20,treinar/\n",
                                          encoding="utf-8")
    assert main(args) == 0
    assert '"passo": "Treinar"' in (conteudo / "dados" / "destravar.json").read_text(encoding="utf-8")


def test_baralhos_exige_audio(capsys):
    import pytest as _pytest

    with _pytest.raises(SystemExit) as saida:
        main(["--baralhos"])
    assert saida.value.code == 2
    assert "precisa de --audio junto" in capsys.readouterr().err
