import re
import pandas as pd
import os
from collections import Counter

'''
仅统计正面情绪或者负面情绪转载频次，不需要判断情绪的条件使用calculate.py
'''

# dir = "test"  # 源文件
dir = "format3/all"  # 源文件
file_list = os.listdir(dir)  # 从文件夹按顺序读取文件

media_list_total = []  # 统计全部的转载频次

global_list1 =[]#存储新闻发布媒体
global_list2 =[]#存储源媒体
global_list3 =[]#存储数字
def judge_exist(report_media,media_name):
    for i in range(len(global_list1)):
        if global_list1[i] == report_media and global_list2[i] == media_name:
            return i,1
    for i in range(len(global_list1)):
        if global_list1[i] == report_media:
            global_list1.insert(i,report_media)
            global_list2.insert(i,media_name)
            return i,2
    global_list1.append(report_media)
    global_list2.append(media_name)
    return len(global_list1)-1,3

def cal():
    for file_name in file_list:
        print("handle file:{}".format(file_name))
        data = pd.read_excel(os.path.join(dir, file_name), keep_default_na=False)  # reading file   #keep_default_na=False使得读取excel空值时，不存储为NaN，而是''

        media = data['news_website_name']  # 读取'news_website_name'的内容，新闻发布的媒体
        media_source = data['from']  # 读取'from'的内容，转载自的源媒体
        news_emotion = data['news_emotion'] #读取新闻情绪

        media_list_temp = []  # 当前遍历到的转载信息
        media_list = []  # 统计全部的转载频次

        for i in range(len(data)):
            #正面情绪：agreeable、believable、good
            #负面情绪：hated、worried、sad
            #统计正面情绪
            if (('agreeable' in str(news_emotion[i])) or ('believable' in str(news_emotion[i])) or ('good' in str(news_emotion[i]))):
            #统计负面情绪
            # if (('hated' in str(news_emotion[i])) or ('worried' in str(news_emotion[i])) or ('sad' in str(news_emotion[i]))):
            #统计客观情绪
            # if (('objective' in str(news_emotion[i]))):
            # 如果不等于空格且不为空，则存在转载关系
                if ((media_source[i] != '   ')) :
                    media_list_temp = media[i]+ media_source[i].replace('  ','#')  # media_list_temp[media , media_source]
                    media_list.append(media_list_temp)   # 每个表里面的频次
                    media_list_total.append(media_list_temp)  # 全部表频次的总和
                else:
                    i += 1

    list_all = Counter(media_list_total)
    for each in list_all.items():#假设存在counter类的count
        (a,b)=each
        list_a = a.split('#')
        report_media = list_a.pop(0)
        for item in list_a:
            index_value,type = judge_exist(report_media.strip(),item.strip())
            if type == 1:
                global_list3[index_value] += b
            elif type ==2:
                global_list3.insert(index_value,b)
            else:
                global_list3.append(b)



def test():
    for file_name in file_list:
        print("handle file:{}".format(file_name))
        data = pd.read_excel(os.path.join(dir, file_name), keep_default_na=False)  # reading file   #keep_default_na=False使得读取excel空值时，不存储为NaN，而是''

        media = data['report media']  # 读取'news_website_name'的内容，新闻发布的媒体
        media_source = data['source media']  # 读取'from'的内容，转载自的源媒体

        media_list_temp = []  # 当前遍历到的转载信息
        media_list = []  # 统计全部的转载频次

        for i in range(len(data)):
            # 如果不等于空格且不为空，则存在转载关系
            if (media_source[i] != ' ') and (media_source[i] != ''):
                media_list_temp = media[i]+ media_source[i].replace('  ','#')  # media_list_temp[media , media_source]
                media_list.append(media_list_temp)   # 每个表里面的频次
                media_list_total.append(media_list_temp)  # 全部表频次的总和
            else:
                i += 1



if __name__ == '__main__':
    # '''
    cal()
    data=pd.DataFrame()
    data.insert(data.shape[1],'report media',global_list1)
    data.insert(data.shape[1],'source media',global_list2)
    data.insert(data.shape[1],'count',global_list3)
    data.to_excel("result3/result(agreeable emotion).xlsx")
    print("finished!")
    # '''
    # test()