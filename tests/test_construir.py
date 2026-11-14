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


CSV_OK = "id,en,pt,situacao,fonte,licenca\nx-1,Hi,Oi,6,projeto,CC BY-SA 4.0\n"


def _kit_minimo(tmp_path):
    """Um projeto pequeno em tmp_path: kit/dados, kit/planos e conteudo, sem --dados de fora."""
    dados = tmp_path / "kit" / "dados"
    dados.mkdir(parents=True)
    (dados / "a.csv").write_text(CSV_OK, encoding="utf-8")
    planos = tmp_path / "kit" / "planos"
    planos.mkdir()
    conteudo = tmp_path / "conteudo"
    conteudo.mkdir()
    (conteudo / "treinar.md").write_text("# Treinar\n", encoding="utf-8")
    return ["--conteudo", str(conteudo)], planos, conteudo


def test_dados_de_fora_so_conferem(tmp_path, capsys):
    args, _, _ = _kit_minimo(tmp_path)
    fora = tmp_path / "fora"
    fora.mkdir()
    (fora / "b.csv").write_text(CSV_OK.replace("x-1", "y-1"), encoding="utf-8")
    assert main(args + ["--dados", str(fora)]) == 0
    assert "Só conferência" in capsys.readouterr().out
    assert not (tmp_path / "kit" / "gerado").exists()
    assert not (tmp_path / "CREDITOS.md").exists()


def test_dados_de_fora_com_audio_e_erro(tmp_path, capsys):
    import pytest as _pytest

    args, _, _ = _kit_minimo(tmp_path)
    with _pytest.raises(SystemExit):
        main(args + ["--dados", str(tmp_path / "fora"), "--audio"])
    assert "precisam dos dados do próprio projeto" in capsys.readouterr().err


def test_outra_raiz_le_o_proprio_kit(tmp_path):
    args, _, _ = _kit_minimo(tmp_path)
    assert main(args) == 0
    assert (tmp_path / "kit" / "gerado" / "frases-06.md").exists()
    assert (tmp_path / "CREDITOS.md").exists()


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


def test_plano_confere_a_situacao_com_as_cartas_do_projeto(tmp_path, capsys):
    # Fase 2A: um passo que pede ?situacao=N sem cartas da situação N é erro, sem somar um erro de minutos
    args, planos, _ = _kit_minimo(tmp_path)
    (planos / "destravar.csv").write_text("semana,dia,ordem,passo,minutos,link\n1,1,1,Treinar,20,treinar/?situacao=3\n", encoding="utf-8")
    assert main(args) == 1
    saida = capsys.readouterr().err
    assert "o link pede a situação 3, que não tem cartas" in saida and "1 problema(s)" in saida
