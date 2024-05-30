import pandas as pd
import numpy as np
import numpy.linalg as nlg
import matplotlib.pyplot as plt
from factor_analyzer import FactorAnalyzer, calculate_kmo, calculate_bartlett_sphericity
from sklearn.preprocessing import StandardScaler
import matplotlib
labels = ['feature assessment','feature bug','gui','guide','download',
          'software','hardware','speed','resource consumption',
          'aging','data','privacy','malicious','account',
          'contents','ad','price','feedback','competitive products',
          'suggest','release','rank','numbers_download'
          ]

def main():
    contribution_rate = 0.8
    auto_choose_N = True  # 设置为True的时候就自动根据贡献率来选择因子个数，为False则要自己设置N
    N = 2

    file = "month_score/final/all_app_all_month_score_education.csv"
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
    print(matrices_var)


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
    ev, v = Load_Matrix.get_eigenvalues()
    print('\n相关矩阵特征值：', ev)
    plt.figure(figsize=(8, 6.5))
    plt.scatter(range(1, f.shape[1]+1), ev)
    plt.plot(range(1, f.shape[1]+1), ev)
    plt.title('碎石图', fontdict={'weight': 'normal', 'size': 25})
    plt.xlabel('因子', fontdict={'weight': 'normal', 'size': 15})
    plt.ylabel('特征值', fontdict={'weight': 'normal', 'size': 15})
    plt.grid()
    plt.show()

    # 使用主成分分析的方法来计算出因子载荷矩阵，使用最大方差法旋转因子载荷矩阵
    Load_Matrix_rotated = FactorAnalyzer(rotation='varimax', n_factors=N, method='principal')
    Load_Matrix_rotated.fit(f)

    #  计算旋转后的载荷矩阵的贡献率
    f_contribution_var_rotated = Load_Matrix_rotated.get_factor_variance()
    matrices_var_rotated = pd.DataFrame()
    matrices_var_rotated["特征值"] = f_contribution_var_rotated[0]
    matrices_var_rotated["方差贡献率"] = f_contribution_var_rotated[1]
    matrices_var_rotated["方差累计贡献率"] = f_contribution_var_rotated[2]
    print(matrices_var_rotated)
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
    print("\n第一列为第一个因子得分函数的对应系数")
    print("因子得分：\n", factor_score_weight)

    factor_score = pd.DataFrame(np.dot(np.mat(f), np.mat(factor_score_weight)))  # 指标 * 对应权重，计算出因子的分数

    i = 0
    factor_score["综合得分"] = 0
    for factor_score_weight in matrices_var_rotated["方差贡献率"]:
        factor_score["综合得分"] += factor_score_weight * factor_score[i]  # 因子贡献率 * 因子的分数 用于计算综合得分
        print(factor_score_weight)
        i += 1
        if i == N:
            break

    exit()
    factor_score["综合得分"] = factor_score["综合得分"] / matrices_var_rotated["方差贡献率"].sum()  # 计算综合得分
    #factor_score.index = ["other", "feature assessment", "feature bug", "gui", "guide", "software", "hardware", "performance", "security", "account", "content", "ads", "feedback", "competitive", "request", "release"]  # 更改索引
    print('\n')
    print(factor_score.sort_values(by=["综合得分"], ascending=False))  # 排序
    #print(factor_score)

if __name__ == '__main__':
    main()

