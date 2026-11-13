from scripts.construir import main


def test_dados_do_repositorio_passam(capsys):
    assert main([]) == 0
    assert "Tudo certo: 1 arquivo(s), 3 linha(s)." in capsys.readouterr().out


def test_pasta_com_erro_devolve_1(tmp_path, capsys):
    (tmp_path / "ruim.csv").write_text(
        "id,en,pt,situacao,fonte,licenca\nx-1,Hi,Oi,6,projeto,CC BY-NC 4.0\n", encoding="utf-8")
    assert main(["--dados", str(tmp_path)]) == 1
    err = capsys.readouterr().err
    assert "ruim.csv:2:" in err and "1 problema(s) encontrado(s)." in err
