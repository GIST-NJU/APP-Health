import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
import common as com
from datetime import datetime

def get_font_num_list(file):
    releases = com.read_csv(file)
    wordNumList = []
    for release in releases:
        release = release[4] + release[5]
        try:
            release = re.sub('[^0-9A-Za-z\u4e00-\u9fa5]', ' ', release)
            wordNumList.append(len(release))
        except:
            print(file)
            print(release)
    wordNumList.sort()
    return wordNumList

def get_date_list(file):
    releases = com.read_csv(file)
    dateList = []
    for release in releases:
        release = release[1].split(" ")[0]
        try:
            dateList.append(release)
        except:
            print(file)
            print(release)
    dateList.sort()
    return dateList
#评论字数
def get_date_reviewnum_dict(file):
    reviews = com.read_csv(file)
    all_date = []
    dict = {}
    for review in reviews:
        date = review[1].split(" ")[0]
        if date not in all_date:
            all_date.append(date)
        if dict.__contains__(date):
            dict[date] += 1
        else:
            dict[date] = 1
    all_date = sorted(all_date)
    review_num_list = []
    for date in all_date:
        review_num_list.append(dict[date])
    all_date_time = []
    for date in all_date:
        all_date_time.append(datetime.strptime(date, '%Y-%m-%d'))

    return all_date_time, review_num_list

# 字数箱线图
def get_word_num_boxplot(y1, y2, y3, y4, y5):

    # 数据长度不一样时
    y1 = pd.Series(np.array(y1))
    y2 = pd.Series(np.array(y2))
    y3 = pd.Series(np.array(y3))
    y4 = pd.Series(np.array(y4))
    y5 = pd.Series(np.array(y5))
    data = pd.DataFrame({"支付宝": y1, "钉钉": y2, "网易云音乐": y3, "腾讯视频": y4, "微信": y5})
    df = pd.DataFrame(data)
    df.plot.box()

    plt.xlabel("应用名", fontsize=13)
    plt.ylabel("字数", fontsize=13)
    plt.grid(linestyle="--", alpha=0.8)
    print(df.describe())  # 显示中位数、上下四分位数、标准偏差等内容
    plt.show()


if __name__=='__main__':
    app_list = ['钉钉','支付宝','腾讯视频','网易云音乐','微信' ]
    # y1 = get_font_num_list('D:/rq23_new/review-raw/{}_review_raw.csv'.format("alipay"))
    # y2 = get_font_num_list('D:/rq23_new/review-raw/{}_review_raw.csv'.format("dingtalk"))
    # y3 = get_font_num_list('D:/rq23_new/review-raw/{}_review_raw.csv'.format("netmusic"))
    # y4 = get_font_num_list('D:/rq23_new/review-raw/{}_review_raw.csv'.format("tencentvideo"))
    # y5 = get_font_num_list('D:/rq23_new/review-raw/{}_review_raw.csv'.format("wechat"))
    rcParams['axes.unicode_minus'] = False
    rcParams['font.sans-serif'] = ['Simhei']
    # get_word_num_boxplot(y1, y2, y3, y4, y5)
    # all_date_time_alipay, review_num_list_alipay = get_date_reviewnum_dict(
    #     'D:/rq23_new/review-raw/{}_review_raw.csv'.format("alipay"))
    # all_date_time_dingtalk, review_num_list_dingtalk = get_date_reviewnum_dict(
    #     'D:/rq23_new/review-raw/{}_review_raw.csv'.format("dingtalk"))
    # all_date_time_netmusic, review_num_list_netmusic = get_date_reviewnum_dict(
    #     'D:/rq23_new/review-raw/{}_review_raw.csv'.format("netmusic"))
    # all_date_time_tencentvideo, review_num_list_tencentvideo = get_date_reviewnum_dict(
    #     'D:/rq23_new/review-raw/{}_review_raw.csv'.format("tencentvideo"))
    all_date_time_wechat, review_num_list_wechat = get_date_reviewnum_dict('raw_review/{}.csv'.format("Wechat"))
    print(review_num_list_wechat)