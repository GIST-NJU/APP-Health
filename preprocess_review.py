import csv
import os
import re
import pandas as pd
from pyltp import SentenceSplitter
from pyltp import Segmentor
from datetime import datetime
import common as com
from random import sample
LTP_DATA_DIR = 'resource/ltp_model'  # ltp模型目录的路径
stop_text_path = 'resource/stopwords.txt'
pos_model_path = os.path.join(LTP_DATA_DIR, 'ltp-model/pos.model')
par_model_path = os.path.join(LTP_DATA_DIR, 'ltp-model/parser.model')
cut_text_path = os.path.join(LTP_DATA_DIR, 'word_segmentation.txt')
stop_text_path = os.path.join(LTP_DATA_DIR, 'stop_words.txt')

cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
segmentor = Segmentor()
segmentor.load(cws_model_path)


segmentor.load_with_lexicon(cws_model_path, cut_text_path)

def readWords():
    result={}
    with open('resource/1.txt', encoding='UTF-8-sig') as f:
        for line in f:
            x = line.strip().split('=')
            result[x[0]]=x[1]
    return result

def keymap_replace(
        string: str,
        mappings: dict,
        lower_keys=False,
        lower_values=False,
        lower_string=False,
    ) -> str:
    replaced_string = string.lower() if lower_string else string
    for character, replacement in mappings.items():
        replaced_string = replaced_string.replace(
            character.lower() if lower_keys else character,
            replacement.lower() if lower_values else replacement
        )
    return replaced_string

def review_process(review):
    # split the whole sentence
    review = re.sub(' +', '', review)
    sentences = SentenceSplitter.split(review)
    # print(review)

    remain_text = []
    for sent in sentences:
        # word segmentation
        # print(sent)
        remain_text = re.sub('[^0-9A-Za-z\u4e00-\u9FEF]', ' ', sent.strip())
        words = list(segmentor.segment(sent))
        # # print(sent1, words)
        # # remove stop words去停用表
        # 去停用词
        stopwords = [line.strip() for line in open(stop_text_path, 'r', encoding='utf-8').readlines()]

        remain_text = [item for item in words if item not in stopwords]
        if len(remain_text) > 0:
            remain_text.append(sent)
    new_text = ''.join(remain_text)
    if new_text.startswith('，'):
        new_text = new_text[1:]
    return new_text

def process(input_file, output_file):
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
            #print(content)
            content = keymap_replace(content, readWords())
            #print(content)
            content = content.replace('\\', '')
            content = content.replace(',', '，')
            content = content.replace('.', '。')
            content = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5\,，。]+', str(content))#只匹配英文数字中文
            content = ''.join(content)
            content = re.sub('@[0-9A-Za-z\u4e00-\u9fa5]+', '',content)
            content = re.sub('[0-9A-Za-z\u4e00-\u9fa5]+？', '',content)
            content = re.sub('http[:.]+\S+','',content)
            #content = re.sub('[]+','',content) 去掉空格有错误
            content = re.sub('-{3,}', '', content)#转义
            content = content.replace('\n', '。')
            text = title + '，' + content
            #print(text)

            if '该条评论已经被删除' in text or len(text) > 5000:
                continue
            if "开发者回复" in text:
                text = text[:text.index('开发者回复')]

            all_reviews.append('-*-'.join([text, date, rate]))
            all_date.append(datetime.strptime(date,'%Y-%m-%d %H:%M:%S'))

            # print(line[5],'  :', text)

            #text_processed = review_process(text)
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


def test_review_after_preprocess(file):
    review_list = com.read_csv(file)
    for review in review_list:
        if len(review) != 5:
            print('length error', review)
        elif review[2] not in ['1', '2', '3', '4', '5']:
            print('rate error', review)
        else:
            try:
                datetime.strptime(review[0],  '%Y-%m-%d %H:%M:%S')
            except:
                print('date error', review)

if __name__ == '__main__':


    apps =  ['maimai','camscanner','tencentnews','BOSSzhipin','shixiseng',
        'TIM','Lark','weidian','qq tongbu','wifi','national antifraud center','china moblie',
        'qqemail','runoob','public exam radar','lebo','Variflight','hello','train12306',
        'trip','muniao','uber','yihai','edaijia','CSDN','Soul','redbook',
        'lover','baike','meipian','duitang','mystery','phoenix','toutiao','PCauto','tengcentnews',
        'yidian','ZOL','QTT','simeon','beijingmetropass','carsmart','cariscoming','nationwideviolation',
        'altitudetable','pocketbus','chexing','baidumap','dragonflyfm','showstart','music','missevan',
        'metronome','garageband','ringtune','sige','claws','lalamove','traffic control',
        'anjuke','fcbox','imdada','tmalgenie','goodlive','damai','shoujiduoduo','humandog',
        'taopiaopiao','radio','wallpaper','zymk','paper','muchong','jiakaobaodian',
        'supercourse','neteaseonline','kaishu','putonghua','xiaoyuan']
    for app in apps:
        #result_file =
        process('newdata/{}_supp.csv'.format(app), 'reviews/{}_supp.txt'.format(app))
    #review=pd.read_csv('reviews/airbnb.csv')
    #print(review)
    exit()
