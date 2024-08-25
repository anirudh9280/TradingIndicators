############## Coding SMA Indicator 2024
import ccxt
import dontshare as k
import pandas as pd 

phemex = ccxt.phemex({
    'enableRateLimit': True, 
    'apiKey': k.p_api_key,
    'secret': k.p_secret_key
})

# Load markets to find correct symbol format
markets = phemex.load_markets()
print("Available symbols on Phemex:")
print(markets.keys())

# Assuming the correct format is 'ETH/USDT'
symbol = 'ETH/USDT'

size = 1
params = {'timeInForce': 'PostOnly'}

def ask_bid(symbol=symbol):
    try:
        ob = phemex.fetch_order_book(symbol)
        bid = ob['bids'][0][0] if ob['bids'] else None
        ask = ob['asks'][0][0] if ob['asks'] else None
        if bid is None or ask is None:
            print(f"No bids or asks available for {symbol}.")
            return None, None
        print(f'This is the ask for {symbol}: {ask}')
        return ask, bid
    except ccxt.NetworkError as e:
        print(f'Network Error: {e}')
    except ccxt.ExchangeError as e:
        print(f'Exchange Error: {e}')
    except Exception as e:
        print(f'Unexpected Error: {e}')
    return None, None

timeframe = '15m'
limit = 100
sma = 20

def df_sma(symbol=symbol, timeframe=timeframe, limit=limit, sma=sma):
    print('Starting indicator calculation...')

    try:
        bars = phemex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    except ccxt.NetworkError as e:
        print(f'Network Error: {e}')
        return
    except ccxt.ExchangeError as e:
        print(f'Exchange Error: {e}')
        return
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return

    # pandas DataFrame setup
    df_sma = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_sma['timestamp'] = pd.to_datetime(df_sma['timestamp'], unit='ms')

    # Calculate the SMA
    df_sma[f'sma{sma}_{timeframe}'] = df_sma['close'].rolling(sma).mean()

    # Get the latest bid price
    ask, bid = ask_bid(symbol)
    if bid is None:
        print('Failed to retrieve bid price. Exiting function.')
        return

    # Set signals based on SMA comparison with bid
    df_sma['sig'] = None
    df_sma.loc[df_sma[f'sma{sma}_{timeframe}'] > bid, 'sig'] = 'SELL'
    df_sma.loc[df_sma[f'sma{sma}_{timeframe}'] < bid, 'sig'] = 'BUY'

    # Support and resistance calculation
    df_sma['support'] = df_sma['close'].min()
    df_sma['resis'] = df_sma['close'].max()

    print(df_sma)
    return df_sma

# Execute the function
df_sma()
