import pandas as pd
import numpy as np

def MACD(close: pd.DataFrame, span1=12, span2=26, span3=9):
    exp1 = EMA(close, span1)
    exp2 = EMA(close, span2)
    macd = 100 * (exp1 - exp2) / exp2
    signal = EMA(macd, span3)

    return macd, signal


def EMA(x, n):
    a = 2 / (n + 1)
    return pd.Series(x).ewm(alpha=a).mean()


# Two new features from the competition tutorial
def upper_shadow(df):
    return df["High"] - np.maximum(df["Close"], df["Open"])


def lower_shadow(df):
    return np.minimum(df["Close"], df["Open"]) - df["Low"]


def get_price_features(df, row=False):
    features = []
    keys = ["Open", "High", "Low", "Close", "Volume", ]

    df_feat = df.copy()

    df_feat['HLmedian'] = (df['High'] + df['Low']) / 2
    features += ["HLmedian", ]

    # add feature Upper_Shadow, Lower_Shadow
    df_feat["Upper_Shadow"] = upper_shadow(df_feat)
    df_feat["Lower_Shadow"] = lower_shadow(df_feat)
    features += ["Upper_Shadow", "Lower_Shadow", ]

    # Ad some more feats
    df_feat["Close/Open"] = df_feat["Close"] / df_feat["Open"]
    df_feat["Close-Open"] = df_feat["Close"] - df_feat["Open"]
    df_feat["High-Low"] = df_feat["High"] - df_feat["Low"]
    df_feat["High/Low"] = df_feat["High"] / df_feat["Low"]
    features += ["Close/Open", "Close-Open", "High-Low", "High/Low", ]

    # if row的话是每列一个时间数据，index在row
    # calculate the mean of Open, High, Low and Close
    if row:
        df_feat['Mean'] = df_feat[['Open', 'High', 'Low', 'Close']].mean()
    else:
        df_feat['Mean'] = df_feat[['Open', 'High', 'Low', 'Close']].mean(axis=1)

    df_feat["High/Mean"] = df_feat["High"] / df_feat["Mean"]
    df_feat["Low/Mean"] = df_feat["Low"] / df_feat["Mean"]
    features += ["Mean", "High/Mean", "Low/Mean", ]

    ## possible seasonality, datetime  features (unlikely to me meaningful, given very short time-frames)
    ### to do: add cyclical features for seasonality
    ## format later
    #     if row:
    #         df_feat["hour"] = times.hour  # .dt
    #         df_feat["dayofweek"] = times.dayofweek
    #         df_feat["day"] = times.day
    #     else:
    #         df_feat["hour"] = times.dt.hour  # .dt
    #         df_feat["dayofweek"] = times.dt.dayofweek
    #         df_feat["day"] = times.dt.day
    # df_feat.drop(columns=["time"],errors="ignore",inplace=True)  # keep original epoch time, drop string

    if row:
        df_feat["Median"] = df_feat[["Open", "High", "Low", "Close"]].median()
    else:
        df_feat["Median"] = df_feat[["Open", "High", "Low", "Close"]].median(axis=1)
    df_feat["High/Median"] = df_feat["High"] / df_feat["Median"]
    df_feat["Low/Median"] = df_feat["Low"] / df_feat["Median"]
    features += ["Median", "High/Median", "Low/Median", ]

    # 数据的平滑处理
    for col in ['Open', 'High', 'Low', 'Close']:
        df_feat[f"Log_1p_{col}"] = np.log1p(df_feat[col])
        features += [f"Log_1p_{col}", ]

    #     # 基準線
    #     max26 = df_feat["High"].rolling(window=26).max()
    #     min26 = df_feat["Low"].rolling(window=26).min()
    #     df_feat["basic_line"] = (max26 + min26) / 2
    #     features += ["basic_line",]

    #     # 転換線
    #     high9 = df_feat["High"].rolling(window=9).max()
    #     low9 = df_feat["Low"].rolling(window=9).min()
    #     df_feat["turn_line"] = (high9 + low9) / 2
    #     features += ["turn_line",]

    # RSI
    # df_feat["RSI"] = RSI(df_feat["Close"], 14)

    # MACD
    macd, macd_signal = MACD(df_feat["Close"], 12, 26, 9)
    df_feat["MACD"] = macd
    df_feat["MACD_signal"] = macd_signal
    features += ["MACD", "MACD_signal", ]

    df_feat = df_feat[keys + features]

    return df_feat