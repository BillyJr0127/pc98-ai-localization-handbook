"""Synthetic character-boundary and reflow examples; no game files are read."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def field_end(data, start, limit, profile):
    """Parse only the fixture's two-byte text subset, bounded by [start, limit)."""
    if not 0 <= start < limit <= len(data):
        raise ValueError('Invalid field bounds')
    position = start
    while position < limit:
        lead = data[position]
        if lead == profile['terminator']:
            return position
        if not profile['lead_min'] <= lead <= profile['lead_max']:
            raise ValueError('Not an admitted text lead byte')
        if position + 1 >= limit:
            raise ValueError('Truncated two-byte character')
        trail = data[position + 1]
        if not (0x40 <= trail <= 0x7e or 0x80 <= trail <= 0xfc):
            raise ValueError('Invalid trail byte')
        position += 2
    raise ValueError('No standalone terminator in field')


def control_skeleton(nodes):
    """Drop text payloads only; merge adjacent plain display nodes, nothing else."""
    result = []
    for node in nodes:
        if node.get('op') == 'text':
            if set(node) != {'op', 'value'} or not isinstance(node['value'], str):
                raise ValueError('Unsupported display node')
            marker = {'op': 'text'}
            if not result or result[-1] != marker:
                result.append(marker)
        else:
            result.append(node.copy())
    return result


def rejected(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError('Malformed fixture was accepted')


def main():
    fixture = json.loads((ROOT/'examples/binary.json').read_text(encoding='utf-8'))
    profile = fixture['profile']
    data = bytes.fromhex(fixture['valid_field_hex'])
    actual = field_end(data, 0, len(data), profile)
    assert actual == fixture['expected_end_offset']
    # Demonstrate the legacy bug rather than merely asserting our own parser.
    naive = data.index(profile['terminator'])
    assert naive == fixture['expected_naive_end_offset'] and naive != actual
    for case in fixture['invalid_fields']:
        value = bytes.fromhex(case['hex'])
        rejected(lambda: field_end(value, 0, len(value), profile))
    rejected(lambda: field_end(data, 0, 1, profile))
    rejected(lambda: field_end(data, 0, len(data) - 1, profile))
    rejected(lambda: field_end(data, -1, len(data), profile))
    rejected(lambda: field_end(data, 0, len(data) + 1, profile))
    framed = b'\x7d\x00' + data + b'\x7d'
    assert field_end(framed, 2, 2 + len(data), profile) == 2 + actual
    original = control_skeleton(fixture['original_nodes'])
    reflow = fixture['reflowed_nodes']
    assert original == control_skeleton(reflow)
    for removed in ('wait', 'page', 'sound'):
        broken = [node for node in reflow if node['op'] != removed]
        assert original != control_skeleton(broken), removed
    changed_wait = [dict(node, ticks=1) if node['op'] == 'wait' else node for node in reflow]
    assert original != control_skeleton(changed_wait)
    print('PASS: trail-byte terminator bug, truncated field, invalid byte, VM lead mismatch, and lost control boundaries detected.')
    print('Scope: synthetic fixtures only; this is not a Shift-JIS decoder, script compiler, or game validator.')


if __name__ == '__main__':
    main()
