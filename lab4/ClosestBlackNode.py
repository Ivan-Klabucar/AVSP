import sys
from collections import deque
#import time

def read_input():
    [N, E] = [int(x) for x in sys.stdin.readline().strip().split()]
    G = {x:[] for x in range(N)}
    G_type = dict.fromkeys(range(N))
    black_nodes = []
    for i in range(N):
        G_type[i] = int(sys.stdin.readline().strip())
        if G_type[i] == 1: black_nodes.append(i)

    for _ in range(E):
        n1, n2 = [int(x) for x in sys.stdin.readline().strip().split()]
        G[n1].append(n2)
        G[n2].append(n1)

    return N, E, G_type, G, black_nodes


N, E, G_type, G, black_nodes = read_input()

Dist = dict.fromkeys(range(N))
q = deque()
for b in black_nodes: 
    q.append(b)
    Dist[b] = (0, b)

while q:
    n = q.popleft()
    for neigh in G[n]:
        if not Dist[neigh] == None: continue
        distance = Dist[n][0] + 1
        Dist[neigh] = (distance, Dist[n][1])
        if distance < 10: q.append(neigh)

for n in range(N):
    if Dist[n] == None:
        print('-1 -1')
    else:
        print(f'{Dist[n][1]} {Dist[n][0]}')

