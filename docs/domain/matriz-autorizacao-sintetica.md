# Matriz de autorização de Processos sintéticos

**Estado:** contrato aprovado em documentação; autorização de Processos ainda não implementada.
**Atualizado em:** 20/11/2026
**Fonte canônica:** [PRD Fokus Cloud Law](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a) e decisões nas REI-231/232.

Esta matriz define regras de sigilo e competência do ambiente sintético. Não copia os ACLs ou os papéis do sistema processual eletrônico do tribunal de referência, nem constitui regra para produção ou dados reais. O catálogo de sigilo adotado é apenas o vocabulário do Decreto Judiciário nº 218/2025: Público e níveis 1 a 5. O texto oficial mantém divergência nominal sobre o nível 2; a autorização compara o identificador exato da entrada, não o texto exibido nem uma ordem numérica.

## Regra cumulativa

Uma requisição de Processo só pode prosseguir se todas as condições aprovadas estiverem satisfeitas:

1. A conta está aprovada, ativa e autenticada conforme os requisitos de sessão/MFA.
2. A conta tem grant explícito para o módulo e para a ação solicitada.
3. A Unidade do Processo está dentro do grant da conta.
4. A conta possui grant explícito da mesma competência atribuída ao Processo. **Há serviços internos de catálogo e grants, mas os controles completos ainda não estão integrados; nenhuma requisição funcional de Processo pode ser liberada.**
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
| Correspondência exata | Processo classificado como nível 2; conta tem grant explícito do mesmo nível e todos os outros gates passam | A regra de sigilo passa; a decisão final também exige grant da competência correspondente |
| Código divergente | Processo classificado como nível 2; conta tem somente grant para nível 1 | Negar, sem inferir proximidade ou hierarquia |
| Sem grant | Processo classificado como nível 2; conta tem grant de módulo/ação, Unidade e competência, mas nenhum grant de sigilo | Negar |
| Sem classificação | Processo sem entrada de sigilo; conta tem grants para níveis 1 a 5 | Negar e não confirmar existência/metadados |
| Classificação alterada | Jorge altera nível 3 para nível 2 com auditoria | A classificação corrente passa a ser nível 2; grant anterior de nível 3 não basta |
| Poder de classificação não é leitura | Jorge classifica, mas sua conta não tem grant de leitura do mesmo nível do Processo | A ação de classificar é permitida e auditada; a leitura segue negada |
| Unidade ou competência falha | Grant de sigilo exato, mas Unidade diverge ou competência não passa | Negar |

## Competência: fonte, atribuição e exemplos

