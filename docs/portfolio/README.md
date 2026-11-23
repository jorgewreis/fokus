# Portfólio Fokus

**Estado:** direção de portfólio registrada em 2026-11-23; inventário e implementação ainda precisam ser reconciliados por produto.

## Limites confirmados

O repositório corporativo `jorgewreis/fokus` é a fonte central planejada para código, documentação técnica e páginas de Fokus Cloud, Admin, Law comercial, Lead, Styles e Jarvis. O Fokus Law on demand da 1ª Vara Crime de Ilhéus é uma aplicação personalizada e fica fora deste repositório, com código, dados, identidade, autorização, ambiente e operação próprios.

O checkout atual ainda contém `apps/law/`, cuja documentação e ADR descrevem o MVP sintético da 1ª Vara. A consulta somente leitura identificou um repositório privado relacionado à Vara, mas não confirmou que ele seja a fonte canônica da revisão atual nem que seja destino adequado para a aplicação Laravel de `apps/law/`. A localização canônica e a separação segura desse aplicativo ainda não estão concluídas. Não mover nem remover essa árvore até confirmar repositório de destino, histórico, processo de publicação, dependências e reversão.

## Produtos e responsabilidades

| Produto | Papel no portfólio | Situação/condição conhecida |
| --- | --- | --- |
| Fokus Cloud | Portal comercial, catálogo público e área de clientes | Prioridade de integração; reúne portal e acesso a produtos comerciais. |
| Fokus Admin | Backoffice administrativo da Fokus e controles operacionais | Escopo deve distinguir administração da plataforma, suporte e administração do espaço do cliente. |
| Fokus Law | Produto jurídico comercial | Confirmar fonte e versão de referência; vínculo pelo login existente no piloto, sem cópia de contatos/processos. |
| Fokus Lead | Produto imobiliário | Discovery pode avançar; integração ao portal depende dos gates registrados para o piloto do Law Advocacia e prova de lead individual. |
| Fokus Styles | Framework visual compartilhado | Base visual dos novos produtos comerciais; novo componente começa no catálogo privado e requer aprovação para publicação. |
| Jarvis | Produto de agentes e interface de assistência Fokus | Inventariar o repositório e a execução atuais; manter dados, permissões e autonomia delimitados. |
| Law on demand — 1ª Vara | Aplicação jurídica institucional personalizada | Excluída do monorepo central; operação e autorização independentes. |

Esses papéis refletem decisões e registros acessíveis, mas não certificam versão implantada, prontidão, integração ou uso atual.

## Ordem de trabalho

1. Reconciliar inventários, fontes oficiais, limites e issues existentes.
2. Definir arquitetura, contratos, documentação e releases independentes.
3. Preparar Cloud/Admin e validar a experiência comercial com o Law Advocacia.
4. Evoluir Styles como fundação visual e preparar Lead em paralelo, respeitando seu gate de integração.
5. Inventariar e planejar a inclusão de Jarvis sem assumir integração automática.
6. Manter o Law on demand em trilha própria e pesquisar visão computacional/GANs somente por discovery com gates.

Não há cronograma aprovado neste documento. A ordem não autoriza migração, publicação, uso de dados reais, integração externa ou campanha.

## Fontes de registro

- **GitHub:** código, documentação técnica versionada, decisões técnicas e evidências reproduzíveis.
- **Linear:** issues, estado, responsáveis, dependências, datas de execução e aceite.
- **Notion:** decisões de portfólio, contexto estratégico e registros de produto, com referências aos artefatos técnicos e issues.

Quando houver conflito, preservar o histórico, registrar a decisão com fonte e data e atualizar as referências relacionadas. Não duplicar a mesma especificação integral em ferramentas distintas.

## Documentos relacionados

- [Arquitetura conceitual do portfólio](../architecture/portfolio-architecture.md)
- [Observação estática de arquitetura — Cloud e Admin](../architecture/cloud-admin-code-observation.md)
- [Inventário de fontes por produto](source-of-truth-inventory.md)
- [Roteiro de implementação](roadmap.md)
- [Backlog preparado para triagem](issue-backlog-plan.md)
- [Avaliações de tecnologia](../architecture/technology-evaluation-register.md)
- [Práticas de engenharia e contratos](../engineering/engineering-practices.md)
- [Critérios de qualidade e aceitação](../quality/acceptance-and-evidence.md)
- [Segurança, privacidade e normas](../security/portfolio-security-privacy.md)
- [Discovery, marketing e vendas](../product/portfolio-discovery.md)
- [Discovery de visão computacional e GANs](../ai/research-gates.md)

## Evidência e limitações

Em 2026-11-23, o checkout estava em `main`, 39 commits atrás de `origin/main`, com `README.md` modificado e diretórios locais não rastreados. Esses itens foram preservados. O README e ADR presentes nesta revisão identificam `apps/law/` como Fokus Law da 1ª Vara; esta constatação não prova que o checkout local represente o último estado remoto.

Fontes consultadas: Plano Diretor e Governança 2027 no Notion; inventário técnico Cloud; inventário do Lead (REI-190); decisão do Law 1ª Vara (PRD e ADR-0001); Issues REI-191, REI-193, REI-189, REI-190, REI-272 e REI-166. Fontes dinâmicas e revisões remotas devem ser revalidadas antes da execução de migrações ou releases.
