# Test register

Every test in this project, registered **before** it ran. This file is
the audit trail: it is what lets me say later which results survived
better data, and which ones I talked myself into.

The previous project's register is in `docs/legacy/test-register.md`,
kept for its format and its cautionary value. None of its conclusions
carry over.

## The bar

**t = 2.88.** One-sided Bonferroni at 25 arms (α = 0.05 / 25 = 0.002).
Harvey, Liu & Zhu argue 3.0 for anything claiming to be a published
finding.

The bar moves if the arm count moves. Twenty-five is a budget I am
choosing now, before the first arm, precisely so it cannot drift upward
one convenient arm at a time. If I need a twenty-sixth, I recompute the
bar and restate every earlier verdict against the new one.

The previous project ran 196 arms and nothing cleared either threshold.
That is the base rate I should expect here too.

## Arms used

```
budget    25
used       0
remaining 25
```

**Update this the moment an arm starts, not when it finishes.**
Reconstructing the count afterwards always undercounts — abandoned arms,
arms that errored halfway, and arms I decided were "just a look" are
exactly the ones that vanish from a retrospective tally, and exactly the
ones that inflate the false-positive rate.

## What spends an arm

An arm is **any run whose output could change what I believe about
returns.** That includes runs I abandon early, runs I don't write up,
and runs I tell myself are only a sanity check.

Infrastructure does not spend an arm, because no hypothesis about
returns is being tested:

- building and testing the point-in-time fundamentals harness
- computing what a benchmark returned
- verifying an arm completed, reconciling trade counts, data-quality checks

If in doubt, it spends an arm. The failure mode I am guarding against is
a generous reading of this section.

## Prefixes

| prefix | meaning |
|---|---|
| **I** | infrastructure — no hypothesis about returns, no budget cost |
| **B** | baseline or benchmark arm |
| **G** | growth signal arm |
| **H** | holdout — runs once, at the end, see `docs/holdout-seal.md` |

## Windows

```
development   through 2018-12-31
SEALED        2019-01-01 onwards
```

Every arm below runs on development data only. See
`docs/holdout-seal.md` — that seal is the reason any of this is worth
recording.

---

## Infrastructure

| id | what | status |
|---|---|---|
| I1 | Point-in-time fundamentals harness: `ARQ`/`ART` only, filtered on `datekey <= as_of`, never `calendardate`. Guard the 9 `ARQ` rows whose `datekey` precedes their `reportperiod`, and the 2.28% with a lag over 120 days. | not started |
| I2 | Benchmark returns through `portfolio_sim` with costs applied: VUG (default), IWF (for windows before 2004-01-30), SPY (always beside, never instead). | not started |
| I3 | Size filter that does not silently change definition mid-backtest. `dailyfundamentals` only starts 2016-01-04; before that, market cap comes from `fundamentals.marketcap` at `datekey`. | not started |

I1 is first and nothing runs before it. Restated fundamentals are
lookahead as pure as the retroactive entry fills that were once worth
the previous project's entire measured edge, and `MRQ`/`MRT`/`MRY` are
restated. This is defect number eight waiting to happen, and it is the
one specific to this fork.

## Arms

| id | registered | hypothesis | prediction | result |
|---|---|---|---|---|
| B1 | 2026-08-06 | The inherited trend-and-regime rule, run over a growth universe on development data, is the honest baseline a growth signal has to beat — not VUG, and certainly not SPY. | Lands near VUG. If it does, "beats SPY" is worth nothing here, and every later arm is measured against B1 and VUG both. | not run |

B1 is contaminated by construction, and that is the point. The rule was
fitted on this data, so its measured performance is flattered, so
requiring a growth signal to beat it is a *harder* test than it appears.
A prior may set the hurdle. It may not be a foundation — see
`docs/holdout-seal.md`.

### Not yet registered

Growth signals are not registered here until each one has a written
prediction specific enough to be wrong. Testing CANSLIM as a block would
repeat the mistake this codebase already disproved once: a nine-condition
checklist lost to a two-line rule, and CANSLIM is seven conditions. The
components go in one at a time, starting with earnings and revenue
acceleration — the best replicated of the set, and the one whose
provenance is external literature rather than this project's own data.

Note the budget arithmetic before registering any of them. Seven
components tested individually and then in combination does not fit in
25 arms.

Two things deliberately held back:

- **`MA_PERIOD = 30`** (`screener/conditions.py:201`) is an untested
  inherited constant, and the closing warning I carried across. It should
  be swept — but not before there is a growth signal worth sweeping it
  around, or I spend budget on the wrong axis.
- **Re-entry after a stop-out.** The most interesting unexplained result
  in the previous project and the least tested. It is an exit mechanism,
  independent of selection, so it can be tested later without
  contaminating the selection arms.

---

## Rules that earned their place

Carried over because each one caught something real.

- **Register the test before running it.** Registration is why I can
  tell which results survived better data. It is not a defence against
  contamination — that is what the holdout is for.
- **Print numbers, read them, then write what they mean.** Two of the
  worst errors in the previous project came from writing the conclusion
  into the script before the output existed.
- **Verify an arm is complete before reading it.** A partial arm reports
  complete-looking statistics. This was misread four times.
- **Two arms with identical results mean a broken experiment**, not an
  inert change.
- **Score the ride, not just the destination.** Martin ratio and weeks
  under water beside CAGR. Return alone once hid that the untuned
  baseline beat the tuned version.
- **Check the worst case after any change to which trades qualify.**
  Three stop-placement defects were invisible in the mean.
- **Never report a result without the benchmark beside it**, and report
  SPY beside whichever benchmark I chose, so the comparison is never
  only against the flattering one.
- **Probe an interface before building on it.**
