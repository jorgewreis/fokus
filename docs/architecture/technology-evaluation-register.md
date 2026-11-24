# Registro de avaliações tecnológicas do Fokus

Este registro define perguntas e gates; não seleciona nem instala componentes. Toda avaliação deve conter requisitos, alternativas, fonte/versão, custo operacional, risco, decisão, responsável e condição de revisão.

| Tema | Avaliação necessária | Default provisório / gate |
| --- | --- | --- |
| Arquitetura de aplicações | Requisitos de isolamento, escala, equipes, interfaces, deploy e falhas por produto. | Fronteiras por produto; monólito modular ou serviços independentes são decisões por ADR, sem converter todo produto em serviço por padrão. |
| API e webservices | Consumidores, autenticação, autorização, versionamento, compatibilidade, erros, limites e idempotência. | Contrato documentado e testável antes de integrar consumidores. |
| API Gateway | Necessidade de entrada única, políticas comuns, roteamento e observabilidade. | Não duplicar gateway se a infraestrutura atual atender; gateway não concentra domínio. |
| Processamento distribuído | Volumes, latência, disponibilidade, jobs demorados, duplicidade, ordenação e consistência. | Começar com chamada simples ou fila gerenciada disponível; distribuir apenas com caso demonstrado, idempotência e observabilidade. |
| Docker | Reprodutibilidade local/CI, isolamento, dependências e compatibilidade com hosting. | Usar containerização para ambiente de desenvolvimento/integração quando compatível com a stack do produto; não publicar portas sem revisão de rede. |
| Kubernetes | Número de serviços, necessidade de autoscaling, SLO, tolerância a falhas, skills, custos e capacidade de operar clusters. | Não adotar por antecipação; exigir ADR e prova de benefício operacional. |
| Branches | Frequência de releases, tamanho de equipe, manutenção de versões e capacidade de CI. | Trunk-based com branches curtas e integração frequente; GitFlow apenas se versões em paralelo e governança justificarem. Releases permanecem independentes por produto. |
| Versionamento | Consumidores, compatibilidade e cadência de cada app/pacote. | SemVer para componentes versionáveis, com changelog e artefato identificável; não versionar produtos como release acoplada sem justificativa. |
| Persistência | Propriedade do dado, tenancy, sigilo, isolamento, consistência, backup e recuperação. | Dono de dado por domínio; não compartilhar esquema/banco por conveniência antes de avaliar raio de falha e autorização. |
| Visão computacional/GANs | Uso, dados, direitos, qualidade, vieses, segurança, custo de GPU e critério de desempenho. | Discovery isolado; nenhuma produção até aprovação dos gates em `docs/ai/research-gates.md`. |
| Normas | Clientes, contratos, jurisdição, setor, certificações exigidas e controles aplicáveis. | Confirmar edição em fontes oficiais e mapear aplicabilidade; não anunciar conformidade sem auditoria apropriada. |

## Registro de cada decisão

Manter ADRs em `docs/adr/` com estado (proposta, aceita, substituída), contexto, alternativas, decisão, consequências, evidências, responsável, data real e gatilho de revisão. Decisão pendente deve ter issue ligada e não ser tratada como arquitetura aprovada.
