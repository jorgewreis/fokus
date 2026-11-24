# Catálogo de eventos de auditoria e dados vedados

**Estado:** documento derivado para implementação e revisão; não aprova regras novas nem demonstra eventos implementados.
**Produto:** Fokus Cloud Law — MVP sintético.
**Fontes:** [PRD canônico](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a), §§3.2, 5.1, 5.2, 6 e 9.3; [REI-199](https://linear.app/reis-developer/issue/REI-199); [REI-206](https://app.notion.com/p/41c6af4c510981fe9a7ee9268c630bfe); [REI-223](https://linear.app/reis-developer/issue/REI-223).

As linhas descrevem apenas campos explicitamente aprovados. Quando a fonte não define a representação do alvo, resultado ou payload, a lacuna permanece pendente; não preencher por conveniência técnica.

## Eventos e rastreabilidade

| Evento / recorte | Fase | Campos aprovados | Limites e dados vedados | Fonte |
|---|---|---|---|---|
| Confirmar cadastro de Pessoa distinta após alerta de duplicidade documental | MVP | Usuário, data/hora, Pessoa afetada, tipo do documento e resultado da confirmação/salvamento. | Não registrar número do documento nem identidade/dados da Pessoa comparada. Não revelar registros fora do escopo autorizado. Representação do identificador da Pessoa afetada pendente. | PRD §5.1 |
| Corrigir CNJ de Processo | MVP | Usuário, data/hora e CNJ anterior e novo; revalidar formato, dígito verificador e unicidade antes de salvar. | Não revelar conflito ou metadados de Processo sem autorização. Não copiar o restante do registro. CNJ anterior/novo só está aprovado neste evento específico. | PRD §5.2 |
| Excluir Pessoa sem vínculos | MVP | Preservar evento mínimo que identifique a ação. | Não registrar nome, CPF/CNPJ, CNJ ou conteúdo removido. Sem cascata. Negar exclusão quando houver vínculo com Processo ou Conta. Campos adicionais permanecem pendentes. | PRD §§5.1 e 6; REI-199 |
| Vincular/alterar vínculo Conta–Pessoa em ambiente sintético | MVP | A ação é feita somente por Jorge e deve ser auditável. | Igualdade de e-mail não cria vínculo. Campos do evento, alvo, resultado e referência de autorização não definidos; não inferir. | PRD §3.2; REI-234 |
| Criação/edição geral de Pessoa ou Processo e autoedição de telefone/endereço | MVP | Auditoria somente nas ações que a fonte exige expressamente. | Payload, granularidade, valores anterior/novo, resultado e identificador do alvo não definidos para eventos gerais. Não copiar o registro inteiro. | PRD §§3.2, 5.1, 5.2 e 6 |
| Eventos próprios de Gestão de Expedições | Fase futura | Não catalogados para aceite do MVP. | Não são requisito de auditoria desta entrega. | PRD §4; REI-206 |

## Matriz de conteúdo

- **Vedado na exclusão:** nome, CPF/CNPJ, CNJ e conteúdo removido.
- **Vedado na duplicidade documental:** número do documento e identidade/dados da Pessoa comparada.
- **Permitido em contexto específico:** CNJ anterior e novo somente na correção de CNJ prevista no PRD §5.2; isso não autoriza replicá-los em exclusão, logs genéricos ou outros eventos.
- **Não especificado:** IDs internos, códigos de resultado, endereço/IP, diffs de campos, motivo, referência de autorização e payloads amplos. Não adicionar sem fonte aprovada.
- **Retenção:** política institucional de retenção/expurgo de eventos e backups segue pendente. Remoção da base operacional não autoriza apagar backup imediatamente nem restaurar o cadastro excluído à operação.
- **Processos:** não há exclusão no MVP; usar os estados de arquivamento aprovados.

## Pendências e estado

- REI-199 permanece bloqueada por REI-196 até definição da autorização aplicável; não implementar eventos genéricos com payload não aprovado.
- A confirmação de e-mail de solicitação de conta não está coberta por este catálogo; seu ciclo exige regra própria.
- Este artefato é documental: nenhum evento ou exclusão foi implementado ou testado por ele. Não autoriza uso institucional, dados reais ou homologação.
