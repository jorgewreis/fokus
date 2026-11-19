# Fokus Law: base local de build e deploy

## Estado e limites

Esta base prepara execução local sintética e verificações automatizadas. Ela não configura nem autoriza deploy no KVM1, não usa dados reais ou PJe e não constitui homologação. O KVM1 é compartilhado com outros produtos; a ativação do ambiente sintético remoto permanece bloqueada pelos controles pendentes em [ADR-001](../../docs/adr/001-law-greenfield-architecture.md) e na REI-195.

O código-fonte canônico está em `apps/law` no worktree desta branch. O diretório físico `gar/` é um worktree Git ligado ao repositório; não o adicione pelo worktree `main` como pasta aninhada. O `apps/law` do worktree `main` ainda contém apenas placeholders. Adicione e versione os arquivos a partir deste worktree.

## Pré-requisitos locais

- Docker Desktop ou Docker Engine com Compose v2.
- Portas locais 8080 livres e espaço suficiente para imagens e volume sintético.

## Primeiro início

No PowerShell, dentro de `gar/apps/law`:

```powershell
Copy-Item docker.env.example docker.env
docker compose build
docker compose run --rm app php artisan key:generate --show
```

Copie o valor exibido para `APP_KEY` em `docker.env` e substitua as senhas locais de exemplo. Elas servem apenas para este banco sintético local. Não coloque segredos no Git, em issues, no PRD ou em logs.

```powershell
docker compose up -d
docker compose exec app php artisan migrate --force
docker compose ps
Invoke-WebRequest http://localhost:8080/up
```

O app fica disponível somente na máquina local em `http://localhost:8080`. MySQL não publica porta no host; a rede Docker é interna. Para parar sem remover o banco: `docker compose down`. Para apagar o banco sintético local e seus dados: `docker compose down --volumes`.

## Pipeline

`.github/workflows/law-ci.yml` valida o Composer, instala dependências sem credenciais de produção, compila assets, executa a suíte automatizada existente e constrói a imagem Docker sem publicar. Usa `GITHUB_TOKEN` somente com permissão de leitura de conteúdo. Não há credenciais de deploy, publicação de imagem ou acesso ao KVM1 configurados.

## Ambientes e promoção

| Ambiente | Estado | Limite |
| --- | --- | --- |
| Local Docker | Base adicionada; requer build/execução local para validar comportamento | Somente dados sintéticos; banco em volume local |
| CI GitHub Actions | Workflow versionado; requer GitHub Actions habilitado após a árvore ser integrada ao Git rastreado | Build e verificações; sem deploy/publicação |
| Hostinger KVM1 | Não configurado para o Fokus Law | Ativar somente após os gates da REI-195 e aceite do desenvolvedor |
| Produção/dados reais | Fora do escopo aprovado | Sem autorização neste ciclo |

## Implantação remota: gates antes de habilitar

Não executar deploy remoto até registrar evidência de cada item na REI-195:

1. Integrar/revisar o diretório `gar/` e estabelecer a cópia canônica versionada.
2. Confirmar se a hospedagem será CloudPanel com PHP-FPM nativo ou container atrás do proxy; este pacote só implementa Docker local.
3. Criar site/usuário e pool PHP do Law segregados, database/user exclusivos, validar InnoDB e executar testes negativos de isolamento.
4. Esclarecer a origem e exposição da porta 3333, confirmar firewall Hostinger e demonstrar restrição de origem Cloudflare sem afetar outros sites.
5. Medir capacidade e espaço considerando Law e backup; confirmar o diretório Docker e a capacidade do PC de recuperação.
6. Configurar transferência SFTP iniciada pelo PC, criptografia, retenção das três cópias mensais e testar restauração em Docker.
7. Confirmar WireGuard e acessos operacionais para manutenção; documentar nomes de variáveis/segredos sem registrar valores.
8. Obter aceite explícito do desenvolvedor para ativar a co-hospedagem sintética.

Depois dos gates: preparar release imutável ligada a commit, fazer backup pré-release, executar migrations em etapa controlada, ativar o release, verificar `/up` e o fluxo sintético e registrar resultado/data no Linear. O mecanismo remoto e as credenciais ainda precisam ser definidos; nenhum passo desse runbook foi executado no servidor.

## Rollback

Para uma falha de aplicação, voltar à imagem/release anterior e verificar `/up` e o fluxo sintético. Não reverter automaticamente migrations nem restaurar banco: avaliar compatibilidade e usar a restauração validada somente por procedimento documentado e autorizado. Registrar causa, versão anterior/nova, evidência e próxima ação na issue Linear.

## Variáveis

`APP_KEY`, `APP_ENV`, `APP_DEBUG`, `APP_URL`, `DB_CONNECTION`, `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_ROOT_PASSWORD`.

Não registrar aqui valores de produção. O `docker.env` local é ignorado pelo Git.
