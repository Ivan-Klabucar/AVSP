import sys
import numpy as np
#import time

def read_input():
    [N, beta] = [float(x) for x in sys.stdin.readline().strip().split()]
    N = int(N)
    G = dict.fromkeys(range(N))
    G_tranpose = {x:[] for x in G.keys()}
    deg = dict.fromkeys(range(N))
    for i in range(N):
        to_nodes = [int(x) for x in sys.stdin.readline().strip().split()]
        G[i] = to_nodes
        deg[i] = len(to_nodes)
        for n in to_nodes:
            G_tranpose[n].append(i)

    Q = int(sys.stdin.readline().strip())
    queries = []
    for i in range(Q):
        queries.append([int(x) for x in sys.stdin.readline().strip().split()])

    return N, beta, G, Q, queries, G_tranpose, deg

#in_start = time.time()
#start = time.time()
N, beta, G, Q, queries, G_tranpose, deg = read_input()
#in_end = time.time()

#comp_start = time.time()
last_t = 0
r_t = np.zeros((101,N))
r_t[0] += (1/N)
for t in range(1, 101):
    S = 0
    for j in range(N):
        r_t[t][j] = beta * np.sum([r_t[t-1][i]/deg[i] for i in G_tranpose[j]])
        S += r_t[t][j]
    leaked_imp = (1 - S)/N
    r_t[t] += leaked_imp

    last_t = t
    diff = False
    for j in range(N):
        if round(r_t[t][j], 10) != round(r_t[t-1][j], 10):
            diff = True
            break
    if not diff: break

#comp_end = time.time()
#print(f'computation took: {comp_end-comp_start}s.', file=sys.stderr)

#p_start = time.time()
for query in queries:
    n, t = query
    if t > last_t: t = last_t
    print('{:.10f}'.format(r_t[t][n]))
#p_end = time.time()
#print(f'printing took: {p_end-p_start}s.', file=sys.stderr)
#end = time.time()
#print(f"total: {end-start}s", file=sys.stderr)

    