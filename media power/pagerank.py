"""
使用neworkx库实现pagerank计算
"""
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os

file_name = "./result3/情绪流转结果/result(emotion) 2021.11-2022.02.xlsx"
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号





def build_digGraph():
    """
    初始化图
    :param edges: 存储有向边的列表
    :return: 使用有向边构造完毕的有向图
    """
    G = nx.DiGraph()  # DiGraph()表示有向图

    data = pd.read_excel(file_name)  # reading file   #keep_default_na=False使得读取excel空值时，不存储为NaN，而是''
    media_source = data['source media']  # 读取'source media'的内容，作为edge0
    media = data['report media']  # 读取'report media'，作为edge1
    w = data['count']  # 读取'count'，作为边的权重

    for i in range(len(data)):
        G.add_edge(media[i], media_source[i], weight=w[i])  # 加入边，由edge0指向edge1,被指向的节点是源头，edge0引用edge1

    # for edge in edges:
    #     G.add_edge(edge[0], edge[1],) # 加入边，由edge0指向edge1,被指向的节点是源头，edge0引用edge1


    # G.add_edge("A", "B", weight=3)  # 加入边
    # G.add_edge("A", "C", weight=3)  # 加入边
    # G.add_edge("A", "D", weight=2)  # 加入边
    # G.add_edge("B", "D", weight=3)  # 加入边
    # G.add_edge("C", "E", weight=5)  # 加入边
    # G.add_edge("D", "E", weight=2)  # 加入边
    # G.add_edge("B", "E", weight=1)  # 加入边
    # G.add_edge("E", "A", weight=3)  # 加入边
    return G

if __name__ == '__main__':


    # edges = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "D"), ("C", "E"), ("D", "E"),("B", "E"),("E", "A")]
    # G = build_digGraph(edges)
    G = build_digGraph()

    # '''
    # 将图形画出来
    layout = nx.spring_layout(G)  #networkx上以中心放射状分布.
    nx.draw(G, pos=layout, node_color='y', with_labels=True)
    plt.show()

    # '''
    for index in G.edges(data=True):
        print(index)  #输出所有边的节点关系和权重

    # plt.show()

    # # 最Naive的pagerank计算，最朴素的方式没有设置随机跳跃的部分，所以alpha=1，但是本例中会出现不收敛
    # pr_value = nx.pagerank(G, alpha=1)
    # print("naive pagerank值是：", pr_value)

    # 改进后的pagerank计算，随机跳跃概率为15%，因此alpha=0.85
    pr_impro_value = nx.pagerank(G, alpha=0.85)
    print('\n')
    print("improved pagerank值是：", pr_impro_value)

    #输出结果到表格
    # '''
    keys = list(pr_impro_value.keys())
    values = list(pr_impro_value.values())
    datatata = pd.DataFrame()
    datatata.insert(datatata.shape[1], 'keys', keys)
    datatata.insert(datatata.shape[1], 'values', values)
    datatata.to_excel("result3/" + "PR(media)emotion 2021.11-2022.02.xlsx")
    # '''


    # layout = nx.spring_layout(G)
    # nx.draw(G, pos=layout, cmap = plt.get_cmap('jet'), node_size=[x * 1000 for x in pr_impro_value.values()], node_color='m', with_labels=True)
    # plt.show()

