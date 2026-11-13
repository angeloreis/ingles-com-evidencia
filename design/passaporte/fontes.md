# Fontes do Passaporte

O site serve as próprias fontes, em vez de carregá-las do Google Fonts, para não enviar dados de quem visita a terceiros. Os arquivos estão em `conteudo/estilos/fontes/` e são declarados em `conteudo/estilos/fontes.css`. Todos foram baixados pelo CDN do jsDelivr em 13/11/2026.

- **Archivo e Figtree:** pacotes do [Fontsource](https://fontsource.org), versão 5.3.0, recorte `latin`.
- **IBM Plex Mono:** pacote oficial da IBM, `@ibm/plex-mono` versão 2.5.0, recorte `Latin1` feito pela própria IBM (veja "Licença").

Os dois recortes cobrem os acentos do português, o `·` da sílaba forte e o travessão.

| Arquivo | Pacote | URL | sha256 |
|---|---|---|---|
| `archivo-latin-wght-normal.woff2` | `@fontsource-variable/archivo@5.3.0` | `https://cdn.jsdelivr.net/npm/@fontsource-variable/archivo@5.3.0/files/archivo-latin-wght-normal.woff2` | `8f704806dbedeaaeca334b11ec348bc3ac3a439d6431544b3afb54f534ee4967` |
| `figtree-latin-wght-normal.woff2` | `@fontsource-variable/figtree@5.3.0` | `https://cdn.jsdelivr.net/npm/@fontsource-variable/figtree@5.3.0/files/figtree-latin-wght-normal.woff2` | `4ba7d3d096695818fe0686be4f1e82c6b05134e18a22260336130335027462dd` |
| `IBMPlexMono-Medium-Latin1.woff2` | `@ibm/plex-mono@2.5.0` | `https://cdn.jsdelivr.net/npm/@ibm/plex-mono@2.5.0/fonts/split/woff2/IBMPlexMono-Medium-Latin1.woff2` | `41201b658a328b9d00368215c2f1102770f80b15952ab82631e4006255e6365d` |
| `IBMPlexMono-SemiBold-Latin1.woff2` | `@ibm/plex-mono@2.5.0` | `https://cdn.jsdelivr.net/npm/@ibm/plex-mono@2.5.0/fonts/split/woff2/IBMPlexMono-SemiBold-Latin1.woff2` | `b7acd05041ab65f3b7039e218ddd893065e11a07e85ea85019473152a51b6b7d` |
| `LICENCAS/archivo-OFL.txt` | `@fontsource-variable/archivo@5.3.0` | `…/archivo@5.3.0/LICENSE` | `c3c8402eec0e31dc9a76851235b1c02a0bb821488b2db8e35bcc2ab60ca8fc2b` |
| `LICENCAS/figtree-OFL.txt` | `@fontsource-variable/figtree@5.3.0` | `…/figtree@5.3.0/LICENSE` | `ee23e6c84000126692e112ff067b456470493349f993ceaa8b4d3766dd6fad5d` |
| `LICENCAS/ibm-plex-mono-OFL.txt` | `@ibm/plex-mono@2.5.0` | `https://cdn.jsdelivr.net/npm/@ibm/plex-mono@2.5.0/LICENSE.txt` | `7e6b2818edbd8f6a01ae80641cc8f16a51080d08fb4e532be3a0b6f74adb07da` |

## Licença

As três fontes estão sob a **SIL Open Font License 1.1**, que permite usar e redistribuir junto com o site, inclusive em uso comercial, desde que a licença acompanhe os arquivos.

- **Archivo:** Copyright 2020 The Archivo Project Authors (<https://github.com/Omnibus-Type/Archivo>). Sem nome reservado: o recorte do Fontsource pode manter o nome.
- **Figtree:** Copyright 2022 The Figtree Project Authors (<https://github.com/erikdkennedy/figtree>). Sem nome reservado.
- **IBM Plex Mono:** Copyright © 2017 IBM Corp. **with Reserved Font Name "Plex"**. Pela OFL, recortar ou converter o formato cria uma versão modificada, e versão modificada não pode usar um nome reservado sem permissão. Por isso o site usa os arquivos para web que **a própria IBM publica**, sem nenhuma alteração. Nunca troque por um recorte de terceiros (Fontsource, Google Fonts baixado, recorte próprio) mantendo o nome "IBM Plex Mono".

## Para atualizar

Troque a versão nas URLs, baixe de novo, confira com `sha256sum` e atualize esta tabela. Antes de trocar a origem de uma fonte, leia a primeira linha da licença original: se ela declarar "Reserved Font Name", só use arquivos publicados por quem detém o nome. Rode `python -m pytest tests/test_fontes.py` para confirmar que os arquivos continuam válidos.
