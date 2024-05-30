import pandas as pd
import numpy as np
import numpy.linalg as nlg
import matplotlib.pyplot as plt
from factor_analyzer import FactorAnalyzer, calculate_kmo, calculate_bartlett_sphericity
from sklearn.preprocessing import StandardScaler
import matplotlib
import scipy.stats as stats
labels = ['feature assessment','feature bug','gui','guide','download',
          'software','hardware','speed','resource consumption',
          'aging','data','privacy','malicious','account',
          'contents','ad','price','feedback','competitive products',
          'suggest','release'
          ]


def get_all_apps_all_months_health_rank():
    contribution_rate = 0.8
    auto_choose_N = True  # 设置为True的时候就自动根据贡献率来选择因子个数，为False则要自己设置N
    N = 2

    file = "month_score/final/supp/cat/all_app_all_month_score_business_supp_v2.csv"
    f = pd.read_csv(file, sep=",", header=None)
    f = StandardScaler().fit_transform(f)  # 数据标准化

    f = pd.DataFrame(f)

    # 皮尔逊相关系数
    f_corr = f.corr()
    kmo = calculate_kmo(f)

    bartlett = calculate_bartlett_sphericity(f)
    if kmo[1] >= 0.7 and bartlett[1] <= 0.05:  # bartlett球形度检验p值要小于0.05 kmo值要大于0.7
        print("\n因子分析适用性检验通过\n")
    else:
        print("\n因子分析适用性检验未通过\n")
    print('kmo:{},bartlett:{}'.format(kmo[1], bartlett[1]))

    #  计算旋转前的载荷矩阵的方差贡献率,可以用来看有几个因子时总共先率到达多少
    Load_Matrix = FactorAnalyzer(rotation=None, n_factors=len(f.T), method='principal')
    Load_Matrix.fit(f)
    f_contribution_var = Load_Matrix.get_factor_variance()
    matrices_var = pd.DataFrame()
    matrices_var["旋转前特征值"] = f_contribution_var[0]
    matrices_var["旋转前方差贡献率"] = f_contribution_var[1]
    matrices_var["旋转前方差累计贡献率"] = f_contribution_var[2]
    #print(matrices_var)

    if auto_choose_N:
        sum_con = 0
        N = 0
        for c in matrices_var["旋转前方差贡献率"]:
            sum_con += c
            N += 1
            if sum_con >= contribution_rate:
                print("\n选择了" + str(N) + "个因子累计贡献率为"+str(sum_con)+"\n")
                break

    matplotlib.rcParams["font.family"] = "SimHei"  # 碎石图主要用来看取多少因子合适，一般是取到平滑处左右，当然还要需要结合贡献率


    # 使用主成分分析的方法来计算出因子载荷矩阵，使用最大方差法旋转因子载荷矩阵
    Load_Matrix_rotated = FactorAnalyzer(rotation='varimax', n_factors=N, method='principal')
    Load_Matrix_rotated.fit(f)

    #  计算旋转后的载荷矩阵的贡献率
    f_contribution_var_rotated = Load_Matrix_rotated.get_factor_variance()
    matrices_var_rotated = pd.DataFrame()
    matrices_var_rotated["特征值"] = f_contribution_var_rotated[0]
    matrices_var_rotated["方差贡献率"] = f_contribution_var_rotated[1]
    matrices_var_rotated["方差累计贡献率"] = f_contribution_var_rotated[2]
    #print(matrices_var_rotated)
    Load_Matrix_rotated = FactorAnalyzer(rotation='varimax', n_factors=N, method='principal')
    Load_Matrix_rotated.fit(f)

    # 计算因子得分（回归方法）（系数矩阵的逆乘以因子载荷矩阵）
    X1 = np.mat(f_corr)
    X1 = nlg.inv(X1)
    factor_score_weight = np.dot(X1, Load_Matrix_rotated.loadings_)
    factor_score_weight = pd.DataFrame(factor_score_weight)
    col = []
    for i in range(N):
        col.append("factor" + str(i+1))
    factor_score_weight.columns = col
    factor_score_weight.index = f_corr.columns
    #print("\n第一列为第一个因子得分函数的对应系数")
    #print("因子得分：\n", factor_score_weight)

    factor_score = pd.DataFrame(np.dot(np.mat(f), np.mat(factor_score_weight)))  # 指标 * 对应权重，计算出因子的分数

    i = 0
    factor_score["综合得分"] = 0
    for factor_score_weight in matrices_var_rotated["方差贡献率"]:
        factor_score["综合得分"] += factor_score_weight * factor_score[i]  # 因子贡献率 * 因子的分数 用于计算综合得分
        i += 1
        if i == N:
            break

    factor_score["综合得分"] = factor_score["综合得分"] / matrices_var_rotated["方差贡献率"].sum()  # 计算综合得分
    #factor_score.index = ["other", "feature assessment", "feature bug", "gui", "guide", "software", "hardware", "performance", "security", "account", "content", "ads", "feedback", "competitive", "request", "release"]  # 更改索引
    print('\n')
    # 20个app全放在一起做因子分析
    # 先给表格加上app名称

    index = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha',
                'tianyancha', '51job', 'sunlogin', 'newcow', 'Hero Scanner', 'Meituan Merchant',
                'zhitong']
    S=0
    app_name_list = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha',
                     'baidu', 'quark', 'Google Chrome', 'sf express', 'biubiu',
                     'airbnb', 'mafengwo', 'didi', 'tongcheng', 'shenzhou',
                     'Wechat', 'zhihu', 'douban', 'qingteng', 'qqzone',
                     'economist', 'CHINA DAILY', 'uc', 'pengpai', 'wangyi',
                     'amap', 'kailichen', 'tengxunmap', 'weiche', 'dida',
                     'NetEase Cloud Music', 'perfect piano', 'kugou', 'migu', 'lizhi',
                     '58job', 'alipay', 'meituan', 'beike', 'zhiyuanhui',
                     'iqiyi', 'bilibili', 'xigua', 'migutv', 'changba',
                     'zuoyebang', 'baicizhan', 'baidutext', 'bubei', 'hongen']

    vals_1 = ['zoom' for i in range(60)]
    vals_2 = ['wecom' for i in range(60)]
    vals_3 = ['dingding' for i in range(60)]
    vals_4 = ['zhilian' for i in range(60)]
    vals_5 = ['qichacha' for i in range(60)]
    #vals_6 = ['tianyancha' for i in range(36)]
    #vals_7 = ['51job' for i in range(36)]
    #vals_8 = ['sunlogin' for i in range(36)]
    #vals_9 = ['newcow' for i in range(36)]
    #vals_10 = ['Hero Scanner' for i in range(36)]
    #vals_11 = ['Meituan Merchant' for i in range(36)]
    #vals_12 = ['zhitong' for i in range(36)]

    vals = ( vals_5+vals_4+vals_3+vals_2+vals_1)[::-1]
    factor_score.insert(loc=0, column='App', value=vals)
    factor_score.to_csv('all_app_month_health_score_business_v2.csv',encoding='utf-8')
    #排序
    #dataframe = factor_score.sort_values(by=["综合得分"], ascending=False)
    #dataframe.to_csv('final_supp/all_app_month_sorted_health_score_education.csv',encoding='utf-8',index=False)
    #print(dataframe)
    # 排序
    exit()
    columns = ['F1', 'F2', 'F3','F4','F5','F6','F7','F8','F9','Scores']
    dates = ['58job', 'airbnb', 'alipay', 'amap', 'baicizhan', 'baidu', 'bilibili', 'CHINA DAILY',
                     'economist', 'iqiyi', 'mafengwo', 'NetEase Cloud Music', 'perfect piano','kailichen'
                     'quark', 'wechat', 'wecom', 'zhihu', 'zoom', 'zuoyebang']
    dates = []

    month = 12
    l = 0
    x = 0
    for m in range(0,36):

        df = pd.DataFrame()  # 新建一个Dataframe
        #print(df)
        #2021年12月-2019年1月
        for n in range(m,720,36):
            #print(type(factor_score.iloc[n]))
            series = pd.Series(factor_score.iloc[n])  # name 就是index的值
            df = df.append(series)

        df.index = ['58job', 'airbnb', 'alipay', 'amap', 'baicizhan',
                    'baidu', 'bilibili', 'CHINA DAILY','economist', 'iqiyi','kailichen',
                    'mafengwo', 'NetEase Cloud Music', 'perfect piano',
                     'quark', 'wechat', 'wecom', 'zhihu', 'zoom', 'zuoyebang']
        if m >= 24:
            month = 12
            df.sort_values(by=["综合得分"], ascending=False).to_csv('month_score/final/all/Rank_in_2019_{}month.csv'.format(month-l),encoding='utf-8')
            l+=1
        elif m >= 12:
            month = 12
            df.sort_values(by=["综合得分"], ascending=False).to_csv('month_score/final/all/Rank_in_2020_{}month.csv'.format(month-x), encoding='utf-8')
            x+=1
        else:
            df.sort_values(by=["综合得分"], ascending=False).to_csv('month_score/final/all/Rank_in_2021_{}month.csv'.format(month), encoding='utf-8')
            month -= 1
    #print(df)

