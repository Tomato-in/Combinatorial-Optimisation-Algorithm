'''
@Author: Michael 2022-09-15 09:52:13
This code is about Dijkstra.

'''
import copy

def Dijkstra(mgraph,start:int,end:int,inf:int):
    mgraph_c = copy.deepcopy(mgraph)
    start,end = start-1,end-1 #目标及索引归一
    passed = [start] #初始化永久标号
    nopass = [i for i in range(len(mgraph_c)) if i!= start] #初始化非永久标号
    dis = mgraph_c[start]#初始化当前最短路径
    prepoint = [start if i!=inf else -1 for i in dis] #初始化前向点

    while len(nopass):
        #寻找当前永久标记点并更新
        idx = nopass[0]
        for i in nopass:
            if dis[i] < dis[idx]: 
                idx = i
        passed.append(idx)
        nopass.remove(idx)

        #经过最新永久标记点，更新前向点、当前最短路径
        for i in nopass:
            if dis[i] > mgraph_c[idx][i]+dis[idx]:
                prepoint[i] = idx
                dis[i] = mgraph_c[idx][i]+dis[idx]

    if prepoint[end] == -1:
        # print(f"{start+1} --> {end+1} 无通路")
        path = []
    else:
        #逆向追踪寻找路径
        path = [end]
        while path[-1] != start:
            path.append(prepoint[path[-1]])
        path = [i+1 for i in path[::-1]]
        # print(f"{start+1} --> {end+1}\n最短路径长为：{dis[end]}\n最短路径为：{path}")
    return path,dis[end]

# def Output(Display=True,flag,start,end,path):
#     if Display and flag:
#         print(f"{start+1} --> {end+1}\n最短路径长为：{dis[end]}\n最短路径为：{path}")
#     if Display:
#         print(f"{start+1} --> {end+1} 无通路")

# inf = 999 #此处表示极大值
# mgraph = [[0,2,5,inf,inf,inf,inf],
#             [inf,0,2,4,3,inf,inf],
#             [inf,inf,0,1,inf,inf,inf],
#             [inf,inf,inf,0,5,6,inf],
#             [inf,inf,inf,inf,0,7,inf],
#             [inf,inf,inf,inf,inf,0,inf],
#             [inf,inf,3,8,inf,2,0]]

# start,end = 1,6 #目标起始点

# path = Dijkstra(mgraph,start,end,inf)
# print(path)