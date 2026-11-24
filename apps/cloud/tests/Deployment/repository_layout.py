"""Layout do Fokus Cloud dentro do monorepo jorgewreis/fokus (REI-315).

O aplicativo mora em ``apps/cloud``. Até 24/11/2026 ele morava na raiz do
repositório jorgewreis/fokus-cloud, e o histórico foi importado com os SHAs
originais. Por isso o mesmo código precisa funcionar em dois layouts:

* legado ou isolado (raiz do Git == raiz do app): fixtures sintéticas, o
  container da homologação e o próprio fokus-cloud;
* monorepo (raiz do app == ``<toplevel>/apps/cloud``).

As fontes revisadas dos workflows ficam inativas em
``apps/cloud/.github/workflows/<nome>.yml``. Desde a Fase 3,
``tools/ci/promote-workflows.py`` deriva delas os workflows ativos em
``<toplevel>/.github/workflows/cloud-<nome>.yml``. ``workflow_path`` aceita os
dois lugares e prefere o da raiz; ``reviewed_workflow_path`` devolve sempre a
fonte revisada, usada pelos testes de bytes exatos.

Somente leitura: nenhuma função aqui escreve no checkout nem acessa a rede.
"""
from pathlib import Path
import subprocess

APP_ROOT = Path(__file__).resolve().parents[2]
APP_PREFIX = 'apps/cloud'
WORKFLOW_PREFIX = 'cloud-'


def repository_root(app_root=APP_ROOT):
    """Diretório que contém ``.git`` (pasta ou arquivo de worktree), ou o próprio app."""
    app_root = Path(app_root).resolve()
    for candidate in (app_root, *app_root.parents):
        if (candidate / '.git').exists():
            return candidate
    return app_root


def workflow_path(name, app_root=APP_ROOT):
    """Arquivo do workflow ``name`` (ex.: ``deploy.yml``) no layout atual."""
    app_root = Path(app_root).resolve()
    top = repository_root(app_root)
    if top != app_root:
        promoted = top / '.github/workflows' / (WORKFLOW_PREFIX + name)
        if promoted.is_file():
            return promoted
    return app_root / '.github/workflows' / name


def reviewed_workflow_path(name, app_root=APP_ROOT):
    """Fonte revisada (inativa) do workflow ``name``, em qualquer layout."""
    return Path(app_root).resolve() / '.github/workflows' / name


def source_treeish(commit, repository):
    """Tree-ish do app em ``commit``.

    Commits anteriores à importação têm o app na raiz; os posteriores, em
    ``apps/cloud``. Falha fechado quando nenhum dos dois contém o app.
    """
    def has_app(prefix):
        spec = f'{commit}:{prefix}artisan'
        return subprocess.run(['git', '-C', str(repository), 'cat-file', '-e', spec],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    if has_app(APP_PREFIX + '/'):
        return f'{commit}:{APP_PREFIX}'
    if has_app(''):
        return commit
    raise ValueError('commit does not contain the Fokus Cloud application')


def archive_source(commit, stream, app_root=APP_ROOT):
    """``git archive`` do app em ``commit``, com os caminhos relativos à raiz do app.

    Rodar ``git archive <sha>`` dentro de ``apps/cloud`` limita o arquivo a esse
    subdiretório, o que zera o baseline anterior à importação. Aqui o comando
    roda sempre na raiz do Git. Para commits com o app na raiz, o comando e os
    bytes são os mesmos de antes.
    """
    top = repository_root(app_root)
    subprocess.run(['git', 'archive', source_treeish(commit, top)], cwd=top, stdout=stream, check=True)


def show_source(commit, name, app_root=APP_ROOT):
    """Conteúdo do arquivo ``name`` (relativo ao app) em ``commit``, em qualquer layout."""
    top = repository_root(app_root)
    treeish = source_treeish(commit, top)
    spec = f'{treeish}/{name}' if ':' in treeish else f'{treeish}:{name}'
    return subprocess.check_output(['git', 'show', spec], cwd=top)


def archive_source_bytes(commit, app_root=APP_ROOT):
    """Mesmo que ``archive_source``, devolvendo os bytes do tar."""
    top = repository_root(app_root)
    return subprocess.check_output(['git', 'archive', source_treeish(commit, top)], cwd=top)
