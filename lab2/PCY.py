import sys
import itertools

def read_input():
    baskets = []
    N = int(sys.stdin.readline().strip())
    s = float(sys.stdin.readline().strip())
    b = int(sys.stdin.readline().strip())
    for i in range(N):
        line = sys.stdin.readline().strip()
        baskets.append([int(x) for x in line.split()])
    return N, s, b, baskets


N, s, b, baskets = read_input()
supp_THRES = int(s * N)

item_cnt = dict()
for basket in baskets:
    for i in basket: item_cnt[i] = item_cnt.get(i, 0) + 1

num_freq_items = 0
for i in item_cnt: 
    if item_cnt[i] >= supp_THRES: num_freq_items += 1 

k = max(item_cnt)
buckets = dict()

for basket in baskets:
    for pair in itertools.combinations(basket, 2):
        if item_cnt[pair[0]] >= supp_THRES and item_cnt[pair[1]] >= supp_THRES:
            indx = ((pair[0] * k) + pair[1]) % b
            buckets[indx] = buckets.get(indx, 0) + 1


pair_cnt = dict()
for basket in baskets:
    for pair in itertools.combinations(basket, 2):
        if item_cnt[pair[0]] >= supp_THRES and item_cnt[pair[1]] >= supp_THRES:
            indx = ((pair[0] * k) + pair[1]) % b
            if buckets[indx] >= supp_THRES: pair_cnt[pair] = pair_cnt.get(pair, 0) + 1

counted_by_PCY = len(pair_cnt)
frequency_output = sorted(pair_cnt.values() ,reverse=True)

print(int((num_freq_items * (num_freq_items - 1))/2))
print(counted_by_PCY)
for f in frequency_output: print(f)



