# Checklist de release

Este checklist deve ser executado antes de qualquer publicação npm a partir
do monorepo. A 3.0.0 já está no npm desde 22/11/2026. A próxima publicação
usa a tag `styles-vX.Y.Z` e o workflow `.github/workflows/styles-release.yml`.
A autenticação é npm Trusted Publishing (OIDC): o job `publish` declara
`id-token: write` e `contents: read`, usa Node 24 com npm >= 11.5.1 e executa
`npm publish --provenance --access public`. O trusted publisher no npmjs.com é
`jorgewreis/fokus` + `styles-release.yml`, sem environment e sem secret
`NPM_TOKEN`. Tags `v*.*.*` não publicam este pacote. Não crie tag nem rode o
workflow sem autorização.

## Contrato público

- [ ] versão definida e changelog revisado;
- [ ] `fokus-styles`, `fs-`, `fs-u-`, `--fs-*`, `data-fs-*` e `FokusStyles` preservados;
- [ ] aliases históricos verificados;
- [ ] exports CSS/Sass/JS testados;
- [ ] mudanças incompatíveis documentadas;
- [ ] pacote conferido com `npm pack --dry-run --json`.

## Qualidade

```text
npm run lint
npm run build
npm test
npm run docs:check
npm run contrast:check
npm run size:check
npm run test:visual
npm run test:a11y
npm run types:check
git diff --check
```

## Visual, acessibilidade e distribuição

- [ ] claro, escuro, RTL e todos os breakpoints;
- [ ] teclado, `:focus-visible`, forced colors e reduced motion;
- [ ] formulários válidos, inválidos, disabled e loading;
- [ ] overflow, textos longos e screenshots revisados;
- [ ] budgets gzip, source maps e bundles granulares aprovados;
- [ ] `npm view`, tag e workflow executados somente após autorização de publicação.
