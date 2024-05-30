import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']  # 例子中使用了"SimHei"字体，这是一种常见的中文字体。
plt.rcParams['axes.unicode_minus'] = False  # 这一行可以确保负号的正确显示

def jiaquan_al(list):
    n = 0
    global  new_al_f1
    global new_al_f2
    global new_al_f3
    global new_al_f4
    global new_al_f5
    global new_al_f6
    global new_al_f7
    global new_al_f8
    global new_al_f9
    for litlist in list:
        #print(litlist)
        n += 1
        for i in litlist:
            if n == 1:
                new_al_f1.append(i * 0.1677)
            elif n==2:
                new_al_f2.append(i * 0.0638)
            elif n == 3:
                new_al_f3.append(i * 0.0576)
            elif n==4:
                new_al_f4.append(i * 0.0524)
            elif n==5:
                new_al_f5.append(i * 0.1654)
            elif n==6:
                new_al_f6.append(i * 0.0711)
            elif n == 7:
                new_al_f7.append(i * 0.0907)
            elif n==8:
                new_al_f8.append(i * 0.0522)
            else:
                new_al_f9.append(i * 0.0883)


def jiaquan_am(list):
    n = 0
    global new_am_f1
    global new_am_f2
    global new_am_f3
    global new_am_f4
    global new_am_f5
    global new_am_f6
    global new_am_f7
    global new_am_f8
    global new_am_f9
    for litlist in list:
        #print(litlist)
        n += 1
        for i in litlist:
            if n == 1:
                new_am_f1.append(i * 0.1677)
            elif n==2:
                new_am_f2.append(i * 0.0638)
            elif n == 3:
                new_am_f3.append(i * 0.0576)
            elif n==4:
                new_am_f4.append(i * 0.0524)
            elif n==5:
                new_am_f5.append(i * 0.1654)
            elif n==6:
                new_am_f6.append(i * 0.0711)
            elif n == 7:
                new_am_f7.append(i * 0.0907)
            elif n==8:
                new_am_f8.append(i * 0.0522)
            else:
                new_am_f9.append(i * 0.0883)

def jiaquan_bd(list):
    n = 0
    global new_bd_f1
    global new_bd_f2
    global new_bd_f3
    global new_bd_f4
    global new_bd_f5
    global new_bd_f6
    global new_bd_f7
    global new_bd_f8
    global new_bd_f9
    for litlist in list:
        #print(litlist)
        n += 1
        for i in litlist:
            if n == 1:
                new_bd_f1.append(i * 0.1677)
            elif n==2:
                new_bd_f2.append(i * 0.0638)
            elif n == 3:
                new_bd_f3.append(i * 0.0576)
            elif n==4:
                new_bd_f4.append(i * 0.0524)
            elif n==5:
                new_bd_f5.append(i * 0.1654)
            elif n==6:
                new_bd_f6.append(i * 0.0711)
            elif n == 7:
                new_bd_f7.append(i * 0.0907)
            elif n==8:
                new_bd_f8.append(i * 0.0522)
            else:
                new_bd_f9.append(i * 0.0883)

def jiaquan_iq(list):
    n = 0
    global new_iq_f1
    global new_iq_f2
    global new_iq_f3
    global new_iq_f4
    global new_iq_f5
    global new_iq_f6
    global new_iq_f7
    global new_iq_f8
    global new_iq_f9
    for litlist in list:
        #print(litlist)
        n += 1
        for i in litlist:
            if n == 1:
                new_iq_f1.append(i * 0.1677)
            elif n==2:
                new_iq_f2.append(i * 0.0638)
            elif n == 3:
                new_iq_f3.append(i * 0.0576)
            elif n==4:
                new_iq_f4.append(i * 0.0524)
            elif n==5:
                new_iq_f5.append(i * 0.1654)
            elif n==6:
                new_iq_f6.append(i * 0.0711)
            elif n == 7:
                new_iq_f7.append(i * 0.0907)
            elif n==8:
                new_iq_f8.append(i * 0.0522)
            else:
                new_iq_f9.append(i * 0.0883)

