# -*- coding: utf-8 -*-
"""
Created on Thu May 30 17:12:37 2019

@author: cm
"""

import os
import sys

pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import numpy as np
import tensorflow as tf
from networks import NetworkAlbertTextCNN
from classifier_utils import get_feature_test, id2label
from hyperparameters import Hyperparamters as hp
import csv
from sklearn.metrics import hamming_loss, precision_score, recall_score, f1_score, classification_report


class ModelAlbertTextCNN(object, ):
    """
    Load NetworkAlbert TextCNN model
    """

    def __init__(self):
        self.albert, self.sess = self.load_model()

    @staticmethod
    def load_model():
        with tf.Graph().as_default():
            sess = tf.Session()
            with sess.as_default():
                albert = NetworkAlbertTextCNN(is_training=False)
                saver = tf.train.Saver()
                sess.run(tf.global_variables_initializer())
                checkpoint_dir = os.path.abspath(os.path.join(pwd, hp.file_load_model))
                print(checkpoint_dir)
                ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
                saver.restore(sess, ckpt.model_checkpoint_path)
        return albert, sess


MODEL = ModelAlbertTextCNN()
print('Load model finished!')


def read_txt(file):
    f = open(file, encoding='utf-8')
    lines = f.readlines()
    return lines


def read_csv(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = []
        reader = csv.reader(f)
        for line in reader:
            lines.append(line)
    f.close()
    return lines


def get_label(sentence):
    """
    Prediction of the sentence's label.
    """
    feature = get_feature_test(sentence)
    fd = {MODEL.albert.input_ids: [feature[0]],
          MODEL.albert.input_masks: [feature[1]],
          MODEL.albert.segment_ids: [feature[2]],
          }
    prediction = MODEL.sess.run(MODEL.albert.predictions, feed_dict=fd)[0]
    return prediction  # [l for l in np.where(prediction==1)[0] if l!=0]


def pred_file(input_file, output_file):
    review_list = read_txt(input_file)
    f = open(output_file, 'w+', newline='', encoding='utf-8')
    num = 0
    for review in review_list:
        num += 1
        if num % 1000 == 0:
            print('已完成 ' + str(num) + ' 条，剩余 ' + str(len(review_list) - num) + ' 条')
        temp_list = review.split('-*-')
        review_content = temp_list[0]
        label = get_label(review_content)
        label = [str(l) for l in np.where(label == 1)[0] if l != 0]
        temp_list.insert(0, '-'.join(label) if len(label) != 0 else '0')
        f.write('-*-'.join(temp_list))
    f.close()


if __name__ == '__main__':
    # pred_file('data/onehot/app/Hero Scanner.txt', 'data/predict/Hero Scanner_review_pred_v2.txt')
    apps = ['didi', 'tongcheng', 'shenzhou', 'douban']
    apps = ['zoom', 'wecom', 'baidu', 'quark', 'airbnb',
            'mafengwo', 'Wechat', 'zhihu',
            'economist', 'CHINA DAILY', 'amap', 'kailichen', 'NetEase Cloud Music',
            'perfect piano', '58job', 'alipay', 'iqiyi', 'bilibili',
            'zuoyebang', 'baicizhan']

    for app in apps:
        pred_file('data/onehot/supp/{}.txt'.format(app), 'data/onehot/supp/{}_review_pred_v2.txt'.format(app))
    exit()

    # prediction = get_label('优惠力度超级大，这里面都是推荐加盟项目的，购物内容很多 而且很有保障 比其他购物平台好多了 多多支持')
    # print([l for l in np.where(prediction==1)[0] if l!=0])
    # exit()
    app_categories = ['business', 'education', 'entertainment', 'life', 'music',
                      'navigation', 'news', 'social', 'tool', 'travel']
    # app_categories = ['life']
    # app_category = ['Airbnb', 'baidu', 'CHINA DAILY', 'economist', 'mafengwo',
    # 'quark', 'Wechat', 'wecom', 'zhihu', 'zoom']
    app_category = ['airbnb']
    f_test = open("median_result.txt", 'w+', encoding='utf-8')
    ave_acc = 0
    y_true, y_pre = [], []
    for app_category in app_category:
        file = 'data/onehot/app/{}.txt'.format(app_category)
        review_list = read_csv(file)
        pred_file('data/onehot/app/{}.txt'.format(app_category),
                  'data/onehot/app/{}_review_pred.txt'.format(app_category))
        f_test.write("\n\n" + "app_category:" + app_category + "\n")
        label_num = 0
        equal_label_num = 0
        for review in review_list[1:]:
            sent = review[0]
            pre_label = get_label(sent)
            actual_label = [int(value) for value in review[1:]]

            # print(actual_label)
            f_test.write(str(review))
            f_test.write('\n')
            f_test.write('golden: ' + sent + "      ")
            f_test.write(str(actual_label))
            f_test.write('\n')
            f_test.write('pred: ' + str(pre_label) + '\n')
            label_num += 1

            y_true.append(actual_label)
            y_pre.append(pre_label)

            pre_label = [l for l in np.where(pre_label == 1)[0] if l != 0]
            actual_label = np.array(actual_label)
            actual_label = [l for l in np.where(actual_label == 1)[0] if l != 0]
            # print(actual_label, '  pre: ', pre_label)
            # f_test.write(str(review) + '\n')
            f_test.write(str(actual_label) + '  pre: ' + str(pre_label) + '\n')

            if pre_label == actual_label:
                equal_label_num += 1
            f_test.write("label_num: " + str(label_num) + '  equal:' + str(equal_label_num) + '\n')
        acc = equal_label_num / label_num
        ave_acc += acc
    # print(app_category, " subset accuracy: ", acc)
    # print("average subset accuracy: ", ave_acc / 10)
    # print('weighted precision', precision_score(y_true, y_pre, average='weighted'))
    # print('macro precision', precision_score(y_true, y_pre, average='macro'))
    # print('samples precision', precision_score(y_true, y_pre, average='samples'))
    # print('weighted recall ', recall_score(y_true, y_pre, average='weighted'))
    # print('macro recall ', recall_score(y_true, y_pre, average='macro'))
    # print('samples recall ', recall_score(y_true, y_pre, average='samples'))
    #
    # print('weighted f1 score', f1_score(y_true, y_pre, average='weighted'))
    # print('macro f1 score', f1_score(y_true, y_pre, average='macro'))
    # print('samples f1 score', f1_score(y_true, y_pre, average='samples'))

    print(classification_report(y_true, y_pre, digits=4))