def get_rank_rank(cate,j):
    file = "month_score/final/supp/cat/all_app_all_month_score_{}_supp_v2.csv".format(cate)


    f = pd.read_csv(file, sep=",",names=['other','feature assessment','feature bug','gui','guide','compatibility','performance','security','account','contents','ad','feedback','competitive products','suggest','release','reviews_num','release_num','release_front_num','downloads','rank'])
    f = f.fillna(0)

    month = 11
    l = 5
    x = 0
    y = 0
    s = 0
    d = 0
    for m in range(0,30):

        df = pd.DataFrame()  # 新建一个Dataframe
        #print(df)
        #2021年12月-2019年1月
        for n in range(m,150,30):
            #print(type(factor_score.iloc[n]))
            series = pd.Series(f.iloc[n])  # name 就是index的值
            df = df.append(series)

        if j == 0:
            df.index = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha']
        elif  j==1:
            df.index = ['baidu', 'quark', 'Google Chrome', 'sf express', 'biubiu']
        elif  j==2:
            df.index = ['airbnb', 'mafengwo', 'didi', 'tongcheng', 'shenzhou']
        elif j==3:
            df.index = ['Wechat', 'zhihu', 'douban', 'qingteng', 'qqzone']
        elif j==4:
            df.index = ['economist', 'CHINA DAILY', 'uc', 'pengpai', 'wangyi']
        elif j ==5:
            df.index = ['amap', 'kailichen', 'tengxunmap', 'weiche', 'dida']
        elif j==6:
            df.index = ['NetEase Cloud Music', 'perfect piano', 'kugou', 'migu', 'lizhi']
        elif j==7:
            df.index = ['58job', 'alipay', 'meituan', 'beike', 'zhiyuanhui']
        elif j==8:
            df.index = ['iqiyi', 'bilibili', 'xigua', 'migutv', 'changba']
        else:
            df.index = ['zuoyebang', 'baicizhan', 'baidutext', 'bubei', 'hongen']



        #df.index =['baidu','quark','Google Chrome','sf express','biubiu']
        #df.index = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha']
        #df.index = ['airbnb', 'mafengwo', 'didi', 'tongcheng', 'shenzhou']
        #df.index = ['Wechat', 'zhihu', 'douban', 'qingteng', 'qqzone']
        #df.index = ['economist', 'CHINA DAILY', 'uc', 'pengpai', 'wangyi']
        #df.index = ['amap', 'kailichen', 'tengxunmap', 'weiche', 'dida']
        #df.index = ['NetEase Cloud Music', 'perfect piano', 'kugou', 'migu', 'lizhi']
        #df.index = ['58job', 'alipay', 'meituan', 'beike', 'zhiyuanhui']
        #df.index = ['iqiyi', 'bilibili', 'xigua', 'migutv', 'changba']
        #df.index = ['zuoyebang', 'baicizhan', 'baidutext', 'bubei', 'hongen']

        if  m >= 24:
            month = 6
            df.sort_values(by=["rank"], ascending=True).to_csv('month_score/final/vs_factor/rank/supp/Rank_in_2019_{}month.csv'.format(month-x),encoding='utf-8')
            x+=1
        elif m >= 18:
            month = 6
            df.sort_values(by=["rank"], ascending=True).to_csv('month_score/final/vs_factor/rank/supp/Rank_in_2020_{}month.csv'.format(month-y), encoding='utf-8')
            y+=1
        elif m >= 12:
            month = 6
            df.sort_values(by=["rank"], ascending=True).to_csv('month_score/final/vs_factor/rank/supp/Rank_in_2021_{}month.csv'.format(month-s), encoding='utf-8')
            s+=1
        elif m >= 6:
            month = 6
            df.sort_values(by=["rank"], ascending=True).to_csv('month_score/final/vs_factor/rank/supp/Rank_in_2022_{}month.csv'.format(month-d), encoding='utf-8')
            d+=1
        elif m < 6:
            df.sort_values(by=["rank"], ascending=True).to_csv('month_score/final/vs_factor/rank/supp/Rank_in_2023_{}month.csv'.format(month-l), encoding='utf-8')
            l += 1

    print(df)


