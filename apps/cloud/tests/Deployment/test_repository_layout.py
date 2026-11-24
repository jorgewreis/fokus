"""Layout do monorepo (REI-315): fixtures Git sintéticas, sem rede nem produção."""
import io
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import repository_layout as layout  # noqa: E402

GIT = ['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false',
       '-c', 'user.email=synthetic@example.invalid', '-c', 'user.name=Synthetic layout test']


class RepositoryLayout(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='repository-layout-')
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.git('init', '-q')
        # Commit anterior ao monorepo: app na raiz, como o baseline 26daac7c.
        self.write('artisan', '#!/usr/bin/env php\n')
        self.write('composer.json', '{"name": "synthetic/legacy"}\n')
        self.write('.github/workflows/deploy.yml', 'name: legacy\n')
        self.legacy = self.commit('legacy root layout')
        # Move para apps/cloud e convivência com outros pacotes do monorepo.
        (self.root / 'apps/cloud').mkdir(parents=True)
        for name in ('artisan', 'composer.json', '.github'):
            self.git('mv', name, 'apps/cloud/' + name)
        self.write('packages/styles/package.json', '{}\n')
        self.write('apps/cloud/composer.json', '{"name": "synthetic/monorepo"}\n')
        self.monorepo = self.commit('monorepo layout')
        self.app = self.root / 'apps/cloud'

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args, cwd=None):
        return subprocess.check_output([*GIT, *args], cwd=cwd or self.root, stderr=subprocess.PIPE)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, message):
        self.git('add', '-A')
        self.git('commit', '-qm', message)
        return self.git('rev-parse', 'HEAD').decode().strip()

    @staticmethod
    def names(data):
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            return sorted(member.name for member in archive.getmembers() if member.isfile())

    def test_repository_root(self):
        self.assertEqual(layout.repository_root(self.app), self.root.resolve())
        self.assertEqual(layout.repository_root(self.root), self.root.resolve())

    def test_legacy_baseline_archive_from_the_app_directory(self):
        # Regressão: `git archive <baseline>` com cwd=apps/cloud devolvia 0 entradas.
        plain = subprocess.check_output(['git', 'archive', self.legacy], cwd=self.app)
        with self.assertRaises(tarfile.ReadError):
            self.names(plain)  # tar sem nenhuma entrada
        data = layout.archive_source_bytes(self.legacy, self.app)
        self.assertEqual(self.names(data), ['.github/workflows/deploy.yml', 'artisan', 'composer.json'])
        # Mesmos bytes do comando original rodado na raiz do layout legado.
        self.assertEqual(data, subprocess.check_output(['git', 'archive', self.legacy], cwd=self.root))
        target = Path(self.temp.name) / 'baseline.tar'
        with target.open('wb') as stream:
            layout.archive_source(self.legacy, stream, self.app)
        self.assertEqual(target.read_bytes(), data)

    def test_monorepo_commit_archives_only_the_app(self):
        data = layout.archive_source_bytes(self.monorepo, self.app)
        self.assertEqual(self.names(data), ['.github/workflows/deploy.yml', 'artisan', 'composer.json'])

    def test_show_source_in_both_layouts(self):
        self.assertEqual(layout.show_source(self.legacy, 'composer.json', self.app), b'{"name": "synthetic/legacy"}\n')
        self.assertEqual(layout.show_source(self.monorepo, 'composer.json', self.app), b'{"name": "synthetic/monorepo"}\n')

    def test_commit_without_the_app_fails_closed(self):
        empty_tree = subprocess.check_output([*GIT, 'mktree'], cwd=self.root, input=b'').decode().strip()
        orphan = self.git('commit-tree', empty_tree, '-m', 'empty').decode().strip()
        with self.assertRaises(ValueError):
            layout.archive_source_bytes(orphan, self.app)

    def test_workflow_path_prefers_promoted_root_workflow(self):
        self.assertEqual(layout.workflow_path('deploy.yml', self.app), self.app.resolve() / '.github/workflows/deploy.yml')
        promoted = self.root / '.github/workflows/cloud-deploy.yml'
        promoted.parent.mkdir(parents=True)
        promoted.write_text('name: promoted\n')
        self.assertEqual(layout.workflow_path('deploy.yml', self.app), promoted.resolve())
        # Layout legado ou isolado: o próprio app é a raiz e não há prefixo.
        self.assertEqual(layout.workflow_path('deploy.yml', self.root), self.root.resolve() / '.github/workflows/deploy.yml')


if __name__ == '__main__':
    unittest.main()
