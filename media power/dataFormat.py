import re
import pandas as pd
import os
from collections import Counter

'''
Function：对数据表进行格式化
#########################
Step1：先把‘From’列的数据取出，把前后空格都去掉
Step2：在数据左边添加两个空格，数据右边添加一个空格
Step3：存入excel表，才可以进行calculate.py的计算
'''


dir = "process3"  # 源文件
file_list = os.listdir(dir)  # 从文件夹按顺序读取文件

# new_from = []


def format():
    for file_name in file_list:
        new_from = []
        print("handle file:{}".format(file_name))
        data = pd.read_excel(os.path.join(dir, file_name), keep_default_na=False)  # reading file   #keep_default_na=False使得读取excel空值时，不存储为NaN，而是''
        media_source = data['From']  # 读取'from'的内容，转载自的源媒体

        for i in range(len(data)):
            temp = '  '+media_source[i].strip()+' '
            new_from.append(temp)


        data.insert(data.shape[1], 'from', new_from)
        data.drop(columns=['From'], inplace=True)
        data.to_excel("format3/all/"+file_name)



if __name__ == '__main__':
    format()