def get_download_rank(cate,j):
    file = "month_score/final/supp/cat/all_app_all_month_score_{}_supp_v2.csv".format(cate)

    f = pd.read_csv(file, sep=",",
                    names=['other', 'feature assessment', 'feature bug', 'gui', 'guide', 'compatibility', 'performance',
                           'security', 'account', 'contents', 'ad', 'feedback', 'competitive products', 'suggest',
                           'release', 'reviews_num', 'release_num', 'release_front_num', 'downloads', 'rank'])
    f = f.fillna(0)

    month = 11
    l = 5
    x = 0
    y = 0
    s = 0
    d = 0
    for m in range(0, 30):

        df = pd.DataFrame()  # 新建一个Dataframe
        # print(df)
        # 2021年12月-2019年1月
        for n in range(m, 150, 30):
            # print(type(factor_score.iloc[n]))
            series = pd.Series(f.iloc[n])  # name 就是index的值
            df = df.append(series)

        if j == 0:
            df.index = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha']
        elif j == 1:
            df.index = ['baidu', 'quark', 'Google Chrome', 'sf express', 'biubiu']
        elif j == 2:
            df.index = ['airbnb', 'mafengwo', 'didi', 'tongcheng', 'shenzhou']
        elif j == 3:
            df.index = ['Wechat', 'zhihu', 'douban', 'qingteng', 'qqzone']
        elif j == 4:
            df.index = ['economist', 'CHINA DAILY', 'uc', 'pengpai', 'wangyi']
        elif j == 5:
            df.index = ['amap', 'kailichen', 'tengxunmap', 'weiche', 'dida']
        elif j == 6:
            df.index = ['NetEase Cloud Music', 'perfect piano', 'kugou', 'migu', 'lizhi']
        elif j == 7:
            df.index = ['58job', 'alipay', 'meituan', 'beike', 'zhiyuanhui']
        elif j == 8:
            df.index = ['iqiyi', 'bilibili', 'xigua', 'migutv', 'changba']
        else:
            df.index = ['zuoyebang', 'baicizhan', 'baidutext', 'bubei', 'hongen']

        #df.index = ['baidu', 'quark', 'Google Chrome', 'sf express', 'biubiu']
        #df.index = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha']
        #df.index = ['airbnb', 'mafengwo', 'didi', 'tongcheng', 'shenzhou']
        #df.index = ['Wechat', 'zhihu', 'douban', 'qingteng', 'qqzone']
        #df.index = ['economist', 'CHINA DAILY', 'uc', 'pengpai', 'wangyi']
        #df.index = ['amap', 'kailichen', 'tengxunmap', 'weiche', 'dida']
        #df.index = ['NetEase Cloud Music', 'perfect piano', 'kugou', 'migu', 'lizhi']
        #df.index = ['58job', 'alipay', 'meituan', 'beike', 'zhiyuanhui']

        #df.index = ['iqiyi', 'bilibili', 'xigua', 'migutv', 'changba']
        #df.index = ['zuoyebang', 'baicizhan', 'baidutext', 'bubei', 'hongen']

        if m >= 24:
            month = 6
            df.sort_values(by=["downloads"], ascending=False).to_csv(
                'month_score/final/vs_factor/download/supp/Rank_in_2019_{}month.csv'.format(month - x), encoding='utf-8')
            x += 1
        elif m >= 18:
            month = 6
            df.sort_values(by=["downloads"], ascending=False).to_csv(
                'month_score/final/vs_factor/download/supp/Rank_in_2020_{}month.csv'.format(month - y), encoding='utf-8')
            y += 1
        elif m >= 12:
            month = 6
            df.sort_values(by=["downloads"], ascending=False).to_csv(
                'month_score/final/vs_factor/download/supp/Rank_in_2021_{}month.csv'.format(month - s), encoding='utf-8')
            s += 1
        elif m >= 6:
            month = 6
            df.sort_values(by=["downloads"], ascending=False).to_csv(
                'month_score/final/vs_factor/download/supp/Rank_in_2022_{}month.csv'.format(month - d), encoding='utf-8')
            d += 1
        elif m < 6:
            df.sort_values(by=["downloads"], ascending=False).to_csv(
                'month_score/final/vs_factor/download/supp/Rank_in_2023_{}month.csv'.format(month - l), encoding='utf-8')
            l += 1
    print(df)


