import unittest
import networkx as nx

from openfermion import QubitOperator
from .maxcut import get_maxcut_hamiltonian,\
    get_solution_cut_size, solve_maxcut_by_exhaustive_search

class TestMaxcut(unittest.TestCase):

    def test_get_maxcut_hamiltonian(self):
        # Given
        graph = nx.Graph()
        graph.add_edge(1, 2, weight=0.4)
        graph.add_edge(2, 3, weight=-0.1)
        graph.add_edge(1, 3, weight=0.2)
        target_hamiltonian = 0.4*QubitOperator('Z0 Z1') - 0.1*QubitOperator('Z1 Z2') + 0.2*QubitOperator('Z0 Z2')

        # When
        hamiltonian = get_maxcut_hamiltonian(graph)
        
        # Then
        self.assertEqual(hamiltonian, target_hamiltonian)
    
    def test_maxcut_exhaustive_solution(self):
        # Given
        graph = nx.Graph()
        graph.add_edge(1, 2, weight=1)
        graph.add_edge(1, 3, weight=1)
        graph.add_edge(2, 3, weight=1)
        graph.add_edge(2, 4, weight=1)
        graph.add_edge(3, 5, weight=1)
        graph.add_edge(4, 5, weight=1)
        # When
        maxcut, solution_set = solve_maxcut_by_exhaustive_search(graph)
        # Then
        self.assertEqual(maxcut, 5)
        for solution in solution_set:
            cut = get_solution_cut_size(solution, graph)
            self.assertEqual(cut, 5)

    def test_get_solution_cut_size(self):
        # Given 
        solution_1 = [0, 0, 0, 0, 0]
        solution_2 = [0, 1, 1, 1, 1]
        solution_3 = [0, 0, 1, 0, 1]
        graph = nx.Graph()
        graph.add_edge(1, 2, weight=1)
        graph.add_edge(1, 3, weight=1)
        graph.add_edge(2, 3, weight=1)
        graph.add_edge(2, 4, weight=1)
        graph.add_edge(3, 5, weight=1)
        graph.add_edge(4, 5, weight=1)

        # When
        cut_size_1 = get_solution_cut_size(solution_1, graph)
        cut_size_2 = get_solution_cut_size(solution_2, graph)
        cut_size_3 = get_solution_cut_size(solution_3, graph)

        # Then
        self.assertEqual(cut_size_1, 0)
        self.assertEqual(cut_size_2, 2)
        self.assertEqual(cut_size_3, 3)