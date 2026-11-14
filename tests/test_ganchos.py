"""Ganchos (hooks) do Claude Code: a guarda antes de editar e o construir depois de editar."""
import json
import subprocess
import sys

import pytest

from scripts import RAIZ
from scripts.ganchos import PESSOAIS, construir_depois, guarda


def _evento(caminho, **entrada):
    return {"tool_name": "Write", "tool_input": {"file_path": str(caminho), **entrada}}


@pytest.mark.parametrize("relativo", ["kit/gerado/frases-01.md", "conteudo/dados/cartas.json", "CREDITOS.md",
                                      "conteudo/estilos/tokens.css"])
def test_guarda_barra_arquivo_gerado(relativo):
    motivo = guarda(_evento(RAIZ / relativo, content="x"), RAIZ)
    assert motivo and "gerado" in motivo and "scripts.construir" in motivo


@pytest.mark.parametrize("termo", PESSOAIS)
def test_guarda_barra_dado_pessoal(termo):
    motivo = guarda(_evento(RAIZ / "conteudo/sobre.md", content=f"texto com {termo} no meio"), RAIZ)
    assert motivo and "pessoal" in motivo


def test_guarda_confere_o_trecho_novo_do_edit():
    evento = {"tool_name": "Edit", "tool_input": {"file_path": str(RAIZ / "README.md"), "old_string": "a",
                                                   "new_string": f"b {PESSOAIS[-1]}"}}
    assert guarda(evento, RAIZ)


def test_guarda_deixa_passar_edicao_comum():
    assert guarda(_evento(RAIZ / "kit/dados/situacao-01.csv", content="id,en,pt"), RAIZ) is None


def test_guarda_ignora_arquivo_fora_do_projeto(tmp_path):
    # A memória e o scratchpad ficam fora do repositório e podem ter esses termos.
    assert guarda(_evento(tmp_path / "nota.md", content=PESSOAIS[-1]), RAIZ) is None


def test_construir_depois_so_para_kit_scripts_e_conteudo():
    chamadas = []

    def executar(raiz):
        chamadas.append(raiz)
        return 0, ""

    assert construir_depois(_evento(RAIZ / "README.md"), RAIZ, executar) is None
    assert construir_depois(_evento(RAIZ / "tests/test_site.py"), RAIZ, executar) is None
    assert chamadas == []
    for relativo in ("kit/dados/situacao-01.csv", "scripts/paginas.py", "conteudo/sobre.md"):
        assert construir_depois(_evento(RAIZ / relativo), RAIZ, executar) is None
    assert len(chamadas) == 3


def test_construir_depois_devolve_a_saida_quando_falha():
    resultado = construir_depois(_evento(RAIZ / "kit/dados/situacao-01.csv"), RAIZ,
                                 lambda raiz: (1, "situacao-01.csv, linha 3: licença não permitida"))
    assert "linha 3: licença não permitida" in resultado


def test_construir_depois_de_verdade_no_projeto():
    assert construir_depois(_evento(RAIZ / "kit/dados/situacao-01.csv"), RAIZ) is None


def test_linha_de_comando_da_guarda():
    # O Claude Code manda o evento em JSON na entrada; código 2 bloqueia e o motivo vai para o Claude.
    entrada = json.dumps(_evento(RAIZ / "CREDITOS.md", content="x"))
    saida = subprocess.run([sys.executable, "-m", "scripts.ganchos", "guarda"], input=entrada, text=True,
                           capture_output=True, cwd=RAIZ)
    assert saida.returncode == 2 and "gerado" in saida.stderr
    entrada = json.dumps(_evento(RAIZ / "README.md", content="x"))
    saida = subprocess.run([sys.executable, "-m", "scripts.ganchos", "guarda"], input=entrada, text=True,
                           capture_output=True, cwd=RAIZ)
    assert saida.returncode == 0 and saida.stderr == ""
