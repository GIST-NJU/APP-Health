import jieba
import os
# 创建缩略词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open('C:/Users/nanya/PycharmProjects/sample/resource/stopwords.txt', 'r',encoding="utf-8").readlines()]
    return stopwords
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist(r'C:/Users/nanya/PycharmProjects/sample/resource/stopwords.txt') # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


filepath = 'C:\\Users\\nanya\PycharmProjects\sample\\newdata'
filelist=os.listdir(filepath)
for i in filelist:
        inputs = open('newdata/camscanner'+i, 'r',encoding="utf-8") #加载要处理的文件的路径
        outputs = open('newdata/camscanner1'+i, 'w',encoding="utf-8") #加载处理后的文件路径
        for line in inputs:
            line_seg = seg_sentence(line)  # 这里的返回值是字符串
            outputs.write(line_seg)
outputs.close()
inputs.close()
