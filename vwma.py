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
bid = 29000
params = {'timeInForce': 'PostOnly',}

   
# ask_bid 
def ask_bid(symbol=symbol):
    ob = phemex.fetch_order_book(symbol)
    #print(ob)
    bid = ob['bids'][0][0]
    ask = ob['asks'][0][0]
    print(f'this is the ask for {symbol} {ask}')
    return ask, bid # ask_bid()[0] = ask , [1] = bid


timeframe = '15m'
limit = 100
sma = 20 

def get_df_vwma():

    num_bars = 100
    timeframe = '1d'
    # IF I CHNAGE THE ABOVE VARS.. MAKE SURE THAT THEY ARE == 24 hours
    # becuase VWAP is a 24 hour inidicator only.

    ### GETTING NEWEST DATAFRAME ###

    #print(f"fetching new bars for {datetime.now().isoformat()}")
    bars = phemex.fetch_ohlcv(symbol, timeframe=timeframe, limit=num_bars) # here is where i change the ticker i wanna trade + the time frame & # of bars # I MADE CUSTOMIZATIONS HERE IF DIDNT WORK LOOK AT ARGS
    df_vwma = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']) # this is where is set the column titles in DF
    df_vwma['timestamp'] = pd.to_datetime(df_vwma['timestamp'], unit='ms')

    return df_vwma

def vwma_indi():

    df_vwma = get_df_vwma() # getting the data frame from above
    ### storing the SMA for three different periods
    df_vwma['SMA(41)'] = df_vwma.close.rolling(41).mean()
    df_vwma['SMA(20)'] = df_vwma.close.rolling(20).mean()
    df_vwma['SMA(75)'] = df_vwma.close.rolling(75).mean()
    print(df_vwma)
    # now get VWMA

    vwmas = [20, 41, 75]
    for n in vwmas:
        df_vwma[f'sum_vol{n}'] = df_vwma['volume'].rolling(min_periods=1, window=n).sum() # sum of volume from the three periods
        df_vwma['volXclose'] = (df_vwma['volume'])*(df_vwma['close']) # creating a new column with close
        df_vwma[f'vXc{n}'] = df_vwma['volXclose'].rolling(min_periods=1, window=n).sum() # summing previous column
        # VWMA
        df_vwma[f'VWMA({n})'] = (df_vwma[f'vXc{n}']) / (df_vwma[f'sum_vol{n}']) # finding VWMA by dividing sum of (volume x close) / sum_volume
        # this is for VWMA signals - buy if vmwa > sma for that period
        # buy
        df_vwma.loc[df_vwma[f'VWMA({n})'] > df_vwma['SMA(41)'], f'41sig{n}'] = 'BUY' 
        df_vwma.loc[df_vwma[f'VWMA({n})'] > df_vwma['SMA(20)'], f'20sig{n}'] = 'BUY'
        df_vwma.loc[df_vwma[f'VWMA({n})'] > df_vwma['SMA(75)'], f'75sig{n}'] = 'BUY'
        # sell
        df_vwma.loc[df_vwma[f'VWMA({n})'] < df_vwma['SMA(41)'], f'41sig{n}'] = 'SELL' 
        df_vwma.loc[df_vwma[f'VWMA({n})'] < df_vwma['SMA(20)'], f'20sig{n}'] = 'SELL'
        df_vwma.loc[df_vwma[f'VWMA({n})'] < df_vwma['SMA(75)'], f'75sig{n}'] = 'SELL'
        print(df_vwma)

    return df_vwma

vwma_indi()