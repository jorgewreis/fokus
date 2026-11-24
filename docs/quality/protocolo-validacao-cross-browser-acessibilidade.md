# Protocolo de validação cross-browser e acessibilidade

**Estado:** protocolo reutilizável; nenhuma execução, conformidade ou compatibilidade é declarada.
**Fontes:** [PRD canônico](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a), §§8.1 e 9; [REI-205](https://linear.app/reis-developer/issue/REI-205); [REI-221](https://linear.app/reis-developer/issue/REI-221).

## 1. Plataformas exigidas

Em cada execução, registre as versões estáveis observadas naquele dia; não fixe versões neste protocolo.

| Plataforma | Navegador/dispositivo |
|---|---|
| Desktop | Chrome em computador |
| Desktop | Edge em computador |
| Mobile | Chrome em Android |
| Mobile | Safari em iPhone |

## 2. Fluxos críticos e evidências

Execute cada fluxo em todas as combinações acima, registrando separado o resultado automatizado e a revisão manual:

| Fluxo | Casos mínimos |
|---|---|
| Login e TOTP | Campos e erros de autenticação, navegação por teclado e leitura/estado dos controles. Não usar dados ou segredos reais. |
| Pessoa → Processo | Estados vazios, sucesso, validação, duplicidade acessível, vínculo tipado, falha de CEP e negação sem revelar registro fora do escopo. |
| Consulta de auditoria | Consulta autorizada, resultado vazio, resultado disponível e negação de acesso sem ampliar exposição. Usar apenas dados sintéticos. |

Para cada fluxo:

- **Automação:** executar verificações automatizadas pertinentes à interface e anexar relatório, ambiente e commit. Falha ou execução ausente fica explícita.
- **Teclado e leitor de tela:** revisão manual com tecnologia assistiva registrada; percorrer controles, rótulo/função/estado, foco e mensagens. Anotar passos e resultado.
- **Contraste:** alvo mínimo aprovado pelo PRD: **WCAG 2.2 AA**. Registrar ferramenta/método, componentes avaliados, valores, falhas e limitações. O protocolo não declara conformidade antecipada.
- **Browser/device:** testar o fluxo e os resultados no ambiente correspondente, sem inferir compatibilidade a partir de outra combinação ou somente da CI.

## 3. Modelo obrigatório de evidência

Preencher para cada combinação × fluxo:

```text
Data e horário:
Commit revisado:
Navegador e versão observados:
Sistema/dispositivo e versão:
Fluxo e passo:
Requisito/estado da fonte:
Automação executada e resultado/evidência:
Revisão manual de teclado e resultado:
Leitor de tela/tecnologia assistiva e resultado:
Contraste WCAG 2.2 AA: método, elementos e resultados:
Resultado geral: passou | falhou | não executado
Reprodução/evidência sintética:
Limitações/pontos pendentes:
Responsável pela execução:
```

Registre cada dimensão como passou, falhou ou não executado; não converta cobertura parcial em compatibilidade, conformidade ou homologação institucional. Não incluir dados pessoais ou segredos. Anexar os resultados à REI-205 para aceite.

## 4. Limites

Gestão de Expedições é fase futura e não integra o percurso MVP. Mensagens/copy e estados sem decisão aprovada permanecem pendentes. Este protocolo não é evidência de execução, implementação ou homologação.