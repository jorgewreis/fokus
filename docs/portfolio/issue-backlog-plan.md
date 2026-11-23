# Backlog de implementação do portfólio Fokus

**Estado:** drafts documentados em 2026-11-23; criação adicional no Linear bloqueada pelo limite de issues do workspace. Não tratar as linhas abaixo como issues existentes.

## Registros existentes a reutilizar

| Referência | Uso neste plano | Estado observado na consulta |
| --- | --- | --- |
| [REI-191](https://linear.app/reis-developer/issue/REI-191/plat-auditar-servicos-compartilhados-e-arquitetura-do-monorepo) | Issue-mãe de arquitetura do monorepo, inventário e documentação inicial. | Em andamento; descrição atualizada. |
| [REI-193](https://linear.app/reis-developer/issue/REI-193/gov-inventariar-dependencias-compartilhadas-para-inicio-greenfield) | Dependências compartilhadas e origem dos ativos comerciais. | Em andamento. |
| [REI-189](https://linear.app/reis-developer/issue/REI-189/law-inventariar-modulos-e-lacunas-do-produto-juridico) | Inventário e fronteira do Law comercial. | Em andamento. |
| [REI-190](https://linear.app/reis-developer/issue/REI-190/lead-inventariar-produto-imobiliario-e-definir-mvp) | Inventário/escopo documentado do Lead; não prova implementação. | Concluído conforme critérios documentais próprios. |
| [REI-272](https://linear.app/reis-developer/issue/REI-272/gov-reconciliar-plano-diretor-2027-com-o-prd-vigente-do-fokus-law) | Reconciliar fronteira de portfólio com PRD e Plano Diretor. | Movida a Em andamento e atualizada em 23/11/2026. |
| [REI-24](https://linear.app/reis-developer/issue/REI-24/planejar-ativacao-de-releases-imutaveis) | Evidências/gates operacionais de releases do sistema legado. | Em revisão; não substitui desenho do monorepo. |
| [REI-45](https://linear.app/reis-developer/issue/REI-45/ux-plano-de-analise-e-correcoes-fokus-styles-cloud-e-law) | Auditoria UX existente de Styles, Cloud e Law; Lead explicitamente não incluído. | Em andamento. |
| [REI-165](https://linear.app/reis-developer/issue/REI-165/seguranca-impedir-enumeracao-pre-login-e-exposicao-de-vinculos-lawlead) | Achado e correção específicos de enumeração Law/Lead. | Não duplicar; não equivale ao contrato completo de identidade do portal. |
| [REI-27](https://linear.app/reis-developer/issue/REI-27/acompanhar-qualidade-e-evolucao-do-jarvis), [REI-28](https://linear.app/reis-developer/issue/REI-28/reconciliar-base-e-executor-do-jarvis), [REI-274](https://linear.app/reis-developer/issue/REI-274/jarvis-preparar-e-validar-o-primeiro-ciclo-autonomo-documental) | Continuidade e limites do ciclo existente do Jarvis. | Não ampliam automaticamente escopo para migração do repositório. |

Os estados são uma fotografia da consulta realizada, não devem ser reutilizados como estado atual sem nova leitura. `REI-191` já existia e permaneceu a issue-mãe; os drafts abaixo não foram criados para evitar duplicar trabalho coberto ou contornar o limite do workspace.

## Issues novas preparadas para triagem

As candidatas usam estado inicial `Planejado`, prioridade padrão `Medium`, sem responsável e sem prazo até triagem explícita. Na criação, associar a `FOKUS 2027 | Plataforma Cloud` e `REI-191`, exceto Marketing, que pertence ao projeto `FOKUS 2027 | Marketing e Campanhas`. Não marcar como concluídas até haver evidência.

| Título sugerido | Escopo e critério de aceite principal | Dependências/referências |
| --- | --- | --- |
| `[PLAT] Consolidar requisitos e critérios de aceitação de Cloud e Admin` | Matriz de jornadas/perfis, RF/RNF com IDs, origem, prioridade, critério e dependências; separar área de cliente, backoffice e administrador do espaço. | REI-191, REI-193, REI-272; `docs/product/portfolio-discovery.md`; `docs/quality/acceptance-and-evidence.md`. |
| `[PLAT] Formalizar contrato de identidade, acesso e revogação do portal` | Contrato por usuário/espaço/produto; convites, vínculo, seleção, sessão, suporte e revogação com estados de falha e testes negativos. | REI-165, REI-189, REI-191; Plano Diretor. |
| `[PLAT] Documentar APIs e avaliar gateway e processamento distribuído` | Inventário de produtor/consumidor/dados; contratos versionados; ADR para gateway, fila e distribuição apenas com necessidade comprovada. | REI-191, REI-193, REI-24; `docs/architecture/technology-evaluation-register.md`. |
| `[PLAT] Definir estratégia de testes e manuais de aceitação por produto` | Frameworks e CI verificados; matriz requisito-teste-evidência; cenários positivos, negativos, falhas e manuais sintéticos por perfil. | REI-186, REI-45, REI-189, REI-190; `docs/quality/acceptance-and-evidence.md`. |
| `[SEC] Avaliar privacidade, segurança e normas aplicáveis ao portfólio` | Matriz por produto de dados/finalidade/acesso/retenção/jurisdição; avaliar LGPD/GDPR e edições NBR/ISO em fontes oficiais; sem alegar certificação. | REI-191, REI-193, REI-165; `docs/security/portfolio-security-privacy.md`. |
| `[OPS] Definir CI, trunk-based e releases independentes por produto` | ADR de branch/release, gates por app, artefatos e rollback; decisão Docker/Kubernetes fundamentada; sem alterar produção no escopo da definição. | REI-191, REI-24, REI-193; `docs/architecture/technology-evaluation-register.md`. |
| `[UX] Definir critérios transversais de usabilidade, responsividade e acessibilidade` | Critérios observáveis por produto, fluxo e estado; roteiros de teclado, viewport e inspeção; preservar auditorias de produto. | REI-45/48/49; `docs/quality/acceptance-and-evidence.md`. |
| `[PLAT] Preparar discovery isolado de visão computacional e GANs` | Caso de uso, usuário, dados/direitos, baseline, métricas, viés, risco, custo e recomendação; protótipo isolado somente com autorização. | `docs/ai/research-gates.md`; REI-191. |
| `[PLAT] Planejar inclusão do Jarvis no repositório central` | Origem/destino, histórico, runtime, dados, ferramentas, agentes, autonomia, CI e rollback identificados; sem mover até gate validado. | REI-191, REI-27/28/274; Notion Jarvis. |
| `[MKT] Validar segmentos, jornadas e métricas por produto Fokus` | Stakeholders, problemas, alternativas, posicionamento em rascunho, funis e métricas rastreáveis por produto; sem ativar campanha/ADS. | REI-190, REI-237/248; `docs/product/portfolio-discovery.md`. |

## Critérios comuns para as issues

- Projeto e área coerentes com a frente; relações `parentId`, `relatedTo`, `blockedBy` apenas quando a semântica for verdadeira.
- Descrição inclui objetivo, contexto, escopo/exclusões, entregável, riscos, checklist, aceite, verificação, evidência e próxima ação.
- Sem datas inventadas; prazo vazio até aprovado. Responsável selecionado na triagem, não presumido.
- Estados refletem trabalho observado; issue não é concluída só pela existência de documentação ou código.
- Após criar, reler issue e conferir título, projeto, pai, estado, prioridade, labels, responsável, prazo e relações.

## Bloqueio observado

Em 23/11/2026, as tentativas de criação de issues via MCP Linear retornaram `INVALID_ARGUMENT`; nenhuma retornou ID. Uma chamada mínima de confirmação respondeu HTTP 400: `You've exceeded the free issue limit for this workspace. Please upgrade or contact sales@linear.app for a free trial.` Portanto, nenhum draft listado foi criado. Não foi tentada outra conta, workspace ou mecanismo para contornar o limite. A criação pode ser retomada no mesmo workspace quando o limite for liberado; até lá estes drafts permanecem apenas versionados no repositório.
