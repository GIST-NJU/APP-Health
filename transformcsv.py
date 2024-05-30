import pandas as pd
#读取excel表格,pandas直接转换为DataFrame
import common as com
import csv
#apps=['amap','baicizhan','baidu','bilibili','CHINA DAILY','iqiyi','kailichen','mafengwo','NetEase Cloud Music','perfect piano','quark',
#'wecom','zhihu','zoom','zuoyebang']
apps = ['didi','tongcheng','shenzhou','douban','qingteng','qqzone','uc','pengpai',
            'wangyi','tengxunmap','weiche','dida','kugou','migu','lizhi','meituan',
            'beike','zhiyuanhui','xigua','migutv','changba','baidutext','bubei','hongen']
apps = ['zoom','wecom','baidu','quark','airbnb',
        'mafengwo','Wechat','zhihu',
        'economist','CHINA DAILY','amap','kailichen','NetEase Cloud Music',
        'perfect piano','58job','alipay','iqiyi','bilibili',
        'zuoyebang','baicizhan']
apps = ['maimai','camscanner','tencentnews','BOSSzhipin','shixiseng',
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
apps=['qq tongbu','wifi','national antifraud center','china moblie',
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
    dataframe = pd.read_excel('data/reviews/supp/{}.xlsx'.format(app), header=3)  # path是excel文件保存路径
    # print(dataframe)
    # exit()
    dataframe.to_csv('newdata/{}_supp.csv'.format(app), encoding='utf-8')
    print(dataframe)
exit()

for app in apps:
    dataframe = pd.read_excel('data/release/{}_all_releases.xlsx'.format(app),index_col=0) #path是excel文件保存路径
    dataframe.to_csv('data/release/{}_all_releases_1.csv'.format(app),encoding='utf-8')
    print(dataframe)
exit()



#if __name__ == '__main__':
    #app_categories = ['58job', 'alipay', 'anjuke', 'claws', 'fcbox', 'goodlive', 'imdada', 'lalamove', 'TmallGenie', 'traffic control']
    #for app_category in app_categories:
        #review_file = 'C:/Users/nanya/PycharmProjects/sample/data/life/{}.xlsx'.format(app_category)
        #review_list = pd.read_excel(review_file,header=3)
        #write_file = 'C:/Users/nanya/PycharmProjects/sample/newdata/life/{}.csv'.format(app_category)

        #review_list.to_csv('C:/Users/nanya/PycharmProjects/sample/newdata/life/{}.csv'.format(app_category), encoding='utf-8')
        #print(review_list)
exit()

        #result = open(write_file, 'w+', encoding='utf-8')  # , encoding= 'utf-8')
        #csv_writer = csv.writer(result)

       # for review in review_list:
       #     csv_writer.writerow(review_list)
        #print(csv_writer)
    #exit()


#评论数量十分庞大的情况下先筛
#samples = dataframe.sample(n=30000)
#samples.to_csv('newdata/baidu.csv',encoding='utf-8')
#print(samples)
#需手动转换完格式
