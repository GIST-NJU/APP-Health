import math
import pandas as pd
import csv
import random
import matplotlib
from common import read_txt, read_csv
import datetime
import csv
import re
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from loguru import logger
#获取 app 得版本日期 和 带标记得用户评论
#num_of_releases = 5
num_of_releases = 1
release_date_index = 1

review_label_index = 0
review_content_index = 1
review_date_index = 2
review_rate_index = 3

#start_release_no = 50  #开始的 release 标号

date_str = '%Y-%m-%d'
date_str1 = '%Y-%m-%d %H:%M'
release_path = 'data/release'
pred_path = 'data'

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  #SimHei黑体  FangSong仿宋
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.unicode_minus'] = False

labels = ['feature assessment','feature bug','gui','guide','download',
          'accessibility','software','hardware','speed','resource consumption',
          'aging','data','privacy','malicious','account',
          'contents','ad','price','feedback','competitive products',
          'suggest','release'
          ]

def get_start_release(app_name):
    app_release_path='data/release/month.csv'.format(app_name)
    releases= pd.read_csv(app_release_path)
    num=len(releases)
    #可能存在超出索引问题
    #start_num = random.sample(range(0,num),5)
    #print(start_num)
    return num



def get_days(day1, day2):
    """
    计算两个日期相隔几天
    :param day1: {str} 如 2020-04-05 17:41:20
    :param day2:
    :return:  days {int}
    """
    d1 = datetime.datetime.strptime(day1, date_str)
    d2 = datetime.datetime.strptime(day2, date_str)
    delta = d1 - d2
    return delta.days + 1

#获取 app 得版本日期 和 带标记得用户评论
def get_release_date(app_name):
    app_release_sub_path = '{}_all_releases.csv'.format(app_name)
    app_pred_sub_path = 'review_predicted/{}_review_pred.txt'.format(app_name)
    app_release_file = os.path.join(release_path, app_release_sub_path)
    app_review_pred_file = os.path.join(pred_path, app_pred_sub_path)
    releases = read_csv(app_release_file)
    app_categories = ['Wechat']
    #改了一下日期显示
    result_file = 'data/release/{}_all_releases_1.csv'.format(app_name)

    result = open(result_file, 'w', encoding='utf-8', newline='')  # , encoding= 'utf-8')
    csv_writer = csv.writer(result)
    lines = 0
    release_date_list = []
    for release in releases:
        lines += 1
        #content = release[1].strip()
        releas=release[0]
        content=release[7].replace('\n', '')
        #print(content)
        #exit()
        time = release[1].replace('年', '/')
        time= time.replace('月', '/')
        release[1] = time.replace('日', '').strip()
        csv_writer.writerow( release)




#get_release_date('Wechat')

def get_month_date_and_labeled_reviews(app_name):
    app_month_sub_path = 'month.csv'
    app_pred_sub_path = 'review_predicted/{}_review_pred_v2.txt'.format(app_name)
    app_month_file = os.path.join(release_path, app_month_sub_path)
    app_review_pred_file = os.path.join(pred_path, app_pred_sub_path)
    months = read_csv(app_month_file)

    month_date_list = []
    for month in months:
        month_date = re.sub('/', '-', month[1])
        month_date = datetime.datetime.strptime(month_date, date_str)
        month_date_list.append(month_date)
    labeled_reviews = read_txt(app_review_pred_file)  # 带标记的评论
    #print(release_date_list, labeled_reviews)
    return month_date_list, labeled_reviews


#get_release_date_and_labeled_reviews('Wechat')


def get_average_rating(releases_reviews_list):
    average_ratings = [0] * 24

    for index, review_list in enumerate(releases_reviews_list):

        for review in review_list:
            review_rate = int(review[review_rate_index])
            average_ratings[index] += review_rate

        if len(review_list) != 0:
            average_ratings[index] = average_ratings[index] / len(review_list)

        else:

            average_ratings[index] = 2.5
    return average_ratings


# 评论推荐，pre_releases_reviews_list 存放了该版本每个关注点对应的评论
def recommending_reviews(reviews_list, index):
    if index == 0:
        logger.info('评论类型：无用评论')
    elif index == 15:
        logger.info('评论类型：所有评论')
    elif index > 0 and index < 15:
        logger.info('评论类型：' + labels[index - 1])
    else:
        logger.warning('无效索引，请重新输入！')
        exit()
    logger.info('评论条数：' + str(len(reviews_list[index])))

    recommended_reviews = []
    for review in reviews_list[index]:  # 对index方面进行推荐：[3], 0 : 无关评论  15：所有评论
        review_content = review[review_content_index].strip()
        review_rate = int(review[review_rate_index])
        score = math.exp(-(review_rate / len(review_content)))
        recommended_reviews.append([review_content, score, review_rate])
    recommended_reviews.sort(key=takeSecond, reverse=True)
    return recommended_reviews


