import sys
import math
from decimal import Decimal, ROUND_HALF_UP

def sim(x, y, x_m, y_m):
    #print(f'SIM')
    #print(f'{x}, {y}, {x_m}, {y_m}')
    x = list(x)
    y = list(y)
    if not len(x) == len(y): raise Exception('x and y not of same length sim func')
    sum_1 = 0
    sum_2 = 0
    sum_3 = 0

    for i in range(len(x)):
        if x[i] == -1: x[i] = x_m
        if y[i] == -1: y[i] = y_m

    for i in range(len(x)):
        if x[i] == -1 or y[i] == -1: continue
        sum_1 += (x[i] - x_m) * (y[i] - y_m)
        sum_2 += (x[i] - x_m)**2
        sum_3 += (y[i] - y_m)**2
    if sum_3 == 0 or sum_2 == 0: 
        return 0
    #print(sum_1/math.sqrt(sum_2*sum_3))
    return sum_1/math.sqrt(sum_2*sum_3)

def ui_from_iu(iu, N, M):
    ui = dict()
    for u in range(1, M+1):
        ui[u] = dict()
        for i in iu:
            ui[u][i] = iu[i][u]
    return ui

def read_input():
    baskets = []
    [N, M] = [int(x) for x in sys.stdin.readline().strip().split()]
    iu = dict()
    for i in range(1, N+1):
        line = [-1 if x=='X' else int(x) for x in sys.stdin.readline().strip().split()]
        iu[i] = dict()
        for j,x in enumerate(line):
            iu[i][j+1] = x
    
    ui = ui_from_iu(iu, N, M)
    Q = int(sys.stdin.readline().strip())
    queries = []
    for i in range(Q):
        queries.append([int(x) for x in sys.stdin.readline().strip().split()])

    return N, M, iu, ui, Q, queries


N, M, iu, ui, Q, queries = read_input()

I_mean = dict()
for i in iu:
    relevant = [iu[i][u] for u in iu[i] if iu[i][u] != -1]
    I_mean[i] = sum(relevant) / len(relevant)

U_mean = dict()
for u in ui:
    relevant = [ui[u][i] for i in ui[u] if ui[u][i] != -1]
    U_mean[u] = sum(relevant) / len(relevant)


uu_sim = dict()
ii_sim = dict()

for i in range(1, N+1):
    ii_sim[i] = dict()
for u in range(1, M+1):
    uu_sim[u] = dict()

for query in queries:
    [I, J, T, K] = query
    if T == 0:
        result = 0
        devisor = 0
        candidates = list()
        for i in ui[J]:
            if ui[J][i] == -1 or i == I: continue
            if i not in ii_sim[I]:
                i_vec = []
                I_vec = []
                for u in range(1, M+1):
                    i_vec.append(iu[i][u])
                    I_vec.append(iu[I][u])
                p_sim = sim(i_vec, I_vec, I_mean[i], I_mean[I])
                ii_sim[I][i] = p_sim
                ii_sim[i][I] = p_sim
            if ii_sim[I][i] <= 0: continue
            candidates.append((ii_sim[I][i], N-i, ui[J][i]))
        candidates.sort(reverse=True)
        if len(candidates) < K: K = len(candidates)
        #print(candidates)
        candidates = candidates[:K]
        dev = sum([x[0] for x in candidates])
        s = sum([x[0]*x[2] for x in candidates])
        res = s/dev
        x=Decimal(Decimal(res).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))
        print(x)
    
    if T==1:
        result = 0
        devisor = 0
        candidates = list()
        for u in iu[I]:
            if iu[I][u] == -1 or u == J: continue
            if u not in uu_sim[J]:
                u_vec = []
                J_vec = []
                for i in range(1, N+1):
                    u_vec.append(ui[u][i])
                    J_vec.append(ui[J][i])
                p_sim = sim(u_vec, J_vec, U_mean[u], U_mean[J])
                uu_sim[J][u] = p_sim
                uu_sim[u][J] = p_sim
            if uu_sim[J][u] <= 0: continue
            candidates.append((uu_sim[J][u], M-u, iu[I][u]))
        candidates.sort(reverse=True)
        if len(candidates) < K: K = len(candidates)
        candidates = candidates[:K]
        dev = sum([x[0] for x in candidates])
        s = sum([x[0]*x[2] for x in candidates])
        res = s/dev
        x=Decimal(Decimal(res).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))
        print(x)

