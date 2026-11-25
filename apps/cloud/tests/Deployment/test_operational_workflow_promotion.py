"""Workflows do Cloud promovidos para a raiz do monorepo (REI-315, fase 3).

Os bytes revisados continuam nas fontes inativas em ``apps/cloud/.github/workflows``
(conferidos pelos testes de composição exata). Aqui se exige que cada
``<raiz>/.github/workflows/cloud-<nome>.yml`` seja exatamente a saída de
``tools/ci/promote-workflows.py`` e que a promoção preserve as travas de
publicação. Sem rede, sem GitHub e sem escrever no checkout.
"""
import importlib.util
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP_ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(APP_ROOT / 'deploy'))
sys.path.insert(0, str(APP_ROOT / 'tools/releases'))
from repository_layout import repository_root  # noqa: E402

spec = importlib.util.spec_from_file_location('promote_workflows', APP_ROOT / 'tools/ci/promote-workflows.py')
promote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(promote)

TOP = repository_root(APP_ROOT)
MONOREPO = TOP != APP_ROOT
SOURCES = sorted((APP_ROOT / '.github/workflows').glob('*.yml'))


def on_block(text):
    match = re.search(r'^"?on"?:\n((?:(?:  .*)?\n)*)', text, re.M)
    assert match, 'workflow without on block'
    return match.group(1)


def events(text):
    return re.findall(r'^  ([a-z_]+):', on_block(text), re.M)


class SyntheticPromotion(unittest.TestCase):
    SOURCE = '''name: Synthetic
"on":
  push:
    branches:
      - main
  pull_request:
    paths:
      - 'tools/x/**'
      - '.github/workflows/deploy.yml'
  schedule:
    - cron: '1 2 * * *'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  first:
    runs-on: ubuntu-latest
    steps:
      - name: Before checkout
        run: test "$GITHUB_REF" = refs/heads/main
      - uses: actions/checkout@v5
      - run: php build.php --root "$GITHUB_WORKSPACE"
      - uses: actions/upload-artifact@v4
        with:
          name: report
          path: |
            report/
            ${{ runner.temp }}/x/
  remote:
    runs-on: ubuntu-latest
    steps:
      - run: ssh host true
'''

    def test_transform(self):
        out = promote.promote('synthetic.yml', self.SOURCE)
        self.assertIn('name: Cloud · Synthetic\n', out)
        self.assertNotIn('schedule', out)
        self.assertNotIn('cron', out)
        self.assertIn("    branches:\n      - main\n    paths:\n      - 'apps/cloud/**'\n"
                      "      - '.github/workflows/cloud-synthetic.yml'\n", out)
        self.assertIn("      - 'apps/cloud/tools/x/**'\n      - '.github/workflows/cloud-deploy.yml'\n"
                      "      - '.github/workflows/cloud-synthetic.yml'\n", out)
        self.assertIn('  first:\n    defaults:\n      run:\n        working-directory: apps/cloud\n', out)
        self.assertIn('      - name: Before checkout\n        working-directory: ${{ github.workspace }}\n', out)
        self.assertIn('--root "$GITHUB_WORKSPACE/apps/cloud"', out)
        self.assertIn('            apps/cloud/report/\n            ${{ runner.temp }}/x/\n', out)
        remote = out.split('  remote:\n', 1)[1]
        self.assertNotIn('working-directory', remote)
        self.assertEqual(out, promote.promote('synthetic.yml', self.SOURCE))
        backup = promote.promote('production-backup.yml', self.SOURCE)
        self.assertIn("  schedule:\n    - cron: '1 2 * * *'\n", backup)

    def test_refuses_unknown_shapes(self):
        for source in (self.SOURCE.replace('jobs:', 'defaults:\n  run:\n    shell: bash\n\njobs:'),
                       self.SOURCE.replace("      - 'tools/x/**'", "      - '!tools/x/**'"),
                       self.SOURCE.replace('--root "$GITHUB_WORKSPACE"', '--root $GITHUB_WORKSPACE/x'),
                       self.SOURCE.replace('\n', '\r\n')):
            with self.assertRaises(promote.PromotionError):
                promote.promote('synthetic.yml', source)


