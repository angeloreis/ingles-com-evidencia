from scripts import RAIZ
from scripts.creditos import gerar_creditos


def kit(tmp_path, linhas_baralho):
    (tmp_path / "kit" / "dados").mkdir(parents=True)
    (tmp_path / "kit" / "dados" / "a.csv").write_text(
        "id,en,pt,situacao,fonte,licenca,autor\n" + "".join(l + "\n" for l in linhas_baralho), encoding="utf-8")
    return tmp_path


def test_creditos_tatoeba_com_link_e_autor(tmp_path):
    raiz = kit(tmp_path, ["t-1,Hi,Oi,6,tatoeba:123,CC BY 2.0 FR,CK", "p-1,Bye,Tchau,6,projeto,CC BY-SA 4.0,"])
    texto = gerar_creditos(raiz)
    assert "[frase 123](https://tatoeba.org/pt-br/sentences/show/123)" in texto
    assert "CK" in texto and "CC BY 2.0 FR" in texto
    assert "projeto" in texto and "Kokoro-82M" in texto and "IBM Plex Mono" in texto


def test_sem_ngsl_nao_cita_ngsl(tmp_path):
    assert "NGSL" not in gerar_creditos(kit(tmp_path, ["p-1,Bye,Tchau,6,projeto,CC BY-SA 4.0,"]))


def test_creditos_do_repositorio_em_dia():
    assert (RAIZ / "CREDITOS.md").read_text(encoding="utf-8") == gerar_creditos(RAIZ)
