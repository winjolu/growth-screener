# The sealed holdout

**Sealed on 2026-08-06, before the first arm ran.**

```
development   through 2018-12-31
SEALED        2019-01-01 onwards        do not run anything against this
```

Nothing in this project may read data dated 2019-01-01 or later until the
strategy is finished and I have said in writing that it is finished. That
includes exploratory queries, plots, sanity checks and "just looking at
whether the signal fires." A holdout I peek at once is not a holdout; it
is a slow second development set.

## Why a holdout at all, given I already pre-register

Registration and contamination are different problems and I only used to
cover one. Registering a test before running it stops me rationalising a
result after seeing it. It does nothing about the fact that I have
already seen the data. A window I have looked at is not out of sample for
me, no matter how honestly I write down the hypothesis beforehand.

## Why not 2005-2009

That was the previous project's holdout and it is burned. Its results
have been read, written up, and written up, and I carried the conclusions across.
Inheriting it would mean starting this project having already peeked.
It sits inside the development window here, which is fine — development
data is allowed to be dirty.

## Why the most recent window rather than a slice out of the middle

Indicator lookbacks. A holdout carved out of the middle leaves a
development segment on the far side of it, and every indicator in that
segment reads backwards across the seal — a 30-week moving average in
early 2016 is looking at late 2015. A terminal holdout has one boundary
instead of two, and lookbacks point away from it. There is nothing to
leak through.

## What this holdout can and cannot tell me

2019-2026 was a growth-favourable stretch, and I am building a growth
strategy. That asymmetry is the whole caveat:

- **A failure here is damning.** If a growth strategy cannot clear a
  growth benchmark in a growth regime, there is nothing to salvage.
- **A pass here is weak evidence.** It is consistent with the strategy
  working and equally consistent with having bought the regime.

The window is not purely kind — it contains the 2020 crash and 2022,
when VUG fell about a third — but I should not talk myself into reading
a pass as more than it is.

One honest limitation: the previous project ran full-history arms that
crossed this window, so I have seen *price* behaviour here. What makes
the seal worth having is that the signal layer in this project is
fundamentals, and no fundamental signal has been examined in any window.
That part is genuinely untouched. Where a result leans on price
behaviour rather than fundamentals, the holdout is weaker than it looks
and I should say so rather than claim the full protection.

## Inherited priors are not findings

What I inherited says momentum works, that the edge concentrates in thin
illiquid names, and that a two-line trend rule beats nine hand-tuned
conditions. Every one of those came out of the same 1998-2026 US equity
prices I am about to use. They are hypotheses that survived one
project's testing. Re-confirming them on overlapping data is the same
evidence counted twice, not replication.

The practical rule I am holding myself to: **a prior may set the hurdle,
but may not be a foundation.**

- Using the inherited trend-and-regime rule as the number to beat is
  safe. It was fitted on this data, so its measured performance is
  flattered, so requiring a growth strategy to beat it is a harder test
  than it looks. Contamination cuts conservatively here.
- Building it into the growth strategy is not safe. The combination
  inherits the fit and I lose any way of seeing which layer carries the
  result.

What I inherited wants both — it scopes the project as growth screening
combined with the trend and regime logic that already works, while also
warning against building on inherited priors. If I do combine them, the
combined arm gets scored against **trend-and-regime alone**, not only
against VUG, so the growth layer's marginal contribution is visible
rather than hidden inside a fitted component's performance.

## Breaking the seal

When the strategy is finished, I run the holdout **once**, record the
result whatever it is, and stop. Not once per variant. If the holdout
result sends me back to change the strategy, the seal is gone and the
honest thing is to say so in the register and treat every subsequent
number as development data.
