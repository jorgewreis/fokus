# Protocolo de validação cross-browser e acessibilidade

**Estado:** protocolo reutilizável; nenhuma execução ou compatibilidade é declarada.
**Fonte:** [PRD canônico](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a), §9; [REI-205](https://linear.app/reis-developer/issue/REI-205/vara-validar-percurso-sintetico-e-aceite-interno-do-mvp); [REI-221](https://linear.app/reis-developer/issue/REI-221/vara-definir-protocolo-de-validacao-cross-browser-e-acessibilidade).

## 1. Combinações exigidas

Em cada execução, registre versões estáveis observadas naquele dia; não fixe versões neste protocolo.

| Plataforma | Navegador/dispositivo | Fluxos a percorrer |
|---|---|---|
| Desktop | Chrome, computador | Cadastro/consulta de Pessoa; cadastro/consulta de Processo por CNJ; vínculo tipado Pessoa–Processo. |
| Desktop | Edge, computador | Cadastro/consulta de Pessoa; cadastro/consulta de Processo por CNJ; vínculo tipado Pessoa–Processo. |
| Mobile | Chrome, Android | Cadastro/consulta de Pessoa; cadastro/consulta de Processo por CNJ; vínculo tipado Pessoa–Processo. |
| Mobile | Safari, iPhone | Cadastro/consulta de Pessoa; cadastro/consulta de Processo por CNJ; vínculo tipado Pessoa–Processo. |

## 2. Verificações por combinação

Para cada fluxo, registrar resultado separado para:

- Estado vazio, carregamento quando aplicável, sucesso e validação de campos.
- Duplicidade acessível e negação de acesso; a negação não pode confirmar nem revelar registros fora do escopo.
- Falha/ausência de resposta do serviço de CEP: preenchimento manual permitido conforme PRD.
- Teclado: navegar, acionar e sair de controles sem depender do ponteiro; registrar foco e bloqueios.
- Leitor de tela: nome/função/estado dos controles e mensagens de validação ou resultado são anunciados no contexto correto.
- Contraste: registrar elementos e ferramenta/medição observados, valores e limitações. O protocolo não escolhe nível normativo ou declara conformidade automática.

Expedições não fazem parte do percurso MVP. Requisitos sem comportamento/copy aprovados ficam anotados como pendentes, sem criar mensagens de produto por inferência.

## 3. Modelo obrigatório de evidência

Uma execução deve preencher todos os campos:

```text
Data e horário:
Commit revisado:
Navegador e versão observados:
Sistema/dispositivo e versão:
Fluxo e passo:
Requisito/estado da fonte:
Resultado: passou | falhou | não executado
Evidência/reprodução:
Verificação teclado:
Verificação leitor de tela e tecnologia assistiva:
Contraste medido e método:
Limitações/pontos pendentes:
Responsável pela execução:
```

Anexar apenas evidência sintética, sem dados pessoais ou segredos. Distinguir planejado, executado e falhou. Não converter execução parcial em declaração de compatibilidade ou homologação institucional. Para aceite do MVP, anexar matriz preenchida à REI-205.

## 4. Limites

A matriz deve refletir o fluxo atual Pessoa → Processo. Não incluir Expedições, dados reais, PJe ou integração institucional. Os resultados dependem da execução com as versões registradas e não são inferidos a partir de CI, navegador de desenvolvimento ou leitura deste protocolo.