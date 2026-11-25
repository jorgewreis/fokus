#!/usr/bin/env python3
"""Gera os workflows do Cloud na raiz do monorepo jorgewreis/fokus (REI-315, fase 3).

As fontes revisadas continuam inativas em ``apps/cloud/.github/workflows/<nome>.yml``
(os testes de composição exata leem essas fontes). Este script deriva, de forma
determinística, ``<raiz>/.github/workflows/cloud-<nome>.yml`` com somente as
adaptações de layout:

* ``name`` com prefixo ``Cloud · ``;
* ``defaults.run.working-directory: apps/cloud`` nos jobs com checkout (o checkout
  fica na raiz); passos ``run`` antes do checkout ficam na raiz do workspace;
* ``$GITHUB_WORKSPACE`` passa a apontar para ``$GITHUB_WORKSPACE/apps/cloud``;
* caminhos relativos de ``actions/upload-artifact`` recebem o prefixo ``apps/cloud/``;
* filtros ``paths`` em ``push``/``pull_request``: os filtros existentes ganham o
  prefixo e as referências a workflows apontam para ``cloud-*.yml``; sem filtro,
  ``apps/cloud/**`` mais o próprio arquivo do workflow;
* ``schedule`` removido nos demais workflows de produção;
  ``production-backup.yml`` preserva o agendamento diário no monorepo;
* grupos de ``concurrency`` inalterados (nenhum colide com Law/Styles);
* ``git diff --name-only`` com ``--relative`` (o diretório de trabalho é o app);
* ``law-schema-preflight``: o checkout proposto fica em ``proposed/`` e o app em
  ``proposed/apps/cloud/``; a release antiga (``b3d441ae``) segue no layout legado.

Uso: ``python3 tools/ci/promote-workflows.py [--check]`` a partir de ``apps/cloud``.
Sem rede e sem escrever fora de ``<raiz>/.github/workflows``.
"""
from pathlib import Path
import re
import sys

APP_PREFIX = 'apps/cloud'
WORKFLOW_PREFIX = 'cloud-'
APP_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = APP_ROOT / '.github/workflows'
HEADER = ('# Gerado por apps/cloud/tools/ci/promote-workflows.py a partir de\n'
          '# apps/cloud/.github/workflows/{name}. Não edite à mão: altere a fonte\n'
          '# revisada e rode o script (o teste test_operational_workflow_promotion.py\n'
          '# falha se este arquivo divergir).\n')
SPECIAL_CHECKOUT = {'law-schema-preflight.yml'}
KEEP_SCHEDULE = {'production-backup.yml'}


class PromotionError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise PromotionError(message)


def target_name(name):
    return WORKFLOW_PREFIX + name


def map_path_filter(value):
    if value.startswith('.github/workflows/'):
        return '.github/workflows/' + target_name(value.rsplit('/', 1)[1])
    require(not value.startswith(('/', '!', '../')), 'unsupported path filter: ' + value)
    return APP_PREFIX + '/' + value


def split_top_level(lines):
    """Blocos de chaves de nível zero, preservando comentários/linhas em branco."""
    blocks, current = [], None
    for line in lines:
        if line and not line[0].isspace() and not line.startswith('#'):
            key = line.split(':', 1)[0].strip('"\'')
            current = [key, [line]]
            blocks.append(current)
        else:
            if current is None:
                current = ['', []]
                blocks.append(current)
            current[1].append(line)
    return blocks


