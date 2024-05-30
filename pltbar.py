import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']  # 例子中使用了"SimHei"字体，这是一种常见的中文字体。
plt.rcParams['axes.unicode_minus'] = False  # 这一行可以确保负号的正确显示

fig,ax = plt.subplots(1,1,figsize=(9,4.5),dpi=200)
labels = ['Business', 'Tool', 'Travel', 'Social', 'News', 'Navigation','Music','Life','Entertainment','Education']
labels = ['商务', '工具', '旅游', '社交', '新闻', '导航','音乐','生活','娱乐','教育']

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars


means_2006 = [20, 10, 9, 28, 18, 9, 12, 8, 12, 14]
means_2016 = [9, 8, 10, 11, 11, 11, 11, 10, 11, 7]
rects1 = ax.bar(x - width/2, means_2006, width, label='收敛次数',ec='k',color='white',lw=.8
               )
#rects2 = ax.bar(x + width/2 + .05, means_2016, width, label='2016',ec='k',color='white',
                #lw=.8)
rects2 = ax.bar(x + width/2 + .05, means_2016, width, label='公因子数量',ec='k',color='k',
                 lw=.8,alpha=.8)
ax.tick_params(which='major',direction='in',length=5,width=1.5,labelsize=11,bottom=False)
ax.tick_params(axis='x',labelsize=11,bottom=False,labelrotation=15)
ax.set_xticks(x)
ax.set_ylim(ymin = 0,ymax = 30)
ax.set_yticks(np.arange(0,30,5))

ax.set_ylabel('数量')
ax.set_xticklabels(labels)
#ax.legend(markerscale=10,fontsize=12,prop=legend_font)
ax.legend(markerscale=10,fontsize=12)

# Add some text for labels, title and custom x-axis tick labels, etc.
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(rects1)
autolabel(rects2)
fig.tight_layout()
plt.savefig(r'barplot06.jpg',dpi=600,bbox_inches = 'tight')
