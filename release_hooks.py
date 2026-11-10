# -*- coding: utf-8 -*-
"""zest.releaser hooks.

uv records the project's own version in ``uv.lock``, so a version bump
leaves the lock stale and ``uv sync --locked`` fails in CI. These hooks
regenerate the lock after the new version is written and before
zest.releaser commits it.
"""
import shutil
import subprocess


def uv_lock(data):
    """Regenerate uv.lock so the release commit stays consistent."""
    uv = shutil.which('uv')
    if uv is None:
        raise RuntimeError(
            'uv is not installed, cannot refresh uv.lock for this release'
        )
    subprocess.check_call([uv, 'lock'])
