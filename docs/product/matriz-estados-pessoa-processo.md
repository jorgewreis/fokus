# Matriz de estados do fluxo Pessoa → Processo

**Estado:** mapa documental de estados observáveis; não representa telas implementadas ou testadas.
**Fontes:** [PRD canônico](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a), §§2–5 e 9; [REI-201](https://linear.app/reis-developer/issue/REI-201/vara-implementar-cadastro-de-pessoas-e-deduplicacao-assistida); [REI-202](https://linear.app/reis-developer/issue/REI-202/vara-implementar-cadastro-e-vinculo-de-processos-por-cnj); [REI-222](https://linear.app/reis-developer/issue/REI-222/vara-mapear-telas-e-estados-do-fluxo-pessoa-processo).

| Etapa | Estado/condição | Resultado definido pela fonte | Limite / pendência |
|---|---|---|---|
| Qualquer etapa com requisição assíncrona | Carregando | Indicar que a operação está em andamento e impedir submissão duplicada enquanto a mesma operação não terminou, quando a interface precisar aguardar resposta. | Forma visual/copy não definidos; registrar como inaplicável onde a etapa for síncrona. |
| Localizar Pessoas | Lista inicial ou busca sem resultados | Busca somente por nome; cadastro de Pessoa continua disponível a usuário autorizado. | Copy, ordenação e paginação não definidos aqui. |
| Cadastrar Pessoa | Campos válidos e dados sintéticos | Salvar Pessoa conforme campos obrigatórios e tipo PF/PJ fixo após criação. | Não existe fluxo aprovado para alterar classificação PF/PJ. |
| Cadastrar Pessoa | Campo obrigatório inválido/ausente | Bloquear salvamento até satisfazer validações aprovadas. | Texto de mensagem e foco pós-erro não definidos. |
| Cadastrar Pessoa | Possível duplicidade documental acessível | Exibir alerta genérico; não revelar identidade/dados da Pessoa existente; permitir prosseguir após confirmação auditada. | Comparação aguarda regras por tipo da REI-233; não comparar por normalização inventada. |
| Consultar endereço | CEP encontrado | Preencher campos retornados e bloqueá-los conforme PRD. | Consulta individual iniciada pelo usuário; enviar somente CEP. |
| Consultar endereço | Falha ou ausência de resultado | Permitir preenchimento manual e registrar a ocorrência. | Mensagem específica não aprovada; não consultar em lote. |
| Cadastrar/consultar Processo | CNJ válido | Validar formato e dígito; permitir localizar/criar conforme autorização e Unidade. | Resultado não pode confirmar existência de Processo inacessível. |
| Cadastrar/consultar Processo | CNJ inválido | Impedir continuação até formato/dígito serem válidos. | Texto/código do erro não definido. |
| Cadastrar/consultar Processo | Dependência externa indisponível | Manter o último catálogo válido; mostrar data da última sincronização bem-sucedida. Sem carga inicial válida, desabilitar somente seleção de classe/assuntos e ainda permitir cadastro por CNJ. | Sincronização do SGT é de catálogos; não importa Processos. |
| Vincular Pessoa–Processo | Vínculo válido | Criar/reutilizar Processo e exigir um tipo: Réu, Vítima, Testemunha ou Defensor; Testemunha registra origem no mesmo vínculo. | Não duplicar o par para representar as duas origens de Testemunha. |
| Vincular Pessoa–Processo | Tipo ausente ou não permitido | Bloquear salvamento e exigir exatamente um tipo permitido para o vínculo. | Para Testemunha, a origem é registrada no vínculo; mensagem/copy não definida. |
| Qualquer etapa protegida | Sem autorização efetiva ou fora do escopo | Negar acesso sem revelar a existência de registro fora do escopo autorizado. | Catálogos de sigilo e competência pendentes nas REI-231/232 bloqueiam implementação de autorização completa de Processo. |
| Processo arquivado | Busca padrão ou filtro | Arquivados ficam fora da lista padrão e podem ser encontrados por filtro. | Processo não é excluído no MVP. |

## Fora do fluxo e lacunas

- Gestão de Expedições é fase futura, fora do MVP.
- Mensagens/copy e detalhes de recuperação devem ser aprovados antes de implementação.
- Esta tabela não é critério de implementação concluída, teste E2E ou evidência de homologação.
- Antes de codificar deduplicação documental, fechar REI-233; para acesso completo a Processo, fechar REI-231 e REI-232.

## Uso em revisão

Para cada linha, comparar implementação e teste com o resultado definido, registrar fonte/commit e marcar como executado, falhou ou pendente. Não preencher lacunas de produto por conveniência técnica.