def get_average_rank(cate,j):
    file = "month_score/all_month_score_average_supp_{}.csv".format(cate)

    f = pd.read_csv(file, sep=",",
                    names=['other', 'feature assessment', 'feature bug', 'gui', 'guide', 'compatibility', 'performance',
                           'security', 'account', 'contents', 'ad', 'feedback', 'competitive products', 'suggest',
                           'release', 'average'])
    f = f.fillna(0)

    month = 11
    l = 5
    x = 0
    y = 0
    s = 0
    d = 0
    for m in range(0, 30):

        df = pd.DataFrame()  # 新建一个Dataframe
        # print(df)
        # 2021年12月-2019年1月
        for n in range(m, 150, 30):
            # print(type(factor_score.iloc[n]))
            series = pd.Series(f.iloc[n])  # name 就是index的值
            df = df.append(series)

        if j == 0:
            df.index = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha']
        elif j == 1:
            df.index = ['baidu', 'quark', 'Google Chrome', 'sf express', 'biubiu']
        elif j == 2:
            df.index = ['airbnb', 'mafengwo', 'didi', 'tongcheng', 'shenzhou']
        elif j == 3:
            df.index = ['Wechat', 'zhihu', 'douban', 'qingteng', 'qqzone']
        elif j == 4:
            df.index = ['economist', 'CHINA DAILY', 'uc', 'pengpai', 'wangyi']
        elif j == 5:
            df.index = ['amap', 'kailichen', 'tengxunmap', 'weiche', 'dida']
        elif j == 6:
            df.index = ['NetEase Cloud Music', 'perfect piano', 'kugou', 'migu', 'lizhi']
        elif j == 7:
            df.index = ['58job', 'alipay', 'meituan', 'beike', 'zhiyuanhui']
        elif j == 8:
            df.index = ['iqiyi', 'bilibili', 'xigua', 'migutv', 'changba']
        else:
            df.index = ['zuoyebang', 'baicizhan', 'baidutext', 'bubei', 'hongen']

        if m >= 24:
            month = 6
            df.sort_values(by=["average"], ascending=False).to_csv(
                'month_score/final/vs_factor/average/supp/Rank_in_2019_{}month.csv'.format(month - x),
                encoding='utf-8')
            x += 1
        elif m >= 18:
            month = 6
            df.sort_values(by=["average"], ascending=False).to_csv(
                'month_score/final/vs_factor/average/supp/Rank_in_2020_{}month.csv'.format(month - y),
                encoding='utf-8')
            y += 1
        elif m >= 12:
            month = 6
            df.sort_values(by=["average"], ascending=False).to_csv(
                'month_score/final/vs_factor/average/supp/Rank_in_2021_{}month.csv'.format(month - s),
                encoding='utf-8')
            s += 1
        elif m >= 6:
            month = 6
            df.sort_values(by=["average"], ascending=False).to_csv(
                'month_score/final/vs_factor/average/supp/Rank_in_2022_{}month.csv'.format(month - d),
                encoding='utf-8')
            d += 1
        elif m < 6:
            df.sort_values(by=["average"], ascending=False).to_csv(
                'month_score/final/vs_factor/average/supp/Rank_in_2023_{}month.csv'.format(month - l),
                encoding='utf-8')
            l += 1

    print(df)


