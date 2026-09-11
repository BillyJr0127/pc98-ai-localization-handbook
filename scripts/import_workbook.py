"""Validate an XLSX batch and write a NEW candidate JSON; never compile or modify a game."""
import argparse
import zipfile
from pathlib import Path
from engine_adapter import SyntheticAdapter
from translation_exchange import LANGUAGES, import_candidate, read_json, write_new_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('catalog', type=Path)
    parser.add_argument('workbook', type=Path)
    parser.add_argument('--language', choices=LANGUAGES, default='zh-TW')
    parser.add_argument('--state', type=Path, help='Previous language-state JSON; read only')
    parser.add_argument('--out', required=True, type=Path, help='New candidate JSON; no overwrite')
    parser.add_argument('--clear-blank', action='store_true', help='Clear blank unit rows in this batch only')
    args = parser.parse_args()
    try:
        candidate = import_candidate(SyntheticAdapter(read_json(args.catalog)), args.workbook,
                                     args.language, read_json(args.state) if args.state else None,
                                     args.clear_blank)
        write_new_json(args.out, candidate)
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        parser.exit(1, f'{error}\n')
    print('Candidate state written. No game build, font generation or installation was performed.')


if __name__ == '__main__':
    main()