def promote_triggers(lines, name):
    own = '.github/workflows/' + target_name(name)
    out, i = [lines[0]], 1
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^  ([a-z_]+):\s*$', line)
        if not m:
            out.append(line)
            i += 1
            continue
        event = m.group(1)
        j = i + 1
        while j < len(lines) and (lines[j].startswith('   ') or not lines[j].strip()):
            j += 1
        body = lines[i + 1:j]
        trailing = []
        while body and not body[-1].strip():
            trailing.insert(0, body.pop())
        if event == 'schedule' and name not in KEEP_SCHEDULE:
            i = j
            continue
        if event in ('push', 'pull_request'):
            new_body, has_paths, k = [], False, 0
            while k < len(body):
                b = body[k]
                if re.match(r'^    paths:\s*$', b):
                    has_paths = True
                    new_body.append(b)
                    k += 1
                    seen = set()
                    while k < len(body) and re.match(r'^      - ', body[k]):
                        pm = re.match(r"^      - '([^']+)'\s*$", body[k])
                        require(pm is not None, 'unsupported path filter line: ' + body[k])
                        mapped = map_path_filter(pm.group(1))
                        seen.add(mapped)
                        new_body.append(f"      - '{mapped}'")
                        k += 1
                    if own not in seen:
                        new_body.append(f"      - '{own}'")
                    continue
                require(not re.match(r'^    (paths-ignore|branches-ignore):', b), 'unsupported filter in ' + name)
                new_body.append(b)
                k += 1
            if not has_paths:
                new_body += ['    paths:', f"      - '{APP_PREFIX}/**'", f"      - '{own}'"]
            body = new_body
        out.append(line)
        out.extend(body)
        out.extend(trailing)
        i = j
    return out


def prefix_artifact_paths(lines):
    out, in_upload, in_with, block_indent = [], False, False, None
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\s*(- )?(uses|name|run|id|if|env|with|shell|working-directory):', line) and line.lstrip().startswith('- '):
            in_upload, in_with, block_indent = False, False, None
        if re.match(r'^\s*(- )?uses: actions/upload-artifact@', line):
            in_upload = True
        if in_upload and re.match(r'^\s+with:\s*$', line):
            in_with = True
        if in_upload and in_with:
            m = re.match(r'^(\s+)path:\s*(.*)$', line)
            if m:
                value = m.group(2)
                if value == '|':
                    block_indent = len(m.group(1)) + 2
                    out.append(line)
                    continue
                out.append(m.group(1) + 'path: ' + prefix_one(value))
                continue
            if block_indent is not None:
                if stripped and len(line) - len(line.lstrip()) >= block_indent:
                    out.append(' ' * block_indent + prefix_one(stripped))
                    continue
                block_indent = None
        out.append(line)
    return out


def prefix_one(value):
    if value.startswith(('${{', '!${{', '/')):
        return value
    if value.startswith('!'):
        return '!' + APP_PREFIX + '/' + value[1:]
    return APP_PREFIX + '/' + value


def add_job_defaults(lines, name):
    """``working-directory: apps/cloud`` só nos jobs com checkout.

    Jobs sem checkout (backup, diagnósticos, agregadores) não têm o diretório do
    app no runner; passos ``run`` anteriores ao checkout ficam explicitamente na
    raiz do workspace.
    """
    header = re.compile(r'^  [A-Za-z0-9_-]+:\s*$')
    chunks, current = [], None
    for line in lines:
        if header.match(line):
            current = [line]
            chunks.append(current)
        elif current is None:
            chunks.append([line])
        else:
            current.append(line)
    out = []
    for chunk in chunks:
        if not header.match(chunk[0]) or not any(re.match(r'^\s+(- )?uses: actions/checkout@', l) for l in chunk):
            out += chunk
            continue
        require(not any(re.match(r'^    defaults:', l) for l in chunk), 'job defaults already set in ' + name)
        out += [chunk[0], '    defaults:', '      run:', f'        working-directory: {APP_PREFIX}']
        steps, seen_checkout, i = chunk[1:], False, 0
        while i < len(steps):
            line = steps[i]
            if re.match(r'^      - ', line) and not seen_checkout:
                j = i + 1
                while j < len(steps) and not re.match(r'^      - ', steps[j]) and (steps[j].startswith('        ') or not steps[j].strip()):
                    j += 1
                step = steps[i:j]
                if any(re.match(r'^      - uses: actions/checkout@|^        uses: actions/checkout@', l) for l in step):
                    seen_checkout = True
                    out += step
                elif any(re.match(r'^(      - |        )run:', l) for l in step):
                    require(not any('working-directory:' in l for l in step), 'step already sets working-directory in ' + name)
                    out += [step[0], '        working-directory: ${{ github.workspace }}'] + step[1:]
                else:
                    out += step
                i = j
                continue
            out.append(line)
            i += 1
    return out


