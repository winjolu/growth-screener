"""Test package setup.

Point the results database at a throwaway directory for the whole
session, before any test module is imported.

This is not hypothetical tidiness. tests/test_backtest.py calls
run_backtest without redirecting db.DB_PATH, so every run of the suite
was writing fake arms — parameter_set "test_shortrunner" and friends —
into the real results database. Both projects key backtest_trades on
parameter_set, and the report tooling aggregates whatever rows it finds,
so invented arms sat in the same table as measured ones.

Doing it here rather than in three setUp methods means a test added
later inherits the isolation instead of having to remember it. Modules
that redirect DB_PATH themselves still work: they save and restore
around whatever they find.
"""
import atexit
import os
import tempfile

from screener import db

_SANDBOX = tempfile.TemporaryDirectory(prefix="growth-screener-tests-")
db.DB_PATH = os.path.join(_SANDBOX.name, "screener.db")
db._schema_ready_for = None

atexit.register(_SANDBOX.cleanup)
