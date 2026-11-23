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
| Law on demand — 1ª Vara | A aplicação institucional ainda aparece em `apps/law/` neste repositório. | O estado desejado aprovado é mantê-la fora do repositório central. Seu destino canônico e a revisão que atende usuários ainda não estão confirmados. | Definir origem, destino compatível, consumidores, histórico, dependências e reversão antes de qualquer movimento. |

## Critério de leitura

- “Descrito” significa que uma fonte documental afirma a capacidade; não prova implementação.
- “Presente no código” significa somente que arquivos ou rotas existem em uma revisão identificada; não prova que foram executados, aceitos ou publicados.
- “Publicado” requer evidência do artefato/revisão servida e do fluxo correspondente; não inferir a partir de branch, pacote ou workflow configurado.
- O inventário interno detalhado e os registros de trabalho ficam nos espaços privados do projeto. Atualizar esta visão pública somente quando houver evidência verificável e apropriada para publicação.
