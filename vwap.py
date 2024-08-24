import ccxt
import dontshare as d
import time , schedule 
import pandas as pd 
# pip install ta 
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

timeframe = '15m'
limit = 100
sma = 20 

# VWAP

def get_df_vwap():
        ### GETTING NEWEST DATAFRAME ###
        bars = phemex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit) # here is where i change the ticker i wanna trade + the time frame & # of bars # I MADE CUSTOMIZATIONS HERE IF DIDNT WORK LOOK AT ARGS
        df_vwap = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']) # this is where is set the column titles in DF
        df_vwap['timestamp'] = pd.to_datetime(df_vwap['timestamp'], unit='ms')
        print('dv_vwap after', df_vwap)
        return df_vwap

def vwap_indi():
        print('starting the vwma indicator to see if to be long or short.. ')
        df_vwap = get_df_vwap()
        # VWAP = (sum(first13valuesVolumexClose)) / (sum(volume colume top 13))
        df_vwap['volXclose'] = df_vwap['close']*df_vwap['volume']
        df_vwap['cum_vol'] = df_vwap['volume'].cumsum()
        # then cum sum of vol * price.. gonna do hi + low + close / 3 to get avg
        df_vwap['cum_volXclose'] = (df_vwap['volume'] * (df_vwap['high'] + df_vwap['low'] + df_vwap['close'])/3).cumsum()
        df_vwap['VWAP'] =  df_vwap['cum_volXclose'] / df_vwap['cum_vol']
        df_vwap = df_vwap.fillna(0)
        # vwap equation = sum(volume * avg price) / sum(vol)
        return df_vwap
    
vwap_indi()
