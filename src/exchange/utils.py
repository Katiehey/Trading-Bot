#import pandas as pd

#def ohlcv_to_df(data):
    #return pd.DataFrame(
        #data,
        #columns=["datetime", "open", "high", "low", "close", "volume"]
    #).assign(
        #timestamp=lambda x: pd.to_datetime(x["datetime"], unit="ms")
    #)

import pandas as pd

def ohlcv_to_df(data):
    # Create the DataFrame first
    df = pd.DataFrame(
        data,
        columns=["timestamp_ms", "open", "high", "low", "close", "volume"]
    )
    
    # Convert the raw millisecond timestamp column to a proper UTC datetime object
    df["datetime"] = pd.to_datetime(df["timestamp_ms"], unit="ms", utc=True)

    # Optional: You can drop the raw millisecond column and use 'datetime' as the standard
    # df = df.drop(columns=["timestamp_ms"])
    
    return df
