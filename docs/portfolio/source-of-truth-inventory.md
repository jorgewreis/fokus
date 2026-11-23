# Inventário público do portfólio

**Escopo:** visão de alto nível dos produtos e fontes documentais, não inventário operacional. Verificado em 2026-11-23 por leitura de documentação e metadados públicos. Não inclui dados de infraestrutura privada, worktrees, hosts, identificadores de serviços, credenciais ou links de backlog interno.

| Produto | Fonte pública ou situação descrita | Limite conhecido | Próxima prova necessária |
| --- | --- | --- | --- |
| Fokus (repositório central) | [jorgewreis/fokus](https://github.com/jorgewreis/fokus) é a fonte central pretendida para documentação e os produtos comerciais. | A existência de código não prova que ele esteja em uso ou publicado. | Revisar documentos e código no SHA atual antes de integrar ou liberar cada produto. |
| Fokus Cloud | [jorgewreis/fokus-cloud](https://github.com/jorgewreis/fokus-cloud) contém a plataforma, portal e serviços compartilhados descritos no código e na documentação. | Implementação observada não comprova comportamento em runtime, isolamento de dados ou estado de produção. | Confirmar contratos, ambiente/revisão servida e gates de segurança antes de ampliar o uso. |
| Admin | A documentação e o código observado situam o backoffice administrativo junto à plataforma Cloud. | Fronteira lógica observada não decide se Admin terá aplicação ou release independente. | Registrar decisão de domínio, acesso, operação e release em ADR. |
| Law Advocacia | A documentação do Cloud descreve módulos jurídicos comerciais e integração futura ao portal. | Estado de homologação, aplicação de referência e fluxo comercial precisam ser reconciliados. | Demonstrar o fluxo do piloto com permissões e dados sintéticos antes da integração. |
| Lead | Há documentação de produto e interfaces descritas junto ao Cloud, além de especificação em repositório privado. | Fonte canônica, migrations executáveis, runtime e fluxo de lead individual ainda precisam de confirmação. | Demonstrar cadastro e acompanhamento individual com fixtures sintéticas; integrar ao portal somente após os gates do piloto Law. |
| Styles | [jorgewreis/fokus-styles](https://github.com/jorgewreis/fokus-styles) é a fonte visual existente, com pacote público próprio. | Publicação do pacote não prova incorporação ou compatibilidade de produção no repositório central. | Revisar a importação e os contratos de consumo antes da integração. |
| Jarvis | Produto associado a repositório privado próprio. | Esta cópia pública não descreve runtime, dados, agentes ou autonomia internos. | Inventariar e aprovar interfaces, isolamento e limites antes de qualquer integração. |
| Law on demand — 1ª Vara | A aplicação institucional ainda aparece em `apps/law/` neste repositório. A reconciliação técnica compara a árvore Laravel sintética com as linhas institucionais descritas nas fontes privadas. | O estado desejado aprovado é mantê-la fora do repositório central. Seu destino canônico e a revisão que atende usuários ainda não estão confirmados; nenhuma transferência de histórico foi ensaiada. | Seguir [reconciliação de origem e destino](../architecture/law-on-demand-repository-reconciliation.md); confirmar origem, destino compatível, consumidores, histórico, dependências e reversão antes de qualquer movimento. |

## Snapshot de fontes públicas · 2026-11-23

Leitura somente de metadados, README e arquivos declarativos nas branches padrão; não inclui execução de código, dados, serviços ou ambientes:

| Fonte | Revisão observada | Evidência documental/código | Lacuna que impede conclusão |
| --- | --- | --- | --- |
| [Repositório central](https://github.com/jorgewreis/fokus/tree/010ff6087c355c2cd6abdf86733636717d91291f) | `main` · `010ff608` | A raiz contém `apps/` e `docs/`; o README navega para `apps/law/` e identifica o produto como Fokus Law. | O README aponta para o PRD da 1ª Vara. Esta revisão antecede o PR #31 e não materializa a fronteira aprovada de exclusão. |
| [Fokus Cloud](https://github.com/jorgewreis/fokus-cloud/tree/5a34b4dcf0caf256126b4495f43c981bf3cc609d) | `main` · `5a34b4d` | A raiz contém uma aplicação Laravel, rotas, documentação e testes. O README descreve a reconstrução como não homologada e não publicada. | Código e declarações do README não identificam a revisão efetivamente servida; outras afirmações do site/README precisam de reconciliação. |
| [Fokus Styles](https://github.com/jorgewreis/fokus-styles/tree/9f34bdbe6fa41ee29dc6edc36d9452b82d2e7ac2) | `main` · `9f34bdb` | `package.json` declara `3.0.0`; o README ainda declara status `2.7.0` e versão 3.0.0 “em preparação”. Consulta ao npm em 23/11/2026 confirma `latest` 3.0.0, publicada em 22/11/2026. | A resposta do registro não fornece `gitHead`; a relação entre tarball e SHA e a adoção/compatibilidade pelo Cloud continuam sem prova. Corrigir o README na fonte Styles e verificar o pacote consumido antes de afirmar adoção. |

O snapshot não altera a decisão de portfólio. O PR #31 está aberto em Draft; por isso, `main` ainda não contém a correção documental submetida sobre a fronteira do Law on demand. Há mais de uma linha privada relacionada à aplicação institucional nos registros consultados, mas nenhuma foi eleita aqui como canônica e nenhum destino de migração foi aprovado. Os detalhes internos ficam no Notion/Linear.

Para Lead e Jarvis, a conferência de repositórios privados confirma material documental e provas existentes, mas não é adequada para publicação de identificadores ou detalhes internos. Os registros privados vinculados no Notion/Linear devem sustentar a próxima revisão deste inventário; presença de documentação ou PoC não prova runtime ou prontidão.

## Critério de leitura

- “Descrito” significa que uma fonte documental afirma a capacidade; não prova implementação.
- “Presente no código” significa somente que arquivos ou rotas existem em uma revisão identificada; não prova que foram executados, aceitos ou publicados.
- “Publicado” requer evidência do artefato/revisão servida e do fluxo correspondente; não inferir a partir de branch, pacote ou workflow configurado.
- O inventário interno detalhado e os registros de trabalho ficam nos espaços privados do projeto. Atualizar esta visão pública somente quando houver evidência verificável e apropriada para publicação.
