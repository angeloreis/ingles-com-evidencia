"""A Action de publicação (.github/workflows/site.yml): versões travadas, caches e Release repetível."""
import re

from scripts import RAIZ
from scripts.audio import MODELO, VOZES

ACTION = (RAIZ / ".github/workflows/site.yml").read_text(encoding="utf-8")
TRAVADO = RAIZ / "requirements-travado.txt"


def test_pip_com_versoes_travadas():
    linhas = [l for l in ACTION.splitlines() if "pip install" in l]
    assert linhas
    for linha in linhas:
        assert "-c requirements-travado.txt" in linha, linha


def test_requisitos_dentro_das_restricoes():
    travado = TRAVADO.read_text(encoding="utf-8").splitlines()
    assert not [l for l in travado if " @ " in l]
    fixas = {l.split("==")[0].lower(): l.lower() for l in travado if "==" in l}
    for nome in ("site", "kit", "dev"):
        for linha in (RAIZ / f"requirements-{nome}.txt").read_text(encoding="utf-8").splitlines():
            if "==" in linha:
                pacote = linha.split("==")[0].strip().lower()
                assert fixas.get(pacote) == linha.strip().lower(), linha


def test_cache_do_kokoro_com_os_dois_arquivos():
    chaves = re.findall(r"key: (kokoro-\S+)", ACTION)
    assert len(chaves) == 2
    for chave in chaves:
        assert MODELO["sha256"] in chave and VOZES["sha256"] in chave


def test_cache_do_audio_nos_dois_jobs():
    assert ACTION.count("path: conteudo/audio") == 2
    assert ACTION.count("restore-keys: audio-") == 2


def test_release_pode_rodar_de_novo():
    assert "gh release view" in ACTION
    assert re.search(r"gh release upload .*--clobber", ACTION)


def test_publicacao_do_site_pode_rodar_de_novo():
    # Rodar de novo o job que falhou guarda um segundo pacote "github-pages" na mesma execução, e o deploy-pages
    # recusa quando acha dois (aconteceu no push da v0.3.0). Cada tentativa usa um pacote com nome próprio.
    upload = re.search(r"uses: actions/upload-pages-artifact@\S+\n\s+with:\n((?:\s+\S.*\n)+)", ACTION)
    deploy = re.search(r"uses: actions/deploy-pages@\S+\n((?:\s+\S.*\n)+)", ACTION)
    assert upload and deploy
    nome = "github-pages-${{ github.run_attempt }}"
    assert f"name: {nome}" in upload.group(1)
    assert f"artifact_name: {nome}" in deploy.group(1)
