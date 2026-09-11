"""Export self-authored normalized text to a fresh directory of XLSX/map pairs."""
import argparse
from pathlib import Path
from engine_adapter import SyntheticAdapter
from translation_exchange import export_workbooks, read_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('catalog', type=Path)
    parser.add_argument('--out', required=True, type=Path, help='New directory; must not already exist')
    parser.add_argument('--state', type=Path)
    parser.add_argument('--rows-per-book', type=int, default=10000)
    args = parser.parse_args()
    try:
        manifest = export_workbooks(SyntheticAdapter(read_json(args.catalog)), args.out,
                                    read_json(args.state) if args.state else None, args.rows_per_book)
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')
    print(f'Exported {len(manifest["books"])} workbook(s); original catalog unchanged.')


if __name__ == '__main__':
    main()
