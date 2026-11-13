# Fontes do Passaporte

O site serve as próprias fontes, em vez de carregá-las do Google Fonts, para não enviar dados de quem visita a terceiros. Os arquivos estão em `conteudo/estilos/fontes/` e são declarados em `conteudo/estilos/fontes.css`.

Todos vêm dos pacotes do [Fontsource](https://fontsource.org), versão 5.3.0, pelo CDN do jsDelivr, baixados em 13/11/2026. O recorte `latin` cobre os acentos do português, o `·` da sílaba forte e o travessão.

| Arquivo | Pacote | URL | sha256 |
|---|---|---|---|
| `archivo-latin-wght-normal.woff2` | `@fontsource-variable/archivo@5.3.0` | `https://cdn.jsdelivr.net/npm/@fontsource-variable/archivo@5.3.0/files/archivo-latin-wght-normal.woff2` | `8f704806dbedeaaeca334b11ec348bc3ac3a439d6431544b3afb54f534ee4967` |
| `figtree-latin-wght-normal.woff2` | `@fontsource-variable/figtree@5.3.0` | `https://cdn.jsdelivr.net/npm/@fontsource-variable/figtree@5.3.0/files/figtree-latin-wght-normal.woff2` | `4ba7d3d096695818fe0686be4f1e82c6b05134e18a22260336130335027462dd` |
| `ibm-plex-mono-latin-500-normal.woff2` | `@fontsource/ibm-plex-mono@5.3.0` | `https://cdn.jsdelivr.net/npm/@fontsource/ibm-plex-mono@5.3.0/files/ibm-plex-mono-latin-500-normal.woff2` | `01d285447409c8a588692162439a038b8cbd7871309ee20267b0d2d91c6e8e22` |
| `ibm-plex-mono-latin-600-normal.woff2` | `@fontsource/ibm-plex-mono@5.3.0` | `https://cdn.jsdelivr.net/npm/@fontsource/ibm-plex-mono@5.3.0/files/ibm-plex-mono-latin-600-normal.woff2` | `0d1f0b8d0722224e32e9f28261bdc86c79115be73444ae5eceb73976a1bcdf83` |
| `LICENCAS/archivo-OFL.txt` | `@fontsource-variable/archivo@5.3.0` | `…/archivo@5.3.0/LICENSE` | `c3c8402eec0e31dc9a76851235b1c02a0bb821488b2db8e35bcc2ab60ca8fc2b` |
| `LICENCAS/figtree-OFL.txt` | `@fontsource-variable/figtree@5.3.0` | `…/figtree@5.3.0/LICENSE` | `ee23e6c84000126692e112ff067b456470493349f993ceaa8b4d3766dd6fad5d` |
| `LICENCAS/ibm-plex-mono-OFL.txt` | `@fontsource/ibm-plex-mono@5.3.0` | `…/ibm-plex-mono@5.3.0/LICENSE` | `23b0a9d0c6d3f140a0b77e483c5cfa6bba574325ef5cb189ed9f2fec4884533f` |

## Licença

As três fontes estão sob a **SIL Open Font License 1.1**, que permite usar, recortar e redistribuir junto com o site, inclusive em uso comercial, desde que a licença acompanhe os arquivos.

- Archivo: Copyright 2020 The Archivo Project Authors (<https://github.com/Omnibus-Type/Archivo>). Sem nome reservado.
- Figtree: Copyright 2022 The Figtree Project Authors (<https://github.com/erikdkennedy/figtree>). Sem nome reservado.
- IBM Plex Mono: Copyright © 2017 IBM Corp. **with Reserved Font Name "Plex"**, segundo a licença original da IBM (<https://github.com/IBM/plex/blob/master/LICENSE.txt>). O `LICENSE` do Fontsource, copiado em `LICENCAS/ibm-plex-mono-OFL.txt`, omite essa linha.

### Pendência: IBM Plex Mono

Pela OFL, recortar e converter o formato cria uma versão modificada, e versão modificada não pode usar o nome reservado ("Plex") sem permissão da IBM. O arquivo atual foi recortado pelo Fontsource, então não deveria se chamar "IBM Plex Mono".

A saída prevista é trocar pelos arquivos para web publicados pela própria IBM no pacote `@ibm/plex-mono` (versão 2.5.0: `fonts/split/woff2/IBMPlexMono-Medium-Latin1.woff2` e `IBMPlexMono-SemiBold-Latin1.woff2`, cerca de 18 KB cada, e `LICENSE.txt` com o nome reservado). Recortes feitos pela dona da fonte não são modificação de terceiros. A troca depende do OK do mantenedor para o download.

## Para atualizar

Troque a versão nas URLs, baixe de novo, confira com `sha256sum` e atualize esta tabela. Rode `python -m pytest tests/test_fontes.py` para confirmar que os arquivos continuam válidos.
