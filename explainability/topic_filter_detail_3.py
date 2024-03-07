import pandas as pd
import os
import re

# 用于从新闻中查找该新闻包含哪些具体的主题，例如病例增加、病例减少

dir = "paper_result1/emotional_contagion_news"  # 读取源数据
file_list = os.listdir(dir)

# 疫苗有效
effective_list = ["protection", "antibody", "antibodies", "concentration", "protection", "concentration",
                  "effective", "efficacy", "effectiveness", "effect", "useful", "efficacious", "effectual"]
# 疫苗无效
ineffective_list = ["ineffectiveness", "ineffective", "inefficacious", "bootless", "no effect", "fruitless", "useless",
                    "unproductive", "immunocompromized"]
# 无需上下文，源词即可判断所属主题
keywords_list = [
    # kid education  青少年教育
    ["school", "teacher", "students", "student", "teachers", "K-12", "schools"],
    # unemployment 失业停工
    ["unemployment", "out of work", "unemployed", "lose jobs", "fire", "fired", "dismissal", "dismissals", "tighter labor",
     "layoff", "stop work", "excluded", "excludes", "exclude", "lost jobs", "lose job", "lost job", "Labor shortages",
     "tight labor", "labour shortages"],
    # return to work 复工
    ["return to work", "resume work"],
    # variant 病毒毒株变种
    ["variant", "variants", "mutations", "mutation", "mutated", "mrna", "delta", "alpha", "omikron"],
    # allergic  过敏反应/副作用
    ["anaphylaxis", "reactions", "allergic", "allergy", "side effects"],
    # brand 疫苗品牌
    ["sinovac", "sinopharm", "biontech", "moderna", "astrazeneca", "covaxin", "covishield", "covovax", "johnson",
     "kexing", "guoyao", "novavax", "Pfizer"],
    # economy 经济
    ["economy", "economic", "inflation", "prices", "finance", "fiscal", "deficit", "stocks", "price", "share", "shares",
     "market", "stock", "salary", "finance", "bond", "monetary", "wages", "income", "wage", "incomes", "GDP", "CPI",
     "30-stock Dow", "S&P 500", "Nasdaq", "Dow futures", "markets", "stoxx 600", "STOXX Europe 600"]
]

# 防疫政策
policy_list = ["policy", "law", "statute", "regulations", "legislation", "government", "political", "federal",
               "president",  "strategy", "cdc", "prime minister", "premier", "announced", "Emmanuel macron", 'modi',
               "Kremlin", "official", "officials", "measure", "impose", "measures", "Cyril Ramaphosa", "mayors", "rules",
               "governors", "governor", "mayor", "imposed", "obligation", "force", "obligations", "administration"]
# policy_restrict 防疫政策严格
policy_restrict_list = ["closures", "closing", "blockade", "block", "restriction", "restrictions", "control", "close",
                        "stay at home", "mask", "masks", "restrict", "limitation", "lockdown", "indoors", "prevent",
                        "suspension", "containment", "strict", "banning", "mandatory", "prohibited", "curfews",
                        "compulsory", "repression"]
# policy_relaxed 防疫政策放松
policy_relaxed_list = ["relaxed", "relax", "loosen", "relieve", "open", "unclosed", "unlocked", "opens", "opened",
                       "unmask", "reopen", "opening", "reopening", "lifted", "relaxation"]

# 新冠感染病例
case_list = ["case", "cases", "infections", "infection", "infected", "patients", "patient", "pollution", "pollutions",
             "infectious", "positive rate", "wave"]
# 新冠死亡病例
death_list = ["death", "kill", "killed", "deaths", "mortality"]
# 数量增多
num_increase = ["surge", "increase", "increased", "increases", "increased", "grow", "grows", "raise", "rise", "spike",
                "high", "resurgence", "rising", "rose", "improves", "improve", "improved", "risen", "higher", "gained",
                "more", "quadrupled", "twofold", "double", "doubling", "trebling", "treble", "threefold", "triple",
                "thrice", "quattuor", "fourfold", "quintupling", "quintuple", "quintuple", "quintuple", "sevenfold",
                "septuple", "octuple", "eightfold", "Nonuple", "ninefold", "ninefold", "exceeded", "highest", "accelerating"]
