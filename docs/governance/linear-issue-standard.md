# Padrão de issues — Fokus 2027

**Fonte de execução:** Linear. **Decisões e documentação:** Notion. **Código e evidências versionadas:** GitHub.  
Política operacional relacionada: [REI-186](https://linear.app/reis-developer/issue/REI-186/gov-publicar-padrao-de-nomenclatura-ciclos-bloqueios-e-criterios-de).

## 1. Títulos e branches

- Título: `[AREA] Verbo no infinitivo + objeto + resultado concreto`.
- Áreas: `GOV` governança, `PLAT` plataforma, `LEAD` imobiliário, `LAW` jurídico comercial, `VARA` solução sob demanda, `OPS` operações.
- Exemplo: `[VARA] Validar fluxo de intimação com evidências de homologação`.
- Não repetir o identificador `REI-...` no título. Para branches: `feature/REI-123-descricao`, `fix/REI-123-descricao`, `chore/REI-123-descricao`.

## 2. Campos e descrição

Toda issue deve ter projeto, tipo, área, prioridade, estado, responsável real, prazo aprovado ou justificativa para sua ausência, milestone, ciclo somente quando comprometido e dependências nativas quando houver precedência real.

A descrição deve registrar:

1. Contexto, problema e objetivo.
2. Escopo e exclusões.
3. Entregável, riscos e impacto.
4. Checklist de execução.
5. Critérios de aceite verificáveis.
6. Testes e até cinco grupos FEKS pré-merge, quando houver código.
7. Evidência, PR ou decisão e checkpoints.
8. Próxima ação, bloqueios e dependências.

## 3. Estados e ciclos

Usar os estados existentes da equipe REI: `Planejado` (backlog), `A fazer` (selecionada), `Em andamento` (trabalho iniciado), `Em revisão` (testes/revisão), `Concluído` (critérios aceitos com evidências), `Cancelado` ou `Duplicate` quando apropriado. Não usar o estado legado/ambíguo `Pendente` em novas issues até revisão. Bloqueio não substitui estado.

Ciclos quinzenais pertencem à equipe REI, não a projetos. Incluir apenas trabalho comprometido para a janela. Planejamento mensal ou trimestral fica no projeto e nas milestones; não criar equipes por produto nem duplicar filas.

## 4. Dependências

- `blockedBy` e `blocks`: precedência efetiva.
- `parentId`: decomposição hierárquica, não bloqueio.
- `relatedTo`: referência sem precedência.
- A etiqueta `Dependência` informa contexto; não substitui relação nativa.
- Dependência externa sem issue: usar `Bloqueio externo` com motivo, impacto, responsável pela decisão, condição de desbloqueio e próxima revisão. Usar `Ag. aprovação` para autorização.
- Não criar dependência artificial por sequência de milestones.

## 5. Andamento, datas e evidências

Registrar no Linear cada movimentação material no momento em que ocorrer: início, avanço verificável, bloqueio, mudança de escopo, handoff, revisão e conclusão. Cada checkpoint informa data real no fuso `America/Bahia`, o que mudou, fonte/evidência, pendências, dependências e próxima ação. Preservar a cronologia e decisões anteriores.

- `Em andamento` somente após início efetivo; `startedAt` deve refletir a transição real.
- Não inventar, inferir ou retroagir datas. Se o início não foi registrado, declarar isso e registrar apenas a data conhecida do trabalho.
- Sem prazo aprovado, deixar `dueDate` vazio e registrar justificativa, pendências, dependências e próximo checkpoint; não criar data arbitrária.
- Só concluir após verificar critérios e evidências. Registrar limitações; não equiparar análise documental a validação técnica ou homologação.
- Depois de alterar uma issue, conferir descrição, estado, datas, responsável e relações. Antes do fechamento de lote, reconciliar issue-mãe e filhas e seus históricos.

## 6. Registro entre ferramentas

Linear é o registro oficial do trabalho, estado, responsável, datas, bloqueios e evidências de execução. Notion mantém políticas, decisões, diagnóstico e relatórios, com referência à issue Linear correspondente. GitHub mantém artefatos versionados, código, branches e PRs; uma busca sem resultado não comprova documentação ou integração. Referenciar as fontes entre si e declarar quando a verificação for somente leitura ou incompleta.

## 7. Limite do aceite

A aprovação desta política não representa, por si só, aceite técnico, homologação do FEKS, aprovação institucional, implantação ou autorização para dados reais. Esses resultados exigem critérios e evidências próprios.
