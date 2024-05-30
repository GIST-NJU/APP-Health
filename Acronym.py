import re
import os
import csv
import pandas as pd
from pyltp import SentenceSplitter
from pyltp import Segmentor
from datetime import datetime
import common as com

def reset():
    i = 0
    path = r"/newdata"
    filelist = os.listdir(path)  # 该文件夹下所有文件（包括文件夹）
    for files in filelist:  # 遍历所有文件
        i = i + 1
        Olddir = os.path.join(path, files);  # 原来的文件路径
        if os.path.isdir(Olddir):
            continue;

        filename = os.path.splitext(files)[0];
        filetype = os.path.splitext(files)[1];
        filePath = path + filename + filetype

        alter(filePath, "16", "1")


def alter(file, old_str, new_str):
    with open(file, "r", encoding="utf-8") as f1, open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:

            if old_str in line:
                line = line.replace(old_str, new_str)

            f2.write(line)

    os.remove(file)
    os.rename("%s.bak" % file, file)

def readWords():
    result={}
    with open('resource/1.txt', encoding='UTF-8-sig') as f:
        for line in f:
            x = line.strip().split('=')
            result[x[0]]=x[1]
    return result

def keymap_replace(
        string: str,
        mappings: dict,
        lower_keys=False,
        lower_values=False,
        lower_string=False,
    ) -> str:
    replaced_string = string.lower() if lower_string else string
    for character, replacement in mappings.items():
        replaced_string = replaced_string.replace(
            character.lower() if lower_keys else character,
            replacement.lower() if lower_values else replacement
        )
    return replaced_string

def Acronym_replace(input_file, output_file):
    line_num = 1
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for line in reader:
            line_num += 1
            content = line[6].strip()

            #print(type(content))
            #print(content)
            content = keymap_replace(content, readWords())
            #print(content)
    with open(output_file, 'w', encoding='utf-8') as file:
        reader = csv.reader(file)
        for line in reader:
            file.write(line)
            file.write('\n')

if __name__ == '__main__':
    Acronym_replace('newdata/4.csv', 'newdata/5.csv')
    exit()


reset()