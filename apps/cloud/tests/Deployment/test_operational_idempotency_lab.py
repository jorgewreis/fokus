"""Regressão REI-315: o lab de idempotência roda a partir de apps/cloud no monorepo.

A homologação 45499599970 falhou em 0,002 s com log vazio porque o script fazia
``test -e .git`` no cwd do app. Sem rede, Docker ou produção: fixtures Git
sintéticas e o gancho FOKUS_LAB_ARCHIVE_ONLY do próprio script.
"""
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parents[2]
LAB_SCRIPT = ROOT / 'tests/Isolated/run-company-idempotency-api-mysql-lab.sh'
RELEASE = ROOT / 'tests/Deployment/linux-release.py'
GIT = ['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false',
       '-c', 'user.email=synthetic@example.invalid', '-c', 'user.name=Synthetic idempotency lab']


class IdempotencyLabMonorepo(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='idempotency-lab-')

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args, cwd):
        return subprocess.check_output([*GIT, *args], cwd=cwd, stderr=subprocess.PIPE)

    def init_repo(self, root):
        root.mkdir(parents=True)
        self.git('init', '-q', cwd=root)

    def write(self, root, path, text):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, root, message):
        self.git('add', '-A', cwd=root)
        self.git('commit', '-qm', message, cwd=root)
        return self.git('rev-parse', 'HEAD', cwd=root).decode().strip()

    def archive_only(self, cwd):
        return subprocess.run(
            ['bash', str(LAB_SCRIPT)],
            cwd=cwd,
            env={**os.environ, 'FOKUS_LAB_ARCHIVE_ONLY': '1'},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    @staticmethod
    def names(data):
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            return sorted(member.name for member in archive.getmembers() if member.isfile())

    def test_source_rejects_git_directory_probe_and_archives_from_toplevel(self):
        script = LAB_SCRIPT.read_text(encoding='utf-8')
        self.assertNotIn('test -e .git', script)
        self.assertIn('git rev-parse --is-inside-work-tree', script)
        self.assertIn('git -C "$(git rev-parse --show-toplevel)" archive --format=tar "HEAD:$(git rev-parse --show-prefix)"', script)
        self.assertIn('composer.lock is missing', script)
        release = RELEASE.read_text(encoding='utf-8')
        self.assertIn("cwd=ROOT", release)
        self.assertIn("def run(label,command,check=True,cwd=None):", release)
        self.assertIn("subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,cwd=cwd)", release)
        self.assertIn(
            "run('idempotency-mysql-lab',['bash',str(ROOT/'tests/Isolated/run-company-idempotency-api-mysql-lab.sh')],check=False,cwd=ROOT)",
            release,
        )

    def test_prerequisites_fail_with_a_clear_message(self):
        empty = Path(self.temp.name) / 'empty'
        empty.mkdir()
        result = self.archive_only(empty)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'composer.lock is missing', result.stderr)

    def test_monorepo_app_directory_archives_composer_lock_at_workspace_root(self):
        root = Path(self.temp.name) / 'monorepo'
        self.init_repo(root)
        self.write(root, 'packages/styles/package.json', '{}\n')
        self.write(root, 'apps/cloud/composer.lock', '{"name": "synthetic/monorepo"}\n')
        self.write(root, 'apps/cloud/tests/Isolated/company-idempotency-api-mysql-bootstrap.php', '<?php\n')
        self.commit(root, 'monorepo layout')
        app = root / 'apps/cloud'
        self.assertFalse((app / '.git').exists())
        self.assertEqual(
            self.git('rev-parse', '--is-inside-work-tree', cwd=app).decode().strip(),
            'true',
        )
        # The naive combination (cwd=apps/cloud and HEAD:<prefix>) is empty.
        prefix = self.git('rev-parse', '--show-prefix', cwd=app).decode().strip()
        naive = subprocess.check_output(
            [*GIT, 'archive', '--format=tar', f'HEAD:{prefix}'],
            cwd=app,
        )
        try:
            naive_names = self.names(naive)
        except tarfile.ReadError:
            naive_names = []
        self.assertNotIn('composer.lock', naive_names)
        result = self.archive_only(app)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        names = self.names(result.stdout)
        self.assertEqual(
            names,
            ['composer.lock', 'tests/Isolated/company-idempotency-api-mysql-bootstrap.php'],
        )
        self.assertNotIn('apps/cloud/composer.lock', names)
        self.assertNotIn('packages/styles/package.json', names)

    def test_standalone_checkout_with_empty_prefix_still_archives_the_app_root(self):
        root = Path(self.temp.name) / 'standalone'
        self.init_repo(root)
        self.write(root, 'composer.lock', '{"name": "synthetic/standalone"}\n')
        self.write(root, 'tests/Isolated/company-idempotency-api-mysql-bootstrap.php', '<?php\n')
        self.commit(root, 'standalone layout')
        self.assertEqual(self.git('rev-parse', '--show-prefix', cwd=root).decode().strip(), '')
        result = self.archive_only(root)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(
            self.names(result.stdout),
            ['composer.lock', 'tests/Isolated/company-idempotency-api-mysql-bootstrap.php'],
        )


if __name__ == '__main__':
    unittest.main()
