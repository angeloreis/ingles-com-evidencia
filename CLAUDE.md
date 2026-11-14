# Inglês com Evidência

## Visão geral do código

Guia e kit de prática de inglês, aberto e em português do Brasil, publicado como site estático no GitHub Pages:
- Os CSVs de `kit/` são a fonte dos dados.
- `python -m scripts.construir` confere os dados, os planos e o guia e gera os trechos das páginas, os JSON do site e os créditos. Com `--audio`, gera também o áudio de voz sintética; com `--audio --baralhos`, também os baralhos do Anki.
- O Zensical monta o site a partir de `conteudo/`, com o design system Passaporte. JavaScript sem módulos cuida do treino de cartas, da página "Hoje" e da ficha, com o progresso só no `localStorage`.

**Tecnologias:** Python 3.12, Zensical 0.1.1, kokoro-onnx (voz), genanki (Anki), pytest e mini-racer (a lógica JS roda nos testes sem Node).

**Estrutura:**
- `conteudo/`: as páginas do site;
- `kit/`: dados e trechos gerados;
- `scripts/`: build;
- `tests/`;
- `design/passaporte/`: a fonte do design system;
- `docs/`: o desenho, os planos e o registro de leitura, fora do site.

A autoridade do projeto é o desenho, em [docs/superpowers/specs/2026-11-12-ingles-com-evidencia-design.md](docs/superpowers/specs/2026-11-12-ingles-com-evidencia-design.md). Os planos de cada fase ficam em `docs/superpowers/plans/`.

Para a arquitetura em detalhe, veja [docs/CODEBASE_MAP.md](docs/CODEBASE_MAP.md).

## Regras que mais pesam

- **Idioma:** tudo em português do Brasil. Toda frase em inglês leva tradução e `lang="en"` no HTML.
- **Celular primeiro:**
  - texto com 17 px ou mais;
  - toque com 48 px ou mais;
  - nenhuma rolagem lateral;
  - contraste AA nos dois temas.
- **Privacidade:** sem rastreadores, sem fontes de terceiros e nenhum dado pessoal no repositório (`test_repositorio_sem_dados_pessoais`).
- **Licenças:** conteúdo em CC BY-SA 4.0 e código em MIT. Toda linha de CSV tem `fonte` e `licenca`, e material com licença NC nunca entra.
- **Gerados:** não se editam à mão. São eles `kit/gerado/`, `conteudo/dados/`, `CREDITOS.md` e `conteudo/estilos/tokens.css`. Depois de mudar um CSV, rode `python -m scripts.construir`.
- **Git:** o mantenedor faz commit, push, tags e deploy.
- **Ganchos do Claude Code:** `scripts/ganchos.py` barra a edição à mão de um gerado e o texto com dado pessoal, e roda o `construir` depois de cada edição em `kit/`, `scripts/` ou `conteudo/`. A ligação fica em `.claude/settings.json`, fora do git, e só vale numa sessão aberta na pasta do projeto.

## Comandos

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m scripts.construir
.venv/bin/zensical build --clean --strict
```
