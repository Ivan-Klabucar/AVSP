import hashlib
import sys


def hamming_dist(s1, s2):
    if not len(s1) == len(s2): raise Exception("len(s1) != len(s2) in hamming dist")
    dist = 0
    for i in range(len(s1)):
        if not s1[i] == s2[i]: dist += 1
    return dist

def num_of_diff_by_atmost_k(subject, others, k):
    res = 0
    for o in others:
        hd = hamming_dist(subject, o)
        if hd <= k: res += 1
    return res

def read_input():
    texts = []
    queries = []
    N = int(sys.stdin.readline().strip())
    for i in range(N):
        texts.append(sys.stdin.readline().strip())
    Q = int(sys.stdin.readline().strip())
    for i in range(Q):
        queries.append(sys.stdin.readline().strip())
    queries = [[int(x.split()[0]), int(x.split()[1])] for x in queries]
    return N, Q, texts, queries


def simhashtext(text):
    sh = [0] * 128
    units = text.strip().split()
    for u in units:
        h = format(int(hashlib.md5(u.encode()).hexdigest(), 16), '#0130b')[2:]
        for i,d in enumerate(h):
            if d == '1':
                sh[i] += 1
            else:
                sh[i] -= 1
    sh = ['1' if x >= 0 else '0' for x in sh]
    return ''.join(sh)

    
