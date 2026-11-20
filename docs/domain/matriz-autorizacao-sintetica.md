# Matriz de autorização de Processos sintéticos

**Estado:** contrato aprovado em documentação; autorização de Processos ainda não implementada.
**Atualizado em:** 20/11/2026
**Fonte canônica:** [PRD Fokus Cloud Law](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a) e decisões nas REI-231/232.

Esta matriz define a regra de sigilo do ambiente sintético. Não copia os ACLs ou os papéis do PJe/TJBA, nem constitui regra para produção ou dados reais. O catálogo adotado é apenas o vocabulário do Decreto Judiciário TJBA nº 218/2025: Público e níveis 1 a 5. O texto oficial mantém divergência nominal sobre o nível 2; a autorização compara o identificador exato da entrada, não o texto exibido nem uma ordem numérica.

## Regra cumulativa

Uma requisição de Processo só pode prosseguir se todas as condições aprovadas estiverem satisfeitas:

1. A conta está aprovada, ativa e autenticada conforme os requisitos de sessão/MFA.
2. A conta tem grant explícito para o módulo e para a ação solicitada.
3. A Unidade do Processo está dentro do grant da conta.
4. A conta possui grant explícito da mesma competência atribuída ao Processo. **O catálogo e os controles ainda não estão implementados; nenhuma requisição funcional de Processo pode ser liberada.**
5. O Processo tem classificação de sigilo explícita.
6. A conta tem grant explícito para a mesma entrada/código de sigilo atribuída ao Processo.

Os grants de sigilo são uma lista de entradas individuais permitidas. Não há comparação por maior/menor valor, hierarquia, herança entre níveis ou liberação por qualquer grant de sigilo. A entrada `Público` não elimina os grants de módulo, ação ou Unidade, nem a autorização por competência.

Nas tabelas abaixo, `C` representa qualquer entrada/código já existente no catálogo aprovado; é somente um símbolo de comparação, não um novo nível.

## Matriz de decisões

| Conta e requisição | Classificação do Processo | Grant de sigilo da conta | Demais gates (módulo/ação, Unidade, competência) | Resultado |
|---|---|---|---|---|
| Conta pendente, inativa ou não autenticada | Qualquer | Qualquer | Qualquer | Negar |
| Conta aprovada e ativa; ação sem grant | Qualquer | Qualquer | Qualquer | Negar |
| Conta com grants e Unidade divergente | Qualquer | Correspondente ou não | Falha | Negar |
| Conta sem grant da competência do Processo, ou Processo sem competência | Qualquer | Correspondente ou não | Falha | Negar; não revelar existência |
| Conta com demais gates satisfeitos | Ausente | Qualquer | Satisfeitos | Negar sem revelar existência ou metadados do Processo |
| Conta com demais gates satisfeitos | Entrada `C` | Grant ausente | Satisfeitos | Negar sem revelar existência ou metadados do Processo |
| Conta com demais gates satisfeitos | Entrada `C` | Grant de entrada diferente de `C` | Satisfeitos | Negar; não aplicar hierarquia ou herança |
| Conta com demais gates satisfeitos | Entrada `C` | Grant explícito da mesma entrada `C` | Satisfeitos | Permitir somente a ação explicitamente concedida |
| Jorge atuando como classificador | Entrada `C` | Sem grant de acesso | Qualquer | Pode classificar/alterar com auditoria; isso não concede leitura ou escrita do Processo |

Para alterar Processo, além da autorização de leitura e dos mesmos gates, a conta precisa do grant explícito de edição. A criação/alteração da classificação é ação de administração separada: somente Jorge pode executá-la no ambiente sintético, sempre com registro auditável.

## Casos verificáveis

| Caso | Exemplo | Esperado |
|---|---|---|
| Correspondência exata | Processo classificado como nível 2; conta tem grant explícito do mesmo nível e todos os outros gates passam | A regra de sigilo passa; a decisão final ainda depende de competência aprovada |
| Código divergente | Processo classificado como nível 2; conta tem somente grant para nível 1 | Negar, sem inferir proximidade ou hierarquia |
| Sem grant | Processo classificado como nível 2; conta tem grant de módulo/ação, Unidade e competência, mas nenhum grant de sigilo | Negar |
| Sem classificação | Processo sem entrada de sigilo; conta tem grants para níveis 1 a 5 | Negar e não confirmar existência/metadados |
| Classificação alterada | Jorge altera nível 3 para nível 2 com auditoria | A classificação corrente passa a ser nível 2; grant anterior de nível 3 não basta |
| Poder de classificação não é leitura | Jorge classifica, mas sua conta não tem grant de leitura do mesmo nível do Processo | A ação de classificar é permitida e auditada; a leitura segue negada |
| Unidade ou competência falha | Grant de sigilo exato, mas Unidade diverge ou competência não passa | Negar |

## Auditoria e implementação

- Registrar cada atribuição/alteração feita por Jorge com ator, data/hora, identificador interno do Processo, operação e código anterior/novo, sem copiar dados pessoais ou documentos para a trilha.
- Avaliar autorização no servidor para listas, detalhe, vínculos e mutações. Não confiar em ocultar controles na interface.
- Aplicar resposta de negação que não revele existência nem metadados de Processo fora do escopo.
- Esta matriz não aprova auditoria geral de todas as tentativas negadas; registrar somente eventos expressamente aprovados no catálogo de auditoria.
- A matriz descreve critérios para implementação e testes futuros; não afirma que os endpoints de Pessoa/Processo ou autorização por Unidade, competência e sigilo já existam.

## Pendências

- REI-232: obter e versionar catálogo de competência, detalhar alterações de configuração e implementar os controles. Até a implementação, todo acesso funcional a Processos permanece negado.
- REI-196: implementar autorização no servidor após resolver as dependências e proteger todos os caminhos de leitura e escrita.
- REI-205: validar o percurso sintético e os casos positivos/negativos após implementação.

## Referências

- [Decreto Judiciário TJBA nº 218/2025, texto compilado](https://www7.tjba.jus.br/secao/lerPublicacao.wsp?tmp.id=39235&tmp.mostrarDiv=sim&tmp.secao=9) — catálogo PJe/TJBA, sem transposição automática de ACL.
- [REI-231 — Sigilo de Processos sintéticos](https://linear.app/reis-developer/issue/REI-231/vara-definir-catalogo-de-sigilo-e-acesso-a-processos-sinteticos).
- [REI-232 — Competência](https://linear.app/reis-developer/issue/REI-232/vara-definir-competencia-e-escopo-de-acesso-a-processos-sinteticos).
- [REI-196 — Autorização](https://linear.app/reis-developer/issue/REI-196/vara-aplicar-autorizacao-por-modulo-sigilo-e-autoria).
