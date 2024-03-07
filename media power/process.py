import pandas as pd
import os
import re

'''
用第一种方式（直接匹配媒体名）找出新闻转载关系
'''

'''
str_media = "Stand News|Mingpao|RTHK|MoDaily|Va Kio Daily|Chinatimes|Liberty Times|China times|NYT|NBC|NPR|VnExpress|Nippon Telegraph & Telephone" \
     "UDN|Singapore Today|Straits Times|Channel News Asia|IndiaToday|Rediff|Tokyo Web|Asahi Shinbun|KCNA|DongA|SBS|The Kyunghyang Shinmun" \
     "The Star|Bernama|Borneo Bulletin|Kazpravda|Thai Rath|Bangkok Post|SiamRath|Kompas|Jawa Pos|NHK|Evening Standard|Seoul Broadcasting System" \
     "Radio Republik Indonesia|Hamshahri|PressTV|Daily Pakistan|Hürriyet|Sabah|DailyMail|Reuters|BBC|Le Figaro|Le Monde|L'Obs|RFI|TASS|RG.RU" \
     "RIA|Bild|Der Spiegel|Weser-Kurier|Süddeutsche Zeitung|Frankfurter Allgemeine Zeitung|ZEIT|SCMP|South China Morning Post|HA" \
     "La Stampa|Corriere Della Sera|La Repubblica|El Mondo|El Pais|La Vanguardia|CMJornal|Publico|Expresso|RTP|Belta|Naviny|Kathimerini|Greek Reporter|FoxNews" \
     "The New York Times|Washington Post|CNBC|CNN|The Globe and Mail|NationalPost|Granma|Televisa|Reforma|UOL|Agencia Brasil" \
     "Folha de Sao Paulo|El Nacional|El Universal|TV Publica|El Mercurio|The Age|Sydney Morning Herald|Stuff|NZ Herald|News24" \
     "SABC News|Daily News Egypt|Daily Nation|Kenyan Times|AP|AFP|Agence France|Bloomberg|XinHua|CNA|VIENTIANE TIMES|VIETNAM NEWS" \
     "the Herald|The Los Angeles Times|Kyodo|Yonhap|Daily Mail|the Guardian|global times|Daily Telegraph|The Independent|Central News" \
     "NTT|Yomiuri|China News|zaobao|ABC|the financial times|Phnom Penh Post|The Nation|Jerusalem Post|El Confidential|morning post|Le Soir|the Telegraph" \
     "Sky News|agency France-Press|EFE|WSJ|Sputnik|Europa press|Sunday Times|DPA|CBS|Wall Street Journal|Asahi Shimbun|Nikkei|ANSA" \
     "Interfax|Jiji|Anadolu|9news|Tasnim|Ha'aretz|TANJUG|Philippine news agency|KUNA|Neue Zurcher Zeitung|NeueZurcherZeitung|YTN|Yedioth Ahronoth|NK" \
     "Newsweek|The Japan Times|Yahoo|the Seattle Times|WAFA|Handelsblatt|WELT|the Hindu|NYTIMES|Apple Daily|Phap Luat|Walla|ettoday" \
     "Ta Kung Pao|Bangkok Times|New York Post|the Beijing Youth Daily|Haaretz|East Asia Daily|TBS news|Sankei|El Mundo|NOWnews|ABS-CBN|VOA|Gulf daily" \
     "TVBS|Fuji News|xinbao|Manila Times|Mainichi|Chosun Ilbo|San Francisco Chronicle|NDTV|People's Daily|ji ji|Nihon Keizai Shimbun|Nippon Hoso Kyokai" \
     "PNA|Philippines News Agency|ANTARA|java pos|Berita Nasional Malaysia|MCOT|Siam Rath|VNA|Vietnam News Agency|PTI|Press Trust of India|UNI" \
     "United News of India|Sinhalaya|TamilNet|RSS|Rastriya Samachar Samiti|Hürriyet|Daily Sabah|Cyprus News Agency|Korean Central News Agency|IRNA|ISNA" \
     "SANA|Syrian Arab News Agency|PETRA|Jordan News Agency|Saudi Press Agency|Kuwait|YNAS|Yemen News Agency Saba|ONA|Oman News Agency|BNA|Bahrain News Agency" \
     "QNA|Qatar News Agency|WAM|Emirates News Agency|Palestine News Agency|JTA|Jewish Telegraphic Agency|Jerusalem Post|Agence France Presse" \
     "DW|Deutsche Welle|Die Zeit|BELGA|Radio Televisao Portuguesa|TT|Tidningarnas Telegrambyra|TASR|Tlacova Agentura Slovenskej Republiky|Khabar Agency" \
     "THINA|Rompres|Romanian News Agency|BTA|Bulgarska Telegraph Agency|The Canadian Press|PL|Prensa Latina|CMC|Caribbean Media Corporation|NZPA|MENA|Middle East News Agency" \
     "SUNA|APS|Maghreb Arabe Presse|ZANA|Universo Online|PNA"
'''
report_media = "FoxNews|Fox News|BBC|Bild|CMJORNAL|CNBC|CNN|Channel News Asia|CNA|DailyMail|Daily Mail|Der Spiegel|EIUniversal|EXPRESSO|El_Mundo|ElMundo" \
            "Frankfurter Allgemeine Zeitung|FAZ|Granma|IndiaToday|India Today|News24|PUBLICO|RFI|Radio France Internationale|RIA|Rediff|Reuters|Straits Times" \
            "Sydney Morning Herald|Süddeutsche Zeitung|Singapore Today|SingaporeToday|The Age|UOL|WESER-KURIER|belta|borneobulletin|kazpravda|lastampa|rg|tass|thestar|the star" \
            "washingtonpost|washington post|DongA|Chinatimes|National Post|NationalPost|The Globe and Mail|TheGlobeandMail|The global and Mail|Le Monde" \
            "L'Obs|MoDaily|UDN|Liberty Times|Yomiuri Shimbun|Le Figaro|RTHK|Radio Television Hong Kong|Borneo Bulletin"