# 数量减少
num_decrease = ["decreased", "decrease", "drop", "decline", "lessen", "lower", "diminish", "fall", "declined",
                "declining", "reducing", "reduced", "reduce", "falling", "shed", "down", "slid", "less",
                "disappear", "decelerate", "decelerating"]

'''
# 经济
economy_list = ["economy", "economic", "inflation", "prices", "finance", "fiscal", "deficit", "stocks", "price",
                "share", "shares", "market", "stock", "salary", "finance", "bond", "monetary", "wages", "income", "wage",
                "incomes", "GDP", "CPI", "30-stock Dow", "S&P 500", "Nasdaq", "Dow futures", "markets", "stoxx 600",
                "STOXX Europe 600"]
# 经济上升
economy_increase = ["rebound", "surge", "surged", "promote", "promotes", "promoted", "advance", "advances", "advanced",
                    "hoist", "hoisted", "hoists", "improve", "improves", "improved", "increase", "increases", "recoveries",
                    "increased", "grow", "grows", "healthier", "healthy", "recovery", "unfolds", "unfold", "healthy",
                    "rising", "rose", "rise", "risen", "higher", "gained", "up", "climbed", "added", "jumped"]
# 经济衰退
economy_decrease = ["sink", "sinks", "decrease", "hardship", "hardships", "decimated", "toll", "disaster", "decrease",
                    "tumbling", "drop", "decline", "lessen", "lower", "diminish", "fall", "decay", "crisis", "depression",
                    "contraction", "plunged", "fell", "downturns", "downturn", "declined", "shed", "tumble", "slipped",
                    "down", "slid", "dropped", "sank", "slumping"]
'''
# 疫苗接种
supply_demand_list = ["doses", "dose", "shots", "appointment", "shot", "vaccination", "vaccinate", "vaccines",
                      "injection", "vaccinated", "vaccinations", "vaccine", "vax"]
# 疫苗供应充足
supply_demand_adequate = ["enough", "adequate", "sufficient", "abundant", "ample"]  # 出现这些词且不出现not
# 疫苗供需不平衡
supply_demand_shortage = ["shortage", "deficiency", "lack", "shortfall", "inadequacy", "scarcity", "dearth", "paucity",
                          "insufficiency", "insufficient", "inadequate", "deficient", "lacking", "bottlenecks", "hardship", "shortages"]  # 或者出现supply_demand_adequate且出现not
# 儿童接种疫苗
child = ["children", "child", "teenager", "teenagers", "adolescent", "adolescents", "teenage", "kid", "kids"]
# 疫苗捐赠
donate_list = ['donate', 'donated', 'delivered', 'delivery', 'assistance', 'grant', 'endow', 'bestow', 'granted',
               'bestowed', 'help', 'endowed', 'service', 'support', "distribution", "shipping"
               'supported', 'serviced', 'cooperation', 'collaboration', "donations", "pledged", "pledging", "pledge", "covax"]


def findall(string, s):
    ret = []  # 定义列表 接受结果
    if s == "":
        return tuple(ret)

    while True:
        index = string.find(s)  # 查找子串返回下标

        if index != -1:
            if len(ret) == 0:  # 第一次找到直接加入列表
                ret.append(index)
            else:
                # 当前位置 = 上次查找位置 + 本次查找 + 字符长度
                ret.append(ret[-1] + index + len(s))
            string = string[index + len(s):]
        else:
            break
    return tuple(ret)