@unittest.skipUnless(MONOREPO, 'somente no monorepo jorgewreis/fokus')
class PromotedWorkflows(unittest.TestCase):
    def promoted(self, name):
        return (TOP / '.github/workflows' / ('cloud-' + name)).read_text(encoding='utf-8')

    def test_every_promoted_workflow_is_the_exact_generated_output(self):
        self.assertTrue(SOURCES)
        expected = promote.expected_outputs()
        present = sorted(p.name for p in (TOP / '.github/workflows').glob('cloud-*.yml'))
        self.assertEqual(present, sorted(expected))
        for name, text in expected.items():
            self.assertEqual((TOP / '.github/workflows' / name).read_text(encoding='utf-8'), text, name)

    def test_gate_code_names_match_promoted_files(self):
        import publication_gate
        import github_oidc
        self.assertEqual(publication_gate.WORKFLOW_FILE, 'cloud-security-homologation.yml')
        self.assertTrue((TOP / publication_gate.WORKFLOW_PATH).is_file())
        self.assertTrue((TOP / '.github/workflows' / github_oidc.DEPLOY_WORKFLOW_FILE).is_file())

    def test_publication_stays_manual_main_and_gated(self):
        deploy = self.promoted('deploy.yml')
        self.assertIn('      bootstrap_first_sealed_release:\n'
                      '        description: Accept only the current unsealed HTML 404 for the first sealed release\n'
                      '        required: false\n        default: false\n        type: boolean\n', deploy)
        job = deploy.split('\n  deploy:\n', 1)[1]
        self.assertIn("    if: github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main' && "
                      "needs.validate.result == 'success' && needs.classify.result == 'success' && "
                      "needs.classify.outputs.docs_only == 'false'\n", job)
        self.assertIn('    environment: production\n', job)
        self.assertIn('        run: python3 deploy/publication_gate.py\n', job)
        before_job = deploy.split('\n  deploy:\n', 1)[0]
        self.assertNotIn('secrets.', before_job)
        self.assertNotIn('environment:', before_job)

    def test_production_workflows_are_dispatch_only(self):
        for source in SOURCES:
            text = self.promoted(source.name)
            if source.name == 'production-backup.yml':
                self.assertIn('schedule:', on_block(text), source.name)
                self.assertEqual(events(text), ['schedule', 'workflow_dispatch'], source.name)
                continue
            self.assertNotIn('schedule:', on_block(text), source.name)
            if source.name == 'deploy.yml':
                continue
            if 'secrets.' in text or 'environment:' in text:
                self.assertEqual(events(text), ['workflow_dispatch'], source.name)

    def test_production_backup_supports_atomic_release_layout(self):
        backup = self.promoted('production-backup.yml')
        self.assertIn('$DEPLOY_PATH/current/deploy/export-database.php', backup)
        self.assertIn('$DEPLOY_PATH/shared/storage/app', backup)

    def test_automatic_triggers_are_scoped_to_the_cloud(self):
        for source in SOURCES:
            text = self.promoted(source.name)
            block = on_block(text)
            for event in ('push', 'pull_request'):
                body = re.search(rf'^  {event}:\n((?:    .*\n)*)', block, re.M)
                if not body:
                    continue
                paths = re.search(r"^    paths:\n((?:      - '.*'\n)+)", body.group(1), re.M)
                self.assertIsNotNone(paths, f'{source.name} {event} without paths')
                for value in re.findall(r"'([^']+)'", paths.group(1)):
                    self.assertTrue(value.startswith(('apps/cloud/', '.github/workflows/cloud-')),
                                    f'{source.name}: {value}')
                self.assertIn(f"'.github/workflows/cloud-{source.name}'", paths.group(1))


if __name__ == '__main__':
    unittest.main()
