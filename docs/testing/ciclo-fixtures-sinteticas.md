# Ciclo de vida das fixtures sintéticas

**Estado:** procedimento documental para dados sintéticos; não representa cobertura já implementada.
**Atualizado em:** 19/11/2026
**Produto:** Fokus Cloud Law — MVP sintético.
**Fontes:** [PRD vigente](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a), seção 8 e decisões de autorização; [REI-198 — ambiente sintético isolado](https://linear.app/reis-developer/issue/REI-198); [REI-219 — ciclo de fixtures](https://linear.app/reis-developer/issue/REI-219); [README de apps/law](../../apps/law/README.md).

## 1. Finalidade e limites

Fixtures são dados deliberadamente inventados para testes reproduzíveis. Não são dados reais anonimizados, não podem ser derivados de processos, pessoas, logs, cópias de banco ou documentos reais, e não devem conter segredos, credenciais ou dados pessoais reais. O ambiente sintético não autoriza acesso institucional, homologação, integração PJe ou produção.

Este documento distingue:

- **Existente no repositório:** seeder idempotente da cópia local e teste automatizado do guard de destino e da idempotência; os testes do guard não provam isolamento de banco ou infraestrutura.
- **Alvo de modelagem aprovado:** baseline pequeno e determinístico e cenários isolados de vínculo múltiplo, allow/deny, duplicidade e validação. Ainda dependem da implementação dos modelos e das regras correspondentes; não são cobertura comprovada.

## 2. Alvos autorizados

| Uso | Alvo | Guarda documentada | Observação |
|---|---|---|---|
| Testes automatizados | SQLite `:memory:` com `APP_ENV=testing`. | O seeder exige simultaneamente ambiente `testing`, driver `sqlite` e database `:memory:`. | O teste usa `RefreshDatabase`; o banco é efêmero. Não usar SQLite em arquivo para este fluxo. |
| Verificação manual local | MySQL local dedicado `fokus_law_synthetic`, host `localhost` ou `127.0.0.1`, `APP_ENV=local`. | O guard atual do seeder aceita MySQL em `local` ou `development`, somente em host loopback e database exato. | Para reset manual, aplica-se a regra mais restritiva: confirmar especificamente `APP_ENV=local`, host loopback e nome exato `fokus_law_synthetic`. |
| Seeder no Compose da branch REI-198 | MySQL do serviço Compose (`host=db`, porta `3306`), `APP_ENV=local`, usuário `fokus_law_local`, database `fokus_law_synthetic` e URL vazia. | O guard do seeder nessa branch aceita esse destino interno dedicado. | Esse host não é loopback. A regra de reset manual aprovada não se estende automaticamente a esse caminho; não executar reset manual nele por inferência. |
| Outros destinos | Remoto, compartilhado, institucional, produção ou qualquer alvo fora das condições acima. | Recusado pelo guard do seeder antes de abrir conexão. | Não corrigir configuração para contornar recusa; interromper e investigar. |

O guard não detecta um túnel deliberado que exponha um destino remoto em endereço loopback. A confirmação de host/database/ambiente é necessária e não substitui a garantia de que o MySQL apontado é realmente local. A política aprovada permite reset direto de MySQL somente após confirmar cumulativamente `APP_ENV=local`, host loopback e database exatamente `fokus_law_synthetic`. Para limpeza de volume Compose, conferir o nome do projeto e do volume efetivos antes de qualquer comando destrutivo; essa é uma via distinta do reset direto e também não foi executada nesta tarefa.

## 3. Baseline aprovado para evolução

O baseline planejado deve ser pequeno, fixo e inteiramente inventado. Usar valores de fixture fixos e seed idempotente, sem fixar o tipo físico dos identificadores internos, e nunca copiar dados de produção. Alterações nos dados-base devem ser intencionais, revisáveis e acompanhadas dos testes afetados.

| Grupo | Conteúdo mínimo planejado | Estado |
|---|---|---|
| Conta autorizada | Conta de teste aprovada, com grants explícitos para o recurso e escopo de teste definidos; aprovação sozinha não concede acesso. | Decisão de produto aprovada; ainda não demonstrada nas entidades/fluxos de negócio locais. |
| Solicitação pendente | Solicitação de conta sintética sem usuário, senha, sessão ou grant; estados de aprovação permanecem distintos. | Fluxo aprovado no PRD; cenário de aplicação pendente nesta cópia local. |
| Conta sem grant | Conta sintética sem grant para o recurso exercitado. Não inventar papel: representar o grant efetivo como ausente. | Decisão de cenário aprovada; implementação pendente. |
| Pessoa e Processo | Registros integralmente fictícios, ligados à Unidade sintética definida para o cenário; CNJ fictício válido apenas para validação local. | Modelo conceitual definido; modelos/fixtures ainda não existem. |
| Vínculos | Um caso simples como base; cenários adicionais isolados para uma Pessoa em vários Processos e um Processo com várias Pessoas. | Cardinalidade aprovada; implementação pendente. |

As três contas/capacidades são estados sintéticos de autorização e não criam perfis novos. Jorge aprova a conta de teste e concede explicitamente módulos, ações, Unidade e dimensões aprovadas; e-mail confirmado, convite ou sessão não concede acesso.

## 4. CNJ e outros valores fictícios

- Gerar números de CNJ inventados que satisfaçam apenas a validação local aprovada (formato e dígito verificador); marcá-los no código/dataset como sintéticos.
- Não consultar PJe, DataJud ou qualquer serviço externo para obter ou confirmar os valores.
- Não usar número de processo real, mesmo que público, sanitizado ou aparentemente inofensivo.
- Duplicidade de CNJ deve ser exercitada somente em alvo sintético e de acordo com unicidade por Unidade. Não revelar a existência de Processo fora do escopo autorizado.
- Documentos de Pessoa usados em testes também devem ser valores fabricados; a comparação por tipo depende das regras aprovadas na REI-233. Não introduzir números reais válidos pertencentes a pessoas.

## 5. Cenários de validação planejados

Cada cenário deve ser isolado ou restaurar o baseline ao final, para manter o resultado reproduzível. Até as regras de sigilo e competência serem decididas, os cenários negativos podem validar apenas grants/módulo/unidade em recursos sintéticos que não dependam de inferir esses catálogos; não declarar cobertura de autorização completa de Processo.

| Cenário | Preparação | Resultado observável esperado | Condição de reprovação |
|---|---|---|---|
| Criação idempotente do baseline | Executar o seeder duas vezes em alvo permitido. | Não duplica registros determinísticos; cada conta conserva estado explícito esperado. | Duplicatas, concessão implícita ou estado variável entre execuções. |
| Vínculo múltiplo | Associar uma Pessoa sintética a mais de um Processo e um Processo a mais de uma Pessoa. | Cada vínculo é independente e mantém tipo obrigatório. | Relação duplicada para o mesmo par ou perda de tipo/origem. |
| Acesso permitido | Usar conta aprovada com grants explícitos e escopo correspondente já definido. | A ação permitida ocorre somente dentro do grant. | Acesso derivado apenas de login/aprovação ou fora do escopo concedido. |
| Negação por estado/grant | Repetir ação com conta pendente e conta sem grant para o recurso. | A ação é negada sem revelar informação não autorizada. | Conta pendente ou sem grant realiza a ação, ou recebe confirmação de recurso fora do escopo. |
| Duplicidade | Usar par fictício duplicado no alvo sintético, respeitando regras por tipo/unidade já aprovadas. | Detecta ou bloqueia conforme a regra vigente; não mescla automaticamente e não revela outra Pessoa. | Dado real, comparação por regra inventada, mesclagem automática ou vazamento de identidade. |
| Validação | Submeter valor sintético válido e inválido para regra já aprovada. | Aceitação/rejeição observável corresponde à regra; cenários pendentes ficam marcados como não executáveis. | A validação depende de consulta externa ou de regra ainda não aprovada. |
| Recusa de alvo inseguro | Testar guard unitário com ambiente, driver, host ou database fora da lista permitida. | Guard retorna recusa antes de conexão. | Destino remoto/compartilhado é aceito ou se tenta conexão para provar a recusa. |

**Bloqueios de autorização de Processo:** catálogo de sigilo e comportamento aguardam decisão na [REI-231](https://linear.app/reis-developer/issue/REI-231); competência e forma de atribuição aguardam decisão na [REI-232](https://linear.app/reis-developer/issue/REI-232). Não criar defaults, valores de teste ou regras baseadas em CNJ/Unidade/participação para contornar esses bloqueios.

**Duplicidade documental:** a normalização é pendente na [REI-233](https://linear.app/reis-developer/issue/REI-233). Até decisão, pode-se testar validações locais já especificadas, mas não afirmar cobertura do alerta/comparação de duplicidade documental.

## 6. Execução, reset e encerramento

### Testes automatizados

Executar a suíte dentro de `apps/law` com o ambiente PHPUnit configurado para `APP_ENV=testing`, SQLite `:memory:` e `DB_URL` vazio. O comando da suíte é `php artisan test`. O arquivo `phpunit.xml` define esses valores e `SyntheticFixtureSeederTest` atualmente cobre criação idempotente, conta explicitamente sintética sem e-mail verificado, aceitação do alvo MySQL dedicado e rejeição de host remoto e ambiente production. Os testes atuais da cópia local verificam uma fixture Laravel `User` não verificada e os predicados do guard; a suíte não comprova isolamento de infraestrutura, cenários Pessoa–Processo ou grants previstos na seção 5.

### Verificação manual no MySQL local

Antes de qualquer reset autorizado, verificar visualmente e registrar apenas o resultado destas condições, sem copiar credenciais ou conteúdo de `.env`:

1. `APP_ENV=local`.
2. Driver MySQL e host `localhost` ou `127.0.0.1`.
3. Database exatamente `fokus_law_synthetic`.
4. Confirmação independente de que o destino é o serviço local dedicado e não túnel ou proxy remoto.

Se uma condição falhar ou não puder ser confirmada, não executar seed/reset nem abrir conexão. Não executar `migrate:fresh`, exclusão manual de tabelas ou outro comando destrutivo por inferência: o repositório ainda não oferece uma rotina de reset MySQL documentada e verificada. A autorização condicional de reset define o limite do alvo, mas o procedimento operacional precisa ser especificado e revisado antes de ser usado. O seeder pode ser executado somente depois da checagem do alvo e é idempotente para a conta que ele atualmente cria.

### Registro do resultado

Registrar em relatório/issue: data real de execução, commit revisado, ambiente e alvo por rótulos não secretos, cenários executados, resultado (passou/falhou/não executado), evidência sem dados pessoais e limpeza verificada. Nunca registrar senha, token, URL de conexão, valor integral de documento/CNJ ou conteúdo de configuração. Não alegar que execução em SQLite comprova isolamento de produção ou MySQL/InnoDB.

## 7. Estado observado nos worktrees

Inspeção em 19/11/2026:

- O checkout principal (`codex/rei-195-laravel-bootstrap`, `acb2d88`) ainda contém `apps/law/database/seeders/SyntheticFixtureSeeder.php`, que cria por `firstOrCreate` um `App\\Models\\User` chamado `Conta Sintética de Teste 001`, com e-mail reservado `.test`, sem confirmação de e-mail e senha aleatória não exibida. Alterações locais recentes adicionam rejeição de `DB_URL` não vazio, mas não substituem essa fixture por `AccountRequest`. O teste correspondente tem cinco métodos de criação/idempotência e guard; não exercita conexão remota real nem prova isolamento da infraestrutura.
- Existe um worktree separado da branch REI-198 (`gar`, base `7eccb48`) com alterações locais ainda não commitadas: migration/model/status/seeder `AccountRequest`, formulário público, confirmação assinada e serviço/comando de expiração. O seed cria solicitação sintética `pending_email_confirmation`, com expiração em sete dias, sem criar User, senha, sessão ou grant. Essas alterações estão no worktree da issue, não no checkout principal; não foram copiadas nem promovidas por este documento.
- Antes das últimas alterações de ciclo de vida, a suíte do worktree passou com 11 testes/42 assertions; essa contagem histórica não representa a versão atual. Os testes de fluxo usam `Mail::fake()`; as execuções realizadas com mailer `array` não entregaram e-mail. Isso não prova validação MySQL/Compose, execução no GitHub Actions ou integração/merge ao checkout principal.
- O fluxo não confirma solicitação com link expirado: GET e POST verificam HMAC e expiração do link. Ao primeiro acesso válido após o vencimento, a solicitação passa para `Expired` e os dados de nome/e-mail são removidos; o comando `account-requests:expire` também faz essa transição e é agendado de hora em hora. Uma solicitação nova com o mesmo e-mail expira a anterior vencida antes de criar registro independente. A auditoria integral permanece pendente na REI-199; a tarefa agendada remota e seu comportamento em produção não foram configurados nem verificados.
- Após essas alterações, executei a suíte completa no worktree com `APP_ENV=testing`, SQLite `:memory:`, `DB_URL` vazio e mailer `array`: 14 testes/68 assertions passaram. Esta execução não acessou MySQL, não iniciou Compose, não enviou e-mail e não executou GitHub Actions.
- `php artisan schedule:list` confirmou o comando `account-requests:expire` em agenda horária quando executado com cache `array`; `compose.yaml` define o serviço `scheduler` usando `php artisan schedule:work`, e `docker compose -p fokus-law-synthetic config --quiet` validou a configuração. Não iniciei o serviço; portanto, a execução horária em runtime local continua não verificada. O primeiro `schedule:list` isolado falhou porque o cache herdado tentou usar a tabela `cache_locks` inexistente no SQLite `:memory:`; a checagem repetida com cache em memória passou.
- O PRD no Notion registra os contratos `AccountRequest`, limpeza após expiração e execução local com 14/68; mantém também notas históricas de 11/42 e cinco testes/12 assertions. A leitura mais recente prevalece; resultados de versões diferentes não devem ser somados.
- No checkout principal, após isolar a configuração do teste de `DB_URL` em `try/finally`, a suíte SQLite passou com 6 testes/7 assertions. A primeira execução falhou no teardown ao tentar resolver o host `example.invalid` deixado pelo próprio teste; o DNS falhou e não houve conexão MySQL. A execução seguinte, com restauração da configuração antes do teardown, passou.
- As migrations de domínio Pessoa, Processo, Unidade, vínculo ou grants ainda não existem em nenhum dos dois worktrees inspecionados. Esses cenários permanecem plano aprovado, não comportamento implementado.

## 8. Cobertura observada por área e tipo de teste

| Área | Teste existente | Cobertura conhecida |
|---|---|---|
| Fixture `AccountRequest`, confirmação e expiração | Feature (`SyntheticAccountRequestSeederTest`, `SyntheticAccountRequestSeederSafetyTest`, `AccountRequestFlowTest`) no worktree REI-198 | Doze testes nesses três arquivos; a suíte total passou com 14 testes/68 assertions em SQLite em memória. Guard da branch exige SQLite de teste ou MySQL Compose local e recusa URL externa; testes não provam isolamento de infraestrutura. Percentual não medido. |
| Seeder `User` legado | Feature (`SyntheticFixtureSeederTest`) no checkout principal | Cinco testes no arquivo; suíte do checkout passou com 6 testes/7 assertions após corrigir restauração de configuração no caso de `DB_URL` remoto. Ainda não implementa a fixture `AccountRequest`. |
| Pessoas, Processos, Unidade, vínculos e grants | Nenhum teste de domínio identificado | Não implementado/sem cobertura observada. |
| E2E/browser, MySQL/InnoDB do fluxo HTTP e GitHub Actions | Nenhum teste/execução confirmado nesta continuação | Não comprovado pela execução em SQLite; verificação manual e workflow continuam pendentes. |

A pasta `tests/Unit` não contém testes de domínio no estado inspecionado. Não declarar cobertura percentual sem execução de ferramenta de coverage e escopo medido.

## 9. Próximas dependências

1. Fechar bloqueios de sigilo (REI-231) e competência (REI-232) antes de cenários que afirmem autorização completa de Processo.
2. Reconciliar backlog com a REI-217 antes de iniciar migrations/telas.
3. Integrar/reconciliar a branch REI-198 com o checkout principal pelo fluxo Git aprovado, preservando as alterações locais e sem marcar a issue concluída antes de evidência versionada.
4. Traduzir o dicionário conceitual já documentado em modelos/fixtures em etapas técnicas posteriores, após fechar os gates de autorização.
5. Definir procedimento MySQL de reset com proteção observável e revisão antes de qualquer uso destrutivo.
