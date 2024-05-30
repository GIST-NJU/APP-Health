import csv
import os
from openpyxl import load_workbook


reg = r"[^0-9A-Za-z\u4e00-\u9fa5]"
def read_tsv(filename):
    train_all_list = []
    with open(filename, 'r', encoding='utf-8') as tsv_in:
        tsv_reader = csv.reader(tsv_in, delimiter='\t')
        for data in tsv_reader:
            train_all_list.append(data)
    return train_all_list

def read_csv(filename):
    """
    读取csv文件，每一行为一个子list
    :param filename:
    :return: {list}
    """
    #  , encoding='utf-8'
    with open(filename, 'r', encoding='utf-8') as f:
        lines =[]
        reader = csv.reader(f)
        for line in reader:
            lines.append(line)
    f.close()
    #print(lines)
    return lines

def read_xlsx(file):
    wb = load_workbook(file)
    sheets = wb.worksheets  # 获取当前所有的sheet

    # 获取 功能对应的 sheet
    sheet1 = sheets[0]
    # print(sheet1)
    rows = sheet1.rows
    lines = []
    for row in rows:
        row_val = [col.value for col in row]
        lines.append(row_val[1:])

    return lines


def read_txt(file):
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    return lines

if __name__ == '__main__':
    read_csv('data/reviews_raw/_02_review_raw.csv')