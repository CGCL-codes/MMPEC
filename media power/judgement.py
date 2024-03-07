'''
计算文本余弦相似度。通过相似度找到转载的原文，判断原文与转载文的emotion是否一致，若一致则转载关系成立，否则不成立。
pymongo版本==3.12.1
'''


import pandas as pds
import os
import datetime
from turtle import pd
import datetime as dt
from config import mongo
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
import jieba
import math
import re


#分词与停用词表，将词分好并保存到向量中
stopwords=[]
fstop=open('stop_words.txt','r',encoding='utf-8-sig')
for eachWord in fstop:
    eachWord = re.sub("\n", "", eachWord)
    stopwords.append(eachWord)
fstop.close()
# 数据库连接的部分我已经封装好了 直接使用mongo[collection_name]的形式就可以连上指定的collection
# 打开数据库
COLLECTION_NAME = 'YIMIAO'  #修改查询的数据表
db = mongo[COLLECTION_NAME]

dir = "test"  # 源文件
file_list = os.listdir(dir)  # 从文件夹按顺序读取文件


# #指定查询国家和查询日期
# country = 'Taiwan, China'
# news_website_name = 'BBC'
# start_time = '2020-01-01'  # >=start_time
# end_time = '2022-01-01'    # <end_time
#
# # country_list='Australia','Belarus','Brazil','Brunei','Canada','Cuba','France','Germany','India','Italy','Japan','Malaysia','Portugal','Russia','Singapore','South Africa',
# # 'South Korea', 'Spain', 'The United Kingdom', 'Venezuela', 'the United States', 'Hong Kong, China', 'Macao, China', 'Taiwan, China'

def datetime_to_timestamp(datetime, timezone):
    """
    根据 datetime 与 tzoff 表示的时区转换为时间戳
    :param: datetime should be datetime object
    :param: UTC+(hour_off:min_off) = timezone UTC+8:30  UTC-9
    :return: timestamp int
    """
    timezone = str(timezone).replace('UTC', '')
    if timezone.startswith('-'):
        timezone = timezone.replace(':', ':-')  # -8:30:08 > -8:-30:-08
    temp = timezone.split(':')
    hour_off = int(temp[0]) if len(temp) > 0 else 0
    min_off = int(temp[1]) if len(temp) > 1 else 0
    sec_off = int(temp[2]) if len(temp) > 2 else 0
    return int(datetime.replace(tzinfo=dt.timezone(dt.timedelta(hours=hour_off, minutes=min_off, seconds=sec_off))).timestamp())
def time_to_timestamp(time, timezone='UTC+8'):
    '''
    转换时间到时间戳
    :param time: 标准时间，格式形如：'%Y-%m-%d'
    :param timezone: 标准时区，格式如'UTC+8'
    :return: 返回时间戳
    '''

    # return datetime_to_timestamp(dt.datetime.strptime(time, '%Y-%m-%d'), 'UTC+8')
    return datetime_to_timestamp(time, 'UTC+8')

'''
获取数据库里的新闻数据
'''
def get_news(news_website_name, time):
    # time = datetime.datetime.strptime(time, "%Y-%m-%d")  # 将时间字符串转换成格式化的时间格式
    # 计算time的前7后7天作为开始结束时间
    start_time = time + datetime.timedelta(days=-7)
    end_time = time + datetime.timedelta(days=8)
    print(start_time)
    print(end_time)

    data = db.find({'news_website_name': news_website_name,
                    'news_publish_timestamp': {'$gte': time_to_timestamp(start_time), '$lt': time_to_timestamp(end_time)} ,  #如果不需要指定起止时间，则删去news_publish_timestamp的约束
                    # 'news_content_translate_en': {
                    #     '$regex': "China|CHINA|china|Chinese|Sino|sino|CN|cn|Cn|zhongguo",  # 中国关键词，按照关键词进行筛除
                    #     '$options': "$i"
                    #     },
                    },
                   {
                       '_id': True,   #默认会展示id，所以赋0不展示
                       'news_website_name':True,             #新闻媒体
                       'news_publish_beijing_time': True,    #新闻发布时间
                       'news_content_translate_en': True,    #新闻内容翻译
                       'news_emotion': True                  #情旭
                   })

    # 创建list用于存储从mongoDB中读取到的数据
    mongo_data_list = []
    

    for i in data:
        # 创建dict用于存储各条数据的各个字段名称及内容
        mongo_data_dict = {}
        # 与find()函数里的字段信息保持一致
        news_id = i.get("_id")
        news_website_name = i.get("news_website_name")
        news_publish_beijing_time = i.get("news_publish_beijing_time")
        news_content_translate_en = i.get("news_content_translate_en")
        # emotion1 = i.get("news_emotion")  # emotion是list类型，需要转化为str再存入excel
        # emotion2 = [str(i) for i in emotion1]
        # news_emotion = ' '.join(emotion2)

        # 将查询到的的数据字段内容以更新添加的方式添加到每个dict中
        mongo_data_dict.update({"news_id": str(news_id)})
        mongo_data_dict.update({"news_website_name": news_website_name})
        mongo_data_dict.update({"news_publish_beijing_time": news_publish_beijing_time})
        mongo_data_dict.update({"news_content_translate_en": news_content_translate_en})
        # mongo_data_dict.update({"news_emotion": news_emotion})


        emotion1 = i.get("news_emotion")  # emotion是list类型，需要转化为str再存入excel
        #判断是否存在emotion
        if emotion1:
            emotion2 = [str(i) for i in emotion1]
            news_emotion = ' '.join(emotion2)
            mongo_data_dict.update({"news_emotion": news_emotion})



        # print("mongo_data_dict:", mongo_data_dict)  #在控制台输出查询信息
        mongo_data_list.append(mongo_data_dict)  #mongo_data_list是个列表

    
    # print(dict)
    return mongo_data_list  #返回值是个列表



