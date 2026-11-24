# Fokus

Monorepo corporativo planejado como fonte central de código, documentação e páginas do Fokus Cloud, Admin, Law comercial, Lead, Styles e Jarvis. Este checkout ainda contém em [apps/law/](apps/law/) o MVP sintético personalizado do Fokus Law on demand da 1ª Vara Crime de Ilhéus; ele não é o produto Law comercial e sua separação para um repositório externo permanece pendente de confirmar destino, histórico, dependências e reversão.

## Fokus Styles

O [Fokus Styles](packages/styles/README.md) reúne framework, catálogo, documentação, exemplos e testes. O código sob [`packages/styles/`](packages/styles/) mantém sua [licença MIT](packages/styles/LICENSE), separada da licença da raiz. O pacote npm continua `fokus-styles`. Este monorepo é a fonte do código e da publicação.

### Publicar o Fokus Styles

A publicação sai de `packages/styles` pela tag `styles-vX.Y.Z`, em que `X.Y.Z` é a versão de `packages/styles/package.json` (exemplo: `styles-v3.0.1`). O workflow [`.github/workflows/styles-release.yml`](.github/workflows/styles-release.yml) roda a suíte nesse diretório e publica em `https://registry.npmjs.org` por npm Trusted Publishing (OIDC). O job `publish` declara `id-token: write` e `contents: read`, usa Node 24 com npm >= 11.5.1 e executa `npm publish --provenance --access public`. Tags `v*.*.*` não publicam este pacote.

O trusted publisher no npmjs.com é o repositório `jorgewreis/fokus` com o arquivo `styles-release.yml`, sem environment. A credencial é o OIDC de curta duração do job; o repositório não usa secret `NPM_TOKEN` nem `NODE_AUTH_TOKEN`. A 3.0.0 já está no npm desde 22/11/2026 e não deve ser republicada por uma tag nova.

Passo a passo: [packages/styles/CONTRIBUTING.md](packages/styles/CONTRIBUTING.md#processo-de-release).

## Navegação

- [Plano diretor do portfólio Fokus](docs/portfolio/README.md)
- [Roteiro de implementação do portfólio](docs/portfolio/roadmap.md)
- [Aplicação Fokus Law on demand — 1ª Vara Crime](apps/law/)
- [Instalação e execução local](apps/law/README.md)
- [ADR-0001: arquitetura e fronteiras de ambiente](docs/adr/0001-fokus-law-greenfield-stack-and-boundaries.md)
- [Dicionário conceitual de Pessoas e Processos](docs/domain/dicionario-dominio.md)
- [Ciclo de vida das fixtures sintéticas](docs/testing/ciclo-fixtures-sinteticas.md)
- [Padrão de issues do projeto](docs/governance/linear-issue-standard.md)

## Fontes do produto

- Requisitos e decisões do MVP institucional são mantidos nos espaços privados apropriados.

Use somente dados sintéticos locais conforme as instruções do aplicativo. Este repositório não autoriza dados institucionais, conexão com produção, homologação ou implantação.
