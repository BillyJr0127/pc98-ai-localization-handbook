"""Tiny synthetic demonstrations; not a game validator or full MIDI parser."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def real_time_ok(case, minimum, maximum):
    if case['wall_seconds'] <= 0 or case['audio_seconds'] < 0:
        raise ValueError('Invalid duration')
    ratio = case['audio_seconds'] / case['wall_seconds']
    return minimum <= ratio <= maximum and case['underruns'] == 0


def active_notes(events):
    """Strict note-only fixture: reject everything this example cannot model."""
    active = set()
    previous = -1
    for event in events:
        if event['t'] < previous:
            raise ValueError('Events must be ordered')
        previous = event['t']
        data = event['bytes']
        if len(data) != 3 or data[0] & 0xf0 not in (0x80, 0x90):
            raise ValueError('Example supports decoded note messages only')
        if not all(isinstance(x, int) and 0 <= x <= 127 for x in data[1:]):
            raise ValueError('Invalid MIDI data byte')
        if not 0x80 <= data[0] <= 0x9f:
            raise ValueError('Invalid status')
        key = (data[0] & 0x0f, data[1])
        on = data[0] & 0xf0 == 0x90 and data[2] != 0
        if on:
            if key in active:
                raise ValueError('Overlapping same-key notes are outside this fixture')
            active.add(key)
        else:
            if key not in active:
                raise ValueError('Unmatched release')
            active.remove(key)
    return active


def placeholders(text):
    return Counter(re.findall(r'\{[A-Za-z_][A-Za-z_0-9]*\}', text))


def main():
    audio = json.loads((ROOT/'examples/audio.json').read_text(encoding='utf-8'))
    window = audio['performance_window']
    assert window['same_start_and_end_events']
    for case in audio['performance_cases']:
        result = real_time_ok(case, window['acceptable_ratio_min'], window['acceptable_ratio_max'])
        assert result == case['expected_pass'], case['id']
    events = audio['midi_fixture']['events']
    assert len(active_notes(events)) == 0
    assert len(active_notes(events[:-1])) == 1
    for invalid in ([{'t': 0, 'bytes': [0xb0, 64, 127]}], list(reversed(events))):
        try:
            active_notes(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('Unsupported/out-of-order data was silently accepted')
    text = json.loads((ROOT/'examples/text.json').read_text(encoding='utf-8'))
    for record in text['records']:
        assert placeholders(record['source']) == placeholders(record['translation']), record['id']
    bad = text['deliberately_bad_translation']
    original = next(r for r in text['records'] if r['id'] == bad['id'])
    assert placeholders(original['source']) != placeholders(bad['translation'])
    print('PASS: zero-underrun slowdown, fast playback, missing note release, unsupported MIDI, and placeholder mismatch detected.')
    print('Scope: synthetic fixtures only. No real game, sound device or full MIDI implementation was tested.')


if __name__ == '__main__':
    main()