'''
余弦相似度，衡量文本相似度
'''
def preprocess(sentence):
    return [w for w in sentence.lower().split() if w not in stopwords]


def cossim(s1, s2):
    s1_cut = preprocess(s1)
    s2_cut = preprocess(s2)
    # print(s1_cut)
    # print(s2_cut)
    word_set = set(s1_cut).union(set(s2_cut))

    #用字典保存两篇文章中出现的所有词并编上号
    word_dict = dict()
    i = 0
    for word in word_set:
        word_dict[word] = i
        i += 1


    #根据词袋模型统计词在每篇文档中出现的次数，形成向量
    s1_cut_code = [0]*len(word_dict)

    for word in s1_cut:
        s1_cut_code[word_dict[word]]+=1

    s2_cut_code = [0]*len(word_dict)
    for word in s2_cut:
        s2_cut_code[word_dict[word]]+=1

    # 计算余弦相似度
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(s1_cut_code)):
        sum += s1_cut_code[i] * s2_cut_code[i]
        sq1 += pow(s1_cut_code[i], 2)
        sq2 += pow(s2_cut_code[i], 2)

    try:
        result = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)), 3)
    except ZeroDivisionError:
        result = 0.0
    return result
    print("\n余弦相似度为：%f"%result)

'''
判断转载文章的emotion和原文的emotion是否一致
'''
def judgement():
    for file_name in file_list:
        # 获取excel里的report news数据
        print("handle file:{}".format(file_name))
        data = pds.read_excel(os.path.join(dir, file_name), keep_default_na=False)  # reading file   #keep_default_na=False使得读取excel空值时，不存储为NaN，而是''
        # data = pd.read_excel(os.path.join(dir, file_name))  # reading file
        data_copy = data.copy()

        media_source = data_copy['From']  # 读取'From'的内容，转载自的源媒体
        news_report = data_copy['news_content_translate_en']  # 获取报道的新闻内容
        emotion_report = data_copy['news_emotion']  # 获取报道的新闻emotion
        time = data_copy['news_publish_beijing_time']  # 获取新闻的报道时间

        for i in range(len(data_copy)):

            if (media_source[i] != ' '):
                media_source2 = str(media_source[i]).strip()
                media = str(media_source2).split("  ")  # 获得源媒体，在数据库中查询源媒体和时间匹配的数据
                # print(media)

                str_temp = ' '

                for j in range(len(media)):
                    similarity = 0 #余弦相似度初始化为0，最小值
                    data_list = get_news(media[j], time[i])  # 根据媒体和时间在数据库中查询需要匹配的新闻，存储在字典中
                    data_source = {}
                    # str_temp = ' '
                    
                    if len(data_list):
                        #若列表存在，则转化为字典格式
                        for m in range(len(data_list)):
                            m_temp = str(m)
                            data_source.update({m_temp: data_list[m]})

                        #计算data_source中每一篇文章的余弦相似度
                        for k in data_source:
                            # data_source[k].update({"distanceWMD": distanceWMD})
                            data_source[k].update({"similarity": similarity})
                            news_source = data_source[k]["news_content_translate_en"]
                            # emotion_source = data_source[k]["news_emotion"]
                            # print(news_source)
                            # print(emotion_source)
                            # distanceWMD = run_wmd(str(news_report[i]), str(news_source))  # 使用wmd算法计算文本迁移距离
                            similarity = cossim(str(news_report[i]), str(news_source))  # 使用文本余弦相似度
                            print("余弦相似度:"+str(similarity))
                            data_source[k]["similarity"] = similarity  # 更新余弦相似度

                        sequence_dict = sorted(data_source.items(), key=lambda d: d[1]['similarity'], reverse=True)  #对字典按照相似度进行从大到小排列
                        print(sequence_dict[0][1])

                        #数据库中有些新闻无法进行预处理添加情绪，需要首先判断关键词-emotion是否存在
                        if 'news_emotion' in sequence_dict[0][1]:
                            emotion_final = sequence_dict[0][1]['news_emotion']
                            if emotion_report[i] == emotion_final:
                                # media_source[i]
                                # s1 = str(media_source[i])
                                # s2 = str(meida[j])
                                # media_source[i] = s1.replace(s2, '')
                                # print(media_source[i])
                                str_temp += media[j] + '  '
                media_source[i] = str_temp
                print(media_source[i])
                # str_temp = ' '

        data.drop('From',axis = 1,inplace = True) #删除原data的from列
        data.insert(data.shape[1],'From',media_source)
        data.to_excel("process3/"+file_name)   #输出数据结果















def test():
    judgement()




if __name__ == '__main__':
    # data = get_news();
    judgement()


