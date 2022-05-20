import sys
import numpy as np

def vec_sim(x, y):
    if len(x) != len(y): raise Exception(f'Vectors differen length: {x} and {y}')
    sim = 0
    for i in range(len(x)):
        if x[i] == y[i]:
            sim += 1
    return sim

def reading_is_fundemental():
    edges = set()
    G = dict()
    N = 0
    edge_cnt = 0
    n_to_i = dict()
    i_to_n = dict()
    x = None
    while True:
        x = sys.stdin.readline().strip()
        if x == '': break
        x = [int(i) for i in x.split()]
        for n in x:
            if not n in n_to_i:
                n_to_i[n] = N
                i_to_n[N] = n
                N += 1
        
        x = [n_to_i[node] for node in x]
        if x[0] not in G: G[x[0]] = set()
        if x[1] not in G: G[x[1]] = set()
        G[x[0]].add(x[1])
        G[x[1]].add(x[0])

        edges.add(tuple(sorted([x[0], x[1]])))
        edge_cnt += 1
    N = len(n_to_i)

    node_vectors = dict()
    max_sim = -1

    while True:
        x = sys.stdin.readline().strip()
        if x == '': break
        cur_line = [int(i) for i in x.split()]
        cur_vec = cur_line[1:]
        max_sim = len(cur_vec)
        if cur_line[0] not in n_to_i:
            n_to_i[cur_line[0]] = N
            i_to_n[N] = cur_line[0]
            G[N] = set()
            N += 1
        cur_node = n_to_i[cur_line[0]]
        node_vectors[cur_node] = cur_vec

    adj = np.zeros((N,N)) + np.inf
    for i in i_to_n:
        for j in i_to_n:
            if i == j:
                adj[i][j] = 0
                continue
            if i in G[j]:
                sim = vec_sim(node_vectors[i], node_vectors[j])
                adj[i][j] = max_sim - (sim - 1)
                adj[j][i] = max_sim - (sim - 1)
    
    return N, n_to_i, i_to_n, G, node_vectors, adj, edge_cnt, max_sim, edges

def print_original_shortest_paths(sh_paths):
    for from_n in sh_paths:
        for to_n in sh_paths[from_n]:
            print(f's_paths from {i_to_n[from_n]} to {i_to_n[to_n]}:')
            for p in sh_paths[from_n][to_n]:
                original_p = [i_to_n[x] for x in p]
                original_p = '->'.join([str(x) for x in original_p])
                print(f"{original_p}") 

def print_shortest_paths(sh_paths):
    for from_n in sh_paths:
        for to_n in sh_paths[from_n]:
            print(f's_paths from {from_n} to {to_n}:')
            for p in sh_paths[from_n][to_n]:
                pp = '->'.join([str(x) for x in p])
                print(f"{pp}") 

def neighs(adj_row):
    return list(np.where((adj_row > 0) & (adj_row < np.inf))[0])

def gen_all_paths(path, adj):
    additional = []
    last_n = path[1][-1]
    for neigh in neighs(adj[last_n]):
        if neigh not in path[1]:
            new_seq = list(path[1])
            new_seq.append(neigh)
            new_path = (path[0]+adj[last_n][neigh], new_seq)
            additional.append(new_path)
            additional.extend(gen_all_paths(new_path, adj))
    return additional

def all_shortest_paths(adj):
    paths = dict()
    for i in range(len(adj)):
        all_p_from_i = gen_all_paths((0, [i]), adj)
        paths[i] = dict()
        for j in range(len(adj)):
            relevant_paths = [p for p in all_p_from_i if p[1][-1] == j]
            if len(relevant_paths) == 0: continue
            min_cost = min([p[0] for p in relevant_paths])
            min_paths = [p[1] for p in relevant_paths if p[0] == min_cost]
            paths[i][j] = min_paths
    return paths

def get_edge_betweenness(edges, adj):
    betweenness = {x: 0 for x in edges}
    ash_paths = all_shortest_paths(adj)
    #print_shortest_paths(ash_paths)
    for i in range(len(adj)):
        for j in range(len(adj)):
            if (not i in ash_paths) or (not j in ash_paths[i]) or (len(ash_paths[i][j]) == 0): continue
            betweenness_increase = 1/len(ash_paths[i][j])
            for path in ash_paths[i][j]:
                for k in range(1, len(path)):
                    betweenness[tuple(sorted(path[k-1:k+1]))] += betweenness_increase
    for e in betweenness:
        betweenness[e] = round(betweenness[e]/2, 4)
    #print(betweenness)
    return betweenness

