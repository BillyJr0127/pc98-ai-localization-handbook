"""An executable synthetic adapter and explicit, unimplemented game build boundary."""
import hashlib
import json
import re
from pathlib import Path
from typing import Protocol


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def literal(value):
    require(isinstance(value, str) and 0 < len(value) <= 30000,
            'Expected nonempty text of at most 30000 characters')
    require(not any(ord(c) < 32 and c != '\n' for c in value), 'Unsupported control character')
    require(not any(0xD800 <= ord(c) <= 0xDFFF or ord(c) in (0xFFFE, 0xFFFF)
                    for c in value), 'Unsupported Unicode character')
    return value


class ExchangeAdapter(Protocol):
    """Adapters must validate against immutable originals, not only a sidecar."""
    catalog: dict
    occurrences: dict
    fingerprint: str

    def split_translation(self, occurrence: dict, translation: str) -> list[str]:
        """Validate boundaries/tokens/newlines; return exactly the original call count."""
        ...


class GameBuildAdapter(Protocol):
    """NOT implemented by this teaching package. Methods must fail on unmet contracts."""

    def extract(self, originals: Path) -> ExchangeAdapter:
        """Parse actual scripts, group safe text nodes, bind source and control hashes."""
        ...

    def plan_glyphs(self, candidate: dict, previous: dict) -> dict:
        """Use the build's allocator/rasterizer; preserve existing codes; reject missing glyphs."""
        ...

    def encode(self, occurrence: dict, parts: list[str], glyphs: dict) -> bytes:
        """Check VM byte restrictions and decoding identity, not merely codec support."""
        ...

    def build_staged(self, candidate: dict, glyphs: dict, staging: Path) -> dict:
        """Build into fresh staging; return file hashes; never write originals or saves."""
        ...

    def verify_staged(self, staging: Path, manifest: dict) -> dict:
        """Read with original decoders; check controls/fonts; emit bounded evidence."""
        ...


class SyntheticAdapter:
    """Only a self-authored JSON catalog. No FDI, script parser, glyphs or DOS compiler."""
    def __init__(self, catalog):
        require(catalog.get('schema') == 1 and
                catalog.get('adapter') == 'synthetic-single-call-v1', 'Unknown catalog schema/adapter')
        require(isinstance(catalog.get('occurrences'), list) and
                0 < len(catalog['occurrences']) <= 100000, 'Invalid catalog size')
        self.catalog = catalog
        self.occurrences = {}
        for occurrence in catalog['occurrences']:
            require(set(occurrence) == {'id', 'source', 'mode'}, 'Unexpected occurrence fields')
            oid = occurrence['id']
            require(isinstance(oid, str) and re.fullmatch(r'[a-z0-9_-]+/[a-z0-9_-]+:T[0-9]{5}', oid),
                    'Invalid synthetic position ID (IDs are never filesystem paths)')
            require(oid not in self.occurrences, 'Duplicate position ID')
            literal(occurrence['source'])
            require(occurrence['mode'] == 'single', 'Synthetic adapter supports single calls only')
            self.occurrences[oid] = occurrence
        self.fingerprint = digest(catalog)

    def split_translation(self, occurrence, translation):
        literal(translation)
        source = occurrence['source']
        require(re.findall(r'\{[^{}]*\}', translation) == re.findall(r'\{[^{}]*\}', source),
                'Dynamic tokens must retain their order and count')
        require(translation.count('{') == source.count('{') and
                translation.count('}') == source.count('}'), 'Changed token braces')
        require(translation.count('\n') == source.count('\n'), 'Changed newline count')
        return [translation]
