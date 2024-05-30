import csv
import common as com
import random

if __name__ == '__main__':
    app_categories = ['life', 'business', 'education', 'music', 'entertainment', 'navigation', 'news', 'social', 'tool',
                      'travel']

    title = ['content', '|', 'feature assessment', 'feature bug', 'gui', 'guide', 'download', 'accessibility',
             'software', 'hardware', 'speed', 'resource consumption', 'aging',
             'data', 'privacy', 'malicious', 'account', 'content', 'ad', 'price', 'feedback', 'competitive products',
             'suggest', 'release']
    train_file = 'data/selected_test_reviews/已标记/merge/onehot/train.csv'
    result = open(train_file, 'w', encoding='utf-8', newline='')  # , encoding= 'utf-8')
    train_csv_writer = csv.writer(result)
    train_csv_writer.writerow(title)
    label_num = [0] * 23

    ##随机挑选部分内容
    for app_category in app_categories:
        # 训练集和测试集划分
        file = 'data/selected_test_reviews/已标记/merge/onehot/{}_onehot.csv'.format(app_category)
        test_file = 'data/selected_test_reviews/已标记/merge/onehot/{}_test.csv'.format(app_category)
        result = open(test_file, 'w', encoding='utf-8', newline='')  # , encoding= 'utf-8')
        csv_writer = csv.writer(result)
        csv_writer.writerow(title)

        review_list = com.read_csv(file)[1:]  # 第一行为title
        random.shuffle(review_list)  # 打乱数据
        for review in review_list[0:800]:
            train_csv_writer.writerow(review)

        for review in review_list[800:]:
            csv_writer.writerow(review)
