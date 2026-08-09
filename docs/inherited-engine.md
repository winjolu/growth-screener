# What this fork inherited

This project began as a fork. It keeps a backtesting engine and discards
a strategy. The strategy it discarded was an implementation of stage
analysis that became a test of stage analysis: a two-line trend rule
plus a market-regime filter beat the nine-condition checklist on every
risk-adjusted measure, nothing cleared the significance bar, and the
edge that survived was bear-market avoidance rather than stock
selection.

**The strategy was never the asset. The engine is.** Everything below
the signal layer is strategy-agnostic and took roughly two hundred
backtest arms to get right, most of that spent finding defects that
produced confident, wrong answers.

## Kept unchanged

- `screener/backtest.py` — point-in-time engine, no lookahead,
  gap-aware stop fills, delisting exits
- `screener/portfolio_sim.py` — fixed-capital accounting, mark-to-market
  drawdown, six risk measures, the random-thinning control
- `screener/costs.py` — broker-agnostic cost profiles, breakeven sweep
- `screener/sharadar.py` — the data client
- `screener/db.py`, `neighbours.py`, `moving_averages.py`, `stop_loss.py`
- the entire `tests/` directory

`screener/conditions.py` is the strategy and the only file that should
be changing.

## The seven defects a fresh build would rediscover

Every one produced a confident, plausible, wrong result.

1. **Stop exits filling at the stop price** when the bar gapped through
   it. Worth 0.16-0.28 points a trade, always flattering.
2. **Positions held into a delisting marked "still open"** and excluded
   from scoring. Of 88 such trades, 73 were gains at a median +16.2% —
   acquisitions closing at a premium. The bankruptcies were counted and
   the buyouts discarded.
3. **Split-corrupted vendor data.** 621 tickers carry an impossible
   weekly move; GE shows an 87% collapse that never happened. In one
   window, every trade losing more than 60% sat on corrupt data.
4. **Survivorship.** The true 2005 universe was 3,957 names, 69% since
   delisted. Testing on 1,257 survivors — a fifth of the market — missed
   GOOGL, Yahoo, Dell and Broadcom even among companies that lived.
   Correcting it cost the tuned rule 47% of its return.
5. **Retroactive entry fills**, worth +1.11 points a trade, which was
   the whole measured edge.
6. **A price-index cache keyed on `id()`**, which returns another
   symbol's prices after garbage collection reuses the address.
7. **Partial backtest arms read as complete.** Four times.

An eighth is specific to this fork and has not happened yet: restated
fundamentals. Sharadar's `MRQ`/`MRT`/`MRY` dimensions are restated, so
using them is lookahead as pure as defect 5. Only `ARQ`/`ART` are
as-reported, and the filter must be on `datekey`, never `calendardate`.

## Data available

| asset | size | contents |
|---|---|---|
| `sharadar.db` | ~18 GB | 46.3M daily bars 1998-2026, survivorship-free; 78,904 tickers with `permaticker`/`isdelisted`; 15.4M fund bars; 3.2M quarterly fundamentals; 14.5M daily fundamentals; 11.5M insider filings; 2.5M corporate events; 672k corporate actions; S&P 500 point-in-time membership |
| weekly cache | 481 MB | 10,230 tickers, weekly, incl. SPY/QQQ/DIA/IWM/MTUM/VTWO/VONE |
| daily cache | 591 MB | 3,958 tickers, daily, the 2005-2009 crash window |
| `security_identity` | — | 5,803 tickers resolved to SEC CIKs |
| `delisting_events` | — | 36,346 SEC delisting notices, 2004-2026 |

All three Sharadar tiers are loaded. `sharadar.refresh(table)` tops the
database up from the API for anything needing current data, asking only
for dates after what is stored.

`dailyfundamentals` carries market cap per day, but only from
2016-01-04. Before that, size comes from `fundamentals.marketcap` at
`datekey`.

## Benchmarks present in `fundprices`

| ticker | fund | history from |
|---|---|---|
| IWF | Russell 1000 Growth | 2000-05-26 |
| IWO | Russell 2000 Growth | 2000-07-28 |
| VUG | Vanguard Growth | 2004-01-30 |
| VOT | Vanguard Mid-Cap Growth | 2006-08-25 |
| SCHG | Schwab US Large-Cap Growth | 2010-01-04 |
| ARKK | ARK Innovation | 2014-10-31 |
| QQQ | Nasdaq 100 | 1999-03-10 |
| MTUM | MSCI USA Momentum | 2013-04-18 |

Which of these is the yardstick is settled in `docs/test-register.md`
I4, not here — the short version is that naming one in advance is a
lever, so the hurdle is the best of the set over the window being
measured.

## Two open questions worth keeping

**Retention beats selection.** For every trade exited, the stock went on
to underperform SPY by 3.1% over the following year, so exits are
well-timed. But 2.78% of exits doubled within a year, and those were
overwhelmingly small stopped-out losses that then ran. One name: five
failed attempts averaging -7%, then +559.8%, net +517%. The mechanism
that pays is re-entry after being stopped out, not better selection.

**Nobody varied the moving average.** After 196 arms the 30-week period
was still the book's number, untested. Sweeping 5 to 50 weeks put 30
seventh of ten, and the curve was jagged rather than smooth, which means
the parameter is mostly noise. A constant should not be inherited
without testing, and the best-looking value from one window should not
be adopted either.

## Process rules that earned their place

- Register the test before running it.
- Print numbers, read them, then write what they mean.
- Probe an interface before building on it.
- Verify an arm is complete before reading it.
- Score the ride, not just the destination.
- Check the worst case after any change to which trades qualify.
- Two arms with identical results mean a broken experiment.
- Adjust the significance bar for the number of looks.

The reasoning behind the contamination rules is in
`docs/holdout-seal.md`; the arm budget and what spends one is in
`docs/test-register.md`.
