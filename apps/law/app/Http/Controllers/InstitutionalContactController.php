<?php

namespace App\Http\Controllers;

use Illuminate\View\View;

class InstitutionalContactController extends Controller
{
    public function __invoke(): View
    {
        return view('institutional-contacts.show', [
            'contacts' => [
                'phones' => [
                    ['label' => 'Cartório', 'display' => '(73) 3234-3428', 'tel' => '+557332343428'],
                    ['label' => 'Diretoria', 'display' => '(73) 3234-3429', 'tel' => '+557332343429'],
                    ['label' => 'Gabinete', 'display' => '(73) 3234-3430', 'tel' => '+557332343430'],
                    ['label' => 'Assessoria', 'display' => '(73) 3234-3421', 'tel' => '+557332343421'],
                    ['label' => 'Audiência', 'display' => '(73) 3234-3432', 'tel' => '+557332343432'],
                ],
                'whatsapp' => [
                    'display' => '(71) 99610-8241',
                    'url' => 'https://wa.me/5571996108241',
                ],
                'email' => 'ilheus1vcriminal@tjba.jus.br',
                'address' => 'Avenida Osvaldo Cruz, s/n, Bairro Cidade Nova, Ilhéus, Bahia.',
                'hours' => null,
                'source' => 'https://www.tjba.jus.br/contatos/contato/1a-vara-criminal-de-ilheus/',
                'checkedAt' => '19/11/2026',
            ],
        ]);
    }
}
