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

## Threat modeling e gates

Modelar ameaças por fluxo e ativo: tomada de conta, elevação de privilégio, cross-tenant, enumeração, exposição de arquivos, replay, falha de revogação, abuso de suporte, integrações/webhooks e prompt/data leakage no Jarvis. Associar mitigação e cenário de teste; escalar risco crítico antes do piloto.

Critérios mínimos: negação server-side por padrão; testes negativos entre espaços/produtos; mínimo privilégio; logs sem segredos e dados desnecessários; expiração/rotação; restauração e rollback comprováveis antes de qualquer expansão correspondente.
