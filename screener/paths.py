"""Where this project writes things — bound to the shared implementation.

The logic lives in market_core.paths, parameterised by app name so each
project keeps its own directory and its own environment variables. This
module is the binding, and exists only to supply the two things the
shared package cannot know: which app this is, and where this checkout
starts.

Keeping the logic here was the same mistake that put a second copy of
the Sharadar client in the project — recurring, pointedly, inside the
module written to stop files being written into a synced folder. A third
project would have invented a third naming convention.

`inside_checkout` takes the repository root explicitly. Deriving it from
__file__ inside the shared package would measure market-core's own
directory, so every path in every project would test as outside it and
the check would pass for everything, forever, while looking installed.

Nothing here is project-specific except APP and REPO. Fix path bugs in
market-core.
"""
import os

from market_core import paths as _paths

APP = "growth-screener"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def data_dir():
    return _paths.data_dir(APP)


def data_file(name, env=None):
    return _paths.data_file(APP, name, env=env)


def inside_checkout(path):
    return _paths.inside_checkout(path, REPO)
