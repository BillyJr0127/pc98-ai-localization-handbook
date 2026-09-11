"""Validate the teaching-only package, links, examples and read-only inventory."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from build_handbook import ROOT, render

FILES = {
    '.gitignore', '.gitattributes', 'LICENSE', 'README.md', 'AGENTS.md', 'AI-HANDBOOK.md', 'AI-GUIDE.md',
    'WORKFLOW.md', 'AUDIO.md', 'VALIDATION.md', 'LESSONS.md', 'FOLLOW-UP.md', 'RIGHTS.md', 'SOURCES.md', 'CHANGELOG.md',
    'templates/PROJECT.json', 'templates/AUDIO-PROFILE.json', 'templates/STATUS.md',
    'templates/ISSUE.json', 'templates/RELEASE.json', 'examples/text.json', 'examples/audio.json', 'examples/binary.json',
    'scripts/inspect_inputs.py', 'scripts/check_examples.py', 'scripts/check_binary_examples.py', 'scripts/build_handbook.py',
    'scripts/check_handbook.py', 'scripts/build_bundle.py',
    'FAST-PORT.md', 'TEXT-ROUNDTRIP.md', 'requirements.txt', 'templates/ENGINE-ADAPTER.md',
    'examples/translation-catalog.json', 'scripts/engine_adapter.py', 'scripts/translation_exchange.py',
    'scripts/export_workbook.py', 'scripts/import_workbook.py', 'scripts/check_translation_workflow.py',
}


def run(*args, expected=0):
    result = subprocess.run([sys.executable, '-X', 'utf8', *map(str, args)], capture_output=True, text=True, encoding='utf-8')
    if expected == 0:
        assert result.returncode == 0, result.stdout + result.stderr
    else:
        assert result.returncode != 0, 'Expected a rejected operation'
    return result


def main():
    actual = set()
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if '.git' in relative.parts or '__pycache__' in relative.parts:
            continue
        assert not path.is_symlink(), f'Symlink not allowed: {relative}'
        if path.is_file():
            actual.add(relative.as_posix())
    assert actual == FILES, {'unexpected': sorted(actual - FILES), 'missing': sorted(FILES - actual)}
    for name in FILES:
        text = (ROOT/name).read_text(encoding='utf-8')
        assert '\x00' not in text, name
        assert not re.search(r'[A-Za-z]:[/\\](?:Users|codex)[/\\]', text), f'Private path: {name}'
        assert not re.search(r'(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}', text), f'Credential pattern: {name}'
        if name.endswith('.json'):
            json.loads(text)
        if name.endswith('.md'):
            assert len(re.findall(r'^```', text, re.M)) % 2 == 0, f'Unclosed fence: {name}'
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                if target.startswith(('https://', 'http://', '#')):
                    continue
                resolved = ((ROOT/name).parent/target.split('#')[0]).resolve()
                assert resolved.is_relative_to(ROOT.resolve()) and resolved.is_file(), (name, target)
    assert (ROOT/'AI-HANDBOOK.md').read_text(encoding='utf-8') == render(), 'Rebuild the single-file handbook'
    run(ROOT/'scripts/check_examples.py')
    run(ROOT/'scripts/check_binary_examples.py')
    run(ROOT/'scripts/check_translation_workflow.py')
    # Self-created bytes only; verify reading, hash accuracy and both overwrite guards.
    with tempfile.TemporaryDirectory(prefix='pc98-handbook-check-') as folder:
        temp = Path(folder)
        source = temp/'synthetic-input.dat'
        data = b'Self-created test data\x00\x01\x02'
        source.write_bytes(data)
        output = temp/'inventory.json'
        run(ROOT/'scripts/inspect_inputs.py', source, '--out', output)
        entry = json.loads(output.read_text(encoding='utf-8'))['inputs'][0]
        assert entry['sha256'] == hashlib.sha256(data).hexdigest()
        assert entry['container'] == entry['filesystem'] == 'unknown'
        assert source.read_bytes() == data
        output_before = output.read_bytes()
        run(ROOT/'scripts/inspect_inputs.py', source, '--out', output, expected=1)
        run(ROOT/'scripts/inspect_inputs.py', source, '--out', source, expected=1)
        assert source.read_bytes() == data and output.read_bytes() == output_before
    print(json.dumps({'teaching_files': len(FILES), 'links_and_json_valid': True,
                      'single_file_current': True, 'synthetic_examples_pass': True,
                      'inventory_is_read_only': True, 'allowlist_pass': True,
                      'legal_clearance_claimed': False}, indent=2))


if __name__ == '__main__':
    main()
