'''
@Author: Michael 2022-09-29 18:37:17

'''
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from Dijkstra import Dijkstra

def load_data(path):
    df_edge = pd.read_excel(path, sheet_name = 'Edge')
    df_OD = pd.read_excel(path, sheet_name = 'OD')
    Edge = np.array(df_edge)
    OD = np.array(df_OD)

    T_a0 = Edge[:,3]
    C_a = Edge[:,2]
    num_node = int(np.max(np.max(Edge,axis = 0)[:2]))

    return num_node, Edge, OD, T_a0, C_a

def Mgraph(Edge, X_a, OD, alpha, beta, num_node, T_a0, C_a):
    inf = 10 * len(OD) * np.max(T_a0) * (1 + alpha * (np.sum(OD[:,-1])/np.min(C_a)) ** beta)
    mgraph = np.ones((num_node, num_node)) * inf
    T_a = T_a0 * (1 + alpha * (X_a / C_a) ** beta)
    for i in range(len(Edge)):
        row = int(Edge[i,0] - 1)
        column = int(Edge[i,1] - 1)
        mgraph[row, column] = T_a[i]
    
    return mgraph, inf

def Get_Y_a(mgraph, Edge, OD, inf, num_node):
    Y_a = np.zeros(len(Edge))
    for i in range(len(OD)):
        Q = np.zeros((num_node,num_node))
        start = int(OD[i,0])
        end = int(OD[i,1])
        q = OD[i,2]
        path, _ = Dijkstra(mgraph, start, end, inf)
        for j in range(len(path)-1):
            row = path[j] - 1
            column = path[j+1] - 1
            Q[row,column] = q
        for k in range(len(Edge)):
            row = int(Edge[k,0] - 1)
            column = int(Edge[k,1] - 1)
            Y_a[k] = Y_a[k] + Q[row,column]
    
    return Y_a

def Lamda(T_a0, X_a, C_a,Y_a, lamda, alpha, beta):
    f = lambda T_a0, X_a, C_a, Y_a, lamda, alpha, beta: np.sum((Y_a - X_a) * T_a0 * (1 + alpha * ((X_a + lamda * (Y_a - X_a)) / C_a) ** beta))
    a,b = 0,1
    while 1:
        lamda = 0.5 * (a + b)
        if abs(f(T_a0, X_a, C_a,Y_a, lamda, alpha, beta)) < 1e-6:
            break
        elif f(T_a0, X_a, C_a,Y_a, a, alpha, beta) * f(T_a0, X_a, C_a,Y_a, lamda, alpha, beta) < 0:
            b = lamda
        else:
            a = lamda
        if b - a <= 1e-3:
            break
    return lamda

def Frank_Wolfe(path, alpha, beta):
    start_time = time.time()
    num_node, Edge, OD, T_a0, C_a = load_data(path)
    X_a = np.zeros(len(Edge))
    n = 1
    Cost = []
    ls_lamda = []
    ls_gap = []

    while 1:
        mgraph, inf = Mgraph(Edge, X_a, OD, alpha, beta, num_node, T_a0, C_a)
        Y_a = Get_Y_a(mgraph, Edge, OD, inf, num_node)
        UEIT = np.sum(Y_a * T_a0 * (1 + alpha * (X_a / C_a) ** beta)) #UE ideal time

        if n == 1:
            lamda = 1
        else:
            lamda = Lamda(T_a0, X_a, C_a,Y_a, lamda, alpha, beta)
    
        # crit = np.power(np.sum((lamda * (Y_a - X_a)) ** 2) , 0.5) / (np.sum(X_a) + 1e-6)

        X_a = lamda * Y_a + (1 - lamda) * X_a
        n = n + 1
        TSTT = np.sum(X_a * T_a0 * (1 + alpha * (X_a / C_a) ** beta)) # total system travel time
        gap = abs(TSTT / UEIT - 1)

        Cost.append(TSTT)
        ls_lamda.append(lamda)
        ls_gap.append(gap)
        display(Cost, ls_lamda, ls_gap)

        print(f'iter:{n - 1}, cost:{TSTT}, lamda:{lamda}, gap:{gap}')

        if gap <= 1e-4:
            break
    
    T_a = T_a0 * (1 + alpha * (X_a / C_a) ** beta)

    end_time = time.time()
    run_time = end_time - start_time - 1e-3 * n

    return Edge, X_a, T_a, n, run_time, Cost, ls_gap, ls_lamda

def Output(Edge, X_a, T_a, n, run_time, Cost, ls_gap, ls_lamda):
    
    head_UE = ['init_node', 'term_node', 'capacity', 'X_a', 'T_a']
    UE = np.concatenate((Edge[:,0:3], X_a.reshape(-1,1), T_a.reshape(-1,1)), axis = 1)
    data_UE = pd.DataFrame(UE)
    # data_UE.to_excel(r'F:\Code\交通网络均衡\Traffic_Flow_Equilibrium\Frank-Wolfe\result.xlsx', header = head_UE, sheet_name = 'UE_result')

    head_Aux = ['Cost', 'gap', 'lamda']
    Aux = np.concatenate((np.array(Cost).reshape(-1,1), np.array(ls_gap).reshape(-1,1), np.array(ls_lamda).reshape(-1,1)), axis = 1)
    data_Aux = pd.DataFrame(Aux)
    # data_Aux.to_excel(r'F:\Code\交通网络均衡\Traffic_Flow_Equilibrium\Frank-Wolfe\result.xlsx', header = head_Aux, sheet_name = 'Aux_data')

    with pd.ExcelWriter(r'F:\Code\交通网络均衡\Traffic_Flow_Equilibrium\Frank-Wolfe\result.xlsx') as writer:
        data_UE.to_excel(writer, header = head_UE, sheet_name = 'UE_result')
        data_Aux.to_excel(writer, header = head_Aux, sheet_name = 'Aux_data')

    print(f"迭代次数,{n - 1},运行时间,{run_time}s,系统总消耗时间,{Cost[-1]}")

def display(Cost, ls_lamda, ls_gap):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus']=False

    plt.subplot(1,3,1)
    plt.plot(Cost[:])
    plt.xlabel('迭代次数')
    plt.ylabel('TSTT') 

    plt.subplot(1,3,2)
    plt.plot(ls_lamda[:])
    plt.xlabel('迭代次数')
    plt.ylabel('步长')

    plt.subplot(1,3,3)
    plt.plot(ls_gap[:])
    plt.xlabel('迭代次数')
    plt.ylabel('gap')

    plt.pause(1e-3)

def main(path, alpha, beta):
    Edge, X_a, T_a, n, run_time, Cost, ls_gape, ls_lamda = Frank_Wolfe(path, alpha, beta)
    Output(Edge, X_a, T_a, n, run_time, Cost, ls_gape, ls_lamda)
    plt.show()

# main(r'F:\Code\交通网络均衡\Traffic_Flow_Equilibrium\Frank-Wolfe\N_Q.xlsx', 0.15, 4)

main(r'F:\Code\交通网络均衡\Traffic_Flow_Equilibrium\Frank-Wolfe\Anaheim_net.xlsx', 0.15, 4)