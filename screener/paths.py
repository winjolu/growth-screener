"""Where this project writes things.

Nothing written during a run belongs inside the checkout. This one lives
in a synced Drive folder, and a sync client uploading a SQLite file
mid-transaction is not a theoretical hazard: on the sibling project it
killed a four-hour sweep on a lock timeout, roughly tripled arm
runtimes, and left two arms short by 961 and 40,945 rows with no
accounting for where they went. A backtest writes one transaction per
trade, so the window for that collision is open more or less
continuously.

Results and caches therefore live under the user data directory. Each
has an environment override, and GROWTH_SCREENER_DATA_DIR moves all of
them at once — useful for pointing a run at a scratch disk, and for
tests.

The market archive is unaffected either way. It is read-only, it is not
in a synced folder, and it is nobody's output.
"""
import os
import sys

APP = "growth-screener"


def data_dir():
    """The directory for everything this project writes."""
    override = os.environ.get("GROWTH_SCREENER_DATA_DIR")
    if override:
        return os.path.expanduser(override)
    if sys.platform == "darwin":
        return os.path.expanduser(f"~/Library/Application Support/{APP}")
    # Linux and anything else: XDG, falling back to its documented default.
    base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(base, APP)


def data_file(name, env=None):
    """Full path for a file this project writes.

    `env` names a per-file override, which wins over the directory-wide
    one so a single artefact can be relocated without moving the rest.
    """
    if env:
        override = os.environ.get(env)
        if override:
            return os.path.expanduser(override)
    return os.path.join(data_dir(), name)


def inside_checkout(path):
    """True if `path` sits within this repository.

    Used by the tests that keep runtime output out of the synced folder.
    """
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.abspath(path).startswith(repo + os.sep)
