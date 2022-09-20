'''
@Author: Michael 2022-09-16 21:57:27
This code is about Yen, K-Shortest-Paths.

'''

from Dijkstra import Dijkstra
import copy

def Short_limit(mgraph, inf, start, end, passed:list, noaccess:list):
    '''
    mgraph 为临界距离矩阵(以列表储存)
    inf    为设置的极大值
    passed 为当前必须经过点
    nopass 为当前禁止通行路段，以列表储存，其元素为二维列表，表示禁止通行的路段

    path   为当前条件下最短路径，以列表储存
    dis  为当前条件下最短路长度

    此处start,end,passed,noaccess均为现实标号

    '''

    mgraph_copy_1 = copy.deepcopy(mgraph)
    mgraph_copy_2 = copy.deepcopy(mgraph)

    if len(passed) != 0:
        start = passed[-1]

    for i,j in noaccess:
        mgraph_copy_2[i-1][j-1] = inf

    for i in passed:
        for j in range(len(mgraph)):
        #此步保证无重复点
            if i != passed[-1]:
                mgraph_copy_2[i-1][j] = inf
            mgraph_copy_2[j][i-1] = inf

    path,dis = Dijkstra(mgraph_copy_2,start,end,inf)

    path = passed[:-1]+path
    for k in range(len(passed)-1):
        dis += mgraph_copy_1[passed[k]-1][passed[k+1]-1]

    return path, dis

def Init(mgraph,inf,start,end,k):  #初始化
    passed, noaccess, path, dis = [],[],[],[]
    PASS,DIS = [],[]
    path_,dis_ = Short_limit(mgraph, inf, start, end, passed, noaccess)
    PASS.append(path_)
    DIS.append(dis_)
    k = k-1

    for i in range(len(path_)-1):
        passed.append(path_[:i+1])
        noaccess.append([[path_[i],path_[i+1]]])

    for i in range(len(passed)):
        path_,dis_ = Short_limit(mgraph,inf,start,end,passed[i],noaccess[i])
        path.append(path_)
        dis.append(dis_)
    return passed, noaccess, path, dis, PASS, DIS, k

def Branch(passed, noaccess, path, dis, k, PASS, DIS):
    inx = dis.index(min(dis))
    PASS.append(path[inx])
    DIS.append(dis[inx])
    k = k-1

    for i in range(len(passed[inx]),len(path[inx])):
        passed.append(passed[inx]+path[inx][len(passed[inx]):i])
        noaccess.append(noaccess[inx]+[path[inx][i-1:i+1]])
        path_,dis_ = Short_limit(mgraph, inf, start, end, passed[-1], noaccess[-1])
        # if path_ == passed[-1][:-1]:
        if dis_ >= 999:
            del passed[-1]
            del noaccess[-1]
        else:
            path.append(path_)
            dis.append(dis_)

    del passed[inx]
    del noaccess[inx]
    del path[inx]
    del dis[inx]

    while k>0 and len(path) != 0:
        Branch(passed, noaccess, path, dis, k, PASS, DIS)
        return PASS, DIS

def Yen(mgraph, inf, start, end, k):
    passed, noaccess, path, dis, PASS, DIS, k = Init(mgraph,inf,start,end,k)
    PASS, DIS = Branch(passed, noaccess, path, dis, k, PASS, DIS)
    print(f"共寻得{len(PASS)}最短路")
    for i in range(len(DIS)):
        print(f'第{i+1}短路,长{DIS[i]},{PASS[i]}')

# inf = 999 #此处表示极大值
# mgraph = [[0,1,5,inf,inf,inf],
#  [inf,0,3,1,6,inf],
#  [6,2,0,4,2,inf],
#  [inf,4,2,0,5,8],
#  [inf,3,10,1,0,3],
#  [inf,inf,inf,inf,inf,0]]
# start,end,k = 1,6,15

# Yen(mgraph, inf, start, end, k)
