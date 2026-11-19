<?php

namespace Tests\Feature;

use App\Models\User;
use Database\Seeders\SyntheticFixtureSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class SyntheticFixtureSeederTest extends TestCase
{
    use RefreshDatabase;

    public function test_database_seeder_creates_an_explicitly_synthetic_unverified_account_idempotently(): void
    {
        $this->seed();
        $this->seed();

        $this->assertSame(1, User::query()->count());
        $this->assertDatabaseHas('users', [
            'name' => 'Conta Sintética de Teste 001',
            'email' => 'conta.teste.001@example.test',
            'email_verified_at' => null,
        ]);
    }

    public function test_fixture_seeder_rejects_a_remote_database_even_outside_production(): void
    {
        $this->expectException(\RuntimeException::class);
        $this->expectExceptionMessage('only be seeded into the in-memory test database');

        SyntheticFixtureSeeder::assertAllowedTarget(
            'local',
            'mysql',
            'db.example.invalid',
            'fokus_law_synthetic',
        );
    }
}
