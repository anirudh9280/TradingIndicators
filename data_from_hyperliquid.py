import pandas as pd
from datetime import datetime, timedelta
import requests

# Define symbol, timeframe, and total limit
symbol = 'ETHUSDT'
timeframe = '24h'
total_limit = 5000

# Maximum records per call allowed by the API
max_call_limit = 1000

# Calculate the number of iterations needed
iterations = -(-total_limit // max_call_limit)  # Ceiling division

# Initialize an empty DataFrame
all_data = pd.DataFrame()
print(all_data)

def fetch_ohlcv_data(symbol, interval, start_time, end_time):
    url = 'https://api.hyperliquid.xyz/info'
    headers = {'Content-Type': 'application/json'}
    data = {
        "type": "candleSnapshot",
        "req": {
            "coin": symbol,
            "interval": interval,
            "startTime": int(start_time.timestamp() * 1000),
            "endTime": int(end_time.timestamp() * 1000)
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(f'API response status code:', {response.status_code})
    if response.status_code == 200:
        snapshot_data = response.json()
        return snapshot_data
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return None

def process_data_to_df(snapshot_data):
    if snapshot_data and 'candles' in snapshot_data:
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        data = []
        for snapshot in snapshot_data['candles']:
            timestamp = datetime.fromtimestamp(snapshot['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            open_price = snapshot['o']
            high_price = snapshot['h']
            low_price = snapshot['l']
            close_price = snapshot['c']
            volume = snapshot['v']
            data.append([timestamp, open_price, high_price, low_price, close_price, volume])

        df = pd.DataFrame(data, columns=columns)

        # Ensure that support and resis are correct
        if len(df) > 2:
            df['support'] = df['close'][:-2].min()
            df['resis'] = df['close'][:-2].max()
        else:
            # If fewer than 2 rows, set support and resistance using available data
            df['support'] = df['close'].min() if not df['close'].empty else None
            df['resis'] = df['close'].max() if not df['close'].empty else None

        return df
    else:
        print("No valid snapshot data received.")
        return pd.DataFrame()

# Loop to fetch and append data
for i in range(iterations):
    print(f'Fetching data for iteration {i + 1}/{iterations}')
    end_time = datetime.now() - timedelta(hours=i * max_call_limit)
    start_time = end_time - timedelta(hours=max_call_limit)

    # Fetch the OHLCV data
    snapshot_data = fetch_ohlcv_data(symbol, timeframe, start_time, end_time)

    # Log the fetched data for debugging
    if snapshot_data:
        print(f"Snapshot data for {symbol}: {snapshot_data}")

    # Process the data
    df = process_data_to_df(snapshot_data)

    # Check DataFrame content
    print(f"DataFrame structure for iteration {i+1}:")
    print(df.info())
    
    # Append the fetched data to the all_data DataFrame if not empty
    if not df.empty:
        all_data = pd.concat([all_data, df], ignore_index=True)
    else:
        print(f"No data to append for iteration {i + 1}.")

# Construct the file path
file_path = f'{symbol}_{timeframe}_{total_limit}.csv'

# Save the concatenated DataFrame to CSV
all_data.to_csv(file_path, index=False)

print(all_data)
print(f'Data saved to {file_path}')
