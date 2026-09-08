"""Read-only input inventory. This does NOT identify or extract FDI formats."""
import argparse
import hashlib
import json
from pathlib import Path


def inspect(path, source_id):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise ValueError(f"Not a regular file: {path.name}")
    before = path.stat()
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError(f"Input changed during inspection: {path.name}")
    return {
        'source_id': source_id,
        'name': path.name,
        'bytes': after.st_size,
        'sha256': digest.hexdigest(),
        'container': 'unknown',
        'filesystem': 'unknown',
        'evidence': ['size and SHA-256 only; filename extension is not proof'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+', type=Path)
    parser.add_argument('--out', type=Path, help='New private JSON file; never overwrite')
    args = parser.parse_args()
    sources = [path.resolve(strict=True) for path in args.inputs]
    if args.out and args.out.resolve() in sources:
        parser.error('The output must not be an input file')
    report = {
        'schema_version': 1,
        'tool_scope': 'read-only inventory, no format detection or extraction',
        'inputs': [inspect(path, f'input-{i + 1}') for i, path in enumerate(sources)],
    }
    data = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open('x', encoding='utf-8') as handle:
            handle.write(data)
        print(f'Inventory written: {args.out}')
    else:
        print(data)


if __name__ == '__main__':
    main()
