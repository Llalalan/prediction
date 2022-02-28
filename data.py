import requests
import time
import pandas as pd


def timestamp_to_fomat(timestamp=None, format='%Y-%m-%d %H:%M:%S'):
    # 默认返回当前格式化好的时间
    # 传入时间戳的话，把时间戳转换成格式化好的时间，返回
    if timestamp:
        time_tuple = time.localtime(timestamp)
        res = time.strftime(format, time_tuple)
    else:
        res = time.strftime(format)  # 默认读取当前时间
    return res

def request_data_1d():
    BASE_URL = "https://api.binance.com"
    # url = BASE_URL + "/api/v1/klines?symbol=BTCUSDT&interval=1d&limit=1000" # 会不一样
    url = BASE_URL + "/api/v1/klines?symbol=ETHBUSD&interval=1d&limit=1000"
    resp = requests.get(url)
    resp = resp.json()
    df = pd.DataFrame(resp)
    df = df.drop(columns=[6, 7, 8, 9, 10, 11])
    df.columns=["opentime", "Open", "High", "Low", "Close", "Volume"]
    df["Date"] = (df["opentime"]//1000).map(timestamp_to_fomat)
    df = df.set_index(df["Date"])
    df = df.drop(["opentime"],axis=1)
    df['Open'] = pd.to_numeric(df['Open'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    df['Volume'] = pd.to_numeric(df['Volume'])
    print(df)
    return df

def request_data_2h():
    BASE_URL = "https://api.binance.com"
    # url = BASE_URL + "/api/v1/klines?symbol=BTCUSDT&interval=2h&limit=1000" # 会不一样
    url = BASE_URL + "/api/v1/klines?symbol=ETHBUSD&interval=30m&limit=1000"
    resp = requests.get(url)
    resp = resp.json()
    df = pd.DataFrame(resp)
    df = df.drop(columns=[6, 7, 8, 9, 10, 11])
    df.columns=["opentime", "Open", "High", "Low", "Close", "Volume"]
    df["Date"] = (df["opentime"]//1000).map(timestamp_to_fomat)
    df = df.set_index(df["Date"])
    df = df.drop(["opentime"],axis=1)
    df['Open'] = pd.to_numeric(df['Open'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    df['Volume'] = pd.to_numeric(df['Volume'])
    print(df)
    return df