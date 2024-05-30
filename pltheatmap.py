import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 17})
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']  # 例子中使用了"SimHei"字体，这是一种常见的中文字体。
plt.rcParams['axes.unicode_minus'] = False  # 这一行可以确保负号的正确显示

# 创建一个随机的二维数组作为数据，假设是10个 category 和 20 个 metric 的数据
data = [[0,0,4,5,2,5,5,3,2,0],
[3,0,4,5,2,0,0,3,2,2],
[1,1,0,4,4,4,3,2,0,3],
[0,1,0,4,4,4,3,2,0,3],
[5,5,0,2,5,5,0,5,0,4],
[4,0,0,0,0,0,0,0,0,0],
[0,0,0,0,5,0,2,0,0,5],
[0,0,0,1,0,0,4,4,3,5],
[0,2,2,0,0,0,0,0,0,0],
[0,0,1,0,0,0,0,0,1,0],
[4,0,0,3,0,0,0,4,0,5],
[4,0,0,1,0,0,0,0,0,5],
[5,5,0,0,5,0,0,5,0,4],
[0,0,0,0,0,3,0,1,0,5],
[0,0,5,3,0,2,0,5,5,0],
[5,3,5,0,0,0,0,0,0,0],
[0,2,3,0,0,0,0,0,0,4],
[0,4,0,0,1,1,0,0,4,0],
[0,5,5,0,0,0,1,0,0,4],
[2,0,0,5,0,5,5,0,0,0]]
data = [[0,0,4,5,2,5,5,3,2,1],
[3,0,4,5,2,0,5,3,2,2],
[1,1,0,4,4,4,3,2,0,3],
[0,1,0,4,4,4,3,2,0,3],
[5,5,3,2,5,5,0,5,5,4],
[4,0,2,0,3,1,0,0,0,4],
[5,0,0,0,5,0,2,0,4,5],
[0,0,0,1,0,0,4,4,3,5],
[0,2,2,0,3,0,0,0,0,5],
[5,5,1,0,0,0,0,0,1,5],
[4,3,0,3,0,0,0,4,0,5],
[4,5,5,1,0,3,4,0,5,5],
[5,5,5,2,5,0,0,5,0,4],
[0,0,0,0,0,3,0,1,0,5],
[5,0,5,3,0,2,0,5,5,0],
[5,3,5,0,0,0,0,1,0,0],
[0,2,3,2,0,0,0,0,0,4],
[0,4,0,0,1,1,4,0,4,5],
[0,5,5,0,0,0,1,5,0,4],
[2,0,0,5,5,5,5,0,0,1]]

# 创建横坐标和纵坐标的标签
x_labels = ['Business', 'Tool', 'Travel', 'Social', 'News', 'Navigation','Music','Life','Entertainment','Education']

x_labels = ['商务', '工具', '旅游', '社交', '新闻', '导航','音乐','生活','娱乐','教育']
x_labels = ['Business', 'Tool', 'Travel', 'Social', 'News', 'Navigation','Music','Life','Entertainment','Education']

y_labels = ['Downloads','List Ranking','Number of Release Notes','Length of the Version Update','Feature Assessment','Feature Bug Report','GUI','Guide','Compatiblity','Performance','Security','Account','Content','Ads','Feedback','Competitive Products','Request','Release','Other','Number of Reviews']

y_labels = ['下载量','排名','版本日志次数','版本日志字数','功能评估','BUG','GUI','教程','兼容性','性能','安全性','账户','内容','广告','反馈','竞品','建议','版本','其他','用户评论数量']
y_labels = ['Downloads','List Ranking','Number of Release Notes','Length of the Release Note','Feature Assessment','Bug Report','GUI','Guide','Compatibility','Performance','Security','Account','Content','Ads','Feedback','Competitive Products','Request','Release','Other','Number of Reviews']

# 使用 seaborn 的 heatmap 函数绘制热力图
plt.figure(figsize=(25, 20),dpi=65)  # 设置画布大小
sns.heatmap(data, cmap='Reds',linewidths=0.02,linecolor="white", annot=True, fmt=".1f", xticklabels=x_labels, yticklabels=y_labels)
plt.xlabel('Category')  # 设置横坐标标签
plt.ylabel('Metric')  # 设置纵坐标标签
# 旋转横坐标标签
plt.xticks(rotation=35)
plt.yticks(rotation=35)

plt.savefig(r'heatmap01.jpg',dpi=300)
