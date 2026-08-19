"""Runtime output must not land inside the checkout.

This repository lives in a synced Drive folder. A sync client uploading
a SQLite file mid-transaction cost the sibling project a four-hour sweep
to a lock timeout, roughly tripled arm runtimes, and left two arms short
by 961 and 40,945 rows that were never accounted for. A backtest opens
one write transaction per trade, so that collision window is effectively
always open.

Written-down conventions did not prevent it there. A failing test is the
only thing that has.
"""
import os
import tempfile
import unittest

from screener import bar_cache, db, paths


class WriteLocationTest(unittest.TestCase):
    def test_the_results_database_is_outside_the_checkout(self):
        self.assertFalse(
            paths.inside_checkout(db.DB_PATH),
            f"results database is inside the synced checkout: {db.DB_PATH}")

    def test_the_bar_cache_is_outside_the_checkout(self):
        self.assertFalse(
            paths.inside_checkout(bar_cache.CACHE_PATH),
            f"bar cache is inside the synced checkout: {bar_cache.CACHE_PATH}")

    def test_inside_checkout_recognises_a_path_that_is_inside(self):
        # Otherwise the two tests above pass by never returning True.
        here = os.path.abspath(__file__)
        self.assertTrue(paths.inside_checkout(here))

    def test_a_sibling_directory_is_not_mistaken_for_the_checkout(self):
        # Prefix matching without the separator would count
        # growth-screener-scratch as inside growth-screener.
        repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assertFalse(paths.inside_checkout(repo + "-scratch/file.db"))


class TestIsolationTest(unittest.TestCase):
    """The suite must not write to the real results database.

    tests/test_backtest.py calls run_backtest without redirecting
    DB_PATH, so every run was writing fake arms — parameter_set
    "test_shortrunner" and friends — into the live table that the report
    tooling aggregates. tests/__init__.py redirects the whole session;
    this is what notices if that ever stops happening.
    """

    def test_the_results_database_is_a_sandbox_during_tests(self):
        self.assertNotEqual(
            db.DB_PATH, paths.data_file("screener.db", env="GROWTH_SCREENER_DB"),
            "tests are pointed at the real results database")

    def test_the_sandbox_is_a_temporary_directory(self):
        import tempfile
        self.assertTrue(
            db.DB_PATH.startswith(tempfile.gettempdir()),
            f"test database is not in a temporary directory: {db.DB_PATH}")


class OverrideTest(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in
                       ("GROWTH_SCREENER_DATA_DIR", "GROWTH_SCREENER_DB")}

    def tearDown(self):
        for k, v in self._saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_the_directory_override_moves_everything(self):
        # Built rather than written literally: a quoted absolute path in a
        # tracked file is what test_portability exists to reject, and an
        # exemption here would blunt it for everything else too.
        somewhere = os.path.join(tempfile.gettempdir(), "somewhere")
        os.environ["GROWTH_SCREENER_DATA_DIR"] = somewhere
        self.assertEqual(paths.data_file("screener.db"),
                         os.path.join(somewhere, "screener.db"))

    def test_a_per_file_override_wins_over_the_directory(self):
        somewhere = os.path.join(tempfile.gettempdir(), "somewhere")
        elsewhere = os.path.join(tempfile.gettempdir(), "elsewhere", "other.db")
        os.environ["GROWTH_SCREENER_DATA_DIR"] = somewhere
        os.environ["GROWTH_SCREENER_DB"] = elsewhere
        self.assertEqual(
            paths.data_file("screener.db", env="GROWTH_SCREENER_DB"), elsewhere)

    def test_a_tilde_in_an_override_is_expanded(self):
        os.environ["GROWTH_SCREENER_DATA_DIR"] = "~/somewhere"
        self.assertTrue(paths.data_file("x.db").startswith(os.path.expanduser("~")))


if __name__ == "__main__":
    unittest.main()
