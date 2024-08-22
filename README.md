# Indicators 
- - - 

# Simple Moving Average (SMA) Indicator

This tool is designed to help traders analyze market trends by calculating the Simple Moving Average (SMA) of a given cryptocurrency pair over a specified timeframe. The SMA is a fundamental technical analysis tool that aids in identifying market direction and potential support and resistance levels.


## Overview

The **SMA Indicator** script fetches historical price data for a specified trading pair and calculates the Simple Moving Average over a defined period. It then compares the current bid price to the SMA to generate buy or sell signals. Additionally, it identifies support and resistance levels based on recent price action.

This tool leverages the [CCXT](https://github.com/ccxt/ccxt) library for accessing various cryptocurrency exchanges and [Pandas](https://pandas.pydata.org/) for data manipulation and analysis.

---

## SMA as Support and Resistance

### Support Level
In an uptrend, the SMA often acts as a support level where the price may bounce back up after a pullback.

### Resistance Level
In a downtrend, the SMA can act as a resistance level where the price may reverse back down after a rally.

### Using SMA for Trading Decisions

- **Buy Signal**: If the current bid price crosses above the SMA, it may signal the start of an uptrend, indicating a potential buying opportunity.
- **Sell Signal**: If the current bid price crosses below the SMA, it may signal the start of a downtrend, indicating a potential selling opportunity.

Example: 
<img width="1390" alt="Screenshot 2024-08-22 at 12 51 05 AM" src="https://github.com/user-attachments/assets/3b0c1975-0dbc-4469-9eeb-5dc6ddec638f">



## Features

- **Flexible SMA Calculation**: Calculate SMA over any period and timeframe.
- **Real-time Data Fetching**: Retrieves up-to-date market data from supported exchanges.
- **Buy/Sell Signal Generation**: Provides clear trading signals based on SMA comparison.
- **Support and Resistance Levels**: Identifies key price levels to inform trading decisions.
- **Easy Integration**: Modular functions allow for seamless integration into larger trading systems.

---

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.7 or higher
- [CCXT](https://github.com/ccxt/ccxt)
- [Pandas](https://pandas.pydata.org/)
- A supported cryptocurrency exchange API key and secret (if accessing private endpoints)

---
