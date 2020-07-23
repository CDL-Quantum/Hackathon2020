import networkx as nx
import numpy as np
from itertools import combinations
from random import uniform


from openfermion import QubitOperator
from zquantum.core.utils import dec2bin
from zquantum.core.graph import generate_graph_node_dict

def get_maxcut_hamiltonian(graph):
    """Converts a MAXCUT instance, as described by a weighted graph, to an Ising 
    Hamiltonian.

    Args:
        graph (networkx.Graph): undirected weighted graph describing the MAXCUT 
        instance.
    
    Returns:
        zquantum.core.qubitoperator.QubitOperator object describing the 
        Hamiltonian.
    """

    output = QubitOperator()

    nodes_dict = generate_graph_node_dict(graph)

    for edge in graph.edges:
        coeff = graph.edges[edge[0],edge[1]]['weight']
        node_index1 = nodes_dict[edge[0]]
        node_index2 = nodes_dict[edge[1]]
        ZZ_term_str = 'Z' + str(node_index1) + ' Z' + str(node_index2)
        output += QubitOperator(ZZ_term_str, coeff)
    
    return output

def get_solution_cut_size(solution, graph):
    """Compute the Cut given a partition of the nodes.

    Args:
        solution: list[0,1]
            A list of 0-1 values indicating the partition of the nodes of a graph into two
            separate sets.
        graph: networkx.Graph
            Input graph object.
    """

    if len(solution) != len(graph.nodes):
        raise Exception("trial solution size is {}, which does not match graph size which is {}".format(len(solution), len(graph.nodes)))

    cut_size = 0
    node_dict = generate_graph_node_dict(graph)
    for edge in graph.edges:
        node_index1 = node_dict[edge[0]]
        node_index2 = node_dict[edge[1]]
        if solution[node_index1] != solution[node_index2]:
            cut_size += 1
    return cut_size

def solve_maxcut_by_exhaustive_search(graph):
    """Brute-force solver for MAXCUT instances using exhaustive search.
    Args:
        graph (networkx.Graph): undirected weighted graph describing the MAXCUT 
        instance.
    
    Returns:
        tuple: tuple whose first elements is the number of cuts, and second is a list
            of bit strings that correspond to the solution(s).
    """

    solution_set = []
    num_nodes = len(graph.nodes)

    # find one MAXCUT solution
    maxcut = -1
    one_maxcut_solution = None
    for i in range(0, 2**num_nodes):
        trial_solution = dec2bin(i, num_nodes)
        current_cut = get_solution_cut_size(trial_solution, graph)
        if current_cut > maxcut:
            one_maxcut_solution = trial_solution
            maxcut = current_cut
    solution_set.append(one_maxcut_solution)
    
    # search again to pick up any degeneracies
    for i in range(0, 2**num_nodes):
        trial_solution = dec2bin(i, num_nodes)
        current_cut = get_solution_cut_size(trial_solution, graph)
        if current_cut == maxcut and trial_solution != one_maxcut_solution:
            solution_set.append(trial_solution)

    return maxcut, solution_set