A fonte de referência é a aba `Competencias juízo` da [planilha oficial de tabelas auxiliares MPM](https://www.cnj.jus.br/wp-content/uploads/2025/04/tabelas-auxiliares-mpm.xlsx). A [extração versionada](catalogos/README.md) contém 39 códigos e descrições, com hash e limites da fonte; a planilha não informa versão semântica, não declara as competências da Vara e não fornece mapa classe–competência. A vigência precisa ser verificada. Jorge revisará e aprovará cada atualização antes de aplicá-la no ambiente sintético; códigos retirados serão preservados em Processos e grants históricos, sem alteração silenciosa de acesso. Esse fluxo de atualização ainda não foi implementado. Por decisão de Jorge, o código MPM `999` (“Não se aplica”) não é selecionável nem concedido no ambiente sintético; o serviço interno atual o recusa para grant.

No ambiente sintético, Jorge configura e audita ramo, grau, uma ou mais competências da Vara e o mapa explícito dessas competências às classes SGT. A classe oferecida respeita o ramo, o grau e o mapa. Quando a possibilidade de seleção não puder ser confirmada pela fonte oficial, a classe permanece bloqueada até verificação com evidência e revisão por Jorge, preservados os Processos existentes; não presumir terminalidade ou vigência. Havendo várias competências mapeadas para a classe, quem cadastra escolhe uma; uma única correspondência pode ser atribuída automaticamente. Quando a classe muda, a competência é revalidada; caso não seja válida para a nova classe, é necessária escolha válida antes de concluir. Sem carga SGT inicial válida, o PRD permite cadastro inicial pelo CNJ, sem classe ou assuntos; a ausência de competência, contudo, não concede acesso funcional ao Processo.

Jorge concede explicitamente a competência à conta sintética. A verificação compara o mesmo código atribuído ao Processo, além de módulo/ação, Unidade e sigilo. A competência retirada da configuração da Vara permanece nos Processos existentes e deixa de ser opção em novos cadastros; não há reclassificação automática. Para esses registros, o acesso continua exigindo o grant correspondente; ao mudar sua classe, é necessária uma competência ativa compatível com a nova classe. A retirada de um vínculo classe–competência também preserva a classificação dos Processos existentes e o acesso sujeito aos grants e demais gates; a combinação retirada não pode ser usada em novos cadastros. Ao alterar a classe, exigir uma combinação ativa antes de concluir.

| Caso sintético | Resultado esperado da regra de competência |
|---|---|
| Processo com competência `3`; conta ativa possui grant explícito `3` | Passa a dimensão de competência; demais gates continuam obrigatórios. |
| Processo com competência `3`; conta possui somente grant `16` | Negar acesso, sem revelar existência ou metadados. |
| Processo sem competência ou conta sem grant correspondente | Negar acesso, sem revelar existência ou metadados. |
| Competência `3` retirada da configuração, preservada no Processo existente; conta mantém grant `3` | Passa a dimensão de competência para o registro existente; demais gates continuam obrigatórios. Não oferecer `3` para novo cadastro. |
| Classe de Processo com competência retirada é alterada | Exigir competência ativa compatível com a nova classe antes de concluir. |
| Vínculo classe–competência retirado; Processo existente conserva a combinação | Preservar classificação; acesso continua sujeito aos grants e demais gates. Não oferecer a combinação em novos cadastros. |
| Classe de Processo com vínculo classe–competência retirado é alterada | Exigir combinação classe–competência ativa antes de concluir. |
| Competência retirada e depois reativada na configuração da Vara | Os vínculos classe–competência antigos permanecem inativos; somente ficam disponíveis após revisão e reativação explícita e auditada por Jorge. |

Os códigos `3` e `16` são exemplos extraídos do snapshot, não uma declaração das competências da Vara. A matriz descreve resultados esperados. O [PR #24](https://github.com/jorgewreis/fokus/pull/24) integrou os serviços internos de catálogo e grants; o [PR #25](https://github.com/jorgewreis/fokus/pull/25) integrou configuração auditada, painel protegido e snapshot histórico SGT. Seleção de classes, mapa classe–competência e autorização completa de Processo continuam pendentes de implementação e integração. Verificação visual, CSRF real e concorrência MySQL permanecem pendentes.

## Auditoria e implementação

- Registrar cada atribuição/alteração feita por Jorge com ator, data/hora, identificador interno do Processo, operação e código anterior/novo, sem copiar dados pessoais ou documentos para a trilha.
- Avaliar autorização no servidor para listas, detalhe, vínculos e mutações. Não confiar em ocultar controles na interface.
- Aplicar resposta de negação que não revele existência nem metadados de Processo fora do escopo.
- Esta matriz não aprova auditoria geral de todas as tentativas negadas; registrar somente eventos expressamente aprovados no catálogo de auditoria.
- A matriz descreve critérios para implementação e testes futuros; não afirma que os endpoints de Pessoa/Processo ou autorização por Unidade, competência e sigilo já existam.

## Pendências

- REI-232: verificar vigência do catálogo e implementar o fluxo aprovado de revisão de atualizações e os controles ainda pendentes. Até a implementação dos gates necessários, todo acesso funcional a Processos permanece negado.
- REI-196: implementar autorização no servidor após resolver as dependências e proteger todos os caminhos de leitura e escrita.
- REI-205: validar o percurso sintético e os casos positivos/negativos após implementação.

## Referências

- Decreto Judiciário nº 218/2025 (texto compilado) — vocabulário de sigilo de referência, sem transposição automática de ACL.
- [REI-231 — Sigilo de Processos sintéticos](https://linear.app/reis-developer/issue/REI-231).
- [REI-232 — Competência](https://linear.app/reis-developer/issue/REI-232).
- [REI-196 — Autorização](https://linear.app/reis-developer/issue/REI-196).
