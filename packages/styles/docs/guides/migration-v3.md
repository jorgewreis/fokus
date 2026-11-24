# Migração para Fokus Styles 3

## Estado da release

A versão 3.0.0 foi publicada no npm em 22/11/2026. O nome do pacote continua
`fokus-styles`. O código-fonte está em
[`packages/styles`](https://github.com/jorgewreis/fokus/tree/main/packages/styles)
do monorepo `jorgewreis/fokus`. A consulta de 10/11/2026, que ainda via
`2.7.0` como latest, ficou desatualizada.

## Por que uma versão major

O contrato declarado do pacote passa de Node >=18 para
`^22.11.0 || ^24.11.0 || >=26.0.0`. Mesmo que dependências de produção já
impedissem a instalação estrita em Node antigo, restringir o manifesto é uma
mudança de contrato visível. Node 18/20, 22 anterior a 22.11, 23, 24 anterior
a 24.11 e 25 não são admitidos.

CSS pré-compilado servido no navegador não executa Node. Já instalar o pacote
agregado inclui as dependências da CLI, mesmo com `--omit=dev`.
Desenvolver e testar o checkout exige
`^22.13.0 || ^24.11.0 || >=26.0.0`.

## Preparar a atualização

1. Confira Node/npm no ambiente local, CI e build de produção. Prefira patches
   atualizados de Node 22 ou 24, sem permanecer no piso apenas por compatibilidade.
2. Atualize deliberadamente a dependência para 3.0.0 e regenere o lockfile
   do seu aplicativo. Instale com `--engine-strict`; não use `--force` para
   ocultar incompatibilidades.
3. Teste os imports CSS/JS, compilação Sass, comandos CLI e componentes usados.
   A 3.0.0 não renomeia classes `fs-*` nem subpaths de importação.
4. Revise regressões de foco/overlays e o estado disabled de Tag após loading:
   um disabled explícito é preservado; reabilite explicitamente se necessário.
5. Confira budgets do aplicativo. O teto gzip JS do framework é 27.008 bytes;
   a medição do candidato deve ser consultada na validação da release.

## CDN e consumidores existentes

Exemplos de URL sem versão, como
`https://cdn.jsdelivr.net/npm/fokus-styles/dist/css/fokus.css`, podem seguir
a versão mais recente, hoje a 3.0.0. Fixe uma versão já publicada e validada,
por exemplo
`https://cdn.jsdelivr.net/npm/fokus-styles@3.0.0/dist/css/fokus.css`
ou, para permanecer na linha anterior,
`https://cdn.jsdelivr.net/npm/fokus-styles@2.7.0/dist/css/fokus.css`,
e atualize CSS/JS/fontes em conjunto somente após testar a versão desejada.

A faixa npm `^2.7.0` não recebe automaticamente 3.0.0. Manter 2.7.0 fixada
não torna suas dependências compatíveis com Node antigo: seu manifesto antigo
era mais amplo que a árvore de produção. Avalie upgrade de Node primeiro.

## Evidências e limites

Consulte [compatibilidade Node](../reference/node-compatibility.md) para separar
evidências históricas dos testes do candidato. Node 26.0 testado não homologa
todas as versões futuras de Node. O smoke existente verifica tipos React,
não a execução de todas as versões do peer; ambientes além de Linux exigem
validação própria. Dependências de produção usam intervalos e são resolvidas
novamente no consumidor, sem o lockfile do repositório.

## Corte posterior

Antes de autorizar publicação, confirme versão livre no registry, CI e smoke
no SHA final, conteúdo e integridade do tarball e o dist-tag pretendido.
No monorepo, o push de uma tag `styles-v*.*.*` dispara
[`.github/workflows/styles-release.yml`](../../../../.github/workflows/styles-release.yml).
Esse workflow publica com npm Trusted Publishing (OIDC): o job `publish` tem
`id-token: write` e `contents: read`, Node 24, npm >= 11.5.1 e
`npm publish --provenance --access public`. O trusted publisher no npmjs.com é
`jorgewreis/fokus` + `styles-release.yml`, sem environment e sem secret
`NPM_TOKEN`. A tag é `styles-v` mais a versão de `packages/styles/package.json`
(`styles-v3.0.1` para a versão `3.0.1`). Tags `v*.*.*` não publicam este
pacote a partir daqui. Não reutilize `v2.7.0` nem a `v3.0.0` já publicada.
Não altere tags históricas.
