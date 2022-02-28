from flask import Flask, render_template
import datetime

import test
import numpy as np
import pandas as pd

import data
import generate_label
import generate_feature

#导入Flask
app = Flask(__name__)
#创建一个Flask实例

#设置路由，即url
@app.route('/')
@app.route('/index.html')
#url对应的函数
def index():
	#返回的页面
    now = datetime.datetime.now()
    df = data.request_data_1d()
    df = generate_feature.get_price_features(df)
    df = generate_label.generate_label_rate(df)
    train_data = df.iloc[:-30]
    test_data = df.iloc[-30:]
    _,prediction_1d_r = test.get_model(train_data,test_data)
    df = generate_label.generate_label_high(df)
    train_data = df.iloc[:-30]
    test_data = df.iloc[-30:]
    _, prediction_1d_h = test.get_model(train_data, test_data)
    df = generate_label.generate_label_low(df)
    train_data = df.iloc[:-30]
    test_data = df.iloc[-30:]
    _, prediction_1d_l = test.get_model(train_data, test_data)
    df = data.request_data_2h()
    df = generate_feature.get_price_features(df)
    df = generate_label.generate_label_rate(df)
    train_data = df.iloc[:-30]
    test_data = df.iloc[-30:]
    _,prediction_2h_r = test.get_model(train_data,test_data)
    df = generate_label.generate_label_high(df)
    train_data = df.iloc[:-30]
    test_data = df.iloc[-30:]
    _, prediction_2h_h = test.get_model(train_data, test_data)
    df = generate_label.generate_label_low(df)
    train_data = df.iloc[:-30]
    test_data = df.iloc[-30:]
    _, prediction_2h_l = test.get_model(train_data, test_data)
    flask_date='Time'
    flask_data_rate = 'Rate'
    flask_data_high = 'High'
    flask_data_low = 'Low'
    flask_data_00 = str(now.date()) + ' ' + '8:00 a.m.' + ' ' + '24h'
    flask_data_01= prediction_1d_r
    flask_data_02= prediction_1d_h
    flask_data_03= prediction_1d_l
    flask_data_10 = '两小时'
    flask_data_11= prediction_2h_r
    flask_data_12= prediction_2h_h
    flask_data_13= prediction_2h_l

    return render_template('index.html', flask_date=flask_date, flask_data_rate=flask_data_rate,
                           flask_data_high = flask_data_high, flask_data_low = flask_data_low,
                           flask_data_00=flask_data_00,flask_data_01=flask_data_01,
                           flask_data_02=flask_data_02,flask_data_03=flask_data_03,
                           flask_data_10=flask_data_10,flask_data_11=flask_data_11,
                           flask_data_12=flask_data_12,flask_data_13=flask_data_13,
                           )

#这个不是作为模块导入的时候运行，比如这个文件为aa.py，当python aa.py就执行这个代码。如果是在其他文件import的话，不执行这个文件。（这个属于python的基础知识）
if __name__ == '__main__':
    app.run()


