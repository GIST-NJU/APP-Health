from common import read_txt, read_csv
import datetime
import csv
import re
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from loguru import logger
from sklearn import preprocessing
import numpy as np
import pandas as pd



pred_path = 'data'
review_date_index = 2
date_str1 = '%Y-%m-%d'



# 获取 应用编号为 start_release_no 的评论
def get_reviews_date(app_name):
    df = pd.read_csv('other_factor/{}_rank.csv'.format(app_name),header=None,encoding='utf-8')
    #df=df.drop(['应用(免费)','社交(免费)'],axis=1)
    print(df.head(2))
    df.to_csv('other_factor/{}_rank.csv'.format(app_name),encoding='utf-8',index=False)
    print(df)
    exit()
    app_pred_sub_path = 'review_predicted/{}_review_pred_v2.txt'.format(app_name)
    review_date_list = []
    labeled_reviews = read_txt(app_pred_sub_path)  # 带标记的评论
    for i in df:
        print()
        exit()
        for labeled_review in labeled_reviews:
            labeled_review = labeled_review.strip('\n').split('-*-')
            # 评论的日期
            review_date = labeled_review[review_date_index]
            review_date = datetime.datetime.strptime(review_date[0:-9], date_str1)
            print(i)
            print(review_date)
            exit()
            #if i == review_date:


#get_reviews_date('wechat')




df = pd.read_csv('month_score/factor_health/58job_factor_health.csv')
print(df['综合得分'])
x = np.array(df['综合得分'].values.reshape(-1,1))

#min_max_scaler = preprocessing.MinMaxScaler()#默认为范围0~1，拷贝操作
min_max_scaler = preprocessing.MinMaxScaler(feature_range = (1,3),copy = False)#范围改为1~3，对原数组操作
x_minmax = min_max_scaler.fit_transform(x)
print('x = ',x)
