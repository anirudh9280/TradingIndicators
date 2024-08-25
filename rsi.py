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
symbol = 'ETHUSDT'
size = 1 
params = {'timeInForce': 'PostOnly',}

size = 1 
params = {'timeInForce': 'PostOnly',}

def ask_bid(symbol=symbol):
    try:
        ob = phemex.fetch_order_book(symbol)
        bid = ob['bids'][0][0]
        ask = ob['asks'][0][0]
        print(f'This is the ask for {symbol}: {ask}')
        return ask, bid
    except ccxt.NetworkError as e:
        print(f'Network Error: {e}')
    except ccxt.ExchangeError as e:
        print(f'Exchange Error: {e}')
    except Exception as e:
        print(f'Unexpected Error: {e}')
    return None, None  # Return a tuple with None values if there's an error

# constants 
timeframe = '15m'
limit = 100
sma = 20 


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
    rsi = RSIIndicator(df_rsi['Close'])
    df_rsi['rsi'] = rsi.rsi()
    print(df_rsi)
    return df_rsi

df_rsi()
    


        
    
