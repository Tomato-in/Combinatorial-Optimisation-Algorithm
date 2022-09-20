'''
@Author: Michael 2022-09-16 16:48:22
This code is about Floyd-Warshall.

'''
import copy
import numpy as np

def Floyd(mgraph,start,end,inf):
    start,end = start-1,end-1 #目标及索引归一
    dis,prepoint = GetDisPoint(mgraph)
    print(f"各点间最短距离矩阵为（若值为{inf}则表示对应点间无通路）：\n{np.array(dis)}")
    PathOut(dis,prepoint,start,end,inf)

def GetDisPoint(mgraph):
    '''
    dis矩阵（此处矩阵均以列表存储，后面不在赘述）表示各点间最短路径
    prepoint矩阵用于存储路径前向点，其中-1表示i，j直连，初始假设各点均直连
    注意！！！若i,j无通路，则其前向点对应也为-1，因此利用前向点矩阵prepoin输出路径时，应先根据dis矩阵做初步判断
    '''
    dis = copy.deepcopy(mgraph)
    prepoint = [[-1 for i in range(len(mgraph))] for i in range(len(mgraph))] 
    for k in range(len(mgraph)):
        for i in [i for i in range(len(mgraph)) if i != k]:
            for j in [i for i in range(len(mgraph)) if i != k]:
                if dis[i][j] > dis[i][k] + dis[k][j]:
                    dis[i][j] = dis[i][k] + dis[k][j]
                    prepoint[i][j] = k
    return dis,prepoint

def RevTrace(start,end,prepoint,path=[]):
    '''
    逆向追踪寻找两点间通路，假设各点间均有通路
    
    '''
    if prepoint[start][end] == -1:
        path.append(end+1)
    else:
        mid = prepoint[start][end]
        RevTrace(start,mid,prepoint)
        RevTrace(mid,end,prepoint)
    return [start+1] + path

def PathOut(dis,prepoint,start,end,inf):
    '''
    输出指定两点间最短路径

    '''
    if dis[start][end] == inf: 
        print(f"\n其中{start+1} --> {end+1} 无通路")
    else:
        path = RevTrace(start,end,prepoint)
        print(f"\n其中{start+1} --> {end+1}\n最短路径长为：{dis[start][end]}\n最短路径为：{path}")


# start,end = 1,6 #目标起始点，用于输出某条路径
# inf = 999 #此处表示极大值
# mgraph = [[0,2,5,inf,inf,inf,inf],
#             [inf,0,2,4,3,inf,inf],
#             [inf,inf,0,1,inf,inf,inf],
#             [inf,inf,inf,0,5,6,inf],
#             [inf,inf,inf,inf,0,7,inf],
#             [inf,inf,inf,inf,inf,0,inf],
#             [inf,inf,3,8,inf,2,0]]

# Floyd(mgraph,start,end,inf)
