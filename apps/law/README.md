# Fokus Law

Greenfield Laravel application for the synthetic MVP. This repository contains no institutional or production data.

## Stack

- Laravel 13
- PHP 8.5
- MySQL 8.4 with InnoDB
- Blade-rendered monolith

## Local setup

1. Use PHP 8.5 with Laravel-required extensions and Composer 2.
2. Run `composer install` in `apps/law`.
3. Copy `.env.example` to `.env` and set a dedicated local synthetic MySQL database and credentials.
4. Run `php artisan key:generate` and `php artisan migrate` only against that synthetic database.
5. Start local development with `php artisan serve`.

## Synthetic fixture

`php artisan db:seed` creates one unverified synthetic test account using the reserved `.test` email domain. The seeder only accepts SQLite `:memory:` while `APP_ENV=testing`, or MySQL on `localhost`/ `127.0.0.1` with database `fokus_law_synthetic` while `APP_ENV=local` or `development`. Other targets are rejected before a database connection is opened. This fixture does not grant application access.

The GitHub Actions workflow validates Composer metadata and runs the Laravel test suite against the in-memory SQLite database. It does not use production secrets or connect to institutional services.

The MVP is not approved for real institutional data, PJe integration, or production deployment. Environment isolation, access controls, synthetic fixtures, backup/restore, and the Pessoa → Processo → Expedição flow are tracked in Linear and remain to be implemented and verified.
