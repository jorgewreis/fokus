# SGT: tentativa de levantamento das classes em 20/11/2026

## Resultado

**Incompleto; não usar como catálogo nem para habilitar classes.** A consulta à API pública retornou HTTP 429 durante a obtenção dos detalhes individuais. As chamadas foram interrompidas. A versão não foi novamente conferida ao final da tentativa, e os detalhes de todos os itens não foram preservados nem validados.

## Fontes e evidências

- API SOAP sucessora: <https://sgt.cloud.cnj.jus.br/api/v1/soap>. `getDataUltimaVersao` retornou `05/11/2026` no início.
- [Página de versões do SGT](https://www.cnj.jus.br/sgt/versoes.php?tipo_tabela=C), com exportações e versão indicada pelo CNJ.
- [Dump de dados publicado pelo SGT](https://www.cnj.jus.br/sgt/enviarArquivo.php?url=85_dump_dados.sql&nome=dump_dados.sql): 35.189.650 bytes; SHA-256 `45a1e0750a3cf4ce330e1569d14ae869c356f818a2d2b625e86b9a18975111a5`. O arquivo foi lido como texto para comparação de identificadores, sem executar seu SQL.
- [Dump de estrutura](https://www.cnj.jus.br/sgt/enviarArquivo.php?url=85_dump_estrutura.sql&nome=dump_estrutura.sql): 18.434 bytes; SHA-256 `f39940d8165d178d3af07f2f5abaf70702b0e9b9c0e873d0c7d5377838b92fec`. Não executar o SQL da fonte na base da aplicação.

Na leitura dos itens de tipo `C` do dump foram identificados 849 códigos distintos, incluindo 10 raízes. O percurso SOAP das dez raízes retornou 849 nós distintos e o conjunto de códigos coincidiu com o extraído do dump; as relações pai informadas nas respostas foram verificadas durante o percurso. Isso não comprova os detalhes individuais ou a elegibilidade de cada classe. O dump também contém 842 inserções na tabela `classes`; a diferença em relação aos itens não foi esclarecida.

O endpoint limitou a consulta dos detalhes com HTTP 429. A tentativa não produziu um arquivo completo de detalhes nem confirmação da versão ao final. A contagem e a comparação acima são evidência do percurso observado, não validação integral de catálogo ou de integridade dos atributos.

## Regras e pendências

- O SGT informa habilitação por ramo e grau e situação; a planilha por ramo/grau, isoladamente, não comprova que uma classe esteja ativa. Por exemplo, a classe 1714 constava na planilha estadual de primeiro grau, mas os detalhes SOAP retornaram situação `I` e inativação em 09/04/2026.
- A [FAQ do SGT](https://www.cnj.jus.br/sgt/visualizar_duvidas.php) admite que um pai habilitado seja considerado último nível para o ramo/grau quando seus filhos não estão habilitados. O trecho consultado não resolve todos os efeitos de inativação, vigência, descendentes indiretos e exceções específicas.
- Antes de propor classes a Jorge, obter os detalhes de todos os códigos com política respeitosa aos limites do serviço, verificar a versão antes e depois, validar campos e relações e documentar lacunas e exceções. Nenhuma classe torna-se selecionável por esta investigação.
