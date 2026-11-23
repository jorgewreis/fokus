# Práticas de engenharia e contratos

## Requisitos e rastreabilidade

- Atribuir identificador estável a requisito funcional e não funcional; descrever contexto, prioridade, origem, critério observável, dependências e evidência esperada.
- Separar necessidade confirmada, hipótese, decisão e solução técnica. Não transformar tecnologias citadas em requisito de produto sem aprovação.
- Relacionar cada requisito com issue, documentação, teste/inspeção e decisão. Requisitos fora de escopo permanecem registrados com justificativa.

## Código e arquitetura

- Manter responsabilidade coesa por módulo/serviço e limites explícitos (SRP). Preferir nomes e fluxos explícitos; evitar abstração sem repetição ou variação que a justifique.
- Validar as regras no servidor e na fronteira do domínio; interface não é controle de acesso.
- Evitar dependência entre domínios via banco ou tabelas internas. Publicar interface interna ou contrato versionado quando a integração entre aplicações for necessária.
- Revisão de código deve apontar comportamento, risco, testabilidade, compatibilidade e critérios de aceite; não impor refatoração sem relação com objetivo.

## API e webservices

Para cada interface registrar consumidor/produtor, versão, autenticação e autorização, dados, schema, validação, erros, idempotência, timeouts, limites, retries, logs permitidos e política de descontinuação. Testes de contrato devem verificar compatibilidade producer/consumer com exemplos seguros e sintéticos.

## Testes e aceitação

Aplicar pirâmide proporcional ao risco: unitários para regras isoladas; integração para persistência/serviços; contrato para interfaces; ponta a ponta para jornadas essenciais. Acrescentar casos negativos de autorização, tenancy, replay, duplicidade, concorrência, falha de dependência e recuperação conforme o produto.

Manuais de aceitação descrevem pré-condições, perfil e permissões, massa sintética, passos, resultado esperado, evidência, critérios de bloqueio e limpeza. Não usar execução manual como substituto permanente para controles automatizados repetíveis.

## Git e releases

- Estratégia padrão proposta: branch curta, PR pequeno, CI obrigatório e `main` integrável continuamente; nenhum branch de longa duração sem razão registrada.
- Cada produto e biblioteca tem versão/artefato rastreável, changelog e fluxo independente de promoção e rollback.
- Proteções, credenciais, checks, release e deploy devem ser conferidos no estado real antes de depender deles. Este documento não habilita promoção ou deploy.