# media_arr = str_media.split('|')
media_arr = report_media.split('|')
# file = "Macao, China,2021-01-01-2021-12-05.xlsx"
# dir = "1.1~12.5"
dir = "test"  #读取源数据
file_list = os.listdir(dir)

def judge_theageof(str_media_judge):#存在the age 并且该处地方不是the age of,the age on,the age group,the age limit返回ture
    index_list = [i.start() for i in re.finditer(' the age ', str_media_judge,flags=re.IGNORECASE)]
    flag = False
    for item in index_list:
        # print(str_media_judge[item+9])
        # print(str_media_judge[item+9:item+14])
        if not (str_media_judge[item+9] == 'o' and str_media_judge[item+10] == 'f') and not (str_media_judge[item+9] == 'o' and str_media_judge[item+10] == 'n') and not (str_media_judge[item+9:item+14] == 'group') and not (str_media_judge[item+9:item+14] == 'limit') and not (str_media_judge[item+9:item+14] == 'range') and not (str_media_judge[item+9:item+18] == 'criterion'):
        # if not (str_media_judge[item+9] == 'o' and str_media_judge[item+10] == 'f') and not (str_media_judge[item+9:item+14] == 'group'):
        # if not (str_media_judge[item+9] == 'o' and str_media_judge[item+10] == 'f'):
            flag = True
            break

    return flag


for file_name in file_list:
    print("handle file:{}".format(file_name))
    data = pd.read_excel(os.path.join(dir,file_name)) #reading file
    news = data['news_content_translate_en']
    count = 0
    media_all = []
    media_list=[' ']
    for i in range(len(data)):
        flag = False
        for index_m in range(len(media_arr)):
            brackets_word = r'\('+str(media_arr[index_m])+'\)'   #媒体两边是括号
            judge1 = re.findall(' '+str(media_arr[index_m])+' ', str(news[i]), flags=re.IGNORECASE)#媒体两边是空格
            judge2 = re.findall(brackets_word, str(news[i]), flags=re.IGNORECASE)
            if len(judge1)+len(judge2)!=0:
                if media_arr[index_m] == 'The Age':
                    judge_theage = judge_theageof(str(news[i]))
                    if not judge_theage:
                        continue
                flag = True
                media_list[0] = media_list[0] + media_arr[index_m]+'  '
        if flag == True:
            count+=1
        media_all+=media_list
        media_list=[' ']
    print("find_count:{},total_count:{}".format(count,len(data)))
    data.insert(data.shape[1],'From',media_all)
    data.to_excel("process/"+file_name)   #输出数据结果
