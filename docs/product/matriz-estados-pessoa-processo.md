# Matriz de estados do fluxo Pessoa → Processo

**Estado:** mapa documental de estados observáveis; não representa telas implementadas ou testadas.
**Fontes:** [PRD canônico](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a), §§2–6 e 9; [REI-201](https://linear.app/reis-developer/issue/REI-201); [REI-202](https://linear.app/reis-developer/issue/REI-202); [REI-222](https://linear.app/reis-developer/issue/REI-222); decisões documentais concluídas em [REI-231](https://linear.app/reis-developer/issue/REI-231), [REI-232](https://linear.app/reis-developer/issue/REI-232) e [REI-233](https://linear.app/reis-developer/issue/REI-233); [matriz de autorização de Processos](../domain/matriz-autorizacao-sintetica.md) e [REI-196](https://linear.app/reis-developer/issue/REI-196) para integração dos gates.

**Estado das decisões:** sigilo e competência têm decisões documentais concluídas em REI-231/232; isso não significa que a autorização funcional de Processos esteja implementada. REI-233 concluiu a definição documental, mas a comparação de documentos permanece desabilitada até haver uma chave aprovada por tipo. As regras detalhadas de autorização continuam centralizadas na [matriz de autorização](../domain/matriz-autorizacao-sintetica.md).

| Etapa | Estado/condição | Resultado definido pela fonte | Limite / pendência |
|---|---|---|---|
| Qualquer etapa com requisição assíncrona | Carregando | Indicar que a operação está em andamento quando a interface precisar aguardar resposta. | Forma visual/copy não definidos; registrar como inaplicável onde a etapa for síncrona. |
| Localizar Pessoas | Lista inicial ou busca sem resultados | Busca somente por nome; cadastro de Pessoa continua disponível a usuário autorizado. | Copy, ordenação e paginação não definidos aqui. |
| Cadastrar Pessoa | Campos válidos e dados sintéticos | Salvar Pessoa conforme campos obrigatórios e tipo PF/PJ fixo após criação. | Não existe fluxo aprovado para alterar classificação PF/PJ. |
| Cadastrar Pessoa | Campo obrigatório inválido/ausente | Bloquear salvamento até satisfazer validações aprovadas. | Texto de mensagem e foco pós-erro não definidos. |
| Cadastrar Pessoa | Possível duplicidade documental, somente quando houver chave aprovada para o tipo | Se a comparação aprovada encontrar duplicidade, exibir alerta genérico; não revelar identidade/dados da outra Pessoa; permitir prosseguir somente após confirmação explícita e auditada. | A comparação documental permanece desabilitada até existir uma chave aprovada para cada tipo; REI-233 concluiu a decisão documental sem aprovar essas chaves. [PRD §5.1](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a) · [REI-233](https://linear.app/reis-developer/issue/REI-233). |
| Consultar endereço | CEP encontrado | Preencher campos retornados e bloqueá-los conforme PRD. | Consulta individual iniciada pelo usuário; enviar somente CEP. |
| Consultar endereço | Falha ou ausência de resultado | Permitir preenchimento manual e registrar a ocorrência. | Mensagem específica não aprovada; não consultar em lote. |
| Cadastrar/consultar Processo | CNJ válido | Validar formato e dígito; permitir localizar/criar conforme autorização e Unidade. | Resultado não pode confirmar existência de Processo inacessível. |
| Cadastrar/consultar Processo | CNJ inválido | Impedir continuação até formato/dígito serem válidos. | Texto/código do erro não definido. |
| Cadastrar/consultar Processo | Dependência externa indisponível | Manter o último catálogo válido; mostrar data da última sincronização bem-sucedida. Sem carga inicial válida, desabilitar somente seleção de classe/assuntos e ainda permitir cadastro por CNJ. | Sincronização do SGT é de catálogos; não importa Processos. |
| Vincular Pessoa–Processo | Vínculo válido | Criar/reutilizar Processo e exigir um tipo: Réu, Vítima, Testemunha ou Defensor; Testemunha registra origem no mesmo vínculo. | Não duplicar o par para representar as duas origens de Testemunha. |
| Vincular Pessoa–Processo | Tipo ausente ou não permitido | Bloquear salvamento e exigir exatamente um tipo permitido para o vínculo. | Para Testemunha, a origem é registrada no vínculo; mensagem/copy não definida. |
| Qualquer etapa protegida de Processo | Todos os gates aprovados e integrados | Só permitir a ação coberta pelos grants e pelo escopo da conta; negar sem revelar a existência do Processo quando qualquer gate falhar. | As decisões de sigilo e competência estão concluídas em REI-231/232, mas o acesso funcional continua bloqueado até a integração e validação de todos os gates. Os requisitos e casos permanecem centralizados na [matriz de autorização](../domain/matriz-autorizacao-sintetica.md); integração na [REI-196](https://linear.app/reis-developer/issue/REI-196). |
| Processo arquivado | Busca padrão ou filtro | Arquivados ficam fora da lista padrão e podem ser encontrados por filtro. | Processo não é excluído no MVP. |

## Fora do fluxo e lacunas

- Gestão de Expedições é fase futura, fora do MVP.
- Mensagens/copy e detalhes de recuperação devem ser aprovados antes de implementação.
- Esta tabela não é critério de implementação concluída, teste E2E ou evidência de homologação.
- Manter a comparação documental desabilitada até haver chave de comparação aprovada para cada tipo; a definição e a pendência estão registradas na [REI-233](https://linear.app/reis-developer/issue/REI-233).
- Manter o acesso funcional a Processos bloqueado até integrar e validar todos os gates. As decisões de sigilo e competência estão concluídas; os detalhes ficam na [matriz de autorização](../domain/matriz-autorizacao-sintetica.md) e a integração está na [REI-196](https://linear.app/reis-developer/issue/REI-196).

## Uso em revisão

Para cada linha, comparar implementação e teste com o resultado definido, registrar fonte/commit e marcar como executado, falhou ou pendente. Não preencher lacunas de produto por conveniência técnica.
