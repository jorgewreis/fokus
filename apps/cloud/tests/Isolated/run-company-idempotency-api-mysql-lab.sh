#!/usr/bin/env bash
set -euo pipefail

# Disposable proof only: this never receives an .env, host database, or host network.
if [[ ! -f composer.lock ]]; then
  echo "idempotency MySQL lab: composer.lock is missing. Run the script from the Fokus Cloud app root (apps/cloud in the monorepo, or the repository root in a standalone checkout)." >&2
  exit 1
fi
if [[ ! -f tests/Isolated/company-idempotency-api-mysql-bootstrap.php ]]; then
  echo "idempotency MySQL lab: tests/Isolated/company-idempotency-api-mysql-bootstrap.php is missing. Run the script from the Fokus Cloud app root." >&2
  exit 1
fi
# Work-tree check, not a local .git path probe: in the monorepo the Git directory lives at
# the repository root, while this script runs from apps/cloud. Linked worktrees
# and standalone checkouts also satisfy git rev-parse --is-inside-work-tree.
if [[ "$(git rev-parse --is-inside-work-tree 2>/dev/null || true)" != true ]]; then
  echo "idempotency MySQL lab: not inside a Git work tree. The lab archives the app with git and cannot run here." >&2
  exit 1
fi

# Archive only the app tree so composer.lock is at the archive root in both
# layouts. `git archive` from apps/cloud with HEAD:<prefix> would apply the
# subdirectory pathspec twice and emit an empty archive; always run it from
# the repository root. An empty prefix (standalone checkout) is HEAD:.
archive_app_tree() {
  git -C "$(git rev-parse --show-toplevel)" archive --format=tar "HEAD:$(git rev-parse --show-prefix)"
}

# Regression hook: prerequisites plus the app archive, without Docker or network.
if [[ "${FOKUS_LAB_ARCHIVE_ONLY:-}" == 1 ]]; then
  archive_app_tree
  exit 0
fi

runtime_image='fokus-rei60-mysql-lab-runtime'
mysql_image='mysql:8.4'
source_volume="fokus-rei60-api-lab-source-$(openssl rand -hex 8)"
mysql_id=''
password="$(openssl rand -hex 24)"

cleanup() {
  if [[ "$mysql_id" =~ ^[0-9a-f]{64}$ ]]; then
    docker rm -f "$mysql_id" >/dev/null 2>&1 || true
  fi
  docker volume rm "$source_volume" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker build -q -t "$runtime_image" -f tests/Deployment/linux-runtime/Dockerfile . >/dev/null
docker volume create "$source_volume" >/dev/null
# git archive deliberately excludes ignored working files such as .env and vendor.
archive_app_tree | docker run --rm -i --network none -v "$source_volume:/workspace" composer:2.8 sh -c 'tar -xf - -C /workspace'
# The archive also omits empty runtime directories. Create mount targets before
# overlaying them with tmpfs in the read-only test container.
docker run --rm --network none -v "$source_volume:/workspace" composer:2.8 \
  sh -c 'mkdir -p /workspace/storage /workspace/bootstrap/cache'
docker run --rm -v "$source_volume:/workspace" -w /workspace "$runtime_image" \
  composer install --no-interaction --prefer-dist --no-scripts --no-plugins --no-progress

mysql_id="$(docker run -d --network none --tmpfs /var/lib/mysql:rw,size=1g \
  -e "MYSQL_ROOT_PASSWORD=$password" -e MYSQL_DATABASE=fokus_idempotency_api_test "$mysql_image")"
[[ "$mysql_id" =~ ^[0-9a-f]{64}$ ]]
test "$(docker inspect --format '{{.HostConfig.NetworkMode}}' "$mysql_id")" = none
for attempt in $(seq 1 90); do
  # mysqladmin ping returns success even while the server rejects credentials;
  # wait for an authenticated statement so the next UUID query cannot race the
  # image initialization sequence.
  if docker exec -e "MYSQL_PWD=$password" "$mysql_id" mysql -h127.0.0.1 -P3306 -uroot -Nse 'SELECT @@server_uuid' >/dev/null 2>&1; then break; fi
  if [[ "$(docker inspect --format '{{.State.Running}}' "$mysql_id")" != true || "$attempt" = 90 ]]; then
    docker logs "$mysql_id" >&2
    exit 1
  fi
  sleep 1
done
uuid="$(docker exec -e "MYSQL_PWD=$password" "$mysql_id" mysql -h127.0.0.1 -P3306 -uroot -Nse 'SELECT @@server_uuid')"
[[ "$uuid" =~ ^[0-9a-fA-F-]{36}$ ]]

run_phpunit() {
  docker run --rm --network "container:$mysql_id" --read-only \
  --tmpfs /tmp:rw,size=128m --tmpfs /workspace/storage:rw,size=128m \
  --tmpfs /workspace/bootstrap/cache:rw,size=16m -v "$source_volume:/workspace:ro" -w /workspace \
  -e FOKUS_COMPANY_IDEMPOTENCY_LAB=1 -e APP_ENV=testing -e APP_BASE_PATH=/workspace \
  -e APP_KEY=base64:MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA= \
  -e DB_CONNECTION=mysql -e DB_HOST=127.0.0.1 -e DB_PORT=3306 -e DB_DATABASE=fokus_idempotency_api_test \
  -e DB_USERNAME=root -e DB_PASSWORD="$password" -e DB_URL= -e DB_SOCKET= \
  -e SESSION_DRIVER=database -e SESSION_CONNECTION= -e SESSION_TABLE=sessions -e SESSION_LIFETIME=120 \
  -e CACHE_STORE=array -e MAIL_MAILER=array -e QUEUE_CONNECTION=sync -e BCRYPT_ROUNDS=4 \
  -e LAB_MYSQL_UUID="$uuid" "$runtime_image" \
  php vendor/bin/phpunit --no-configuration --do-not-cache-result --bootstrap tests/Isolated/company-idempotency-api-mysql-bootstrap.php \
  "$@"
}

# The store contract intentionally builds a partial schema. Run it in its own
# disposable database lifecycle so the API tests always begin after a complete
# migrate:fresh, rather than inheriting that partial schema.
run_phpunit tests/Feature/CompanyIdempotencyStoreTest.php
docker exec -e "MYSQL_PWD=$password" "$mysql_id" mysql -h127.0.0.1 -P3306 -uroot -e \
  'DROP DATABASE `fokus_idempotency_api_test`; CREATE DATABASE `fokus_idempotency_api_test`;'
run_phpunit \
  tests/Isolated/CompanyIdempotencyApiConcurrencyTest.php \
  tests/Feature/CompanyIdempotencyApiLabTest.php \
  tests/Feature/CompanyIdempotencyDisabledTest.php \
  tests/Feature/PlatformSessionAuthorityTest.php