def get_health_rank(cate,j):
    file = "all_app_month_health_score_{}.csv".format(cate)

    f = pd.read_csv(file, sep=",")
    f = f.fillna(0)

    month = 11
    l = 5
    x = 0
    y = 0
    s = 0
    d = 0
    for m in range(0, 30):

        df = pd.DataFrame()  # 新建一个Dataframe
        # print(df)
        # 2021年12月-2019年1月
        for n in range(m, 150, 30):
            # print(type(factor_score.iloc[n]))
            series = pd.Series(f.iloc[n])  # name 就是index的值
            df = df.append(series)

        if j == 0:
            df.index = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha']
        elif j == 1:
            df.index = ['baidu', 'quark', 'Google Chrome', 'sf express', 'biubiu']
        elif j == 2:
            df.index = ['airbnb', 'mafengwo', 'didi', 'tongcheng', 'shenzhou']
        elif j == 3:
            df.index = ['Wechat', 'zhihu', 'douban', 'qingteng', 'qqzone']
        elif j == 4:
            df.index = ['economist', 'CHINA DAILY', 'uc', 'pengpai', 'wangyi']
        elif j == 5:
            df.index = ['amap', 'kailichen', 'tengxunmap', 'weiche', 'dida']
        elif j == 6:
            df.index = ['NetEase Cloud Music', 'perfect piano', 'kugou', 'migu', 'lizhi']
        elif j == 7:
            df.index = ['58job', 'alipay', 'meituan', 'beike', 'zhiyuanhui']
        elif j == 8:
            df.index = ['iqiyi', 'bilibili', 'xigua', 'migutv', 'changba']
        else:
            df.index = ['zuoyebang', 'baicizhan', 'baidutext', 'bubei', 'hongen']

        if m >= 24:
            month = 6
            df.sort_values(by=["综合得分"], ascending=False).to_csv(
                'month_score/final/vs_factor/health/supp/Rank_in_2019_{}month.csv'.format(month - x),
                encoding='utf-8')
            x += 1
        elif m >= 18:
            month = 6
            df.sort_values(by=["综合得分"], ascending=False).to_csv(
                'month_score/final/vs_factor/health/supp/Rank_in_2020_{}month.csv'.format(month - y),
                encoding='utf-8')
            y += 1
        elif m >= 12:
            month = 6
            df.sort_values(by=["综合得分"], ascending=False).to_csv(
                'month_score/final/vs_factor/health/supp/Rank_in_2021_{}month.csv'.format(month - s),
                encoding='utf-8')
            s += 1
        elif m >= 6:
            month = 6
            df.sort_values(by=["综合得分"], ascending=False).to_csv(
                'month_score/final/vs_factor/health/supp/Rank_in_2022_{}month.csv'.format(month - d),
                encoding='utf-8')
            d += 1
        elif m < 6:
            df.sort_values(by=["综合得分"], ascending=False).to_csv(
                'month_score/final/vs_factor/health/supp/Rank_in_2023_{}month.csv'.format(month - l),
                encoding='utf-8')
            l += 1

    print(df)