def takeSecond(element):
    return element[1]


# 获取 应用编号为 start_release_no 的评论
def get_reviews(app_name, start_release_no):
    release_date_list, labeled_reviews = get_month_date_and_labeled_reviews(app_name)
    date_start = release_date_list[start_release_no]
    date_medium = release_date_list[start_release_no + 1]
    date_end = release_date_list[start_release_no + num_of_releases + 1]
    # 存放之前 num_of_releases 个版本对应标签的评论, 15 放所有评论, 0 放无用评论
    pre_releases_reviews_list = [[] for _ in range(16)]
    #print(pre_releases_reviews_list)

    # 存放最近一版本对应标签的评论
    latest_releases_reviews_list = [[] for _ in range(16)]
    # print(pre_releases_reviews_list)
    for labeled_review in labeled_reviews:
        labeled_review = labeled_review.strip('\n').split('-*-')
        # 评论的标签列表
        review_label_list = labeled_review[review_label_index].split('-')
        # 评论的内容
        review_content = labeled_review[review_content_index]
        # 评论的日期
        review_date = labeled_review[review_date_index]
        review_date = datetime.datetime.strptime(review_date[0:-3], date_str1)
        review_rate = labeled_review[review_rate_index]
        #print(review_rate)
        # 评论的对应评分
        # review_rate = labeled_review[review_rate_index]

        if review_date <= date_start and review_date > date_medium:
            for label in review_label_list:
                latest_releases_reviews_list[15].append(labeled_review)
                latest_releases_reviews_list[int(label)].append(labeled_review)

        elif review_date <= date_medium and review_date >= date_end:
            for label in review_label_list:
                pre_releases_reviews_list[15].append(labeled_review)
                pre_releases_reviews_list[int(label)].append(labeled_review)
    #print(latest_releases_reviews_list)
    return pre_releases_reviews_list, latest_releases_reviews_list


# 从评分变化列表中返回处于特别健康 和 特别不健康的值的索引列表
def get_very_positive_negative_index(rating_change_list):
    very_positive_index_list, very_negative_index_list = [], []
    for index, value in enumerate(rating_change_list):
        if index == 0 or index == 15:  # 无用评论/所有评论 的评分变化情况
            continue
        if value >= 1.49:
            very_positive_index_list.append(index)
        elif value <= -1.55:
            very_negative_index_list.append(index)

    return very_positive_index_list, \
           very_negative_index_list


def get_rating_change_list(app_name):
    rating_change_list = []
    f = open('medium_result_ttt.txt', 'w+', encoding='utf-8')
    all_release_change_average_ratings = []
    release_date_list = []
    f.write('----------------------start ' + app_name + '----------------------' + '\n')
    release_date_list, labeled_reviews = get_month_date_and_labeled_reviews(app_name)
    # 对每个 app 每个版本进行操作
    for start_release_no in range(0, len(release_date_list) - num_of_releases - 1):
        # 前 num_of_releases 个版本内的评论列表， 最近一个版本的评论列表
        pre_releases_reviews_list, latest_releases_reviews_list = get_reviews(app_name, start_release_no)
        pre_average_ratings = get_average_rating(pre_releases_reviews_list)
        latest_average_rating = get_average_rating(latest_releases_reviews_list)
        # 评论推荐，pre_releases_reviews_list 存放了该版本每个关注点对应的评论
        # recommended_reviews = recommending_reviews(pre_releases_reviews_list)
        for index, average_rating in enumerate(pre_average_ratings):
            if average_rating != 0 and latest_average_rating[index] != 0:
                rating_change_list.append(latest_average_rating[index] - average_rating)

        # 当前 app 在当前版本上所有类型评论集合得评分变化情况
        change_average_ratings = np.array(latest_average_rating) - np.array(pre_average_ratings)
        all_release_change_average_ratings.append(change_average_ratings)

    rating_change_list.sort()
    return all_release_change_average_ratings, release_date_list[:-6], \
           rating_change_list  # 获得所有评分变化数据


