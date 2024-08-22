#Overview
#SMA Indicator 
- - -
##The SMA Indicator script fetches historical price data for a specified trading pair and calculates the Simple Moving Average over a defined period. It then compares the current bid price to the SMA to generate buy or sell signals. Additionally, it identifies support and resistance levels based on recent price action.

This tool leverages the CCXT library for accessing various cryptocurrency exchanges and Pandas for data manipulation and analysis.

Features
Flexible SMA Calculation: Calculate SMA over any period and timeframe.
Real-time Data Fetching: Retrieves up-to-date market data from supported exchanges.
Buy/Sell Signal Generation: Provides clear trading signals based on SMA comparison.
Support and Resistance Levels: Identifies key price levels to inform trading decisions.
Easy Integration: Modular functions allow for seamless integration into larger trading systems.
Prerequisites
Before running the script, ensure you have the following installed:

Python 3.7 or higher
CCXT
Pandas
A supported cryptocurrency exchange API key and secret (if accessing private endpoints)
