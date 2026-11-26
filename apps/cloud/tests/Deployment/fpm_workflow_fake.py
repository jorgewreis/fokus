"""Executable SSH/SCP/rsync/curl doubles for actual workflow-shell tests, no network."""
import json
import os
from pathlib import Path
import runpy
import shlex
import subprocess
import urllib.parse
import sys

state_path = Path(os.environ['FPM_WORKFLOW_STATE'])
state = json.loads(state_path.read_text())
program = os.environ['FPM_FAKE_PROGRAM']
args = sys.argv[1:]
if program == 'python3':
    if args[0] == 'tools/ci/verify-deployment.py':
        assert args[1:] == ['verify']
        previous = os.environ['EXPECTED_RELEASE'] == 'b' * 40
        state['events'].append(['previous-http-verify' if previous else 'http-verify'])
        state_path.write_text(json.dumps(state))
        module = runpy.run_path(args[0], run_name='fixture_verify')
        def fetch(url, timeout):
            if url.endswith('/up'):
                if previous and state['scenario'] == 'previous_unhealthy':
                    return 503, {}, b'unhealthy'
                return 200, {}, b'healthy'
            nonce = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)['deploy_probe'][0]
            mismatched = {'http_old_sha', 'unsealed_previous', 'invalid_recovery_receipt', 'rollback_refused', 'previous_unhealthy'}
            release = 'b' * 40 if not previous and state['scenario'] in mismatched else os.environ['EXPECTED_RELEASE']
            headers = {'content-type': 'application/json', 'cache-control': 'no-store'}
            if not previous and state['scenario'] == 'http_cached': headers['cache-control'] = 'public, max-age=600'
            return 200, headers, json.dumps({'status': 'ok', 'release': release, 'probe': nonce}).encode()
        module['verify'].__kwdefaults__.update(fetcher=fetch, sleeper=lambda seconds: None)
        sys.exit(module['main'](['verify']))
    if args[0] == 'tools/ci/summarize-deployment.py':
        state['events'].append(['summary'])
        state_path.write_text(json.dumps(state))
    os.execv(sys.executable, [sys.executable, *args])
if program == 'sudo':
    assert args == ['-n', '--', '/usr/bin/systemctl', 'reload', '--', state['service']]
    state['events'].append(['sudo', *args])
    state_path.write_text(json.dumps(state))
    first_reload = sum(event[:3] == ['sudo', '-n', '--'] for event in state['events']) == 1
    sys.exit(1 if state['scenario'] == 'reload_denied' or (state['scenario'] == 'reload_once_failed' and first_reload) else 0)
if program == 'ssh' and args[-1].startswith('LC_ALL=C '):
    assert args[:-1] == [
        '-p', '2222', '-o', 'ConnectionAttempts=1', '-o', 'BatchMode=yes',
        '-o', 'ConnectTimeout=15', '-o', 'StrictHostKeyChecking=yes',
        'fixture@fixture.invalid']
    command = shlex.split(args[-1])
    if command[1:4] == ['bash', '-s', '--']:
        assert command == ['LC_ALL=C', 'bash', '-s', '--', 'reload', state['service']]
        script = sys.stdin.read()
        assert script == Path('deploy/reload-runtime.sh').read_text()
        state['events'].append(['runtime-script', state['service']])
        state_path.write_text(json.dumps(state))
        result = subprocess.run(['bash', '-s', '--', 'reload', state['service']], input=script, text=True)
        sys.exit(result.returncode)
    # Reuse every existing guard scenario after checking the real CLI transport.
    sys.argv = ['fpm_fake_ssh.py', str(state_path), '-o', 'BatchMode=yes',
                '-o', 'ConnectTimeout=15', '-o', 'StrictHostKeyChecking=yes',
                'fixture.invalid', args[-1]]
    runpy.run_path(str(Path(__file__).resolve().with_name('fpm_fake_ssh.py')), run_name='__main__')
    sys.exit(0)
if program == 'ssh':
    assert args[-2] == 'fixture@fixture.invalid'
    assert args[args.index('-p') + 1] == '2222'
    event = ['workflow-ssh', args[-1]]
    # The existing workflow polls a synthetic Composer status via SSH.
    if args[-1].startswith("test -f '/tmp/fokuscloud-composer-install.status'"):
        print('0')
elif program == 'rsync':
    destination = args[-1]
    # The active application root is not a transfer target. Only a new release directory is.
    assert destination.startswith('fixture@fixture.invalid:/srv/fixture/releases/')
    assert not destination.rstrip('/').endswith('/srv/fixture')
    event = [program, *args]
elif program == 'scp':
    assert args[-1].startswith('fixture@fixture.invalid:/tmp/fokuscloud-law-schema-')
    event = [program, *args]
elif program == 'curl':
    assert 'https://api.cloudflare.com/client/v4/zones/fixture-zone/purge_cache' in args
    event = ['purge']
else:
    raise AssertionError(program)
state['events'].append(event)
state_path.write_text(json.dumps(state))
if state['scenario'] == 'schema_failure' and program == 'ssh' and 'mkdir -m 700' in args[-1]:
    sys.exit(1)
if program == 'ssh' and 'atomic_publisher.py' in args[-1]:
    if ' rollback ' in args[-1]:
        assert '--report-previous' in args[-1] and 'StrictHostKeyChecking=yes' in args
        if state['scenario'] == 'rollback_refused':
            sys.exit(1)
        if state['scenario'] == 'invalid_recovery_receipt':
            print('unrecognized receipt')
            sys.exit(0)
        print('atomic_rollback=restored_previous_release')
        print('previous_release=' + ('unsealed' if state['scenario'] == 'unsealed_previous' else 'b' * 40))
    elif ' switch ' in args[-1] and state['scenario'] == 'switch_uncertain':
        sys.exit(255)
