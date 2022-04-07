import sys
import math

def sim(x, y, x_m, y_m):
    if not len(x) == len(y): raise Exception('x and y not of same length sim func')
    sum_1 = 0
    sum_2 = 0
    sum_3 = 0
    for i in range(len(x)):
        if x[i] == -1 or y[i] == -1: continue
        sum_1 += (x[i] - x_m) * (y[i] - y_m)
        sum_2 += (x[i] - x_m)**2
        sum_3 += (y[i] - y_m)**2
    if sum_3 == 0 or sum_2 == 0: return 0
    #print(sum_1/math.sqrt(sum_2*sum_3))
    return sum_1/math.sqrt(sum_2*sum_3)


print(sim([3, 1, -1, 4, -1], [-1, 2, 4, -1, 4], 1, 2))
print()
print(sim([1, -1, 3, 4, -1], [-1, 2, 4, -1, 4], 3, 4))