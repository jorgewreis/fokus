# ADR-001: Arquitetura Greenfield do Fokus Law — 1ª Vara Crime de Ilhéus

- **Estado:** Aceito para as decisões explicitamente aprovadas; controles operacionais listados ao final permanecem pendentes de comprovação.
- **Data:** 2026-11-19
- **Issue:** [REI-195 — Definir arquitetura Greenfield e fronteiras dos ambientes](https://linear.app/reis-developer/issue/REI-195/vara-definir-arquitetura-greenfield-e-fronteiras-dos-ambientes)
- **Requisitos:** [PRD aprovado](https://app.notion.com/p/41b6af4c510981e0b980eff10759823a), especialmente seções 1, 7, 8 e 10.

## Contexto

O Fokus Law é uma solução institucional exclusiva da 1ª Vara Crime de Ilhéus, desenvolvida em Greenfield no repositório Fokus. A implantação inicial é sintética. Não há migração automática de código ou dados legados, integração com PJe, uso de dados reais ou homologação institucional nesta etapa.

A aplicação deve suportar o percurso sintético Pessoa → Processo → Expedição e preservar separação por módulos. A stack-base foi aprovada pelo desenvolvedor na REI-195. A aprovação da arquitetura não comprova que hospedagem, isolamento, autenticação, backup ou recuperação estejam configurados.

## Decisão

1. **Forma da aplicação:** monólito modular com interface renderizada no servidor em Blade.
2. **Stack-base:** Laravel 13, PHP 8.5 e MySQL 8.4 LTS com InnoDB. Confirmar o patch exato e a compatibilidade efetiva dos runtimes antes de configurar ambientes.
3. **Módulos de domínio:** Pessoas, Usuários, Processos, Expedições e Sistema. A existência de diretórios no scaffold não significa que os módulos ou seus contratos estejam implementados.
4. **Fontes e dados:** o MVP recebe manualmente o número CNJ e cria registro local quando necessário. PJe permanece fonte oficial dos atos nele praticados; importação e integração ficam fora desta entrega. A unicidade do CNJ é por unidade. Usar somente dados sintéticos nesta fase.
5. **Autenticação e autorização:** autenticação local com MFA/TOTP e autorização aplicada no servidor, negada por padrão e delimitada por módulo, ações, unidade e sigilo. Convite, login ou TOTP isoladamente não concedem acesso. No ambiente sintético, autocadastro pede apenas nome de exibição e e-mail comum confirmado; a solicitação permanece sem acesso até decisão explícita de Jorge. Suporte técnico não recebe automaticamente poderes de aprovação ou concessão.
6. **Ambientes:** a hospedagem informada para validação sintética é Hostinger VPS KVM1 com Ubuntu 24.04, CloudPanel e Cloudflare. A co-hospedagem lógica do ambiente sintético com outros serviços no KVM1 só pode ser ativada após aprovação do desenvolvedor e comprovação dos controles da seção 10.1 do PRD. Isso não é isolamento de infraestrutura e não autoriza dados reais nem produção do Fokus.
7. **Backup e recuperação sintéticos:** planejar cópia mensal no primeiro sábado, em horário a definir após medir carga e coordenar o PC de destino. Limitar o pacote ao banco sintético, arquivos próprios necessários e identificação imutável do commit e versão das migrations. Criptografar antes da transferência; o PC inicia a conexão SFTP para baixar o pacote ao destino aprovado. Manter três cópias mensais, sem apagar cópias válidas se faltar espaço. Testar restauração em Docker no PC separado após validar capacidade. Isso ainda não está configurado nem validado.

## Alternativas consideradas

| Opção | Vantagens registradas | Custos ou limites |
| --- | --- | --- |
| **Laravel 13 + PHP 8.5 + MySQL 8.4/InnoDB, monólito modular e Blade (escolhida)** | Alinha-se ao ecossistema Fokus Cloud e evita separar frontend e API para este MVP. | Requer comprovar compatibilidade e fronteiras na hospedagem; decisão não autoriza reutilizar código legado. |
| Django 5.2 LTS + PostgreSQL | Oferece autenticação, grupos e permissões integrados. | Introduz outro ecossistema e exige integração adicional de MFA. |
| Separar SPA e API | Foi considerada como alternativa de composição. | Não traz benefício necessário ao fluxo do MVP com um único desenvolvedor e aumenta as partes operacionais. |

## Consequências

- O produto mantém uma única aplicação e banco relacional na stack aprovada, com limites de domínio a serem implementados e revisados.
- Persistem riscos de co-hospedagem, recursos compartilhados, acesso administrativo e recuperação enquanto os controles não forem demonstrados.
- Qualquer reutilização de código ou dados legados, integração com PJe, uso de dados reais, homologação institucional ou produção exige escopo e autorização próprios.
- A aprovação deste ADR registra decisões; não constitui aceite técnico, teste de isolamento, configuração de infraestrutura, backup validado ou autorização de produção.

## Verificações e pendências

| Critério observável | Estado |
| --- | --- |
| Stack e alternativas correspondem às decisões registradas na REI-195 | Conferido documentalmente nesta data |
| Fronteira do MVP exclui migração automática, integração PJe, dados reais e homologação | Conferido no PRD aprovado |
| PHP-FPM e mecanismo de banco observados no VPS | PHP-FPM 8.5 ativo; `mysql --version` reporta Percona Server for MySQL 8.4.11-12. A documentação oficial da Percona o descreve como substituto compatível do MySQL e esta versão inclui recursos e correções do MySQL Community 8.4.11. `SHOW ENGINES` não foi validado por falta de autenticação local ao MySQL; confirmar o engine disponível/configurado pelo usuário dedicado do Law antes de uso. |
| Site user/PHP-FPM de Law separado e demonstrado com teste negativo | Pendente; a listagem de `/etc/php/*/fpm/pool.d/` não mostrou pool do Law, e `systemctl` não mostrou serviço com `law` no nome. O ambiente Law ainda não está implantado, portanto usuário/site/banco exclusivos e testes negativos de isolamento não existem. Não ler dados nem reutilizar pools/contas de produtos existentes. |
| Exposição pública de MySQL e Docker | Parcial, com bloqueio pendente: o host escuta em `*:3306` e `*:33060`; UFW não permite essas portas e testes TCP externos de uma estação IPv4/IPv6 não conectaram. Isso cobre apenas essa origem; a VM não tem firewall Hostinger atribuído. O container `fokuslead-api-1` está em execução e publica `3333/tcp` em `0.0.0.0` e `[::]`; a porta aceitou conexão TCP externa por IPv4, mas não por IPv6 a partir desta estação. `DOCKER-USER` está vazia. Nginx tem um virtualhost `api.fokuslead.com.br` com `proxy_pass http://127.0.0.1:3333`, mas consulta DNS pública a `api.fokuslead.com.br` retornou NXDOMAIN; `lead.fokuscloud.com.br` está DNS-only e aponta para o VPS. A proveniência do container não foi confirmada: não tem mounts nem rótulos OCI de origem/revisão; os rótulos Compose apontam para `/home/admin-ssh/fokuslead/docker-compose.prod.yml`, mas esse diretório/arquivo não existe no host. O README do repositório atual [webapp-fokuslead-2027](https://github.com/jorgewreis/webapp-fokuslead-2027#readme) diz que não há API/runtime em execução; a busca no repositório não encontrou referência a `3333`. Há conflito entre documentação e processo ativo. Em 19/11, Jorge decidiu manter o mapeamento 3333 como está por enquanto. Essa decisão é provisória, não confirma a finalidade nem aprova a exposição para o Law. Nenhum payload foi enviado e nenhuma regra/container foi alterado. |
| Acesso administrativo restrito e WireGuard funcional | Comprovado no firewall local em 2026-11-19: `wg0` ativo na VPS (`10.222.231.1/24`, UDP 51820) e habilitado no boot; cliente Windows automático, handshake e tráfego confirmados. UFW ativo com entrada negada por padrão; SSH (`22/tcp`) permitido pela sub-rede WireGuard, origens do Gateway e exceção administrativa preexistente; CloudPanel (`8443/tcp`) permitido somente pela sub-rede WireGuard. Regras amplas para 22/8443 ausentes em IPv4/IPv6. Testes TCP externos desta estação não conectaram em 22/8443; 80/443 aceitaram. A VM não tem grupo Hostinger atribuído. A origem `law.fokuscloud.com.br` está proxied pelo Cloudflare, mas a origem continua alcançável diretamente em 80/443 por TCP; restrição de origem Cloudflare não está comprovada. Restringir 80/443 no firewall do host pode afetar o registro DNS-only de Lead e outros sites co-hospedados; nenhuma regra web foi alterada. |
| Material de chave local em texto simples removido após ativar o perfil DPAPI do WireGuard | Pendente: o perfil protegido `fokus-law-admin.conf.dpapi` está ativo com ACL limitada a SYSTEM e Administrators (remoção), mas a política bloqueou a exclusão de `C:\ProgramData\FokusLaw\WireGuard\client.key` e `C:\ProgramData\FokusLaw\WireGuard\fokus-law-admin.conf`. Nenhuma tentativa alternativa foi feita; remoção manual ainda necessária. |
| Backup sintético ponta a ponta e restauração testados após medir capacidade | Pendente; nenhum backup/restore foi executado. |
| Capacidade observada por 24 h e esforço/novo alvo sintético recalibrados | Baseline retrospectivo parcial obtido dos registros `sysstat` do servidor (America/Recife): 144 amostras CPU/memória em 10 min no intervalo 18/11 10:10–19/11 10:10, com lacuna de 20 min na virada do dia. Média de CPU idle 88,31%, steal 4,63%; memória disponível média 1,92 GiB e mínima 1,76 GiB. `df -h /` em 19/11 mostrou 27 GB livres de 48 GB (44% usado), sem histórico de espaço em disco. Não inclui carga do Law nem backup; esforço e alvo ainda não recalibrados. |

## Fontes

- Linear REI-195, decisão de stack e escopo arquitetural, consultada em 2026-11-19.
- PRD Fokus Law — 1ª Vara Crime de Ilhéus, aprovado em 2026-11-17; seções 1, 7, 8.1–8.4 e 10.1.
- `apps/law/composer.json`, consultado em 2026-11-19: constraints locais indicam Laravel `^13.17`, PHP `^8.3` e MySQL configurado como alvo no `.env.example`. Constraints locais não confirmam a versão real do VPS nem atualizam por si só a decisão aprovada de PHP 8.5.
- Percona Server for MySQL [documentação 8.4](https://docs.percona.com/percona-server/8.4/index.html) e [notas da versão 8.4.11-12](https://docs.percona.com/percona-server/8.4/release-notes/8.4.11-12.html), consultadas em 2026-11-19.
- MySQL 8.4 Reference Manual, [engine InnoDB padrão](https://dev.mysql.com/doc/refman/8.4/en/storage-engine-setting.html), consultado em 2026-11-19; configuração efetiva do servidor ainda não foi autenticada/verificada.
- [README do repositório webapp-fokuslead-2027](https://github.com/jorgewreis/webapp-fokuslead-2027#readme), consulta read-only em 2026-11-19; declara estágio inicial sem API/runtime, em conflito com o container observado no VPS.
- Configuração Nginx em `/etc/nginx/sites-enabled` encaminha `api.fokuslead.com.br` para `127.0.0.1:3333`; consulta DNS pública de `api.fokuslead.com.br` por `1.1.1.1` retornou NXDOMAIN em 2026-11-19. Jorge determinou manter a porta 3333 inalterada por enquanto.