# 绘制 评分变化随着月份变化的曲线
def plot_rating_change(app_name):
    # all_release_change_average_ratings 每一行为一个版本 各个关注点的评分变化值
    all_release_change_average_ratings, release_date_list, _ = get_rating_change_list(app_name)
    all_release_change_average_ratings = np.array(all_release_change_average_ratings)
    print(all_release_change_average_ratings)
    # print(np.transpose(all_release_change_average_ratings)[1])  # 评分变化值的变化列表，每一行为一个关注点
    # print(len(all_release_change_average_ratings), len(release_date_list))
    # 初始化横坐标的所有值(这里表示为时间的变化)
    release_date_list = np.transpose(release_date_list)[50:70]
    x = range(1, len(release_date_list) + 1)
    # 初始化所有不同数据集纵坐标表示的值(可以表示团队个人一天工作时间的分配)
    user_concern_bug, user_concern_gui, user_concern_performance, user_concern_security, \
    user_concern_resource, user_concern_feedback, user_concern_download, user_concern_pricing, \
    user_concern_ad, user_concern_advice, user_concern_guide, user_concern_compatibility, \
    user_concern_update, user_concern_evaluation, app = np.transpose(all_release_change_average_ratings)[1:16]

    labels = ['feature assessment', 'feature bug', 'gui', 'guide', 'download',
              'accessibility', 'software', 'hardware', 'speed', 'resource consumption',
              'aging', 'data', 'privacy', 'malicious', 'account',
              'contents', 'ad', 'price', 'feedback', 'competitive products',
              'suggest', 'release']

    # 注意传入的多个可迭代对象的维度应该相同
    # plt.plot(x, user_concern_bug, user_concern_gui, user_concern_performance,
    #          labels=['BUG', 'GUI', '性能'], colors=['#6d904f', '#fc4f30', '#008fd5'])

    x_new = np.linspace(x[0], x[-1], 300)  # 300 represents number of points to make between T.min and T.max
    y_smooth_1 = make_interp_spline(x, user_concern_bug[50:70])(x_new)
    y_smooth_2 = make_interp_spline(x, user_concern_gui[50:70])(x_new)
    y_smooth_3 = make_interp_spline(x, user_concern_performance[50:70])(x_new)  # 性能这一关注点
    y_smooth_4 = make_interp_spline(x, user_concern_security[50:70])(x_new)
    app_smoth = make_interp_spline(x, app[50:70])(x_new)  # 整个 app

    # 画单个图
    # plt.plot(x_new, y_smooth_1, color='darkred', label='关注点：BUG', linewidth=1)
    # plt.plot(x_new, y_smooth_2, color='#6d904f', label='关注点：GUI', linewidth=1)
    # plt.plot(x_new, y_smooth_3, color='#fc4f30', label='关注点：性能', linewidth=1)
    # plt.plot(x_new, y_smooth_4, color='#008fd5', label='关注点：安全 & 授权', linewidth=1)
    # plt.legend(loc=1)
    # plt.xlabel('应用版本')  # 设置 x 轴标签及其字体大小
    # plt.ylabel('评分变化值')
    # # 添加水平直线
    # plt.axhline(y=-4, ls="--", c="red", linewidth=1)
    # plt.axhline(y=-1.55, ls="--", c="orangered", linewidth=1)
    # plt.axhline(y=-0.79, ls="--", c="tomato", linewidth=1)
    # plt.axhline(y=0.73, ls="--", c="palegreen", linewidth=1)
    # plt.axhline(y=1.49, ls="--", c="palegreen", linewidth=1)
    # plt.axhline(y=4, ls="--", c="lawngreen", linewidth=1)
    # plt.savefig('fig/dingtalk2.jpg', dpi=500, bbox_inches='tight')
    # # 美化输出
    # plt.tight_layout()
    # plt.show()

    # 后续全为画多个图
    # 画图注释详见同目录下 matplotlib_example.py
    plt.figure(figsize=(20, 20))
    plt.subplot(221)  # 子图, 两行两列，目前第1个图
    plt.plot(x_new, y_smooth_1, color='darkred', label='关注点：feature assessment', linewidth=2)
    plt.legend(loc=1, fontsize=20)
    plt.xlabel('月份', fontsize=20)  # 设置 x 轴标签及其字体大小
    plt.ylabel('评分变化值', fontsize=20)
    # 添加水平直线
    plt.axhline(y=-4, ls="--", c="red", linewidth=2)
    plt.axhline(y=-1.55, ls="--", c="orangered", linewidth=2)
    plt.axhline(y=-0.79, ls="--", c="tomato", linewidth=2)
    plt.axhline(y=0.73, ls="--", c="palegreen", linewidth=2)
    plt.axhline(y=1.49, ls="--", c="palegreen", linewidth=2)
    plt.axhline(y=4, ls="--", c="lawngreen", linewidth=2)

    plt.subplot(222)  # 子图, 两行两列，目前第1个图
    plt.plot(x_new, y_smooth_2, color='#6d904f', label='关注点：feature bug', linewidth=2)
    plt.legend(loc=1, fontsize=20)
    plt.xlabel('应用版本', fontsize=20)  # 设置 x 轴标签及其字体大小
    plt.ylabel('评分变化值', fontsize=20)
    # 添加水平直线
    plt.axhline(y=-4, ls="--", c="red", linewidth=2)
    plt.axhline(y=-1.55, ls="--", c="orangered", linewidth=2)
    plt.axhline(y=-0.79, ls="--", c="tomato", linewidth=2)
    plt.axhline(y=0.73, ls="--", c="palegreen", linewidth=2)
    plt.axhline(y=1.49, ls="--", c="palegreen", linewidth=2)
    plt.axhline(y=4, ls="--", c="lawngreen", linewidth=2)

    plt.subplot(223)
    plt.plot(x_new, y_smooth_3, color='#fc4f30', label='关注点：gui', linewidth=2)
    plt.legend(loc=1, fontsize=20)
    plt.xlabel('应用版本', fontsize=20)  # 设置 x 轴标签及其字体大小
    plt.ylabel('评分变化值', fontsize=20)
    # 添加水平直线
    plt.axhline(y=-4, ls="--", c="red", linewidth=2)
    plt.axhline(y=-1.55, ls="--", c="orangered", linewidth=2)
    plt.axhline(y=-0.79, ls="--", c="tomato", linewidth=2)
    plt.axhline(y=0.73, ls="--", c="palegreen", linewidth=2)
    plt.axhline(y=1.49, ls="--", c="palegreen", linewidth=2)
    plt.axhline(y=4, ls="--", c="lawngreen", linewidth=2)

    plt.subplot(224)
    plt.plot(x_new, y_smooth_4, color='#008fd5', label='关注点：guide', linewidth=2)

    # plt.plot(x_new, app_smoth, color='peru', label='钉钉', linewidth=2)

    # plt.plot(x, user_concern_bug, color='#6d904f', label='BUG', linewidth=2)
    # plt.plot(x, user_concern_gui, color='#fc4f30', label='GUI', linewidth=2)
    # plt.plot(x, user_concern_performance, color='#008fd5', label='性能', linewidth=2)

    # legend接受loc参数可以改变显示标签的放置位置, 可以用一个元组加两个数来表示距离坐标轴原点的百分比距离,\
    #  也可以使用字符串表示:
    plt.legend(loc=1, fontsize=20)
    plt.xlabel('应用版本', fontsize=20)  # 设置 x 轴标签及其字体大小
    plt.ylabel('评分变化值', fontsize=20)
    # 添加水平直线
    plt.axhline(y=-4, ls="--", c="red", linewidth=2)
    plt.axhline(y=-1.55, ls="--", c="orangered", linewidth=2)
    plt.axhline(y=-0.79, ls="--", c="tomato", linewidth=2)
    plt.axhline(y=0.73, ls="--", c="palegreen", linewidth=2)
    plt.axhline(y=1.49, ls="--", c="palegreen", linewidth=2)
    plt.axhline(y=4, ls="--", c="lawngreen", linewidth=2)
    plt.savefig('figure/month/wechat.jpg', dpi=500, bbox_inches='tight')
    # 美化输出
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    print('aaa')
    #plot_rating_change()
    start_release_no = 0
    #app_name_list = ['58job','airbnb','alipay','amap','baicizhan','baidu','bilibili','CHINA DAILY',
                     #'economist','iqiyi','kailichen','mafengwo','NetEase Cloud Music','perfect piano',
                     #'quark','wecom','zhihu','zoom','zuoyebang']
    #app_name_list = ['airbnb', 'baidu', 'CHINA DAILY',
                     #'economist','mafengwo',
                     #'quark', 'wecom', 'zhihu', 'zoom']
    app_name = 'zuoyebang'
    plot_rating_change(app_name)
