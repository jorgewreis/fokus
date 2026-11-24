# Fokus

Monorepo corporativo da Fokus. Este checkout contém o aplicativo Greenfield Fokus Law em [apps/law/](apps/law/), a plataforma Fokus Cloud em [apps/cloud/](apps/cloud/) e o Fokus Styles em [packages/styles/](packages/styles/).

## Fokus Styles

O [Fokus Styles](packages/styles/README.md) reúne framework, catálogo, documentação, exemplos e testes. O código sob [`packages/styles/`](packages/styles/) mantém sua [licença MIT](packages/styles/LICENSE), separada da licença da raiz. O pacote npm continua `fokus-styles`. Este monorepo é a fonte do código e da publicação.

### Publicar o Fokus Styles

A publicação sai de `packages/styles` pela tag `styles-vX.Y.Z`, em que `X.Y.Z` é a versão de `packages/styles/package.json` (exemplo: `styles-v3.0.1`). O workflow [`.github/workflows/styles-release.yml`](.github/workflows/styles-release.yml) roda a suíte nesse diretório e publica em `https://registry.npmjs.org` por npm Trusted Publishing (OIDC). O job `publish` declara `id-token: write` e `contents: read`, usa Node 24 com npm >= 11.5.1 e executa `npm publish --provenance --access public`. Tags `v*.*.*` não publicam este pacote.

O trusted publisher no npmjs.com é o repositório `jorgewreis/fokus` com o arquivo `styles-release.yml`, sem environment. A credencial é o OIDC de curta duração do job; o repositório não usa secret `NPM_TOKEN` nem `NODE_AUTH_TOKEN`. A 3.0.0 já está no npm desde 22/11/2026 e não deve ser republicada por uma tag nova.

Passo a passo: [packages/styles/CONTRIBUTING.md](packages/styles/CONTRIBUTING.md#processo-de-release).

## Fokus Cloud

A plataforma [Fokus Cloud](apps/cloud/README.md) (Laravel) mora em [`apps/cloud/`](apps/cloud/). O histórico do antigo repositório `jorgewreis/fokus-cloud` foi importado com os SHAs originais, porque os gates de homologação e deploy dependem deles (REI-315). O código sob `apps/cloud/` segue a [licença proprietária própria](apps/cloud/LICENSE.md).

Até o corte do deploy, a publicação em produção do Cloud continua saindo do `jorgewreis/fokus-cloud`. Neste repositório, os workflows ativos do Cloud ficam em `.github/workflows/cloud-*.yml`, gerados por `apps/cloud/tools/ci/promote-workflows.py` a partir das fontes revisadas em `apps/cloud/.github/workflows/` (que seguem inativas). Os gatilhos automáticos rodam só para mudanças em `apps/cloud/**`; deploy, backup e diagnósticos de produção são apenas manuais e dependem do environment `production`, que só será configurado no corte.

## Navegação

- [Aplicação Fokus Law](apps/law/)
- [Plataforma Fokus Cloud](apps/cloud/)
- [Instalação e execução local](apps/law/README.md)
- [ADR-0001: arquitetura e fronteiras de ambiente](docs/adr/0001-fokus-law-greenfield-stack-and-boundaries.md)
- [Dicionário conceitual de Pessoas e Processos](docs/domain/dicionario-dominio.md)
- [Ciclo de vida das fixtures sintéticas](docs/testing/ciclo-fixtures-sinteticas.md)
- [Padrão de issues do projeto](docs/governance/linear-issue-standard.md)

## Fontes do produto

- [PRD canônico no Notion](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a): requisitos e decisões atuais.
- [REI-194 no Linear](https://linear.app/reis-developer/issue/REI-194): percurso do MVP.
- [REI-195 no Linear](https://linear.app/reis-developer/issue/REI-195): arquitetura e fronteiras de ambiente.

No [`apps/law/`](apps/law/), use somente dados sintéticos locais conforme as instruções do aplicativo. O `apps/law/` não autoriza dados institucionais, conexão com produção, homologação ou implantação. Essa restrição vale só para o `apps/law/`: o `apps/cloud/` tem pipeline de homologação e produção próprio, descrito na documentação dele.