def effective_extraction(news, size):
    topic_num_list = []
    n = 0
    for news_each in news:
        topic_num = 0
        for key in effective_list:
            pattern = re.compile(r'(?<![a-zA-Z])' + key + '(?![a-zA-Z])', re.IGNORECASE)
            if pattern.search(str(news_each)):
                # if " " + key + " " in str(news_each):
                f = re.finditer(pattern, str(news_each))
                index_all = []
                for i_f in f:
                    index_all.append(i_f.span()[0])

                # index_all = findall(str(news_each), " " + key + " ")
                length_key = len(key)
                length = len(news_each)

                sub = []
                for index in index_all:
                    # 若窗口没有溢出字符串
                    if index - size >= 0 and index + length_key + size <= length:
                        sub.append(news_each[index - size:index + length_key + size])
                    # 若窗口溢出字符串末
                    elif index - size >= 0 and index + length_key + size > length:
                        sub.append(news_each[index - size:])
                    # 若窗口溢出字符串首
                    elif index - size < 0 and index + length_key + size <= length:
                        sub.append(news_each[:index + length_key + size])
                    # 若窗口首尾溢出字符串
                    elif index - size < 0 and index + length_key + size > length:
                        sub.append(news_each)

                # 上下文中出现key，且不出现not
                for substr in sub:
                    if pattern.search(
                            substr) and " not " not in substr and "problem" not in substr and "problems" not in substr and "question" not in substr and "questions" not in substr and "questioned" not in substr and " lower " not in substr and "reduced" not in substr and "absence " not in substr:
                        topic_num += 1

        topic_num_list.append(topic_num)
        global_keywords_list[n].append(topic_num)
        n += 1
    return topic_num_list


def ineffective_extraction(news, size):
    topic_num_list = []
    n = 0
    for news_each in news:
        topic_num = 0
        # 第一种情况key in effective_list且出现not
        for key in effective_list:
            pattern = re.compile(r'(?<![a-zA-Z])' + key + '(?![a-zA-Z])', re.IGNORECASE)
            if pattern.search(str(news_each)):
                # if " " + key + " " in str(news_each):
                f = re.finditer(pattern, str(news_each))
                index_all = []
                for i_f in f:
                    index_all.append(i_f.span()[0])
                # if " " + key + " " in str(news_each):
                #     index_all = findall(str(news_each), " " + key + " ")
                length_key = len(key)
                length = len(news_each)

                sub = []
                for index in index_all:
                    # 若窗口没有溢出字符串
                    if index - size >= 0 and index + length_key + size <= length:
                        sub.append(news_each[index - size:index + length_key + size])
                    # 若窗口溢出字符串末
                    elif index - size >= 0 and index + length_key + size > length:
                        sub.append(news_each[index - size:])
                    # 若窗口溢出字符串首
                    elif index - size < 0 and index + length_key + size <= length:
                        sub.append(news_each[:index + length_key + size])
                    # 若窗口首尾溢出字符串
                    elif index - size < 0 and index + length_key + size > length:
                        sub.append(news_each)

                # 上下文中出现key，且出现not等
                for substr in sub:
                    if pattern.search(substr) and (
                            (re.compile(r'(?<![a-zA-Z])not(?![a-zA-Z])', re.IGNORECASE).search(substr)) or
                            (re.compile(r'(?<![a-zA-Z])problem(?![a-zA-Z])', re.IGNORECASE).search(substr)) or
                            (re.compile(r'(?<![a-zA-Z])problems(?![a-zA-Z])', re.IGNORECASE).search(substr)) or
                            (re.compile(r'(?<![a-zA-Z])question(?![a-zA-Z])', re.IGNORECASE).search(substr)) or
                            (re.compile(r'(?<![a-zA-Z])questions(?![a-zA-Z])', re.IGNORECASE).search(substr)) or
                            (re.compile(r'(?<![a-zA-Z])questioned(?![a-zA-Z])', re.IGNORECASE).search(substr)) or
                            (re.compile(r'(?<![a-zA-Z])lower(?![a-zA-Z])', re.IGNORECASE).search(substr)) or
                            (re.compile(r'(?<![a-zA-Z])reduced(?![a-zA-Z])', re.IGNORECASE).search(substr)) or
                            (re.compile(r'(?<![a-zA-Z])absence(?![a-zA-Z])', re.IGNORECASE).search(substr))):
                        topic_num += 1

        # 第二种情况出现ineffective的key
        for key_2 in ineffective_list:
            pattern2 = re.compile(r'(?<![a-zA-Z])' + key_2 + '(?![a-zA-Z])', re.IGNORECASE)
            if pattern2.search(str(news_each)):
                # if " " + key_2 + " " in str(news_each):
                f = re.finditer(pattern2, str(news_each))
                index_2 = []
                for i_f in f:
                    index_2.append(i_f.span()[0])

                # index_2 = findall(str(news_each), key_2)
                num = len(index_2)
                topic_num += num

        topic_num_list.append(topic_num)
        global_keywords_list[n].append(topic_num)
        n += 1
    return topic_num_list


