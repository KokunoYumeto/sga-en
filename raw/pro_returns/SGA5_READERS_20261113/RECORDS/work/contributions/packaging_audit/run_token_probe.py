#!/usr/bin/env python3
"""Replay the small folio 248 TeX token witness in the active TeX environment."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess

from audit_packages import PATTERNS

OUT = Path('work/contributions/validation_fr')
PROBE = OUT / 'folio248_token_boundary_probe.tex'
EXPECTED = [
    'COMMENT_ENDLINE_DISCARDED=PASS', 'FIRST_ARGUMENT_BEGIN', 'LEADING_SPACE=PASS',
    'NO_PAR_TOKEN=PASS', 'FIRST_ARGUMENT_END', 'SECOND_ARGUMENT_EMPTY=PASS',
    'FOLLOWING_INPUT_BEGIN', 'LEADING_SPACE=PASS', 'NO_PAR_TOKEN=PASS', 'FOLLOWING_INPUT_END',
]


def main():
    metadata = json.loads((OUT / 'folio248_probe_input.json').read_text())
    assert hashlib.sha256(PROBE.read_bytes()).hexdigest() == metadata['probe_sha256']
    command = ['pdftex', '-ini', '-interaction=nonstopmode', '-halt-on-error',
               '-output-directory=' + OUT.as_posix(), PROBE.as_posix()]
    env = os.environ.copy()
    env.update({'SOURCE_DATE_EPOCH': '1794528000', 'FORCE_SOURCE_DATE': '1'})
    run = subprocess.run(command, capture_output=True, text=True, env=env)
    log = PROBE.with_suffix('.log').read_text()
    # This minimal INITEX proof loads no package tree. It is retained verbatim
    # only after the same private-value screen used for the final archives.
    assert not [(name, match.group(0)) for name, pattern in PATTERNS for match in pattern.finditer(log)]
    observed = [line for line in log.splitlines() if line in set(EXPECTED) or '=FAIL' in line]
    assert run.returncode == 0 and observed == EXPECTED
    print(json.dumps({'command': command, 'exit_code': run.returncode,
                      'observations': observed, 'all_observations_match': True,
                      'probe_sha256': metadata['probe_sha256'],
                      'log_sha256': hashlib.sha256(PROBE.with_suffix('.log').read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
