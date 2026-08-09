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
budget       25
started       0
registered    4      B1, and B2 as three policies
uncommitted  21
```

`started` is the number that governs the bar. `registered` is what is
already spoken for before a single growth condition has been written
down — worth keeping in view, because 21 remaining is the real room, not
25.

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
| I2 | Benchmark returns through `portfolio_sim` with costs applied, for every member of the alternatives set (see below). | not started |
| I3 | Size filter that does not silently change definition mid-backtest. `dailyfundamentals` only starts 2016-01-04; before that, market cap comes from `fundamentals.marketcap` at `datekey`. | not started |
| I4 | Does a growth fund hold up better than SPY in a down market? | **resolved 2026-08-06 — no, and the obvious way to ask flatters growth** |
| I5 | Can the Motley Fool record be used as a fourth alternative, point-in-time? | **resolved 2026-08-06 — yes, as their own ETFs, but not until the seal lifts** |

### I4 — the benchmark window is a lever, so it is fixed here

I asked whether idle capital was better parked in a growth fund than in
SPY. On VUG's own history the answer looked like yes:

| 2004-01-30 to 2018-12-31 | CAGR | worst drawdown | downside capture |
|---|---|---|---|
| VUG | +8.34% | -50.7% | 97.2% |
| SPY | +7.58% | -55.2% | — |

VUG's history starts 2004-01-30. **The dot-com crash is not in it.** That
is the single worst episode for growth, and measuring growth over a
window that begins after it is not a neutral choice. IWF goes back to
2000-05-26:

| 2000-05-26 to 2018-12-31 | CAGR | worst drawdown | downside capture |
|---|---|---|---|
| IWF | +4.02% | **-64.2%** | 101.2% |
| SPY | +5.23% | -55.2% | — |

Growth lost to SPY by 12.9 points in 2000, 6.0 in 2001 and 6.4 in 2002,
and fell nine points further at the trough. Both runs stop before
2019-01-01; the seal was not touched.

Two consequences, and the second matters more than the question I asked.

**The alternatives set, and the hurdle is the best of it.** The system is
worth running only if it beat the best thing I could have bought instead
over the same window. So the hurdle is the *maximum* of `{SPY, IWF,
cash at the prevailing rate}`, whichever wins that particular window —
not a benchmark named in advance. Naming one in advance is a lever: on
VUG's window I would have declared victory over a comparator that SPY
itself beat. IWF replaces VUG as the growth member because its history
covers the full development window without splicing, and a benchmark
that changes definition partway through a backtest is the same defect
as a size filter that does. VUG is still reported as the cheaper modern
option; it is just not the yardstick.

**"Growth beats the market" is a claim about one decade.** IWF
underperformed SPY across 2000-2018. The decade that makes growth look
good sits mostly inside the sealed window. That is a caution about this
project's entire premise, and I could reach it without breaking the
seal.

Parking policy stays binary — cash when the gate is off, SPY when the
gate is on and there is nothing to buy. Adding a growth fund as a third
parking option trades an edge under a point a year for nine points of
extra drawdown at exactly the moment a regime gate is least reliable.

### I5 — the Motley Fool comparison, and why it waits

The question was whether "did this beat blindly following the Motley
Fool" can be answered point-in-time. It can, and without scraping a
paywalled pick list: they run their own ETFs, and Sharadar already
carries eight of them with survivorship-free daily prices.

| ticker | fund | usable before the seal | total bars |
|---|---|---|---|
| TMFC | Motley Fool 100 Index | 232 (2018-01-30 → 2018-12-31) | 2,138 |
| TMFS | Small-Cap Growth | 37 | 1,943 |
| TMFX, TMFM, TMFE, TMFG | Next / Mid-Cap / Capital Efficiency / Global | **0** | — |
| MFIG, MFMO, MFVL | the three factor funds | **0** | 162 each |

They launched in 2018 and later, so they sit almost entirely inside the
sealed window. **This comparison cannot run on development data.** It
becomes available the day the seal lifts, and at that point TMFC is the
cleanest form of the question available — an actual investable product
at actual prices, with no self-reporting and no recommendation-date
ambiguity.

Before relying on it, verify what the Fool 100 Index actually holds. It
is an index of large US companies drawn from their recommendations, not
a literal Stock Advisor portfolio, and that distinction belongs in
writing rather than in my assumptions.

**Why not the pick list.** The scorecard is subscriber-gated, which puts
it under the same rule as the journal PDFs — it could never live in this
repo. It is also self-reported, so removed picks may simply not appear,
which is survivorship in the form that already cost the previous project
47% of a tuned rule's return.

The decisive objection is a measurement one. A peer-reviewed evaluation
of Stock Advisor reports a statistically significant market reaction on
the announcement day *and the two days following*. The scorecard books
entries at the close on the recommendation date — after that move.
Subscribers buy on the email. So a backtest built on scorecard entry
prices is contaminated in a known direction by a documented amount,
which is the retroactive-fill defect that was once worth the previous
project's entire measured edge, except here it is published rather than
hypothetical.

I could not retrieve the paper's full text, so I have not recorded which
source it used for pick dates. Third-party sites claiming to have
analysed 500 to 1,093 picks are affiliate reviews working from the
Fool's own scorecard, and are not a provenance I would build on.

I1 is first and nothing runs before it. Restated fundamentals are
lookahead as pure as the retroactive entry fills that were once worth
the previous project's entire measured edge, and `MRQ`/`MRT`/`MRY` are
restated. This is defect number eight waiting to happen, and it is the
one specific to this fork.

## Arms

| id | registered | hypothesis | prediction | result |
|---|---|---|---|---|
| B1 | 2026-08-06 | The inherited trend-and-regime rule, run over a growth universe on development data, is the honest baseline a growth signal has to beat — not a fund, and certainly not a fund I chose. | Lands near the alternatives set. If it does, "beats SPY" is worth nothing here, and every later arm is measured against B1 and the set both. | not run |

B1 is contaminated by construction, and that is the point. The rule was
fitted on this data, so its measured performance is flattered, so
requiring a growth signal to beat it is a *harder* test than it appears.
A prior may set the hurdle. It may not be a foundation — see
`docs/holdout-seal.md`.

| id | registered | hypothesis | prediction | result |
|---|---|---|---|---|
| B2 | 2026-08-06 | What idle capital does is a larger lever than which stocks the system picks. Three policies: cash at the prevailing rate, always parked in the index, and the regime-aware policy (cash when the gate is off, index when it is on and there is nothing to buy). | The policy spread exceeds the spread between B1 and any growth arm. If it does, the parking policy is the first thing to fix and everything downstream is measured with it held constant. | not run |

**B2 runs before any growth condition.** The source project reports the
parking lever as worth several times its strategy edge, and reports
finding that only after roughly 200 arms had gone into tuning entry
rules while the policy sat unregistered as a default. I am not taking
that number — it came from the same prices and, by their own note, from
survivor-biased universes. I am taking the shape of the mistake, which
costs nothing to avoid: measure the biggest parameter before spending
the budget on smaller ones.

Two guards, because this is where the arm budget could quietly drain:

- **Three policies is three arms**, registered together and resolved
  together. Picking the best of three is a selection like any other; the
  source project caught itself reading exactly this table too
  generously. The winner is fixed in advance of every later arm and not
  revisited when a growth condition would look better under a different
  one.
- **Parking is not free.** The ported cost model charges 0.11% a leg,
  billed only while actually parked. An arm that shows a parked policy
  winning on gross returns has not shown anything.

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
  inherited constant and the closing warning I inherited. It should
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
- **Never report a result without the alternatives beside it.** The
  verdict is total P&L against the best of `{SPY, IWF, cash}` over the
  same window — joined by `TMFC` once the seal lifts, see I5 — where the money sat while idle is part of the system,
  not a contaminant of the measurement. Report the deployed/parked split
  too, not to qualify the verdict but because it answers the next
  question: could I have had this P&L more cheaply by holding the fund
  and skipping the system?
- **Do not name the yardstick in advance.** See I4. Choosing the
  benchmark before seeing the window is how a system declares victory
  over a comparator that SPY itself beat.
- **Probe an interface before building on it.**
