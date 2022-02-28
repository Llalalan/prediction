def generate_label_rate(df):
    '''
    比如说在1月15号的时候要操作买卖了，那么就要看1月14号的label。
    1月14号的label是和15号的涨跌相关的。
    label计算方法：（15号的high-low median加上14号的high-low median）除以14号的high-low median
    '''
    # df['HLmedian'] = (df['High'] + df['Low']) / 2
    df['label'] = (df['HLmedian'].shift(-1) - df['HLmedian'])/df['HLmedian']*100
    return df

def generate_label_high(df):
    df['label'] = df['High'].shift(-1)
    return df

def generate_label_low(df):
    df['label'] = df['Low'].shift(-1)
    return df