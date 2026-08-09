"""Settings for the test suite: no external services required.

sqlite + locmem mean `uv run pytest` works on a fresh checkout with
nothing else running. The suite intentionally diverges from the
postgres/redis production stack here; the codebase has no
postgres-specific model fields.
"""

import shutil
from pathlib import Path

# base.py reads variables.txt; a fresh checkout only has the sample.
_settings_dir = Path(__file__).resolve().parent
if not (_settings_dir / "variables.txt").exists():
    shutil.copy(
        _settings_dir / "variables.sample.txt", _settings_dir / "variables.txt"
    )

from .dev import *  # noqa: E402, F401, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
