import pandas as pd
import os
import re

#用于统计内容转载中，哪些新闻主题转载的比较多
dir = "paper_result1/emotional_topic_reprint_result1"  # 读取源数据
file_list = os.listdir(dir)



if __name__ == '__main__':
    allCountry_topic_frequncy = []
    for file_name in file_list:
        print("handle file:{}".format(file_name))
        data_source = pd.read_excel(os.path.join(dir, file_name))  # reading file
        column_name = data_source.columns.values
        # 按列读取数据存入list
        topic_frequncy = []
        for i in column_name[:-2]:
            column_data = data_source[i].values.tolist()
            column_data_sum = sum(column_data)  #汇总某一个主题的总频次
            topic_frequncy.append(column_data_sum)
        allCountry_topic_frequncy.append(topic_frequncy)
    print("finished")
    df = pd.DataFrame(allCountry_topic_frequncy,
                      columns=['kid_education', 'unemployment', 'return_to_work', 'variant', 'allergic', 'brand',
                               'economy', 'effective', 'ineffective', 'policy_restrict', 'policy_relaxed',
                               'case_increase', 'case_decrease', 'death_increase', 'death_decrease',
                               'supply_demand_adequate', 'supply_demand_shortage', 'child_vaccine',
                               'policy_vaccine', 'vaccine_donate'])

    df.to_excel("./paper_result1/emotionalContagion_topicFrequncy_result.xlsx", encoding='utf-8',
                index=False)  # 输出数据结果




