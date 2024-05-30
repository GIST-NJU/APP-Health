import pandas as pd
import csv
import os
import re
from pyltp import SentenceSplitter
from pyltp import Segmentor
from datetime import datetime
import common as com

def sort(input_file, output_file):
    all_reviews = []
    all_date = []
    line_num = 1
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for line in reader:
            line_num += 1
            date = line[2].strip()
            rate = line[4].strip().split('.')[0]
            #strip()表示删除掉数据中的换行符
            #split（‘，’）是数据中遇到‘,’ 就隔开
            # process each text
            #匹配中文，英文字母和数字
            title = re.sub('[^0-9A-Za-z\u4e00-\u9fa5]', '', line[5])#re.sub()用于替换字符串中的匹配项
            content = line[6].strip()

            text = title + '，' + content


            all_reviews.append('-*-'.join([text, date, rate]))
            all_date.append(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

            # print(line[5],'  :', text)

            # text_processed = review_process(text)
            # if len(text_processed) != 0:
            #     review_line = '-*-'.join([text_processed, date, rate])
            #     all_reviews.append(review_line)
            #     print(text,' :', review_line)
            #     all_date.append(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

    # sort by date and write to files
    all_reviews_sorted = [y for _, y in sorted(zip(all_date, all_reviews))]
    with open(output_file, 'w', encoding='utf-8') as file:
        temp_list = []
        for line in all_reviews_sorted:
            if line in temp_list:
                print('duplicated review text: ' + line)
            else:
                temp_list.append(line)
                file.write(line)
                file.write('\n')



if __name__ == '__main__':

    apps = ['didi','tongcheng','shenzhou','douban','qingteng', 'qqzone', 'uc', 'pengpai',
            'wangyi', 'tengxunmap', 'weiche', 'dida', 'kugou', 'migu', 'lizhi', 'meituan',
            'beike', 'zhiyuanhui', 'xigua', 'migutv', 'changba', 'baidutext', 'bubei', 'hongen']
    apps = ['zoom', 'wecom', 'baidu', 'quark', 'airbnb',
            'mafengwo', 'Wechat', 'zhihu',
            'economist', 'CHINA DAILY', 'amap', 'kailichen', 'NetEase Cloud Music',
            'perfect piano', '58job', 'alipay', 'iqiyi', 'bilibili',
            'zuoyebang', 'baicizhan']
    for app in apps:
        dataframe = pd.read_csv('data/review_predicted/supp/dingding_review_pred_v2.txt')   #path是excel文件保存路径
#手动转换完格式才能继续抽样
#dataframe.drop(dataframe.columns[3],axis=1)
#sample方法随机抽取n行
#print(dataframe)
#exit()
        samples = dataframe.sample(n=100)

        samples.to_csv('data/review_predicted/supp/dingding_review_pred_v2_1.txt', encoding='utf-8')
        print(samples)

    exit()



    sort('reviews_train/baidu.txt', 'reviews_train/baidu.txt')
    dataframe = pd.read_csv('reviews_train/baidu.txt')
    #samples.drop(samples.columns[2],axis=1)
    print(dataframe)
    exit()
#写入新的excel
#samples.drop([0],inplace=True,axis=1)
    dataframe.to_csv('reviews_train/baidu.txt',encoding='utf-8')
#samples.to_csv('reviews/tencentmeet.txt',encoding='utf-8')  #保存抽样数据的路径
#dataframe = pd.read_excel('data/wechat_raw.xlsx')
#dataframe.to_csv('newdata/2.csv')
#data=pd.read_csv('newdata/2.csv')
#print(data)
#data1=pd.read_csv('data/tencentvideo_review_raw.csv')
#print(data1)
    exit()
dataframe.drop(dataframe.columns[0],axis=1)
#print(dataframe)
dataframe.to_csv('newdata/2.csv')

#data.to_csv('newdata/2.csv')
