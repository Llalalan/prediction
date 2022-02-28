import numpy as np
import pandas as pd

import data
import generate_label
import generate_feature
from sklearn.metrics import mean_squared_error
from lightgbm import LGBMRegressor


def test_X_Y(test_df):
    # df_proc = df.sample(frac=0.2)
    df_proc = test_df
    # df_proc['y'] = train_df['label']
    df_proc.replace([np.inf, -np.inf], np.nan, inplace=True)
    # df_proc = df_proc.dropna(how="any")

    X = df_proc.drop("label", axis=1)
    y = df_proc["label"]
    return X, y


def get_model(train_df, price_feat_test):
    # df_proc = df.sample(frac=0.2)
    df_proc = train_df
    # df_proc['y'] = train_df['label']
    df_proc.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_proc = df_proc.dropna(how="any")

    X = df_proc.drop("label", axis=1)
    y = df_proc["label"]

    clf = LGBMRegressor(learning_rate=0.01,
                        max_depth=-1,
                        n_estimators=5000,
                        boosting_type='gbdt',
                        random_state=2019,
                        objective='regression', )
    clf.fit(X=X, y=y, eval_metric='MSE', verbose=50)
    #     return clf
    # score = mean_squared_error(y, clf.predict(X))
    test_X, test_y = test_X_Y(price_feat_test)
    print("test_y", test_y)
    result = clf.predict(test_X)
    print("predicted_y：\n", result)
    score = mean_squared_error(test_y[:-1], result[:-1])
    # print(test_X)
    # result = clf.predict(test_X)
    # right = 0
    # for i in range(len(result)):
    #     if result[i] > 0 and test_y[i] > 0:
    #         right += 1
    #     elif result[i] < 0 and test_y[i] < 0:
    #         right += 1
    # accuracy = right / len(result) * 100
    prediction = result[-2]
    return score,prediction

if __name__ == '__main__':
    df = data.request_data_2h()
    df = generate_feature.get_price_features(df)
    # df = generate_label.generate_label_rate(df)
    df = generate_label.generate_label_low(df)
    train_data = df.iloc[:-30]
    test_data = df.iloc[-30:]
    prediction = get_model(train_data, test_data)
    print(prediction)