# Segurança, privacidade e normas do portfólio

**Escopo:** matriz inicial de trabalho; não é parecer jurídico, certificação, auditoria ou declaração de conformidade.

## Registro por aplicação

Para Cloud, Admin, Law comercial, Lead, Styles e Jarvis, e separadamente para o Law on demand externo, identificar:

- controlador/operador e responsáveis aplicáveis;
- categorias de titulares, dados e classificação;
- finalidade/base legal a validar, coleta, compartilhamento, retenção e eliminação;
- região de processamento, subprocessadores e integrações;
- autenticação, autorização, escopo de espaço/produto, registro de acesso e revogação;
- gestão de segredos, criptografia, backups, resposta a incidentes e recuperação;
- riscos, mitigação, evidência e risco residual.

Não presumir que dados do produto institucional podem ser reutilizados pelo produto comercial ou pelo Jarvis. Desenvolvimento e protótipos devem priorizar massa sintética não derivada de cópias de dados reais.

## LGPD e GDPR

Mapear obrigações da LGPD ao contexto brasileiro e avaliar GDPR somente quando escopo territorial, titulares, oferta ou tratamento tornarem aplicável. Registrar conclusão, evidências, responsável e revisão jurídica quando necessária. Definir solicitações dos titulares, retenção e resposta a incidentes de forma específica; não inferir conformidade por ter política publicada.

## Normas ABNT NBR e ISO

1. Levantar exigências explícitas em contratos, clientes, setor, hospedagem e mercado.
2. Consultar catálogos e textos oficiais para confirmar título, edição vigente, escopo e licença de uso.
3. Mapear cláusulas aplicáveis a controles, responsáveis e evidências.
4. Registrar lacunas e custo/impacto; separar alinhamento parcial, auditoria e certificação.

Nenhuma norma específica nem certificação é declarada adotada até concluir a avaliação de aplicabilidade.

### Candidatos para avaliação (revisão documental: 2026-11-23)

Os itens abaixo são referências candidatas, não requisitos automaticamente aplicáveis nem declarações de conformidade. A edição/status foram consultados em catálogos oficiais nesta data; confirmar novamente antes de aprovar um ADR, contrato ou compromisso externo. O texto integral das normas é protegido por direitos autorais e deve ser obtido/licenciado pelos canais oficiais quando necessário.

| Referência e situação consultada | Uso potencial no Fokus | Evidência observável a planejar | Estado |
| --- | --- | --- | --- |
| [ABNT NBR ISO/IEC 27001:2022, Versão Corrigida:2023](https://www.abntcatalogo.com.br/sebrae/norma.aspx?Q=WXV0VDkwSGkvd0dDeU1hYXFtRWlKaTBwVnBZRVdob2x2SEoyQkR6NEFqcz0%3D), catálogo ABNT indica Em Vigor. A ISO registra edição 2022 e Amd 1:2024; a adoção ABNT dessa emenda não foi confirmada nesta consulta. | Sistema de gestão de segurança se houver exigência de cliente/contrato ou objetivo organizacional aprovado. | Escopo e liderança definidos; avaliação e tratamento de riscos; declaração de aplicabilidade quando cabível; auditorias e ações rastreáveis. | Candidato; não adotado. |
| [ABNT NBR ISO/IEC 27002:2022](https://www.abntcatalogo.com.br/sebrae/norma.aspx?Q=T2JVQ1FZQkZsejNuNGtIZXVpbzJEM0ZmZ0FUY2Q0Sno5TDZmY3c5c2FIdz0%3D), catálogo ABNT indica Em Vigor. | Referência de controles para desenho/revisão de segurança, em conjunto com o escopo e risco real. | Controles selecionados ligados a ativos, ameaças, responsável, implementação e evidência; lacunas aceitas explicitamente. | Candidato; não adotado. |
| [ABNT NBR ISO/IEC 27701:2026](https://www.abntcatalogo.com.br/sebrae/norma.aspx?Q=d2lqQjJHMis5WlVCK2JiOXIwWnExdWsvUWUxQXFvRE4rOUUramtBeGpNTT0%3D), catálogo ABNT indica Em Vigor, publicação 2026-01-22; a referência internacional ISO/IEC 27701:2025 é a 2ª edição. | Gestão de privacidade se porte, operações, clientes ou governança justificarem um sistema estruturado. | Papéis, inventário de tratamento, riscos, controles de privacidade, terceiros e ciclo de melhoria delimitados ao escopo escolhido. | Candidato; não adotado. |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html), edição publicada atual consultada: 2ª. | Organizar qualidade de produto e requisitos não funcionais para Cloud, Admin e produtos. | Requisitos mensuráveis por produto ligados a cenários, critérios de aceite e resultados de teste. | Referência candidata. |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html), página ISO consultada marca a edição como “to be revised” e registra revisão em desenvolvimento. | Estruturar engenharia de requisitos e rastreabilidade. | Requisito identificável, justificativa, fonte, critério verificável, dependências e ligações a issue/teste/evidência. | Candidato; verificar nova edição e adoção ABNT antes de fixar. |
| [ISO 9241-11:2018](https://www.iso.org/standard/63500.html), confirmada pela ISO em 2023; [ISO 9241-210:2019](https://www.iso.org/standard/77520.html), confirmada em 2025. | Usabilidade e design centrado no ser humano para jornadas de cada produto. | Tarefas e perfis representativos, eficácia/eficiência/satisfação avaliadas, achados e correções registrados. | Referências candidatas. |
| [WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/), Recomendação W3C, atualização publicada em 2024-12-12. | Critérios de acessibilidade para interface web; nível-alvo depende de contrato, jurisdição e decisão de produto. | Verificações automatizadas complementadas por teclado, foco, leitor de tela e inspeção de fluxos representativos; defeitos vinculados a critérios. | Base técnica candidata; alvo/nível ainda pendente. |
| [ISO/IEC 42001:2023](https://www.iso.org/standard/42001) e [ISO/IEC 23894:2023](https://www.iso.org/standard/77304.html). | Sistema de gestão e gestão de riscos de IA apenas se visão computacional/GANs avançarem além de discovery. | Caso de uso aprovado, inventário de dados/modelo, avaliação de risco e vieses, métricas representativas, supervisão e monitoramento. | Fora do compromisso de produção atual; reavaliar no gate de IA. |

Antes de selecionar qualquer referência, registrar o requisito de cliente/jurisdição ou objetivo interno, escopo, proprietário, custo/licença e versão oficial; mapear os requisitos aplicáveis a controles e evidências verificáveis. Uma matriz interna ou testes parciais não equivalem a certificação. Não anunciar alinhamento ou conformidade sem avaliação competente do escopo e evidência suficiente.

## Threat modeling e gates

Modelar ameaças por fluxo e ativo: tomada de conta, elevação de privilégio, cross-tenant, enumeração, exposição de arquivos, replay, falha de revogação, abuso de suporte, integrações/webhooks e prompt/data leakage no Jarvis. Associar mitigação e cenário de teste; escalar risco crítico antes do piloto.

Critérios mínimos: negação server-side por padrão; testes negativos entre espaços/produtos; mínimo privilégio; logs sem segredos e dados desnecessários; expiração/rotação; restauração e rollback comprováveis antes de qualquer expansão correspondente.
