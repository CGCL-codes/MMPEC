'''
import jieba
from gensim import corpora, models, similarities

if __name__ == '__main__':
    # base_data = [
    #     "好雨知时节，当春乃发生。随风潜入夜，润物细无声。野径云俱黑，江船火独明。晓看红湿处，花重锦官城。",
    #     "君问归期未有期，巴山夜雨涨秋池。何当共剪西窗烛，却话巴山夜雨时。",
    #     "莫听穿林打叶声，何妨吟啸且徐行。竹杖芒鞋轻胜马，谁怕？一蓑烟雨任平生。料峭春风吹酒醒，微冷，山头斜照却相迎。回首向来萧瑟处，归去，也无风雨也无晴。",
    #     "天街小雨润如酥，草色遥看近却无。最是一年春好处，绝胜烟柳满皇都。",
    #     "古木阴中系短篷，杖藜扶我过桥东。沾衣欲湿杏花雨，吹面不寒杨柳风。",
    #     "少年听雨歌楼上。红烛昏罗帐。壮年听雨客舟中。江阔云低、断雁叫西风。 而今听雨僧庐下。鬓已星星也。悲欢离合总无情。一任阶前、点滴到天明。",
    #     "雨里鸡鸣一两家，竹溪村路板桥斜。妇姑相唤浴蚕去，闲看中庭栀子花。",
    #     "一夕轻雷落万丝，霁光浮瓦碧参差。有情芍药含春泪，无力蔷薇卧晓枝。"
    # ]
    base_data = ["好雨知时节，当春乃发生。随风潜入夜，润物细无声。野径云俱黑，江船火独明。晓看红湿处，花重锦官城。"]

    # 1.将base_data中的数据进行遍历后分词
    base_items = [[i for i in jieba.lcut(item)] for item in base_data]
    print(base_items)

    # 2.生成词典
    dictionary = corpora.Dictionary(base_items)
    # 3.通过doc2bow稀疏向量生成语料库
    corpus = [dictionary.doc2bow(item) for item in base_items]
    # 4.通过TF模型算法，计算出tf值
    tf = models.TfidfModel(corpus)
    # 5.通过token2id得到特征数（字典里面的键的个数）
    num_features = len(dictionary.token2id.keys())
    # 6.计算稀疏矩阵相似度，建立一个索引
    index = similarities.MatrixSimilarity(tf[corpus], num_features=num_features)

    # 7.处理测试数据
    test_text = "风雨凄凄，鸡鸣喈喈。既见君子，云胡不夷。风雨潇潇，鸡鸣胶胶。既见君子，云胡不瘳。风雨如晦，鸡鸣不已。既见君子，云胡不喜。"
    test_words = [word for word in jieba.cut(test_text)]
    print(test_words)

    # 8.新的稀疏向量
    new_vec = dictionary.doc2bow(test_words)
    # 9.算出相似度
    sims = index[tf[new_vec]]
    print(list(sims))
'''




import jieba
import math
import re
#读入两个txt文件存入s1,s2字符串中
# s1 = open('rdbg2018.txt','r').read()
# s2 = open('rdbg2019.txt','r').read()


#分词与停用词表，将词分好并保存到向量中
stopwords=[]
fstop=open('stop_words.txt','r',encoding='utf-8-sig')
for eachWord in fstop:
    eachWord = re.sub("\n", "", eachWord)
    stopwords.append(eachWord)
fstop.close()

def preprocess(sentence):
    return [w for w in sentence.lower().split() if w not in stopwords]

# s1_cut = [i for i in jieba.cut(s1, cut_all=True) if (i not in stopwords) and i!='']


#计算余弦相似度
def cossim(s1, s2):
    s1_cut = preprocess(s1)
    s2_cut = preprocess(s2)

    print(s1_cut)
    # s2_cut = [i for i in jieba.cut(s2, cut_all=True) if (i not in stopwords) and i!='']
    print(s2_cut)
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
    print("\n余弦相似度为：%f"%result)



if __name__ == '__main__':
    # s1 = 'Obama speaks to the media in Illinois'  # 需要计算的两个句子
    s1 = 'I LIKE HIM'  # 需要计算的两个句子
    # s2 = 'The president greets the press in Chicago'  # 需要计算的两个句子
    s2 = 'HE LIKE ME'  # 需要计算的两个句子
    cossim(s1, s2)
