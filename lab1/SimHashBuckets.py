from Util import *
import time
import sys


start = time.time()

N, Q, texts, queries = read_input()

hashes = [simhashtext(x) for x in texts]
dict_hashes = {x: hashes[x] for x in range(len(hashes))}
candidates = dict()
for band in range(8):
    buckets = dict()
    for i,curr_hash in enumerate(hashes):
        val = hash(curr_hash[band*16:(band+1)*16])
        texts_in_buckets = set()
        if val in buckets:
            texts_in_buckets = buckets[val]
            for t in texts_in_buckets:
                if t not in candidates: candidates[t] = set()
                if i not in candidates: candidates[i] = set()
                candidates[t].add(i)
                candidates[i].add(t)
        texts_in_buckets.add(i)
        buckets[val] = texts_in_buckets

for q in queries:
    print(num_of_diff_by_atmost_k(hashes[q[0]], [dict_hashes[x] for x in candidates[q[0]]], q[1]))

end = time.time()
sys.stderr.write(f'done in {end-start}s.')