from tabu import TabuSampler
from dwave.system import LeapHybridSampler
from sklearn import cluster, datasets, mixture
import copy
import matplotlib.pyplot as plt
import numpy as np
import dimod
#from anytree import Node, RenderTree
from treelib import Node, Tree

def binary_clustering(feature_vecs,feature_index,**kwargs):
    h= {}
    J= {}
    cluster1 = [] #stores the indices for the first cluster
    cluster2 = [] #stores the indices for the second cluster
    #will recognize tabu or hybrid
    if 'sampler' in kwargs:
        sampler_type = kwargs['sampler']
    else:
        sampler_type = "tabu"
    if 'time_limit' in kwargs:
        time_limit = kwargs['time_limit']
    else:
        time_limit = 20
    sampler = TabuSampler()
    sampler1 = LeapHybridSampler()


    for i in feature_index:
        for j in feature_index:
            if i < j:
                J[(i,j)] = np.linalg.norm(feature_vecs[i] - feature_vecs[j])


    #Now use a sampler to solve it
    if sampler_type == "tabu":
        print("Choosing TABU sampler")
        sampler = TabuSampler()
        sampleset = sampler.sample_ising(h, J, num_reads = 1,timeout=time_limit*1000)
        bin_cluster = sampleset.first[0]
    else:
        
        print("Choosing the hybrid sampler")
        sampler1 = LeapHybridSampler()
        sampleset = sampler1.sample_ising(h, J, time_limit=time_limit)
        bin_cluster = sampleset.first[0]
    # Run the problem on the sampler and print the results


    for key in bin_cluster:
        #put in cluster 1 if -1, else 2
        if bin_cluster[key] == -1:
            cluster1.append(key)
        elif bin_cluster[key] == 1:
            cluster2.append(key)


    return cluster1,cluster2

def squared_dist_sum(feature_vecs,feature_index):
    h= {}
    J= {}
    total = 0.0
    for i in feature_index:
        for j in feature_index:
            if i < j:
                total += np.linalg.norm(feature_vecs[i] - feature_vecs[j])**2
    return total
