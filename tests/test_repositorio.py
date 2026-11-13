from scripts import RAIZ


def ler(nome):
    return (RAIZ / nome).read_text(encoding="utf-8")


def test_licencas():
    assert "Attribution-ShareAlike 4.0 International" in ler("LICENSE")
    assert ler("LICENSE-codigo").startswith("MIT License")


def test_readme_cita_licencas_e_comandos():
    readme = ler("README.md")
    for trecho in ["CC BY-SA 4.0", "MIT", "python -m scripts.construir", "python -m zensical serve"]:
        assert trecho in readme


def test_workflow_testa_antes_de_publicar():
    wf = ler(".github/workflows/site.yml")
    assert wf.index("python -m pytest") < wf.index("zensical build --clean --strict")
    assert "needs: verificar" in wf and "actions/deploy-pages@v5" in wf


FORA_DO_GIT = {".venv", "site", ".cache", ".pytest_cache", ".superpowers", "__pycache__", ".git"}
TEXTO = {".md", ".py", ".toml", ".txt", ".yml", ".csv", ".css", ".json", ".html", ""}
# montados por partes para este arquivo não acusar a si mesmo
PESSOAIS = ["ingles-" + "pessoal", "/ho" + "me/", "/tm" + "p/", "espo" + "sa", "Ang" + "elo"]


def test_repositorio_sem_dados_pessoais():
    achados = []
    for p in RAIZ.rglob("*"):
        partes = p.relative_to(RAIZ).parts
        if not p.is_file() or p.suffix not in TEXTO or FORA_DO_GIT & set(partes):
            continue
        texto = p.read_text(encoding="utf-8", errors="ignore")
        achados += [f"{'/'.join(partes)}: {t}" for t in PESSOAIS if t in texto]
    assert achados == []


def test_job_publicar_pode_ler_o_repositorio():
    # Permissões declaradas no job substituem as do topo: sem contents: read,
    # o checkout do job publicar falha.
    publicar = ler(".github/workflows/site.yml").split("  publicar:", 1)[1]
    assert "contents: read" in publicar
