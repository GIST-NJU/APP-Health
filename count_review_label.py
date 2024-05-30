import csv
import common as com
import random
if __name__ == '__main__':
    app_categories = ['life', 'business', 'education', 'music', 'entertainment', 'navigation', 'news', 'social', 'tool',
                      'travel']

    title =['content','|','feature assessment','feature bug','gui','guide','download','accessibility','software','hardware','speed','resource consumption','aging',
            'data','privacy','malicious','account','contents','ad','price','feedback','competitive products','suggest','release']
    train_file = 'data/selected_test_reviews/已标记/merge/onehot/train.csv'
    #result = open(train_file, 'w', encoding='utf-8', newline='')  # , encoding= 'utf-8')
    #train_csv_writer = csv.writer(result)
    #train_csv_writer.writerow(title)
    label_num = [0] * 23

    for app_category in app_categories:
    # 转化为 onehot 文件
        review_file = 'data/selected_test_reviews/已标记/merge/news/CHINA DAILY_test_reviews_preprocess_label.csv'
        review_list = com.read_csv(review_file)
        write_file = 'data/selected_test_reviews/已标记/merge/onehot/CHINA DAILY_onehot.csv'
        result = open(write_file, 'w+', encoding='utf-8', newline='')  # , encoding= 'utf-8')
        csv_writer = csv.writer(result)
        csv_writer.writerow(title) #写入标题
        i = 0

        for review in review_list:

            write_list = [0] * 24
            write_list[0] = review[1]  # 评论内容
            if review[0] == '0':
             write_list[1] = 1
            else:
                for index in review[0].split('-'):
                    index = int(index)
                    write_list[index + 1] = 1
                    i+=1
                print(i)
                print(write_list)
            csv_writer.writerow(write_list)

    # 统计标签分布
            for review in review_list:
                 label_list = review[0].split('-')
                 for label in label_list:
                     label = int(label)
                     label_num[label] += 1
    print(label_num)

    #tool：[2460000, 1670000, 2740000, 940000, 120000, 1040000, 20000, 410000, 800000, 1010000, 190000, 100000, 100000, 240000, 1000000, 720000, 1750000, 810000, 1050000, 480000, 490000, 700000, 580000]
    #travel：[1710000, 1980000, 1690000, 520000, 330000, 480000, 10000, 380000, 330000, 570000, 80000, 100000, 160000, 380000, 870000, 660000, 2440000, 340000, 2460000, 2540000, 770000, 680000, 480000]
    #life：[1980000, 1910000, 1420000, 690000, 130000, 430000, 0, 160000, 530000, 590000, 80000, 0, 430000, 230000, 960000, 540000, 2070000, 490000, 1800000, 1370000, 270000, 610000, 680000]
    #business：[1800000, 2650000, 2080000, 1210000, 220000, 520000, 0, 710000, 1070000, 600000, 100000, 150000, 230000, 410000, 580000, 820000, 1730000, 500000, 980000, 680000, 650000, 1170000, 560000]
    #education：[3140000, 2220000, 1450000, 430000, 210000, 220000, 0, 260000, 670000, 430000, 10000, 0, 10000, 120000, 120000, 330000, 1020000, 240000, 770000, 130000, 200000, 940000, 470000]
    #navigation:[1710000, 2850000, 1700000, 320000, 20000, 490000, 10000, 410000, 310000, 250000, 70000, 0, 0, 180000, 240000, 80000, 1280000, 1730000, 360000, 190000, 310000, 420000, 930000]
    #news:[2040000, 2120000, 1240000, 1290000, 50000, 740000, 0, 260000, 800000, 440000, 100000, 10000, 150000, 90000, 600000, 170000, 3480000, 880000, 1160000, 220000, 350000, 1180000, 660000]
    #social:[1520000, 2360000, 2380000, 1110000, 70000, 610000, 0, 310000, 1070000, 550000, 120000, 60000, 90000, 470000, 380000, 500000, 1760000, 980000, 530000, 380000, 400000, 1320000, 840000]
    #music:[3290000, 1470000, 1620000, 290000, 120000, 1010000, 0, 290000, 380000, 300000, 40000, 20000, 20000, 60000, 320000, 90000, 1010000, 410000, 2600000, 500000, 200000, 400000, 370000]
    #entertainment:[4490000, 1230000, 1630000, 360000, 80000, 420000, 10000, 130000, 510000, 240000, 70000, 20000, 0, 50000, 230000, 90000, 680000, 580000, 1130000, 450000, 450000, 590000, 610000]
