# TradingView / Pine Script — Reference Index

Fetched: 2026-07-20

## Official docs
- Pine Script v6 User Manual + Reference Manual: https://www.tradingview.com/pine-script-docs/
- Release notes: https://www.tradingview.com/pine-script-docs/release-notes/

## Notes / corrections (2026-07-20)
- No official TradingView MCP server exists. All "TradingView MCP"
  projects found are third-party and unofficial. Several drive
  TradingView Desktop via Chrome DevTools Protocol (localhost:9222),
  a local security exposure, and possibly conflict with TradingView's
  Terms of Use. None are used in this project.
- Pine Script cannot make outbound HTTP calls to external APIs
  (including Webull). Only request.security() against TradingView's
  own carried symbols (e.g. SPX) is usable.
- Mansfield RS indicator in use: "Mansfield Relative Strength
  (Original Version)" by stageanalysis (TradingView Community
  Scripts). Last confirmed update: Sep 15, 2022. Verify current
  compile status and @version tag before depending on it.
