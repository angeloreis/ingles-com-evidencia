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


def _job(nome):
    wf = ler(".github/workflows/site.yml")
    inicio = wf.index(f"\n  {nome}:\n")
    proximo = [i for i in (wf.find("\n  verificar:\n", inicio + 1), wf.find("\n  publicar:\n", inicio + 1),
                           wf.find("\n  baralhos:\n", inicio + 1)) if i > 0]
    return wf[inicio:min(proximo) if proximo else len(wf)]


def test_publicar_gera_audio_antes_do_build():
    publicar = _job("publicar")
    assert publicar.index("scripts.construir --audio") < publicar.index("zensical build")
    assert "actions/cache@v5" in publicar


def test_job_baralhos_so_em_tag():
    baralhos = _job("baralhos")
    for trecho in ["startsWith(github.ref, 'refs/tags/v')", "contents: write", "gh release create",
                   "scripts.construir --audio --baralhos", "needs: verificar"]:
        assert trecho in baralhos


def test_concurrency_so_no_publicar():
    wf = ler(".github/workflows/site.yml")
    assert wf.count("concurrency:") == 1 and "concurrency:" in _job("publicar")
