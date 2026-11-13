# Inglês com Evidência

Guia aberto e gratuito, em português do Brasil, que confere com a pesquisa as técnicas vendidas pelos cursos de inglês, com um kit para praticar: situações de viagem e de trabalho remoto, frases com tradução e áudio, baralhos para o Anki e planos de estudo.

**Site:** <https://angeloreis.github.io/ingles-com-evidencia/>

O projeto está em construção. O desenho completo está em [`docs/superpowers/specs/`](docs/superpowers/specs/).

## Como o repositório é organizado

| Pasta ou arquivo | O que tem |
|---|---|
| `conteudo/` | Páginas do site (Markdown) e estilos em `conteudo/estilos/` |
| `design/passaporte/` | Fonte do design system Passaporte (`tokens.json`, guia de componentes, origem das fontes) |
| `kit/dados/` | CSVs dos baralhos, com fonte e licença de cada linha |
| `scripts/` | Validação dos dados e geração dos estilos |
| `tests/` | Testes (pytest) |
| `docs/` | Documentos do projeto, fora do site |

## Rodar localmente

É preciso ter Python 3.12.

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m zensical serve
```

O site abre em <http://localhost:8000>.

## Conferir os dados e os estilos

- Validar os CSVs dos baralhos: `.venv/bin/python -m scripts.construir`
- Gerar de novo o `conteudo/estilos/tokens.css` depois de mudar `design/passaporte/tokens.json`: `.venv/bin/python -m scripts.estilos`
- Rodar os testes: `.venv/bin/python -m pytest`

Cada linha de CSV precisa de `id`, `en`, `pt`, `situacao` ou `faixa`, `fonte` e `licenca`. As licenças aceitas são `CC BY-SA 4.0`, `CC BY 2.0 FR` e `CC0`. Frases com vírgula ficam entre aspas, e campo vazio também leva vírgula.

O arquivo precisa estar em UTF-8 e separado por vírgula. O Excel em português grava ponto e vírgula mesmo no formato CSV; use o Google Planilhas (Arquivo → Fazer download → Valores separados por vírgula) ou o LibreOffice Calc (Salvar como → CSV, com a vírgula como delimitador de campo).

## Publicação

Cada push na `main` roda os testes e publica o site no GitHub Pages (`.github/workflows/site.yml`).

## Licenças

- **Conteúdo:** [CC BY-SA 4.0](LICENSE), exigida pela lista de vocabulário NGSL. Quem reaproveitar precisa dar o crédito e manter a mesma licença.
- **Código:** [MIT](LICENSE-codigo).
- **Fontes:** SIL Open Font License 1.1 ([textos das licenças](conteudo/estilos/fontes/LICENCAS/)).

## Encontrou um erro?

Abra uma [issue](https://github.com/angeloreis/ingles-com-evidencia/issues) contando a página e o trecho. Erros no inglês das frases são especialmente bem-vindos.