def topic_extracton_simple(news):
    result_list = []  # 存储全部新闻的主题个数
    # 每条新闻
    for news_each in news:
        number_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6:0}
        # keyword_percent_list = []
        result_each = []  # 每条新闻一个list存储各主题个数
        n = 0
        for i in keywords_list:
            for j in i:
                pattern = re.compile(r'(?<![a-zA-Z])' + j + '(?![a-zA-Z])', re.IGNORECASE)
                if pattern.search(str(news_each)):
                    # if " " + j + " " in str(news_each):
                    f = re.finditer(pattern, str(news_each))
                    index_all = []
                    for i_f in f:
                        index_all.append(i_f.span()[0])

                    # index = findall(str(news_each), " " + j + " ")
                    number_dict[n] += len(index_all)
            n += 1

        for k in range(0, len(keywords_list)):
            result_each.append(number_dict[k])

        result_list.append(result_each)
        global_keywords_list.append(result_each)

    # print(result_list)
    return result_list


def topic_extraction_complex(news, size, topic_list, up_list, down_list):
    topic_num = []
    n = 0  # n表示新闻中的第几条
    for news_each in news:
        topic_num.append([])

        # up表增加，严格，充足等主题的个数，down表减少，宽松，短缺等主题的个数
        topic_up_num = 0
        topic_down_num = 0
        topic_num[n].append(0)
        topic_num[n].append(0)
        for key in topic_list:
            pattern = re.compile(r'(?<![a-zA-Z])' + key + '(?![a-zA-Z])', re.IGNORECASE)
            if pattern.search(str(news_each)):
                # if " " + key + " " in str(news_each):
                f = re.finditer(pattern, str(news_each))
                index_all = []
                for i_f in f:
                    index_all.append(i_f.span()[0])

                # if " " + key + " " in str(news_each):
                #     # index = str(news_each).find(key)
                #     index_all = findall(str(news_each), " " + key + " ")
                length_key = len(key)
                length = len(news_each)

                # n_sub = 0
                sub = []
                for index in index_all:
                    # 若窗口没有溢出字符串
                    if index - size >= 0 and index + length_key + size <= length:
                        sub.append(news_each[index - size:index + length_key + size])
                    # 若窗口溢出字符串末
                    elif index - size >= 0 and index + length_key + size > length:
                        sub.append(news_each[index - size:])
                    # 若窗口溢出字符串首
                    elif index - size < 0 and index + length_key + size <= length:
                        sub.append(news_each[:index + length_key + size])
                    # 若窗口首尾溢出字符串
                    elif index - size < 0 and index + length_key + size > length:
                        sub.append(news_each)

                    # n_sub += 1

                # 上下文中出现increase等词，且不出现not
                for substr in sub:
                    for i in up_list:
                        pattern_increase = re.compile(r'(?<![a-zA-Z])' + i + '(?![a-zA-Z])', re.IGNORECASE)

                        if pattern_increase.search(substr) and ' cancel ' not in substr and ' no ' not in substr and ' not ' not in substr and ' drag ' not in substr:
                            topic_up_num += 1
                            topic_num[n][0] = topic_up_num
                            break

                        # elif pattern_increase.search(substr) and (' cancel ' in substr or ' no ' in substr or ' not ' in substr or ' drag ' in substr):
                        #     topic_down_num += 1
                        #     topic_num[n][1] = topic_down_num
                        #     break

                    for i in down_list:
                        pattern_decrease = re.compile(r'(?<![a-zA-Z])' + i + '(?![a-zA-Z])', re.IGNORECASE)
                        if pattern_decrease.search(substr) and ' cancel ' not in substr and ' no ' not in substr and ' not ' not in substr and ' drag ' not in substr:
                            # if i in substr:
                            topic_down_num += 1
                            topic_num[n][1] = topic_down_num
                            break

                        # elif pattern_decrease.search(substr) and (' cancel ' in substr or ' no ' in substr or ' not ' in substr or ' drag ' in substr):
                        #     topic_up_num += 1
                        #     topic_num[n][0] = topic_up_num
                        #     break

        global_keywords_list[n].append(topic_num[n][0])
        global_keywords_list[n].append(topic_num[n][1])
        n += 1

    # print(policy_num)
    return topic_num  # （up的主题个数，down的主题个数）


