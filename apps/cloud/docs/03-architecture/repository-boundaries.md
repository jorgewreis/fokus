# Fronteiras dos repositorios Fokus

## Objetivo

Este documento define como os quatro projetos do ecossistema Fokus se
relacionam. O Fokus Cloud e a plataforma-mae e a porta institucional de entrada;
os demais projetos permanecem independentes, com ciclos de desenvolvimento,
release e deploy proprios, mesmo quando compartilham o monorepo.

## Localizacao do codigo

Desde 24/11/2026 (REI-315), Cloud e Styles ficam no monorepo
[`jorgewreis/fokus`](https://github.com/jorgewreis/fokus), cada um em seu
diretorio, com workflows prefixados (`cloud-*`, `styles-*`). O
historico do antigo `jorgewreis/fokus-cloud` foi importado com os SHAs
originais. Ate o corte do deploy, a publicacao do Cloud continua saindo do
`jorgewreis/fokus-cloud`.

| Projeto | Codigo | Local | Tipo | Responsabilidade | Dominio canonico |
| --- | --- | --- | --- | --- | --- |
| Fokus Cloud | `cloud` | `jorgewreis/fokus` · `apps/cloud` | Plataforma e hub institucional | Marketing, portfolio, identidade, empresas, assinaturas, billing e backoffice | `https://fokuscloud.com.br` |
| Fokus Styles | `styles` | `jorgewreis/fokus` · `packages/styles` | Framework CSS open source | Tokens, temas, componentes, acessibilidade, documentacao e pacote npm | `https://styles.fokuscloud.com.br` |
| Fokus Law | `law` | `fokus-law` | SaaS pago | Operacoes juridicas, cartorarias e modulos Law | `https://law.fokuscloud.com.br` |
| Fokus Lead | `lead` | `fokus-lead` | SaaS pago | CRM imobiliario, leads, imoveis e automacoes comerciais | `https://lead.fokuscloud.com.br` |

## Regra de pertencimento

- O Cloud contem somente recursos comuns, comerciais ou administrativos da
  plataforma.
- Styles contem o framework visual reutilizavel e nao regras de negocio dos
  produtos.
- Law contem regras, dados, permissoes e fluxos juridicos.
- Lead contem regras, dados, permissoes e fluxos imobiliarios.
- Uma funcionalidade comum deve ser contratada no Cloud antes de ser duplicada
  em Law ou Lead.

## Integracoes

O Cloud e a fonte operacional comum para identidade, empresa ativa, catalogo,
assinaturas, billing e autorizacao de acesso aos produtos pagos. Law e Lead
podem enviar metricas de uso por `product_code`, mas nao alteram regras
comerciais da plataforma.

O catalogo usa os codigos estaveis `law` e `lead`. O nome publico pode evoluir
sem alterar esses codigos nem o historico comercial.

## Portfolio publico

O Cloud apresenta os quatro projetos no portfolio institucional. A pagina do
Cloud pode resumir cada projeto, mas a documentacao e a aplicacao de cada
produto permanecem em seu diretorio ou repositorio e dominio canonico.

| Projeto | Chamada principal |
| --- | --- |
| Fokus Styles | Documentacao, NPM e GitHub |
| Fokus Law | Conhecer, assinar e acessar o sistema |
| Fokus Lead | Conhecer, assinar e acessar o sistema |

## Manifesto

Cada projeto deve possuir `fokus-project.json` com identidade, tipo, versao,
status, repositorio, diretorio (`path`, no monorepo) e URLs. O arquivo e validado no CI e usado para documentacao;
nao e uma dependencia de runtime do Cloud.
