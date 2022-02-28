import requests
import time
import pandas as pd

BASE_URL = "https://api.binance.com"

# url = BASE_URL + "/api/v1/klines?symbol=BTCUSDT&interval=5m&limit=100" 会不一样
url = BASE_URL + "/api/v1/klines?symbol=BTCBUSD&interval=8h&limit=100000"
resp = requests.get(url)
resp = resp.json()
resp
df = pd.DataFrame(resp)

import time
def timestamp_to_fomat(timestamp=None,format='%Y-%m-%d %H:%M:%S'):
     #默认返回当前格式化好的时间
     #传入时间戳的话，把时间戳转换成格式化好的时间，返回
    if timestamp:
        time_tuple = time.localtime(timestamp)
        res = time.strftime(format,time_tuple)
    else:
         res = time.strftime(format)#默认读取当前时间
    return res

df = df.drop(columns=[6, 7, 8, 9, 10, 11])
df.columns=["opentime", "Open", "High", "Low", "Close", "Volume"]

df["opentime"] = (df["opentime"]//1000).map(timestamp_to_fomat)
df.set_index(["opentime"], drop=True)

df['Open'] = pd.to_numeric(df['Open'])
df['High'] = pd.to_numeric(df['High'])
df['Low'] = pd.to_numeric(df['Low'])
df['Close'] = pd.to_numeric(df['Close'])

