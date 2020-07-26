import dimod
import neal
import numpy as np
from dwave.system import LeapHybridSampler
from itertools import product



m, n = 2, 2 # shape of the outer rectangle
w, h = 2, 1 # shape of smaller ones to fit in
area = w * h

# for padding the outer rectangle to take care of edge escapes
M, N = m + w, n + w

memory_size = M * N + 2 * m * n
big_grid_size = M * N
small_grid_size = m * n
memory = np.arange(memory_size)

# to encode binary variables representing:
# q: memory is filled or not by the lower-left corner point of the small shape
# Q: memory is filled or not by the other parts of the small shape
# t: is the rectangle shape horizintal or vertical
# I: coefficients of cubic terms
# J: coefficients of quadratic terms
# H: coefficients of linear terms
Q = memory[:big_grid_size].reshape(M, N) 
q = memory[big_grid_size: big_grid_size + small_grid_size].reshape(m, n)
t = memory[big_grid_size + small_grid_size:].reshape(m, n)
I = np.zeros((memory_size, memory_size, memory_size))
J = np.zeros((memory_size, memory_size))
H = np.zeros((memory_size,))


# self explanatory
def set_up_linear_members():
    for i in range(m):
        for j in range(n):
            H[Q[i, j]] = 1
    for i in range(m):
        for j in range(n):
            H[q[i, j]] = area ** 2 + area - 1


def set_up_quadratic_members():
    for i1, j1 in product(range(m), range(n)):
        for i2, j2 in product(range(m), range(n)):
            J[Q[i1, j1], Q[i2, j2]] = 1
            J[q[i1, j1], q[i2, j2]] = 1
            if (i2 >= i1) and (i2 <= i1 + w) and (j2 >= j1) and (j2 <= j1 + h):
                J[q[i1, j1], Q[i2, j2]] = -(2 * area - 1)
            else:
                J[q[i1, j1], Q[i2, j2]] = -2 * area


def set_up_cubic_memebers():
    for i1, j1 in product(range(m), range(n)):
        for i2, j2 in product(range(m), range(n)):
            if (i2 >= i1) and (i2 <= i1 + h) and (j2 >= j1 + h) and (j2 <= j1 + w):
                I[q[i1, j1], t[i1, j1], Q[i2, j2]] = 1
            if (i2 >= i1 + h) and (i2 <= i1 + w) and (j2 >= j1) and (j2 <= j1 + h):
                 I[q[i1, j1], t[i1, j1], Q[i2, j2]] = -1


def get_dic_from_matrix(matrix):
    d = {}
    for i in product(*[range(s) for s in matrix.shape]):
        if matrix[i]:
            d[i] = matrix[i]
    return d


set_up_linear_members()
set_up_quadratic_members()
set_up_cubic_memebers()
# print(get_dic_from_matrix(I))

poly = {
    **get_dic_from_matrix(I),
    **get_dic_from_matrix(J),
    **get_dic_from_matrix(H)
}


# used to make cubic-quadratic conversion
strength = 5

bqm = dimod.make_quadratic(poly, strength, dimod.BINARY)
print(bqm.num_variables)
sampler = neal.SimulatedAnnealingSampler()
result = sampler.sample(bqm, num_reads=20)
# sampler = LeapHybridSampler()
# sampleset = sampler.sample(bqm)
