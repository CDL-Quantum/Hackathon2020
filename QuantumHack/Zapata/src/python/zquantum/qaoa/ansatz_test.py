import unittest
import cirq
import pyquil
import random
import numpy as np
from zquantum.core.utils import RNDSEED, compare_unitary, SCHEMA_VERSION
from zquantum.core.circuit import Circuit, build_ansatz_circuit, generate_random_ansatz_params
from openfermion import QubitOperator
from qeopenfermion import generate_random_qubitop
from .ansatz import build_farhi_qaoa_circuit_template, build_qaoa_circuit, build_qaoa_circuit_grads

class TestQAOA(unittest.TestCase):

    def test_build_farhi_qaoa_circuit_template(self):
        # Given
        hamiltonian = QubitOperator('Z0')
        correct_circuit_template = {'ansatz_type': 'singlet UCCSD', 
                    'ansatz_module': 'zquantum.qaoa.ansatz', 
                    'ansatz_func': 'build_qaoa_circuit', 
                    'ansatz_grad_func': 'build_qaoa_circuit_grads', 
                    'supports_simple_shift_rule': False, 
                    'ansatz_kwargs': {'hamiltonians': 
                    [{'schema': SCHEMA_VERSION + '-qubit_op', 'terms': 
                    [{'pauli_ops': [{'qubit': 0, 'op': 'Z'}], 'coefficient': {'real': 1.0}}]}, 
                    {'schema': SCHEMA_VERSION + '-qubit_op', 'terms': 
                    [{'pauli_ops': [{'qubit': 0, 'op': 'X'}], 'coefficient': {'real': 1.0}}]}]}, 
                    'n_params': [2]}
        # When
        circuit_template = build_farhi_qaoa_circuit_template(hamiltonian)

        # Then
        self.assertEqual(circuit_template, correct_circuit_template)
    
    def test_build_qaoa_circuit(self):
        # Given
        hamiltonian_1 = QubitOperator('Z0')
        hamiltonian_2 = QubitOperator('X0')
        hamiltonians = [hamiltonian_1, hamiltonian_2]
        params = np.array([1, 1])
        pyquil_prog = pyquil.quil.Program().inst(pyquil.gates.H(0),
                                pyquil.gates.RZ(2.0,0),
                                pyquil.gates.H(0),
                                pyquil.gates.RZ(2.0,0),
                                pyquil.gates.H(0))

        correct_circuit = Circuit(pyquil_prog)

        # When
        circuit = build_qaoa_circuit(params, hamiltonians)

        # Then
        self.assertEqual(circuit, correct_circuit)

    def test_build_qaoa_ansatz_grads(self):
        # randomly generate problem and diffusion hamiltonian
        random.seed(RNDSEED)
        #num_layers = random.randint(1, 5)
        num_layers = 1
        num_qubits = random.randint(1, 5)
        num_terms = random.randint(1, num_qubits * 3)
        locality = random.randint(1, num_qubits)
        max_coeff = random.uniform(0.5, 1.5)

        problem_hamiltonian = generate_random_qubitop(num_qubits, num_terms, locality, max_coeff)
        circuit_template = build_farhi_qaoa_circuit_template(problem_hamiltonian)
        params = generate_random_ansatz_params(circuit_template)

        # circuit_grads = build_qaoa_circuit_grads(qaoa_ansatz_params, qaoa_ansatz)
        grad_circuits, grad_factors = build_qaoa_circuit_grads(params, circuit_template['ansatz_kwargs']['hamiltonians'])
        self.assertEqual(num_layers * 2, len(grad_circuits))
        self.assertEqual(num_layers * 2, len(grad_factors))
        self.assertEqual(len(grad_circuits[0]), len(problem_hamiltonian.terms) * 2)
        self.assertEqual(len(grad_circuits[1]), num_qubits * 2)
        self.assertEqual(len(grad_factors[0]), len(problem_hamiltonian.terms) * 2)
        self.assertEqual(len(grad_factors[1]), num_qubits * 2)
