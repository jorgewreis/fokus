# Qualidade, critérios de aceite e evidências

## Rastreabilidade mínima

| Artefato | Evidência de aprovação | Condição de reprovação |
| --- | --- | --- |
| Requisito | ID, origem, prioridade, critério observável e dependências. | Critério ambíguo, sem origem ou sem forma de verificar. |
| Arquitetura/API | Donos, fronteiras, fluxos de dados, contrato e decisão revisável. | Integração implícita, acesso direto indevido ou tecnologia presumida. |
| Código | Revisão, CI aplicável, testes e diff ligado ao requisito. | CI/teste relevante falhou ou mudança sem rastreabilidade. |
| Segurança/privacidade | Cenários positivos e negativos, riscos e controles efetivamente observados. | Exposição cross-tenant, privilégio indevido ou alegação sem prova. |
| UX | Inspeção de jornada, responsividade, acessibilidade e estados de erro/vazio. | Fluxo principal inutilizável ou critério visual sem evidência. |
| Aceite manual | Perfil, ambiente seguro, passos, massa sintética, resultado e evidência. | Critério crítico não percorrido, dados não autorizados ou resultado não reproduzível. |
| Release/operação | Artefato identificado, promoção/rollback e sinais de saúde verificáveis. | Origem/versão incerta ou rollback apenas presumido. |

## Matriz de testes a definir por produto

- Unitários: regras de domínio e validações isoladas.
- Integração: banco, autenticação, armazenamento, filas e serviços realmente usados.
- Contrato: API, webservice e dependências entre consumidores/produtores.
- Ponta a ponta: fluxos críticos, autorização por produto/espaço e revogação.
- Suporte administrativo: para qualquer modo assistido, cobrir em servidor leitura e mutação de dados operacionais, escopo por produto/tenant, encerramento, expiração e revogação; o aceite precisa comprovar ausência de acesso/efeitos vedados.
- UX/acessibilidade: teclado, foco, semântica, contraste conforme critério aplicável, zoom e breakpoints acordados.
- Resiliência: timeout, retry, idempotência, indisponibilidade, backup/restore e rollback quando previstos.

Frameworks, cobertura numérica e comandos só serão documentados após conferência da stack e CI do produto. Não presumir cobertura ou execução de testes a partir deste plano.

## Gate de aceite

1. Critérios da issue satisfeitos e evidência anexada/linkada.
2. Testes e inspeções pertinentes concluídos; falhas e limitações declaradas.
3. Nenhum bloqueador conhecido de segurança, acesso, privacidade ou integridade permanece sem decisão explícita.
4. Documentação atualizada e versão/ambiente identificados.
5. Rollback e suporte proporcionais à mudança foram planejados e verificados.

O status só deve avançar conforme evidências reais. A existência deste documento não constitui aceite de qualquer aplicação.
