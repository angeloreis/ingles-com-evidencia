import re

from scripts import RAIZ
from scripts.estilos import carregar_tokens

ESTILOS = RAIZ / "conteudo/estilos"


def css():
    return (ESTILOS / "fontes.css").read_text(encoding="utf-8")


def test_urls_relativas_e_existentes():
    urls = re.findall(r'url\("([^"]+)"\)', css())
    assert len(urls) == 4
    for u in urls:
        assert not u.startswith(("/", "http:", "https:"))
        assert (ESTILOS / u).is_file()


def test_arquivos_sao_woff2():
    arquivos = list((ESTILOS / "fontes").glob("*.woff2"))
    assert len(arquivos) == 4
    assert all(a.read_bytes()[:4] == b"wOF2" for a in arquivos)


def test_cada_familia_do_passaporte_tem_font_face():
    familias = {v.split(",")[0].strip().strip('"') for v in carregar_tokens()["type"]["families"].values()}
    assert familias == set(re.findall(r'font-family:\s*"([^"]+)"', css())) == {"Archivo", "Figtree", "IBM Plex Mono"}
    assert css().count("font-display: swap;") == 4


def test_ibm_plex_mono_vem_dos_arquivos_da_propria_ibm():
    # A licença da IBM reserva o nome "Plex": um recorte de terceiros não pode
    # usar o nome, então os arquivos são os publicados pela IBM (@ibm/plex-mono).
    urls = re.findall(r'url\("([^"]+)"\)', css())
    assert sorted(u for u in urls if "lex" in u.lower()) == [
        "fontes/IBMPlexMono-Medium-Latin1.woff2",
        "fontes/IBMPlexMono-SemiBold-Latin1.woff2",
    ]
    licenca = (ESTILOS / "fontes/LICENCAS/ibm-plex-mono-OFL.txt").read_text(encoding="utf-8")
    assert 'Reserved Font Name "Plex"' in licenca


def test_cada_fonte_tem_licenca_ofl():
    for nome in ["archivo", "figtree", "ibm-plex-mono"]:
        texto = (ESTILOS / f"fontes/LICENCAS/{nome}-OFL.txt").read_text(encoding="utf-8")
        assert "SIL OPEN FONT LICENSE" in texto.upper()
