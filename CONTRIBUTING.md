# Contribuição e fluxo de desenvolvimento — Fokus

## Modelo de branches

A Fokus adota **GitHub Flow**. A única branch permanente de integração é `main`, com histórico rastreável. **Não criar `dev` ou `develop` permanentes**. Desenvolvimento ocorre em branches curtas derivadas da `main`.

Padrões:
- `feature/REI-123-descricao` — novas funcionalidades;
- `fix/REI-123-descricao` — correções;
- `refactor/REI-123-descricao` — refatorações;
- `chore/REI-123-descricao` — manutenção e infraestrutura;
- `hotfix/REI-123-descricao` — correção urgente.

O identificador `REI-123` é ilustrativo; usar o identificador real do Linear. A branch `setup/fokus-2027-governance` precede a padronização e existe exclusivamente para preparar a estrutura inicial.

## Fluxo
1. Consultar no Linear a tarefa oficial, verificar escopo, autorização, dependências, critérios de aceite, responsável e checkpoint.
2. Criar branch temporária a partir da `main`; realizar alterações e testes pertinentes.
3. Registrar commits e fazer push; abrir PR com vínculo à tarefa, riscos, evidências e impacto nos produtos.
4. Executar no máximo **cinco verificações formais pré-merge consolidadas**, mantendo cobertura adequada: (a) branch/escopo; (b) testes e checks; (c) segurança/dependências; (d) impacto/compatibilidade; (e) proteções e autorização.
5. Revisar e integrar somente após controles FEKS aplicáveis e aprovação exigida. Preferir squash merge quando adequado; apagar branch temporária após merge concluído.

## Versionamento e implantação
- SemVer por produto e biblioteca, com tags distintas como `lead/v1.0.0`, `law/v1.0.0`, `varacrime/v0.1.0`.
- O merge em `main` **não implica deploy automático** em produção.
- CI pode ser disparado por PR; publicação exige pipeline próprio, gates de environment, autorização válida, backup, monitoramento e estratégia de recuperação.
- Ambientes `development`, `staging` e `production` não exigem branches permanentes.
- Não utilizar chaves de API pagas, serviços adicionais pagos ou ações com custo sem autorização.
- Não inserir dados de processos reais, credenciais, tokens ou segredos no repositório.

## Regra transitória
Este documento não altera proteções de branch nem implanta workflows de produção por si só. A efetivação das regras na plataforma GitHub deverá ser verificada separadamente antes de declarar o processo plenamente aplicado.
