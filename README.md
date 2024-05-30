1.文件描述：

Acronym.py 缩略词替换

common.py 读tsv、csv、读xlsx、txt

compute_average_rating_bymonth.py 按月划分计算用户评论平均分数

compute_average_rating_byrelease.py 按版本日期分计算用户评论平均分数

count_review_label.py 统计标签分布

delete_col.py 删除列

generateOneHot.py 训练集和测试集分在十个种类上的onehot

getlabelreview.py 提取评论txt转csv

preprocess_review.py 预处理评论

removestopwords 去停用词

sample.py 随机抽样

transformcsv.py xlsx转csv

factor_analysis.py 因子分析算法

factor_analysis_all_vs_rank_60month.py 异常情况对比健康度有用性

get_other_metric.py 获取其他指标值

【lab1】包含用户多标签分类
【lab2】包含因子分析算法的差异性和有用性
【lab2/health_score】十个类别50个app的公因子分数、健康度分数及其排名分布


2.整体流程
transformcsv
-->preprocess_review
-->sample
-->getlabelreview
-->generateOneHot
-->predict
-->compute_average_rating_bymonth
-->get_other_metric
-->factor_analysis