def get_list(j):
    # 排名

    if j == 0:
        apps = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha']
    elif j == 1:
        apps = ['baidu', 'quark', 'Google Chrome', 'sf express', 'biubiu']
    elif j == 2:
        apps = ['airbnb', 'mafengwo', 'didi', 'tongcheng', 'shenzhou']
    elif j == 3:
        apps = ['Wechat', 'zhihu', 'douban', 'qingteng', 'qqzone']
    elif j == 4:
        apps = ['economist', 'CHINA DAILY', 'uc', 'pengpai', 'wangyi']
    elif j == 5:
        apps = ['amap', 'kailichen', 'tengxunmap', 'weiche', 'dida']
    elif j == 6:
        apps = ['NetEase Cloud Music', 'perfect piano', 'kugou', 'migu', 'lizhi']
    elif j == 7:
        apps = ['58job', 'alipay', 'meituan', 'beike', 'zhiyuanhui']
    elif j == 8:
        apps = ['iqiyi', 'bilibili', 'xigua', 'migutv', 'changba']
    else:
        apps = ['zuoyebang', 'baicizhan', 'baidutext', 'bubei', 'hongen']

    #apps =['baidu', 'quark', 'Google Chrome', 'sf express', 'biubiu']
    #apps = ['zoom', 'wecom', 'dingding', 'zhilian', 'qichacha']
    #apps = ['airbnb', 'mafengwo', 'didi', 'tongcheng', 'shenzhou']
    #apps = ['Wechat', 'zhihu', 'douban', 'qingteng', 'qqzone']
    #apps = ['economist', 'CHINA DAILY', 'uc', 'pengpai', 'wangyi']
    #apps = ['amap', 'kailichen', 'tengxunmap', 'weiche', 'dida']
    #apps = ['NetEase Cloud Music', 'perfect piano', 'kugou', 'migu', 'lizhi']
    #apps = ['58job', 'alipay', 'meituan', 'beike', 'zhiyuanhui']
    #apps = ['iqiyi', 'bilibili', 'xigua', 'migutv', 'changba']
    #apps = ['zuoyebang', 'baicizhan', 'baidutext', 'bubei', 'hongen']
    rank_list = {}
    download_list = {}
    average_list = {}
    health_list = {}

    for app in apps:
        a = {}
        b = {}
        c = {}
        d = {}
        keys1 = [i for i in range(1,7)]
        keys2 = [i for i in range(7, 13)]
        keys3 = [i for i in range(13, 19)]
        keys4 = [i for i in range(19, 25)]
        keys5 = [i for i in range(25, 31)]
        key = keys1 + keys2 + keys3+ keys4 + keys5
        for i in key:
            if i <= 6:
                df1 = pd.read_csv("month_score/final/vs_factor/rank/supp/Rank_in_2019_{}month.csv".format(i), header=None)
                df2 = pd.read_csv("month_score/final/vs_factor/download/supp/Rank_in_2019_{}month.csv".format(i), header=None)
                df3 = pd.read_csv("month_score/final/vs_factor/average/supp/Rank_in_2019_{}month.csv".format(i), header=None)
                df4 = pd.read_csv("month_score/final/vs_factor/health/supp/Rank_in_2019_{}month.csv".format(i), header=None)
            elif i <= 12:
                df1= pd.read_csv("month_score/final/vs_factor/rank/supp/Rank_in_2020_{}month.csv".format(i-6), header=None)
                df2 = pd.read_csv("month_score/final/vs_factor/download/supp/Rank_in_2020_{}month.csv".format(i-6),header=None)
                df3 = pd.read_csv("month_score/final/vs_factor/average/supp/Rank_in_2020_{}month.csv".format(i-6), header=None)
                df4 = pd.read_csv("month_score/final/vs_factor/health/supp/Rank_in_2020_{}month.csv".format(i-6), header=None)
            elif i <= 18:
                df1= pd.read_csv("month_score/final/vs_factor/rank/supp/Rank_in_2021_{}month.csv".format(i-12), header=None)
                df2 = pd.read_csv("month_score/final/vs_factor/download/supp/Rank_in_2021_{}month.csv".format(i-12),header=None)
                df3 = pd.read_csv("month_score/final/vs_factor/average/supp/Rank_in_2021_{}month.csv".format(i-12), header=None)
                df4 = pd.read_csv("month_score/final/vs_factor/health/supp/Rank_in_2021_{}month.csv".format(i-12), header=None)
            elif i <= 24:
                df1= pd.read_csv("month_score/final/vs_factor/rank/supp/Rank_in_2022_{}month.csv".format(i-18), header=None)
                df2 = pd.read_csv("month_score/final/vs_factor/download/supp/Rank_in_2022_{}month.csv".format(i-18),header=None)
                df3 = pd.read_csv("month_score/final/vs_factor/average/supp/Rank_in_2022_{}month.csv".format(i-18), header=None)
                df4 = pd.read_csv("month_score/final/vs_factor/health/supp/Rank_in_2022_{}month.csv".format(i-18), header=None)
            elif i <= 30:
                df1= pd.read_csv("month_score/final/vs_factor/rank/supp/Rank_in_2023_{}month.csv".format(i-24), header=None)
                df2 = pd.read_csv("month_score/final/vs_factor/download/supp/Rank_in_2023_{}month.csv".format(i-24),header=None)
                df3 = pd.read_csv("month_score/final/vs_factor/average/supp/Rank_in_2023_{}month.csv".format(i-24), header=None)
                df4 = pd.read_csv("month_score/final/vs_factor/health/supp/Rank_in_2023_{}month.csv".format(i-24), header=None)

            a[i]= df1.index[df1[0]==app].tolist()[0]
            b[i] = df2.index[df2[0] == app].tolist()[0]
            c[i] = df3.index[df3[0] == app].tolist()[0]
            d[i] = df4.index[df4[0] == app].tolist()[0]
        rank_list[app] = a
        download_list[app] = b
        average_list[app] = c
        health_list[app] = d
        #从2019年1月开始
    print('rank list:')
    print(rank_list)
    print('download list:')
    print(download_list)
    print('average list:')
    print(average_list)
    print('health list:')
    print(health_list)
    return  rank_list,download_list,average_list,health_list

