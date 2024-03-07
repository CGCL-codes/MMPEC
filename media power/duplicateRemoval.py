# 去除source media中和report media相同的media，即去除自己转载自己的媒体
# 同时把中文媒体名转化为英文媒体名
import pandas as pd
import os


dir = "process2"  # 源文件
file_list = os.listdir(dir)  # 从文件夹按顺序读取文件

def removal():
    for file_name in file_list:
        print("handle file:{}".format(file_name))
        data = pd.read_excel(os.path.join(dir, file_name),keep_default_na=False)  # reading file   #keep_default_na=False使得读取excel空值时，不存储为NaN，而是''

        media = data['news_website_name']  # 读取'news_website_name'的内容，新闻发布的媒体
        media_source = data['From']  # 读取'From'的内容，转载自的源媒体

        for i in range(len(data)):
            # 把中文的媒体名都转化为英文
            if media[i] == 'RFI(法国国际广播电台)':
                media[i] = 'RFI'
            elif media[i] == '东亚日报':
                media[i] = 'DongA'
            elif media[i] == '中時新聞網':
                media[i] = 'Chinatimes'
            elif media[i] == '加拿大国家邮报':
                media[i] = 'NationalPost'
            elif media[i] == '加拿大环球邮报':
                media[i] = 'The Globe and Mail'
            elif media[i] == '法国世界报':
                media[i] = 'Le Monde'
            elif media[i] == '法国新观察家':
                media[i] = "L'Obs"
            elif media[i] == '澳門日報':
                media[i] = 'MoDaily'
            elif media[i] == '聯合新聞網':
                media[i] = 'UDN'
            elif media[i] == '自由時報':
                media[i] = 'Liberty Times'
            elif media[i] == '读卖新闻':
                media[i] = 'Yomiuri Shimbun'
            elif media[i] == '费加罗报':
                media[i] = 'Le Figaro'
            elif media[i] == '香港電台網站':
                media[i] = 'RTHK'



            #source media中存在和report media相同的media，需要删除
            if (media_source[i] != ' '):
                s1 = str(media_source[i])
                s2 = str(media[i])
                if(s1.find(s2)) != -1:
                    # print("source media中存在和report media相同的media，需要删除")
                    # print(s1.replace(' '+s2+' ', ''))  # 把' media '替换为''
                    # print(s1)
                    media_source[i] = s1.replace(' '+s2+' ', '')


        # data.insert(data.shape[1], 'media_source', media_source)
        data.to_excel("process2/" + file_name)  # 输出数据结果


if __name__ == '__main__':
    removal()