def topic_extration(news, size, base_list, context_list):
    topic_num = []
    n = 0
    for news_each in news:
        # 每条新闻中儿童疫苗的topic个数
        num = 0
        for key in base_list:
            pattern = re.compile(r'(?<![a-zA-Z])' + key + '(?![a-zA-Z])', re.IGNORECASE)
            if pattern.search(str(news_each)):
                # if " " + key + " " in str(news_each):
                f = re.finditer(pattern, str(news_each))
                index_all = []
                for i_f in f:
                    index_all.append(i_f.span()[0])

                # if " " + key + " " in str(news_each):
                #     # index = str(news_each).find(key)
                #     inedx_all = findall(str(news_each), " " + key + " ")
                length_key = len(key)
                length = len(news_each)

                # n_sub = 0
                sub = []
                # 若窗口没有溢出字符串
                for index in index_all:
                    if index - size >= 0 and index + length_key + size <= length:
                        # substr = news_each[index-size:index + length_key + size]
                        sub.append(news_each[index - size:index + length_key + size])
                    # 若窗口溢出字符串末
                    elif index - size >= 0 and index + length_key + size > length:
                        # substr = news_each[index-size:]
                        sub.append(news_each[index - size:])
                    # 若窗口溢出字符串首
                    elif index - size < 0 and index + length_key + size <= length:
                        # substr = news_each[:index + length_key + size]
                        sub.append(news_each[:index + length_key + size])
                    # 若窗口首尾溢出字符串
                    elif index - size < 0 and index + length_key + size > length:
                        # substr = news_each
                        sub.append(news_each)

                    # n_sub += 1

                for substr in sub:
                    for i in context_list:
                        pattern_context = re.compile(r'(?<![a-zA-Z])' + i + '(?![a-zA-Z])', re.IGNORECASE)
                        if pattern_context.search(substr):
                            # if i in substr:
                            num += 1
                            break

        topic_num.append(num)

        global_keywords_list[n].append(topic_num[n])
        n += 1
    # print(policy_num)
    return topic_num


if __name__ == '__main__':
    for file_name in file_list:
        print("handle file:{}".format(file_name))
        data_source = pd.read_excel(os.path.join(dir, file_name))  # reading file
        # 去除新闻情绪=objective的新闻
        news_source = data_source['news_content_translate_en']
        emotion_source = data_source['news_emotion']
        data_new = []
        num = 0
        for k in range(0, len(news_source)):
            # if emotion_source[k] != 'objective':
                data_new.append([])
                data_new[num].append(news_source[k])
                data_new[num].append(emotion_source[k])
                num += 1

        data = pd.DataFrame(data_new, columns=['news_content_translate_en', 'news_emotion'])

        # 以下news为全都是积极情绪OR消极情绪
        news = data['news_content_translate_en']
        emotion = data['news_emotion']
        global_keywords_list = []
        emotion_score = []

        for emotion_each in emotion:
            score = 0
            if 'worried' in str(emotion_each):
                score += -1
            if 'sad' in str(emotion_each):
                score += -2
            if 'hated' in str(emotion_each):
                score += -3
            if 'good' in str(emotion_each):
                score += 1
            if 'believable' in str(emotion_each):
                score += 2
            if 'agreeable' in str(emotion_each):
                score += 3
            if 'objective' in str(emotion_each):
                score += 0

            emotion_score.append(score)

