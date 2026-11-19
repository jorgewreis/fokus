<?php

namespace Tests\Feature;

use Tests\TestCase;

class InstitutionalContactsTest extends TestCase
{
    public function test_institutional_contacts_are_public_and_use_only_verified_official_values(): void
    {
        $this->get(route('institutional-contacts.show'))
            ->assertOk()
            ->assertSee('Contatos institucionais')
            ->assertSee('(73) 3234-3428')
            ->assertSee('ilheus1vcriminal@tjba.jus.br')
            ->assertSee('Avenida Osvaldo Cruz, s/n, Bairro Cidade Nova, Ilhéus, Bahia.')
            ->assertSee('Não informado na fonte oficial consultada; aguarda confirmação.')
            ->assertSee('https://www.tjba.jus.br/contatos/contato/1a-vara-criminal-de-ilheus/')
            ->assertDontSee('Emanuele Vita Leite');
    }
}