def get_distance(rank,download,average,health):
    apps = ['58job', 'airbnb', 'alipay', 'amap', 'baicizhan', 'baidu', 'bilibili', 'CHINA DAILY',
            'economist', 'iqiyi', 'kailichen', 'mafengwo', 'NetEase Cloud Music', 'perfect piano',
            'quark', 'Wechat','wecom', 'zhihu', 'zoom', 'zuoyebang']

    # 排名与health，average对比距离
    x = 0
    i = 0
    n = 0
    s = 0
    r = 0
    g = 0
    for app in apps:
        app ='hongen'
        print(app + ':')
        rank_list = rank[app]
        download_list =download[app]
        average_list = average[app]
        health_list = health[app]
        #rank_list = list(rank[app].values())
        #download_list = list(download[app].values())
        #average_list = list(average[app].values())
        #health_list = list(health[app].values())

        #vec1 = np.array(rank_list)
        #vec2 = np.array(health_list)
        #vec3 = np.array(average_list)
        #vec4 = np.array(download_list)


        # 创建一个集合，用于存储所有关键字
        main_array =  health_list
        other_arrays = [average_list,download_list,rank_list]
        all_keys = set()
        for arr in [main_array] + other_arrays:
            all_keys.update(arr.keys())

        # 比较关键字和数值差异
        for key in all_keys:
            main_value = main_array.get(key, None)
            other_values = [arr.get(key, None) for arr in other_arrays]

            if all(other_values) and all(abs(main_value - value) >= 2 for value in other_values):
                print(key)
        exit()

if __name__ == '__main__':
    #get_all_apps_all_months_health_rank()
    #exit()
    cate_name_list = ['business','tool','travel','social','news',
                      'navigation','music',
                        'life','entertainment','education']
    j = 0
    cate_name_list = ['business']

    for cate in cate_name_list:

        get_rank_rank(cate,j)
        get_download_rank(cate,j)
        get_average_rank(cate,j)
        get_health_rank(cate,j)
        rank_list, download_list, average_list, health_list = get_list(j)
        get_distance(rank_list, download_list, average_list, health_list)






