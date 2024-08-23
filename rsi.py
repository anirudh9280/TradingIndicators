##### CODING RSI INDICATOR

import ccxt 
import dontshare as d
import pandas as pd
from ta.momentum import * 

phemex = ccxt.phemex({
    'enableRateLimit': True, 
    'apiKey': d.p_api_key_2,
    'secret': d.p_secret_key_2
})
symbol = 'uBTCUSD'
size = 1 
params = {'timeInForce': 'PostOnly',}

size = 1 
params = {'timeInForce': 'PostOnly',}


def ask_bid(symbol=symbol):
    ob = phemex.fetch_order_book(symbol)
    bid = ob['bids'][0][0]
    ask = ob['asks'][0][0]
    print(f'This is the ask for {symbol} {ask}')
    return ask, bid  # ask_bid()[0] = ask, [1] = bid


# constants 
timeframe = '15m'
limit = 100
sma = 20 

def df_sma(symbol=symbol, timeframe=timeframe, limit=limit, sma=sma):
    print('Starting indicator calculation...')
    bars = phemex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    # pandas DataFrame setup
    df_sma = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_sma['timestamp'] = pd.to_datetime(df_sma['timestamp'], unit='ms')
    # Calculate the 20-day SMA
    df_sma[f'sma{sma}_{timeframe}'] = df_sma['close'].rolling(sma).mean()
    # Check the resulting DataFrame after SMA calculation
    # Getting the latest bid price
    bid = ask_bid(symbol)[1]
    # Setting signals based on SMA comparison with bid
    df_sma['sig'] = None  # Initialize the signal column
    df_sma.loc[df_sma[f'sma{sma}_{timeframe}'] > bid, 'sig'] = 'SELL'
    df_sma.loc[df_sma[f'sma{sma}_{timeframe}'] < bid, 'sig'] = 'BUY'
    # Support and resistance calculation
    df_sma['support'] = df_sma['close'].min()  # This should give a scalar
    df_sma['resis'] = df_sma['close'].max()  # This also gives a scalar
    print(df_sma)
    return df_sma



# pandas and TA
def df_rsi(symbol=symbol, timeframe=timeframe, limit=limit):
    print('starting rsi indicators')
    bars = phemex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df_rsi = pd.DataFrame(bars, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
    df_rsi['Timestamp'] = pd.to_datetime(df_rsi['Timestamp'], unit='ms')
    # if bid < 20 day sma then = BEARISH, SMA = BULLISH
    bid = ask_bid(symbol)[1]
    print(df_rsi)
    
    # RSI
    rsi = RSIIndicator(df_rsi['close'])
    df_rsi['rsi'] = rsi.rsi()
    print(df_rsi)
    return df_rsi

df_rsi()
    


        
    
