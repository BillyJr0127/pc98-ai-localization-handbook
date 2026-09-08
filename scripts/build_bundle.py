"""Create a ZIP containing only the checked teaching allowlist."""
import argparse
import hashlib
import zipfile
from pathlib import Path

from check_handbook import ROOT, FILES, main as verify


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.resolve().is_relative_to(ROOT.resolve()):
        parser.error('Place the ZIP outside the teaching source directory')
    verify()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(FILES):
            archive.write(ROOT/name, 'pc98-ai-handbook/' + name)
    with zipfile.ZipFile(args.out) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == {'pc98-ai-handbook/' + name for name in FILES}
        for name in FILES:
            assert archive.read('pc98-ai-handbook/' + name) == (ROOT/name).read_bytes()
    print(f'{args.out.name}: {args.out.stat().st_size} bytes')
    print('SHA256:', hashlib.sha256(args.out.read_bytes()).hexdigest())