def promote(name, text):
    require(text.endswith('\n') and '\r' not in text, 'unexpected line endings in ' + name)
    lines = text[:-1].split('\n')
    blocks = split_top_level(lines)
    keys = [key for key, _ in blocks if key]
    require(keys.count('jobs') == 1 and 'defaults' not in keys, 'unsupported layout in ' + name)
    special = name in SPECIAL_CHECKOUT
    result = []
    for key, block in blocks:
        if key == 'name':
            m = re.match(r'^name: (.+)$', block[0])
            require(m and not m.group(1).startswith(('"', "'")), 'unsupported name in ' + name)
            block = ['name: Cloud · ' + m.group(1)] + block[1:]
        elif key == 'on':
            block = promote_triggers(block, name)
        elif key == 'jobs':
            if not special:
                block = add_job_defaults(block, name)
            block = prefix_artifact_paths(block)
            joined = '\n'.join(block)
            if special:
                joined = re.sub(r'\bproposed/(?!apps/cloud/)', 'proposed/' + APP_PREFIX + '/', joined)
            else:
                joined = joined.replace('"$GITHUB_WORKSPACE"', '"$GITHUB_WORKSPACE/' + APP_PREFIX + '"')
                joined = joined.replace('"$GITHUB_WORKSPACE/database/', '"$GITHUB_WORKSPACE/' + APP_PREFIX + '/database/')
                joined = joined.replace('src=$GITHUB_WORKSPACE,', 'src=$GITHUB_WORKSPACE/' + APP_PREFIX + ',')
                require(re.search(r'GITHUB_WORKSPACE(?!/apps/cloud)', joined) is None,
                        'unadapted GITHUB_WORKSPACE in ' + name)
            joined = joined.replace('git diff --name-only', 'git diff --relative --name-only')
            block = joined.split('\n')
        result += block
    return HEADER.format(name=name) + '\n'.join(result) + '\n'


def repository_root():
    for candidate in (APP_ROOT, *APP_ROOT.parents):
        if (candidate / '.git').exists():
            return candidate
    raise PromotionError('git repository not found')


def expected_outputs(source_dir=SOURCE_DIR):
    return {target_name(path.name): promote(path.name, path.read_text(encoding='utf-8'))
            for path in sorted(source_dir.glob('*.yml'))}


def main(argv):
    check = argv[1:] == ['--check']
    require(argv[1:] in ([], ['--check']), 'usage: promote-workflows.py [--check]')
    top = repository_root()
    require(top != APP_ROOT, 'run inside the monorepo (apps/cloud)')
    target = top / '.github/workflows'
    outputs = expected_outputs()
    present = {p.name for p in target.glob(WORKFLOW_PREFIX + '*.yml')}
    drift = sorted(n for n, t in outputs.items()
                   if not (target / n).is_file() or (target / n).read_text(encoding='utf-8') != t)
    drift += sorted(present - outputs.keys())
    if check:
        if drift:
            print('workflow promotion drift: ' + ', '.join(drift), file=sys.stderr)
            return 1
        return 0
    for name, text in outputs.items():
        (target / name).write_text(text, encoding='utf-8')
    for name in present - outputs.keys():
        (target / name).unlink()
    print(f'{len(outputs)} workflows promoted')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except PromotionError as error:
        print(f'promotion refused: {error}', file=sys.stderr)
        sys.exit(2)
