# -*- coding: utf-8 -*-
"""zest.releaser hooks.

``uv.lock`` records the project's own version, so the version bump during a
release leaves the lock stale and ``uv sync --locked`` fails in CI. These
hooks write the version that zest.releaser is about to write, regenerate the
lock from it, and let zest.releaser commit both together.
"""
import re
import shutil
import subprocess

VERSION_LINE = re.compile(r"(?m)^version = '.*'$")


def lock_new_version(data):
    """Run before the "Preparing release" commit."""
    _lock_for(data['new_version'])


def lock_dev_version(data):
    """Run before the "Back to development" commit."""
    _lock_for(data['dev_version'])


def _lock_for(version):
    _set_version(version)
    uv = shutil.which('uv')
    if uv is None:
        raise RuntimeError(
            'uv is not installed, cannot refresh uv.lock for this release'
        )
    subprocess.check_call([uv, 'lock', '--quiet'])


def _set_version(version):
    """Write the version zest.releaser is about to write itself."""
    with open('pyproject.toml', encoding='utf-8') as pyproject:
        contents = pyproject.read()
    updated, replacements = VERSION_LINE.subn(
        "version = '{0}'".format(version), contents, count=1
    )
    if replacements != 1:
        raise RuntimeError('no version line found in pyproject.toml')
    with open('pyproject.toml', 'w', encoding='utf-8') as pyproject:
        pyproject.write(updated)
