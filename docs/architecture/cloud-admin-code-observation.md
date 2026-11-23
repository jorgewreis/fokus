# Observação arquitetural do Cloud e Admin

**Fonte:** inspeção estática do repositório público `jorgewreis/fokus-cloud`, branch `main`, revisão `5a34b4dcf0caf256126b4495f43c981bf3cc609d`, em 2026-11-23. Nenhum código foi executado; não houve acesso a produção, a dados de clientes ou a configurações privadas.

## O que o código permite afirmar

- O portal, o backoffice administrativo e módulos de produto aparecem na mesma aplicação Laravel observada.
- A implementação usa contextos de autenticação e autorização distintos para clientes e administradores da plataforma.
- Existem controles de associação a empresa/espaço e permissões de produto no código consultado.

Esses fatos descrevem a estrutura daquela revisão. Não determinam a arquitetura-alvo, não comprovam deploy, armazenamento separado, isolamento efetivo, nem aceitação de fluxos reais.

## Critérios de aceite para suporte e isolamento

A política aprovada para o piloto limita o suporte a dados comerciais e técnicos; conteúdo operacional de clientes permanece inacessível. Antes de ampliar o uso, a equipe deve demonstrar em testes server-side isolados que:

1. somente usuários e vínculos autorizados iniciam uma sessão de suporte;
2. a sessão é encerrada ao sair, expirar ou perder autorização;
3. suporte não consegue ler nem alterar conteúdo operacional de Law;
4. suporte não atravessa empresa, espaço ou produto;
5. tentativas negadas não deixam mutações ou efeitos laterais;
6. auditoria registra os eventos necessários sem incluir conteúdo operacional.

Cobrir estados permitido/negado, expiração, revogação, falha parcial e ausência de efeitos colaterais com fixtures sintéticas. Se qualquer verificação não for possível, manter o gate pendente e registrar a limitação; não inferir isolamento pela presença de middleware ou por um teste de outro produto.

## Próximas decisões arquiteturais

- Definir fronteiras de domínio entre Cloud, Admin, Law e Lead, com donos, contratos e releases independentes.
- Registrar em ADR se Admin é módulo da plataforma ou aplicação/release própria, com critérios de operação e reversão.
- Versionar contratos de identidade, empresa/espaço, autorização, suporte e auditoria antes de integrar consumidores.
- Atualizar esta observação quando o SHA de referência mudar; confirmar runtime e fluxos em ambiente isolado antes de declarar aceite.

Esta página é um resumo arquitetural público, não um relatório de auditoria de segurança ou autorização para acesso a sistemas. O detalhamento interno de verificação e a execução das issues permanecem nas ferramentas privadas do projeto.
