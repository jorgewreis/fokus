# Normalização e duplicidade de documentos da Pessoa

**Estado:** matriz de decisão para o MVP sintético; regras ainda pendentes não podem ser inferidas pela implementação.  
**Atualizado em:** 20/11/2026.  
**Produto:** Fokus Cloud Law — 1ª Vara Crime de Ilhéus.

## Regra geral aprovada

- Guardar e exibir o valor informado, sem substituí-lo por uma forma normalizada.
- Validar formato separadamente da comparação de duplicidade.
- Só criar uma chave de comparação depois que uma regra específica para o tipo documental for aprovada.
- Não remover pontuação, espaços, acentos, zeros ou caracteres de forma genérica.
- Não copiar números de documentos para eventos de auditoria, logs ou mensagens de erro.
- Quando uma duplicidade confirmada for detectada conforme regra aprovada, mostrar aviso genérico, sem identificar nem revelar dados da outra Pessoa. O usuário pode prosseguir após confirmação; registrar essa confirmação na auditoria sem o número do documento.

Até que uma chave por tipo seja aprovada, a implementação não compara documentos para afirmar duplicidade. A validação local de CPF/CNPJ não implica uma regra de normalização para comparação.

## Matriz por tipo

“Valor original” significa preservar os caracteres informados para armazenamento e exibição. “Comparação pendente” significa que nenhum alerta de duplicidade documental baseado nesse tipo pode ser produzido ainda.

| Tipo | Aplicabilidade aprovada | Validação aprovada | Valor original | Chave/comparação | Evidência / pendência |
|---|---|---|---|---|---|
| CPF | Pessoa Física | Validação local de formato e dígitos verificadores quando informado | Preservar | Pendente; validação não define normalização | PRD §4.3; requer aprovação de regra de comparação |
| RG | Pessoa Física | Validador local determinístico ainda não especificado; não inventar além de caracteres/tamanho que venham a ser aprovados | Preservar | Pendente | PRD §4.3; regra de validação e comparação por tipo pendentes |
| CNPJ | Pessoa Jurídica | Validação local de formato e dígitos verificadores quando informado | Preservar | Pendente; validação não define normalização | PRD §4.3; requer aprovação de regra de comparação |
| Inscrição Estadual | Pessoa Jurídica | Validador local determinístico ainda não especificado | Preservar | Pendente | PRD §4.3; UF/inscrição e regra de comparação precisam de definição aprovada |
| Passaporte | Pessoa Física | Validador local determinístico ainda não especificado | Preservar | Pendente | PRD §4.3; não aplicar formato internacional presumido |
| CNH | Pessoa Física | Validador local determinístico ainda não especificado | Preservar | Pendente | PRD §4.3; não inferir regras de DV ou máscara |
| Título de Eleitor | Pessoa Física | Validador local determinístico ainda não especificado | Preservar | Pendente | PRD §4.3; não inferir DV ou normalização |
| PIS | Pessoa Física | Validador local determinístico ainda não especificado | Preservar | Pendente | PRD §4.3; não inferir DV ou máscara |
| CAD | Pessoa Física ou Jurídica | Validador local determinístico ainda não especificado | Preservar | Pendente | PRD §4.3; significado/formato específico não definido nesta matriz |
| MAT | Pessoa Física | Validador local determinístico ainda não especificado | Preservar | Pendente | PRD §4.3; significado/formato específico não definido nesta matriz |
| CIN | Pessoa Física | Validador local determinístico ainda não especificado | Preservar | Pendente | PRD §4.3; não inferir máscara ou regra nacional de comparação |

Todos os documentos são opcionais e há no máximo um número por tipo para cada Pessoa. A interface oferece somente os tipos aplicáveis à classificação PF/PJ imutável. Órgão emissor e UF são opcionais quando aplicáveis; validade documental está fora do MVP.

## Fluxo de duplicidade

1. A validação de formato acontece localmente e não consulta serviços externos.
2. A busca por nome segue a regra aprovada no PRD e só pode revelar Pessoas acessíveis ao usuário.
3. A busca por documento só pode acontecer para um tipo cuja chave de comparação esteja aprovada e implementada. Até essa decisão, não comparar nem alegar que não há duplicidade documental.
4. Se uma correspondência coberta por regra aprovada existir, informar apenas que foi encontrada possível duplicidade; não revelar identidade, nome, número ou outros dados da Pessoa correspondente.
5. Prosseguir com cadastro de uma Pessoa distinta exige confirmação explícita e evento de auditoria mínimo; o evento não contém número do documento, nome ou conteúdo livre.
6. Nunca mesclar Pessoas automaticamente.

## Pendências acionáveis

- Definir, tipo a tipo, as transformações de comparação necessárias; CPF/CNPJ permanecem pendentes apesar da validação local aprovada.
- Para os tipos diferentes de CPF/CNPJ, aprovar os validadores locais determinísticos e os limites de caracteres/tamanho antes de codificá-los. Não rejeitar com base em formato presumido.
- Manter qualquer tipo sem regra fora da comparação de duplicidade até decisão aprovada; não bloquear o cadastro do restante da Pessoa.

## Compatibilidade com REI-201

REI-201 pode implementar cadastro, consulta, edição, classificação PF/PJ, aplicabilidade, validação de CPF/CNPJ, valor original e deduplicação de nome conforme o PRD. Comparação de documentos só pode ser habilitada por tipo após a regra correspondente ser aprovada. Para os demais tipos, a ausência de uma comparação não deve ser apresentada como confirmação de ausência de duplicidade. Aviso, confirmação auditada, não exposição e ausência de mesclagem continuam obrigatórios sempre que uma regra aprovada encontrar correspondência.

## Fontes e limites

- PRD canônico, *PRD | Fokus Cloud Law — 1ª Vara Crime de Ilhéus | MVP 2027*, §4.3 (catálogo, aplicabilidade e validação documental), consultado em 20/11/2026: <https://app.notion.com/p/41b6af4c510981e0b980eff10759823a>.
- Receita Federal, [CNPJ alfanumérico](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/cnpj-alfanumerico) e [documentação técnica do CNPJ](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/documentos-tecnicos/cnpj), consultadas em 20/11/2026: formato alfanumérico em produção desde 27/07/2026, com primeiro registro em 31/07/2026. Esta regra amplia somente a validação local de CNPJ; não define chave de comparação por tipo.
- [Dicionário de domínio — Pessoas e Processos](dicionario-dominio.md), seção Documento.
- [REI-233 — Definir normalização e duplicidade dos documentos de Pessoas](https://linear.app/reis-developer/issue/REI-233/vara-definir-normalizacao-e-duplicidade-dos-documentos-de-pessoas), critérios para preservar valor original, não inferir transformação genérica e manter lacunas explícitas.
- [REI-201 — Implementar cadastro de Pessoas e deduplicação assistida](https://linear.app/reis-developer/issue/REI-201/vara-implementar-cadastro-de-pessoas-e-deduplicacao-assistida), escopo e limites de implementação.

Esta matriz não cria regras normativas para formatos documentais e não substitui decisões futuras. Nenhuma fonte consultada define uma chave de comparação aprovada para os tipos listados; por isso, elas permanecem pendentes.