#         news = ["Seoul, March 12.Tass SocietyNorth Korean citizens should not lose vigilance in combating new coronavirus infection.The appeal was made on Friday by the Korean Central newspaper nodon Sinmun, the main printing body of the Korean workers' Party (TPK).\
# Arrogance, carelessness and weakness are the main enemies of the fight against the virus, no matter what time of the year,the editorial said.The note also emphasizes the necessity of not relaxing vigilance.In another publication, the newspaper reported that Ping'an Nandao province was carrying out spring disinfection activities.\
# Pyongyang has repeatedly said that the timely implementation of strict quarantine measures by the authorities has prevented the coronavirus from entering the country.In particular, the authorities completely closed the border.\
# It is estimated that by May this year, the DPRK will receive 1.7 million doses of coronavirus vaccine produced by AstraZeneca, a British Swedish company,The World Health Organization's covax project aims to ensure equal access to vaccines."]
        # news = news[12:]

        result = topic_extracton_simple(news)  # 第一次抽取进行简单抽取
        # print(global_keywords_list)

        effective = effective_extraction(news, 100)
        # print(global_keywords_list)
        ineffective = ineffective_extraction(news, 100)
        # print(global_keywords_list)
        policy = topic_extraction_complex(news, 100, policy_list, policy_restrict_list,
                                          policy_relaxed_list)  # (news, size)size为特定词汇的上下文窗口大小，返回值为（policy_restrict_num，policy_relaxed_number）

        case = topic_extraction_complex(news, 100, case_list, num_increase,
                                        num_decrease)  # 返回值为(case_increase, case_decrease)
        # print(global_keywords_list)
        death = topic_extraction_complex(news, 100, death_list, num_increase,
                                         num_decrease)  # 返回值为(death_increase, death_decrease)
        # economy = topic_extraction_complex(news, 100, economy_list, economy_increase,
        #                                    economy_decrease)  # 返回值为(economy_increase, economy_decrease)

        supply_demand = topic_extraction_complex(news, 100, supply_demand_list, supply_demand_adequate,
                                                 supply_demand_shortage)  # 返回值为(supply_demand_adequate, supply_demand_shortage)

        child_vaccine = topic_extration(news, 100, supply_demand_list, child)
        policy_vaccine = topic_extration(news, 100, policy_list, supply_demand_list)
        vaccine_donate = topic_extration(news, 100, supply_demand_list, donate_list)

        # print(global_keywords_list)
        # 将数据归一化
        # length = len(global_keywords_list)
        # for i in range(0,length):
        #     total = sum(global_keywords_list[i])
        #     for j in range (0, 21):
        #         if total != 0:
        #             global_keywords_list[i][j] = round(global_keywords_list[i][j]/total, 2)
        #         else:
        #             global_keywords_list[i][j] = 0.0

        print(global_keywords_list)
        # 去除所有topic都=0的数据
        length = len(global_keywords_list)
        result_global = []
        n = 0
        for i in range(0, length):
            total = sum(global_keywords_list[i])
            if total != 0:
                result_global.append([])
                for j in range(0, 20):
                    # result_global[n].append(round(global_keywords_list[i][j] / total,2)) #归一化
                    result_global[n].append(global_keywords_list[i][j])  # 不归一化

                result_global[n].append(emotion_score[i])
                result_global[n].append(news[i])
                n += 1

        print(
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(result_global)

        # df = pd.DataFrame(global_keywords_list,
        #                   columns=['kid_education', 'unemployment', 'return_to_work', 'variant',
        #                            'allergic', 'brand', 'economy', 'effective', 'ineffective', 'policy_restrict', 'policy_relaxed', 'case_increase', 'case_decrease',
        #                            'death_increase', 'death_decrease',
        #                            'supply_demand_adequate', 'supply_demand_shortage', 'child_vaccine', 'policy_vaccine', 'vaccine_donate'])
        # df.insert(20, 'emotion', emotion_score)

        df = pd.DataFrame(result_global,
                          columns=['kid_education', 'unemployment', 'return_to_work', 'variant', 'allergic', 'brand',
                                   'economy', 'effective', 'ineffective', 'policy_restrict', 'policy_relaxed',
                                   'case_increase', 'case_decrease', 'death_increase', 'death_decrease',
                                   'supply_demand_adequate', 'supply_demand_shortage', 'child_vaccine',
                                   'policy_vaccine', 'vaccine_donate', 'emotion', 'news'])

        df.to_excel("./paper_result1/emotional_topic_reprint_result1/emotionalContagion_" + file_name, encoding='utf-8', index=False)  # 输出数据结果

