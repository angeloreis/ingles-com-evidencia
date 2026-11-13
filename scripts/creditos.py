"""CREDITOS.md gerado a partir das colunas fonte, licenca e autor dos CSVs do kit."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from scripts.audio import VOZ_PARCEIRA, VOZ_PRINCIPAL
from scripts.paginas import _ler_csvs

CABECALHO = """# Créditos

Este arquivo é gerado por `python -m scripts.construir` a partir dos dados do kit. Não edite à mão.

O conteúdo do projeto está sob a licença [CC BY-SA 4.0](LICENSE) e o código sob a [MIT](LICENSE-codigo).
"""

AUDIO = f"""## Áudio

Todo o áudio é **voz sintética**, gerada pelo projeto:

- modelo [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), de hexgrad, sob Apache 2.0;
- biblioteca [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx), sob MIT;
- vozes `{VOZ_PRINCIPAL}` (frases e pessoa A dos diálogos) e `{VOZ_PARCEIRA}` (pessoa B);
- a conversão de texto em fonemas usa o [espeak-ng](https://github.com/espeak-ng/espeak-ng) (GPL-3.0) só durante a geração; ele não faz parte do site nem dos baralhos.
"""

FONTES = """## Fontes tipográficas

Archivo, Figtree e IBM Plex Mono, sob a SIL Open Font License 1.1. Origem e conferência dos arquivos em [design/passaporte/fontes.md](design/passaporte/fontes.md).
"""

NGSL = """## Vocabulário

Listas de vocabulário da [New General Service List (NGSL)](https://www.newgeneralservicelist.com/), de Browne, Culligan e Phillips, sob CC BY-SA 4.0.
"""


def gerar_creditos(raiz: Path) -> str:
    raiz = Path(raiz)
    linhas = _ler_csvs(raiz / "kit" / "dados") + _ler_csvs(raiz / "kit" / "dialogos")
    blocos = [CABECALHO]

    dados = ["## Dados\n"]
    if not linhas:
        dados.append("Ainda não há frases publicadas.\n")
    else:
        contagem = Counter((l["fonte"].split(":")[0], l["licenca"]) for l in linhas)
        nomes = {"projeto": "escritas pelo projeto", "tatoeba": "do Tatoeba", "ngsl": "da NGSL"}
        for (fonte, licenca), n in sorted(contagem.items()):
            dados.append(f"- {n} frase(s) {nomes.get(fonte, fonte)} ({fonte}), sob {licenca}.")
        tatoeba = sorted((l for l in linhas if l["fonte"].startswith("tatoeba:")),
                         key=lambda l: int(l["fonte"].split(":")[1]))
        if tatoeba:
            dados.append("\n### Frases do Tatoeba\n")
            for l in tatoeba:
                numero = l["fonte"].split(":")[1]
                autor = f", de {l['autor']}" if l.get("autor") else ""
                dados.append(f"- [frase {numero}](https://tatoeba.org/pt-br/sentences/show/{numero}){autor}, "
                             f"sob {l['licenca']} (usada em `{l['id']}`).")
        dados.append("")
    blocos.append("\n".join(dados))
    blocos.append(AUDIO)
    blocos.append(FONTES)
    if any(l["fonte"] == "ngsl" for l in linhas):
        blocos.append(NGSL)
    return "\n".join(blocos)
