# Fokus

Monorepo corporativo da Fokus. Este checkout contém o aplicativo Greenfield Fokus Law em [apps/law/](apps/law/).

## Fokus Styles

O [Fokus Styles](packages/styles/README.md) reúne framework, catálogo, documentação, exemplos e testes. O código sob [`packages/styles/`](packages/styles/) mantém sua [licença MIT](packages/styles/LICENSE), separada da licença da raiz. O pacote npm continua `fokus-styles`. Este monorepo é a fonte do código e da publicação.

### Publicar o Fokus Styles

A publicação sai de `packages/styles` pela tag `styles-vX.Y.Z`, em que `X.Y.Z` é a versão de `packages/styles/package.json` (exemplo: `styles-v3.0.1`). O workflow [`.github/workflows/styles-release.yml`](.github/workflows/styles-release.yml) roda a suíte nesse diretório e publica em `https://registry.npmjs.org` com `NPM_TOKEN`. Tags `v*.*.*` não publicam este pacote.

O repositório `jorgewreis/fokus` precisa do secret de Actions `NPM_TOKEN` (token npm com permissão de publicar `fokus-styles`). Esse secret não vem do repositório antigo `fokus-styles`; ele tem de ser criado em Settings → Secrets and variables → Actions. A 3.0.0 já está no npm desde 22/11/2026 e não deve ser republicada por uma tag nova.

Passo a passo: [packages/styles/CONTRIBUTING.md](packages/styles/CONTRIBUTING.md#processo-de-release).

## Navegação

- [Aplicação Fokus Law](apps/law/)
- [Instalação e execução local](apps/law/README.md)
- [ADR-0001: arquitetura e fronteiras de ambiente](docs/adr/0001-fokus-law-greenfield-stack-and-boundaries.md)
- [Dicionário conceitual de Pessoas e Processos](docs/domain/dicionario-dominio.md)
- [Ciclo de vida das fixtures sintéticas](docs/testing/ciclo-fixtures-sinteticas.md)
- [Padrão de issues do projeto](docs/governance/linear-issue-standard.md)

## Fontes do produto

- [PRD canônico no Notion](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a): requisitos e decisões atuais.
- [REI-194 no Linear](https://linear.app/reis-developer/issue/REI-194/vara-implementar-o-percurso-minimo-do-mvp-institucional): percurso do MVP.
- [REI-195 no Linear](https://linear.app/reis-developer/issue/REI-195/vara-definir-arquitetura-greenfield-e-fronteiras-dos-ambientes): arquitetura e fronteiras de ambiente.

Use somente dados sintéticos locais conforme as instruções do aplicativo. Este repositório não autoriza dados institucionais, conexão com produção, homologação ou implantação.
