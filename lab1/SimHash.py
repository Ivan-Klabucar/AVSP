from Util import *
import time
import sys

start = time.time()

N, Q, texts, queries = read_input()

hashes = [simhashtext(x) for x in texts]

for q in queries:
    all_others = hashes[:q[0]] + hashes[q[0]+1:]
    print(num_of_diff_by_atmost_k(hashes[q[0]], all_others, q[1]))

end = time.time()



sys.stderr.write(f'done in {end-start}s.')