def remove_edges(adj, edges, edges_to_remove):
    for e in edges_to_remove:
        edges.remove(e)
        adj[e[0]][e[1]] = np.inf
        adj[e[1]][e[0]] = np.inf

def get_groups(adj):
    node_group = [None for i in range(len(adj))]
    not_in_group = set(i for i in range(len(adj)))
    queue = []
    group = 0
    while len(not_in_group) != 0:
        curr_group = set()
        queue.append(not_in_group.pop())
        while len(queue) != 0:
            curr_node = queue.pop()
            curr_group.add(curr_node)
            node_group[curr_node] = group
            for i,neigh_dist in enumerate(adj[curr_node]):
                if (not i in curr_group) and neigh_dist > 0 and neigh_dist != np.inf:
                    curr_group.add(i)
                    node_group[i] = group
                    not_in_group.remove(i)
                    queue.append(i)
        group += 1
    node_group_dict = dict()
    for n,g in enumerate(node_group):
        if g not in node_group_dict: node_group_dict[g] = set()
        node_group_dict[g].add(n)
    return node_group, node_group_dict


N, n_to_i, i_to_n, G, node_vectors, adj, edge_cnt, max_sim, edges = reading_is_fundemental()

adj_original = adj.copy()

# sh_paths = all_shortest_paths(adj)


# for p in paths:
#     original_p = [i_to_n[x] for x in p[1]]
#     original_p = '->'.join([str(x) for x in original_p])
#     print(f"cost: {p[0]}, path: {original_p}") 


m = 0
k_i = dict()
for i in range(len(adj)):
    ki = 0
    for j in range(len(adj)):
        if adj[i][j] != np.inf: ki += adj[i][j]
    m += ki
    k_i[i] = ki
m /= 2

# def shortest_paths_to_org(all_shortest_paths, i_to_n):
#     new_sp = dict()
#     for i in all_shortest_paths:
#         new_sp[i_to_n[i]] = dict()
# print('i_to_n:')
# print(i_to_n)
# print()

saved_out = 'None'
max_Q = -np.inf
while len(edges) != 0:

    betweenness = get_edge_betweenness(edges, adj)
    max_bet = max(betweenness.values())
    edges_to_remove = [e for e in betweenness if betweenness[e] == max_bet]
    remove_edges(adj, edges, edges_to_remove)
    node_group, node_group_dict = get_groups(adj)

    Q = 0
    for i in range(len(adj)):
        for j in range(len(adj)):
            if j in node_group_dict[node_group[i]]:
                Aij = adj_original[i][j] 
                if Aij == np.inf: Aij = 0
                Q += Aij - ((k_i[i]*k_i[j])/(2*m))
    Q = (1/(2*m)) * Q
    Q = round(Q, 4)
    edges_to_remove_original = sorted([tuple(sorted([i_to_n[e[0]], i_to_n[e[1]]])) for e in edges_to_remove])

    #print(f'edges to remove:')
    for e in edges_to_remove_original:
        print(f'{e[0]} {e[1]}')
    #print('modularnost:')
    #print(Q)

    if max_Q < Q:
        max_Q = Q
        node_group_original = dict()
        for g in node_group_dict:
            node_group_original[g] = sorted([i_to_n[x] for x in node_group_dict[g]])

        group_sizes = dict()
        for g in node_group_original: group_sizes[g] = len(node_group_original[g])

        outputted_groups = []
        for size in sorted(list(set(group_sizes.values()))):
            g_to_print = []
            for g in node_group_original:
                if len(node_group_original[g]) == size: g_to_print.append(node_group_original[g])
            g_to_print = sorted(g_to_print)
            for gr in g_to_print:
                outputted_groups.append('-'.join([str(x) for x in gr]))
        saved_out = ' '.join(outputted_groups)
print(saved_out)


    







# print('N:')
# print(N)

# print('n_to_i')
# print(n_to_i)

# print('i_to_n')
# print(i_to_n)

# print('G')
# print(G)

# print('node_vrectors')
# print(node_vectors)

# print('adj')
# print(adj)

# print('edge_cnt')
# print(edge_cnt)