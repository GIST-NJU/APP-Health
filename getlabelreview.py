import csv
import os
import re
import pandas as pd
from pyltp import SentenceSplitter
from pyltp import Segmentor
from datetime import datetime
import common as com
from random import sample

# pos_model_path = os.path.join(LTP_DATA_DIR, 'ltp-model/pos.model')
# par_model_path = os.path.join(LTP_DATA_DIR, 'ltp-model/parser.model')
# cut_text_path = os.path.join(LTP_DATA_DIR, 'word_segmentation.txt')
# stop_text_path = os.path.join(LTP_DATA_DIR, 'stop_words.txt')
#
# segmentor = Segmentor()
# segmentor.load(cws_model_path)


# segmentor.load_with_lexicon(cws_model_path, cut_text_path)

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
        # words = list(segmentor.segment(sent1))
        # # print(sent1, words)
        # # remove stop words去停用表
        # remain_text = [item for item in words if item not in stopwords]
        # if len(remain_text) > 0:
        #     new_text.append(sent)
    new_text = ''.join(remain_text)
    if new_text.startswith('，'):
        new_text = new_text[1:]
    return new_text

def process(input_file, output_file):
    all_reviews = []
    #all_date = []
    line_num = 1
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for line in reader:
            line_num += 1
            content = line[1].strip()
            #print(content)

            #去掉-*-2021-07-11 22:55:42-*-5

            p1, p2, p3 = content.partition('-*-')
            #print(p1)
            #exit()
            content = ''.join(p1)
            content = content.replace('\n', '。')
            text = ',' + content
            print(text)


            all_reviews.append(text)

    with open(output_file, 'w', encoding='utf-8') as file:
        temp_list = []
        for line in all_reviews:
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
    apps = [  'xigua', 'migutv', 'changba']
    apps = ['zoom', 'wecom', 'baidu', 'quark', 'airbnb',
            'mafengwo', 'Wechat', 'zhihu',
            'economist', 'CHINA DAILY', 'amap', 'kailichen', 'NetEase Cloud Music',
            'perfect piano', '58job', 'alipay', 'iqiyi', 'bilibili',
            'zuoyebang', 'baicizhan']

    for app in apps:
        process('reviews_train/{}_supp.txt'.format(app), 'data/selected_test_reviews/已标记/merge/supp/{}_test_reviews_preprocess_label.csv'.format(app))
    #review=pd.read_csv('selected_test_reviews/已标记/merge/life/alipay_test_reviews_preprocess_label.csv')
    #print(review)
    exit()
