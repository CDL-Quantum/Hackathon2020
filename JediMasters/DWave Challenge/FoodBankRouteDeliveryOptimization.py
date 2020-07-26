from dwave_qbsolv import QBSolv
from dwave.system import LeapHybridSampler
import numpy as np
import matplotlib.pyplot as plt
import re
#from mpl_toolkits.basemap import Basemap

# Number of houses in our food delivery problem
node_count = 48  # Number of houses
salesmen_count = 8  # Number of volunteers
# Number_Routes = (int)(node_count/salesmen_count)


def key(a, b):
    """key returns a key for QUBO dictionary."""
    return a * node_count + b


# Tunable parameters.
A = 8500
B = 1
chainstrength = 4500
numruns = 100


def food_bank_distances():
    """food_bank_distances loads nodes and edges from food bank files
    and returns distance matrix, where rows and columns represent a cities and each entry is a distance.
    """
    fn = "FoodBankClientDeliveryData.txt"
    try:
        with open(fn, "r") as myfile:
            distance_text = myfile.readlines()
            myfile.close()
    except IOError:
        print(f"{fn} file is missing")
        exit(1)
    distances = [[0 for z in range(node_count)]
                 for y in range(node_count)]
    for i in distance_text:
        if re.search("^between", i):
            m = re.search("^between_(\d+)_(\d+) = (\d+)", i)
            house_a = int(m.group(1))
            house_b = int(m.group(2))
            distances[house_a][house_b] = distances[house_b][house_a] = int(
                m.group(3))
    return distances


def qubo(distances):
    """qubo generates and returns QUBO dictionary"""
    q = {}
    for i in range(node_count*node_count):
        for j in range(node_count*node_count):
            q.update({(i, j): 0})

    # Constraint that each row has exactly one 1, constant = N*A
    for v in range(node_count):
        for j in range(node_count):
            q[(key(v, j), key(v, j))] += -1*A
            for k in range(j+1, node_count):
                q[(key(v, j), key(v, k))] += 2*A
                q[(key(v, k), key(v, j))] += 2*A

    # Constraint that each col has exactly one 1
    for j in range(node_count):
        for v in range(node_count):
            q[(key(v, j), key(v, j))] += -1*A
            for w in range(v+1, node_count):
                q[(key(v, j), key(w, j))] += 2*A
                q[(key(w, j), key(v, j))] += 2*A

    # Objective that minimizes distance
    for u in range(node_count):
        for v in range(node_count):
            if u != v:
                for j in range(node_count):
                    q[(key(u, j), key(
                        v, (j+1) % node_count))] += B*distances[u][v]

    return q


distances = food_bank_distances()
Q = qubo(distances)

# Run the QUBO using qbsolv (classically solving)
resp = QBSolv().sample_qubo(Q)

# Quantum Solution

#from dwave_qbsolv import QBSolv
#from dwave.system.samplers import DWaveSampler
#from dwave.system.composites import EmbeddingComposite
#subqubo_size = 30
#sampler = EmbeddingComposite(DWaveSampler())
#resp = QBSolv().sample_qubo(Q, solver=sampler, solver_limit=subqubo_size)

# # Use LeapHybridSampler() for faster QPU access
# sampler = LeapHybridSampler()
# resp = sampler.sample_qubo(Q)

# First solution is the lowest energy solution found
sample = next(iter(resp))

# Display energy for best solution found
print('Energy: ', next(iter(resp.data())).energy)

# Print route for solution found
route = [-1]*node_count
for node in sample:
    if sample[node] > 0:
        j = node % node_count
        v = (node-j)/node_count
        route[j] = int(v)

# Compute and display total mileage
mileage = 0
for i in range(node_count):
    mileage += distances[route[i]][route[(i+1) % node_count]]

print('Mileage: ', mileage)

# Print route:

houses = [',']*node_count
cities = [',']*node_count

with open('FoodBankHouseLookup.txt', "r") as myfile:
    address_text = myfile.readlines()
    myfile.close()

for i in address_text:
    index, city, house = i.split(',')
    cities[int(index)] = city.rstrip()
    houses[int(index)] = house.rstrip()

output = open('Food_Bank_Delivery.route.offline', 'w')

r_no = 1
for i in range(node_count):
    if(i % (int)(node_count/salesmen_count) == 0):
        output.write('\n' + 'Route ' + str(r_no) + '\n')
        r_no = r_no + 1
    output.write(houses[route[i]] + ',' + cities[route[i]] + '\n')
