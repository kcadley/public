# kcadley/public

## Welcome!
---
Thank you for exploring **kcadley/public**! This project exposes a number of toolkits I've developed from my private repo. It's meant to support and enable independent traders in their algorithmic pursuits while providing a few professional examples of my work for any interested parties.



## About
---
**kcadley/public** is written fully in Python and designed to provide trade execution interfaces, data mining APIs, and derivatives modeling capabilities. Most toolkits are built on a variety of semi-common libraries, with one or two exceptions. Nearly every module is verbosely documented, supporting **help()** queries against every function and providing relatively abundant inline comments. Use cases are left to the individual trader, although there's likely something for everyone here (particularly the **macro** module). Traders who are interested in currency derivatives/spot markets and hold accounts with Oanda and TastyTrade will likely find the most broad utility here, but others should find the underlying code implementation of modules at least mildly interesting to look at. Constructive feedback is always welcome (particularly any interesting module expansion ideas you may have). Happy trading!



## Modules
---
- **BOPM** - Prices European options via the Binomial Option Pricing Model
- **contracts** - Prices FX futures and options, to include Greeks & IV
- **daycount** - Implements various interest rate / trading daycount conventions
- **dxlink** - Retrieves live & historic market data from CME
- **fastoanda** - Supports trade execution against Oanda brokerage accounts. This is a streamlined version of my PyPi release (https://pypi.org/project/easyoanda/), which might be worth checking out in tandum - the PyPi link provides a full how-to guide for the module and couple of tips/tricks on production ready execution
- **macro** - Provides access to FRED, ECB, EUROSTAT, BIS, and YahooFinance databases
- **markethours** - Evaluates global market hours, determines unknown options and futures settlement / expirations dates
- **oalink** - Retrieves live & historic market data for FX currencies (spot)
- **smile** - Models an issue's volatility smile
- **tsty** - Supports account management against TastyTrade brokerage accounts, with trade execution supported via custom payloads requests (very simple to implement, please read their datastructure guidance for requirements)
- **vol** - Provides multiple historic and implied volatility modeling options



## Acknowledgments
---
- **Oanda** - for their fantastic endpoint documentation
- **TastyTrade** - for their fantastic endpoint documentation
- **FRED** - for their exhaustic databases
- **ECB** - for their exhaustic databases
- **EUROSTAT** - for preemptively performing broad statistical calculations over the above macroeconomic datasets
- **BIS** - for aggregating and distributing international banking data
- **yfinance** - for enabling the python trading community for 5+ years
- **statsmodels** - for the time and energy contributed by professional statisticians
- **pandas & numpy** - for being the backbone of nearly all of my analytics (can't thank their contributors enough)
