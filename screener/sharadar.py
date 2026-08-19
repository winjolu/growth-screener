"""Alias to the shared Sharadar client in market-core.

The data layer moved out of this project once a second project started
using the same database. Two copies of a guard is worse than one: the
archival watermark, the refresh gap check and the read-only opens all
have to agree, and they cannot agree if each project keeps its own
version and fixes bugs locally.

This module rebinds itself so that `screener.sharadar` and
`market_core.sharadar` are the *same module object*, not two modules
with matching contents. That distinction is the whole point. A star
import would copy the names, so a test patching `screener.sharadar._get`
would leave `market_core.sharadar.fetch` still calling the real one —
which surfaces as a live HTTP error with nothing pointing at the cause.

Fix data-layer bugs in ~/market-data/market-core, never here.
"""
import sys

from market_core import sharadar as _shared

sys.modules[__name__] = _shared
