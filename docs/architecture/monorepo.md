# Arquitetura-alvo do monorepo Fokus

**Status:** proposta estrutural aprovada; implementação técnica condicionada à auditoria dos repositórios existentes.

## Organização prevista

- `apps/`: aplicações independentes, incluindo Lead, Law e projeto específico da 1ª Vara Crime.
- `services/`: serviços e APIs implantáveis com contratos documentados.
- `packages/`: bibliotecas e componentes comuns; Fokus Styles será auditado antes de migração.
- `infra/`: configuração de ambientes e infraestrutura como código, sem segredos.
- `docs/`: documentação técnica versionada.
- `.github/`: CI, templates e automação FEKS, somente após revisão.

## Regras
- Independência de versões SemVer e releases por produto.
- Segregação de dados, credenciais, acesso e ambientes por produto, especialmente para o contexto institucional.
- Não presumir compartilhamento de banco ou autorização de uso de dados da Vara Crime.
- Componentes comuns dependem de contratos estáveis e testes de compatibilidade.
- PRs com evidências, revisão e até cinco etapas formais consolidadas de verificação antes do merge.
- Produção sujeita a autorização e controles existentes.
- Nenhuma nova despesa recorrente sem autorização expressa.

A estrutura física será materializada gradualmente mediante PRs, após inventário de tecnologia, dependências e pipelines.
