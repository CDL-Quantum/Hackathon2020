#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:31:44 2020

@author: hermanni
"""

import numpy as np
import strawberryfields as sf
from strawberryfields import ops
from strawberryfields.decompositions import takagi
from more_itertools import distinct_permutations
from collections import Counter


sf.store_account('eUAjS1VasR1U1gW1pMSg5Bus3bEXWwA1jLge4QG3')
sf.ping()

##########################
# Arbitrary unitary matrix generator
def rvs(dim=3):
    np.random.seed()
    random_state = np.random
    H = np.eye(dim)
    D = np.ones((dim,))
    for n in range(1, dim):
        x = random_state.normal(size=(dim-n+1,))
        D[n-1] = np.sign(x[0])
        x[0] -= D[n-1]*np.sqrt((x*x).sum())
        # Householder transformation
        Hx = (np.eye(dim-n+1) - 2.*np.outer(x, x)/(x*x).sum())
        mat = np.eye(dim)
        mat[n-1:, n-1:] = Hx
        H = np.dot(H, mat)
        # Fix the last sign such that the determinant is 1
    D[-1] = (-1)**(1-(dim % 2))*D.prod()
    # Equivalent to np.dot(np.diag(D), H) but faster, apparently
    H = (D*H.T).T
    return H


def number_of_photons(i,n=6):
    """Check if number of photons in a sample is higher than n (default value is 6)"""
    bitstring = tuple(i)
    if sum(bitstring) > n:
        return True
    else:
        return False


def truncate_samples(samples):
    """Because number of photons fluctuate from one sample to another, 
    we get rid of all samples where the number of photons is higher than n (=6 by default). 
    n indicates the max number of photons authorized per sample"""   
    somelist = [x for x in samples if not number_of_photons(x)]
    return np.array(somelist)


def estimate_probs(samples):
    """Counts and returns the probability of each sampled strings"""
    shots = len(samples)
    bitstrings = [tuple(i) for i in samples]
    count = Counter(bitstrings)
    sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return {k: v / shots for k, v in sorted_count}

def partition(n=6):
    """Yields the basis for our feature vector (=partition set). Takes n as an input and returns 
    the set of strings forming the basis"""
    answer = set()
    for number in range(1,n+1):
        answer.add((number, ))
        for x in range(1, number):
            for y in partition(number - x):
                answer.add(tuple(sorted((x, ) + y)))
    return sorted(answer)

def orbitals(partition_set):
    """Prepares the feature vector. Returns a dictionnary, where keys are the basis vectors (=orbitals) and values
    are their coordinates (= probability of each orbital)"""
    dictio = {}
    dictio[tuple((0,)*8)]=0 #let's not forget first vector
    for i in partition_set:
        l = len(i)
        j = i + tuple((0,)*(8-l))
        dictio[j] = 0
    return dictio

def vector_coordinates(prob_dic,empty_vector):
    """Takes the probability dictionnary and fills in the empty vector"""
    dic = prob_dic.copy()
    full_vector = empty_vector.copy()
    for i in empty_vector.keys():
        x = 0
        l = distinct_permutations(i)
        for j in l:
            x += dic.pop(j, 0)
        full_vector[i] = x
    return full_vector

def generate_matrices(num_singular_value,unitary):
    num_singular_value=str(num_singular_value)
    diag_dict = {'1':[1,0,0,0], '2':[1,1,0,0], '3':[1,1,1,0]}
    D = np.diag(diag_dict[num_singular_value])
    
    # The mean photon number per mode m
    # is set to ensure that the singular values
    # are scaled such that all Sgates have squeezing value r=1
    
    # One can then generate a valid, random B
    plap = unitary
    B = plap @ D @ plap.T
    
    A = np.block([[0*B, B], [B.T, 0*B]])
    return A

def generate_unitaries(num_unitaries):
    unitaries = [None]*num_unitaries
    for i in range(num_unitaries):
        unitaries[i] = rvs(4)
        
    return unitaries

def kernel_to_array(kernel):
    basis_vecs = kernel.keys()
    #print(basis_vecs)
    list_kernel = []
    for vec in basis_vecs:
        list_kernel.append(kernel[vec])
    vectorized_kernel = np.array(list_kernel)
    return vectorized_kernel


        #Fingerprinting function

def fingerprint(samples, num_photons):
    vector_basis = partition(num_photons)
    empty_vector = orbitals(vector_basis)
    clean_sample = truncate_samples(samples)
    prob_dic = estimate_probs(clean_sample)
    full_vector = vector_coordinates(prob_dic,empty_vector)
    #print('full vector is:')
    return full_vector
