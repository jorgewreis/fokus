# Referência de elegibilidade de classes SGT

Consulta realizada em 20/11/2026 ao [WebService público SGT](https://sgt.cloud.cnj.jus.br/api/v1/soap), indicado pelo próprio endpoint legado como seu sucessor. A operação `getDataUltimaVersao` respondeu `05/11/2026`. Nenhum SQL de origem foi executado.

## Dados observados

O método `getArrayDetalhesItemPublicoWS(codigo, "C")` fornece entre outros campos o código, pai, situação, flags de habilitação por ramo/grau (`just_es_1grau`, `just_es_2grau` e equivalentes), datas de inativação/reativação. `getArrayFilhosItemPublicoWS(codigo, "C")` retorna filhos diretos, situação e indicador de filhos; é necessário buscar os detalhes de cada classe para obter sua habilitação.

| Código e classe | Evidência SGT consultada | Uso permitido pelo sistema |
|---|---|---|
| 386 — Execução da Pena | Situação `A`, `just_es_1grau=S`, sem filhos. | Candidata a revisão; não habilitar automaticamente antes da revisão explícita de Jorge. |
| 1714 — Execução Provisória | Exportação estadual de 1º grau a lista; detalhe retornou `just_es_1grau=S`, situação `I`, inativação em 09/04/2026. | Bloquear seleção nova; preservar vínculos/processos históricos. |
| 406 | Situação `I` e possui filhos. | Não selecionar o nó inativo, mas percorrer sua árvore para não perder descendentes. |
| 385 — Processo Criminal | Nó raiz com filhos; detalhe informa `just_es_1grau=N`. | A flag negativa do pai não autoriza ignorar a árvore nem selecionar o próprio pai. |

A exportação [Justiça Estadual — 1º Grau](https://www.cnj.jus.br/sgt/versoes_tabelas/planilhas/85_Tabela_Classes_Justica_Estadual_1_Grau.xls) foi obtida e tem SHA-256 `8373985e033c940d32670228e82608fa0de94a37f53f4112ddbb384e8ec3bf05`. Embora use extensão `.xls`, seu conteúdo é HTML; a extração de árvore deve tratar a estrutura, não presumir um workbook Excel íntegro.

## Regra conservadora

- Não inferir elegibilidade pela presença na exportação, pelo código CNJ, pela classe pai ou pela existência de filhos.
- Uma nova escolha exige evidência da versão consultada, estado ativo, flag positiva do ramo/grau selecionado e revisão explícita de Jorge.
- Classes inativas não são elegíveis para novos Processos. Manter seus registros e classificações existentes.
- Percorrer descendentes mesmo quando um pai é inativo ou não habilitado no ramo/grau; armazenar estado e relação de cada nó.
- A FAQ oficial admite classe pai como último nível quando seus filhos não estão habilitados, mas não enumera todas as exceções nem resolve todos os efeitos de vigência. Se a estrutura permitir múltiplas interpretações, manter a classe em bloqueio até análise e revisão.
- Reativação de uma competência da Vara não reativa automaticamente vínculos de classe antigos; Jorge deve revisar e reativar cada vínculo, conforme a decisão registrada no [PRD](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a).

## Limites e próxima etapa

As respostas verificadas acima são amostras de contrato, não uma extração completa do catálogo. Os campos `dat_inicio_vigencia` e `dat_fim_vigencia` não apareceram nos detalhes testados, embora existam no dump SQL histórico. Ainda não foi validado se a combinação de flags, situação e datas é suficiente em todas as classes e exceções. Portanto `VerifiedSgtClassCatalog` continua fail-closed; nenhum código real é oferecido para seleção. Antes de ativar candidatos, obter e validar o snapshot completo, documentar a regra de vigência com evidência oficial e exibir a lista versionada para revisão de Jorge.

Fonte consultada em 20/11/2026: [WebService SGT sucessor](https://sgt.cloud.cnj.jus.br/api/v1/soap), [consulta pública de classes](https://www.cnj.jus.br/sgt/consulta_publica_classes.php) e [FAQ SGT](https://www.cnj.jus.br/sgt/visualizar_duvidas.php). Endpoint SOAP legado depreciado: [documentação WebService SGT](https://www.cnj.jus.br/sgt/infWebService.php).