def jiaquan_we(list):
    n = 0
    global new_we_f1
    global new_we_f2
    global new_we_f3
    global new_we_f4
    global new_we_f5
    global new_we_f6
    global new_we_f7
    global new_we_f8
    global new_we_f9
    for litlist in list:
        #print(litlist)
        n += 1
        for i in litlist:
            if n == 1:
                new_we_f1.append(i * 0.1677)
            elif n==2:
                new_we_f2.append(i * 0.0638)
            elif n == 3:
                new_we_f3.append(i * 0.0576)
            elif n==4:
                new_we_f4.append(i * 0.0524)
            elif n==5:
                new_we_f5.append(i * 0.1654)
            elif n==6:
                new_we_f6.append(i * 0.0711)
            elif n == 7:
                new_we_f7.append(i * 0.0907)
            elif n==8:
                new_we_f8.append(i * 0.0522)
            else:
                new_we_f9.append(i * 0.0883)

if __name__ == '__main__':

    dataframe = pd.read_csv("all_app_month_health_score.csv", header=None)
    dataframe[10] = pd.to_numeric(dataframe[10], errors='coerce')
    dataframe = dataframe.drop([0])
    plt.figure(figsize=(15, 4), dpi=80)
    AL_F_1 = dataframe[72:108][1].tolist()[::-1]
    AM_F_1 = dataframe[108:144][1].tolist()[::-1]
    BD_F_1 = dataframe[180:216][1].tolist()[::-1]
    IQ_F_1 = dataframe[325:361][1].tolist()[::-1]
    WE_F_1 = dataframe[577:613][1].tolist()[::-1]
    #print(dataframe[72:108])
    #exit()
    #for i in  AL_F_1:
        #new_af_f1.append(i*0.1677)


    AL_F_2=dataframe[72:108][2].tolist()[::-1]
    AM_F_2 = dataframe[108:144][2].tolist()[::-1]
    BD_F_2 = dataframe[180:216][2].tolist()[::-1]
    IQ_F_2 = dataframe[325:361][2].tolist()[::-1]
    WE_F_2 = dataframe[577:613][2].tolist()[::-1]
    AL_F_3=dataframe[72:108][3].tolist()[::-1]
    AM_F_3 = dataframe[108:144][3].tolist()[::-1]
    BD_F_3 = dataframe[180:216][3].tolist()[::-1]
    IQ_F_3 = dataframe[325:361][3].tolist()[::-1]
    WE_F_3 = dataframe[577:613][3].tolist()[::-1]
    AL_F_4=dataframe[72:108][4].tolist()[::-1]
    AM_F_4 = dataframe[108:144][4].tolist()[::-1]
    BD_F_4 = dataframe[180:216][4].tolist()[::-1]
    IQ_F_4 = dataframe[325:361][4].tolist()[::-1]
    WE_F_4 = dataframe[577:613][4].tolist()[::-1]
    AL_F_5=dataframe[72:108][5].tolist()[::-1]
    AM_F_5 = dataframe[108:144][5].tolist()[::-1]
    BD_F_5 = dataframe[180:216][5].tolist()[::-1]
    IQ_F_5 = dataframe[325:361][5].tolist()[::-1]
    WE_F_5 = dataframe[577:613][5].tolist()[::-1]
    AL_F_6=dataframe[72:108][6].tolist()[::-1]
    AM_F_6 = dataframe[108:144][6].tolist()[::-1]
    BD_F_6 = dataframe[180:216][6].tolist()[::-1]
    IQ_F_6 = dataframe[325:361][6].tolist()[::-1]
    WE_F_6 = dataframe[577:613][6].tolist()[::-1]
    AL_F_7=dataframe[72:108][7].tolist()[::-1]
    AM_F_7 = dataframe[108:144][7].tolist()[::-1]
    BD_F_7 = dataframe[180:216][7].tolist()[::-1]
    IQ_F_7 = dataframe[325:361][7].tolist()[::-1]
    WE_F_7 = dataframe[577:613][7].tolist()[::-1]
    AL_F_8=dataframe[72:108][8].tolist()[::-1]
    AM_F_8 = dataframe[108:144][8].tolist()[::-1]
    BD_F_8 = dataframe[180:216][8].tolist()[::-1]
    IQ_F_8 = dataframe[325:361][8].tolist()[::-1]
    WE_F_8 = dataframe[577:613][8].tolist()[::-1]
    AL_F_9=dataframe[72:108][9].tolist()[::-1]
    AM_F_9 = dataframe[108:144][9].tolist()[::-1]
    BD_F_9 = dataframe[180:216][9].tolist()[::-1]
    IQ_F_9 = dataframe[325:361][9].tolist()[::-1]
    WE_F_9 = dataframe[577:613][9].tolist()[::-1]

    # alipay
    health_list_1 = dataframe[72:108][10].tolist()[::-1]
    # amap
    health_list_2 = dataframe[108:144][10].tolist()[::-1]
    # baidu
    health_list_3 = dataframe[180:216][10].tolist()[::-1]
    # iqiyi
    health_list_4 = dataframe[325:361][10].tolist()[::-1]
    # wechat
    health_list_5 = dataframe[577:613][10].tolist()[::-1]


    labels = ['F1', 'F2', 'F3', 'F4', 'F5','F6','F7','F8','F9']

    AL_data = [AL_F_1,AL_F_2,AL_F_3,AL_F_4,AL_F_5,AL_F_6,AL_F_7,AL_F_8,AL_F_9]
    AM_data = [AM_F_1, AM_F_2, AM_F_3, AM_F_4, AM_F_5, AM_F_6, AM_F_7, AM_F_8, AM_F_9]
    BD_data = [BD_F_1, BD_F_2, BD_F_3, BD_F_4, BD_F_5, BD_F_6, BD_F_7, BD_F_8, BD_F_9]
    IQ_data = [IQ_F_1, IQ_F_2, IQ_F_3, IQ_F_4, IQ_F_5, IQ_F_6, IQ_F_7, IQ_F_8, IQ_F_9]
    WE_data = [WE_F_1, WE_F_2, WE_F_3, WE_F_4, WE_F_5, WE_F_6, WE_F_7, WE_F_8, WE_F_9]
    new_al_f1 = []
    new_al_f2 = []
    new_al_f3 = []
    new_al_f4 = []
    new_al_f5 = []
    new_al_f6 = []
    new_al_f7 = []
    new_al_f8 = []
    new_al_f9 = []
    new_am_f1 = []
    new_am_f2 = []
    new_am_f3 = []
    new_am_f4 = []
    new_am_f5 = []
    new_am_f6 = []
    new_am_f7 = []
    new_am_f8 = []
    new_am_f9 = []
    new_bd_f1 = []
    new_bd_f2 = []
    new_bd_f3 = []
    new_bd_f4 = []
    new_bd_f5 = []
    new_bd_f6 = []
    new_bd_f7 = []
    new_bd_f8 = []
    new_bd_f9 = []
    new_iq_f1 = []
    new_iq_f2 = []
    new_iq_f3 = []
    new_iq_f4 = []
    new_iq_f5 = []
    new_iq_f6 = []
    new_iq_f7 = []
    new_iq_f8 = []
    new_iq_f9 = []
    new_we_f1 = []
    new_we_f2 = []
    new_we_f3 = []
    new_we_f4 = []
    new_we_f5 = []
    new_we_f6 = []
    new_we_f7 = []
    new_we_f8 = []
    new_we_f9 = []

    jiaquan_al(AL_data)
    jiaquan_am(AM_data)
    jiaquan_bd(BD_data)
    jiaquan_iq(IQ_data)
    jiaquan_we(WE_data)
    NEW_AL_data = [new_al_f1,new_al_f2,new_al_f3,new_al_f4,new_al_f5,new_al_f6,new_al_f7,new_al_f8,new_al_f9]
    NEW_AM_data =  [ new_am_f1,new_am_f2,new_am_f3,new_am_f4,new_am_f5,new_am_f6,new_am_f7,new_am_f8,new_am_f9]
    NEW_BD_data =  [ new_bd_f1,new_bd_f2,new_bd_f3,new_bd_f4,new_bd_f5,new_bd_f6,new_bd_f7,new_bd_f8,new_bd_f9]
    NEW_IQ_data =  [ new_iq_f1,new_iq_f2,new_iq_f3,new_iq_f4,new_iq_f5,new_iq_f6,new_iq_f7,new_iq_f8,new_iq_f9]
    NEW_WE_data =  [ new_we_f1,new_we_f2,new_we_f3,new_we_f4,new_we_f5,new_we_f6,new_we_f7,new_we_f8,new_we_f9]

    ALL_data = NEW_AL_data  + NEW_AM_data+ NEW_BD_data+ NEW_IQ_data +  NEW_WE_data


    min_max_scaler = preprocessing.MinMaxScaler(feature_range = (1,12),copy = False)#范围改为1~3，对原数组操作
    x_minmax = min_max_scaler.fit_transform(ALL_data)

    AL_data =[x_minmax[0],x_minmax[1],x_minmax[2],x_minmax[3],x_minmax[4],x_minmax[5],x_minmax[6],x_minmax[7],x_minmax[8]]
    AM_data=[x_minmax[9],x_minmax[10],x_minmax[11],x_minmax[12],x_minmax[13],x_minmax[14],x_minmax[15],x_minmax[16],x_minmax[17]]

    BD_data=[x_minmax[18],x_minmax[19],x_minmax[20],x_minmax[21],x_minmax[22],x_minmax[23],x_minmax[24],x_minmax[25],x_minmax[26]]

    IQ_data=[x_minmax[27],x_minmax[28],x_minmax[29],x_minmax[30],x_minmax[31],x_minmax[32],x_minmax[33],x_minmax[34],x_minmax[35]]

    WE_data=[x_minmax[36],x_minmax[37],x_minmax[38],x_minmax[39],x_minmax[40],x_minmax[41],x_minmax[42],x_minmax[43],x_minmax[44]]


    x = range(36)

    plt.stackplot(x, np.array(WE_data), labels=labels,baseline='zero')
    #plt.title("Wechat scores stackplot")
    plt.ylim(0, 100)
    plt.xlabel("月份")
    plt.ylabel("健康度")
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig("figure/stack/{}_health01.jpg".format('alipay'))

    #plt.show()
    exit()
    bs=['Baidu', 'WeChat', 'Alipay', 'iqiyi', 'Amap']
    fig, ax = plt.subplots(5, 1)

    ax[0, 0].stackplot(x,np.array(IQ_data), labels=labels)
    #ax.set_xlim(0, 4)
    #ax.set_xticks(x)
    ax[0, 0].set_title('Alipay')
    ax[0, 0].legend()
    plt.show()
    exit()
    ax[1, 0].stackplot(36, np.array(AM_data), labels=labels)
    #ax.set_xlim(0, 4)
    #ax.set_xticks(x)
    ax[1, 0].set_title('Amap')
    ax[1, 0].legend()
    ax[0, 1].stackplot(36, np.array(BD_data), labels=labels)
    #ax.set_xlim(0, 4)
    #ax.set_xticks(x)
    ax[0, 1].set_title('Baidu')
    ax[0, 1].legend()
    ax[1, 1].stackplot(36, np.array(IQ_data), labels=labels)
    #ax.set_xlim(0, 4)
    #ax.set_xticks(x)
    ax[1, 1].set_title('iqiyi')
    ax[1, 1].legend()

    ax[0, 2].stackplot(36, np.array(WE_data), labels=labels)
    #ax.set_xlim(0, 4)
    #ax.set_xticks(x)
    ax[0, 2].set_title('Wechat')
    ax[0, 2].legend()
    plt.show()

