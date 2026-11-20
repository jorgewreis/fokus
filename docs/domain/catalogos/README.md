# Referência de competências do MPM

O arquivo [cnj-mpm-competencias-2025-04.csv](cnj-mpm-competencias-2025-04.csv) reproduz as colunas `seq_competencia` e `dsc_competencia` da aba `Competencias juízo` da [planilha de tabelas auxiliares MPM do CNJ](https://www.cnj.jus.br/wp-content/uploads/2025/04/tabelas-auxiliares-mpm.xlsx), obtida em 20/11/2026. Contém 39 registros com códigos distintos, incluindo `999` (Não se aplica).

- SHA-256 do XLSX obtido: `db5dc957af531bea815236d4b19e099406fcbe0f7438794c38899206658afd99`.
- O caminho da fonte contém `2025/04`; isso não demonstra uma versão oficial nem que a lista permaneça vigente. Metadados internos da planilha não informam versão.
- CSV preserva códigos e descrições da aba, na mesma ordem; o nome do arquivo identifica o caminho de publicação, não uma versão semântica.
- A tabela é uma referência de vocabulário; não identifica as competências atribuídas à Vara, nem mapeia classes SGT, nem concede acesso. A configuração e os grants exigem as decisões e controles do PRD.
- Antes de usar em configuração operacional, conferir fonte vigente, política de atualização e tratamento de códigos retirados; não atribuir automaticamente o código `999`.

## Classes SGT

- A versão observada na API oficial sucessora em 20/11/2026 foi `05/11/2026`; a leitura completa dos detalhes foi limitada por HTTP 429 e interrompida.
- A tentativa recuperou 849 nós e comparou seus códigos com o dump, mas não comprovou os atributos de todos os nós nem explicou a diferença entre 849 itens e 842 linhas `classes`.
- Não existe lista importada nem classe aprovada para seleção; a implementação mantém fail-closed até coletar detalhes completos e Jorge revisar os candidatos.
- Evidências, amostras, hashes e regras conservadoras: [relatório de completude](sgt-relatorio-completude-2026-11-20.md) e [referência de classes](../referencia-sgt-classes.md).

Rastreamento: [REI-232](https://linear.app/reis-developer/issue/REI-232/vara-definir-competencia-e-escopo-de-acesso-a-processos-sinteticos).
