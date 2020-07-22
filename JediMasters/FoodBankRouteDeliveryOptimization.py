# Copyright [2020] [JediMasters - CDL Hackathon 2020]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dwave.system import LeapHybridSampler
import numpy as np
import matplotlib.pyplot as plt
import re
#from mpl_toolkits.basemap import Basemap

# Number of houses in our food delivery problem
Total_Number_Houses = 48
Number_Volunteers = 8
Number_Routes = (int)(Total_Number_Houses/Number_Volunteers)

# Function to compute index in QUBO for variable 
def return_QUBO_Index(a, b):
    return (a)*Total_Number_Houses+(b)

# Tunable parameters. 
A = 8500
B = 1
chainstrength = 4500
numruns = 100

## Constructing the distance matrix
# Distance matrix - a matrix, where row and column represents a city and each entry is a distance.
D = [[0 for z in range(Total_Number_Houses)] for y in range(Total_Number_Houses)]

# Input file containing inter-house distances for all counties
fn = "FoodBankClientDeliveryData.txt"

# check that the user has provided input file
try:
  with open(fn, "r") as myfile:
    distance_text = myfile.readlines()
    myfile.close()
except IOError:
  print("Input inter-house distance file missing")
  exit(1)

# Extract the distances from the input file. 
for i in distance_text:
  if re.search("^between", i):
    m = re.search("^between_(\d+)_(\d+) = (\d+)", i)
    housea = int(m.group(1))
    houseb = int(m.group(2))
    D[housea][houseb] = D[houseb][housea] = int(m.group(3))

## Creating the QUBO
# Start with an empty QUBO
Q = {}
for i in range(Total_Number_Houses*Total_Number_Houses):
    for j in range(Total_Number_Houses*Total_Number_Houses):
        Q.update({(i,j): 0})

# Constraint that each row has exactly one 1, constant = N*A
for v in range(Total_Number_Houses):
    for j in range(Total_Number_Houses):
        Q[(return_QUBO_Index(v,j), return_QUBO_Index(v,j))] += -1*A
        for k in range(j+1, Total_Number_Houses):
            Q[(return_QUBO_Index(v,j), return_QUBO_Index(v,k))] += 2*A
            Q[(return_QUBO_Index(v,k), return_QUBO_Index(v,j))] += 2*A

# Constraint that each col has exactly one 1
for j in range(Total_Number_Houses):
    for v in range(Total_Number_Houses):
        Q[(return_QUBO_Index(v,j), return_QUBO_Index(v,j))] += -1*A
        for w in range(v+1,Total_Number_Houses):
            Q[(return_QUBO_Index(v,j), return_QUBO_Index(w,j))] += 2*A
            Q[(return_QUBO_Index(w,j), return_QUBO_Index(v,j))] += 2*A

# Objective that minimizes distance
for u in range(Total_Number_Houses):
    for v in range(Total_Number_Houses):
        if u!=v:
            for j in range(Total_Number_Houses):
                Q[(return_QUBO_Index(u,j), return_QUBO_Index(v,(j+1)%Total_Number_Houses))] += B*D[u][v]

# Run the QUBO using qbsolv (classically solving)
#from dwave_qbsolv import QBSolv
#resp = QBSolv().sample_qubo(Q)

#Quantum Solution

#from dwave_qbsolv import QBSolv
#from dwave.system.samplers import DWaveSampler
#from dwave.system.composites import EmbeddingComposite
#subqubo_size = 30
#sampler = EmbeddingComposite(DWaveSampler())
#resp = QBSolv().sample_qubo(Q, solver=sampler, solver_limit=subqubo_size)

# Use LeapHybridSampler() for faster QPU access
sampler = LeapHybridSampler()
resp = sampler.sample_qubo(Q)

# First solution is the lowest energy solution found
sample = next(iter(resp))

# Display energy for best solution found
print('Energy: ', next(iter(resp.data())).energy)

# Print route for solution found
route = [-1]*Total_Number_Houses
for node in sample:
    if sample[node]>0:
        j = node%Total_Number_Houses
        v = (node-j)/Total_Number_Houses
        route[j] = int(v)

# Compute and display total mileage
mileage = 0
for i in range(Total_Number_Houses):
    mileage+=D[route[i]][route[(i+1)%Total_Number_Houses]]

print('Mileage: ', mileage)

# Print route:

houses = [',']*Total_Number_Houses
cities = [',']*Total_Number_Houses

with open('FoodBankHouseLookup.txt', "r") as myfile:
    address_text = myfile.readlines()
    myfile.close()

for i in address_text:
    index, city, house = i.split(',')
    cities[int(index)] = city.rstrip()
    houses[int(index)] = house.rstrip()

output = open('Food_Bank_Delivery.route.offline', 'w')

r_no = 1
for i in range(Total_Number_Houses):
    if(i % Number_Routes == 0):
        output.write('\n' + 'Route ' + str(r_no) + '\n')
        r_no = r_no + 1
    output.write(houses[route[i]] + ',' + cities[route[i]] + '\n')

