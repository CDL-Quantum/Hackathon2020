"""API for QAOA, which includes Quantum Approximate Optimization Algorithm,
Quantum Alternating Operator Ansatz, and any layered ansatzes."""

import numpy as np
import scipy

from numpy import mod
from openfermion.utils import count_qubits
from zquantum.core.circuit import Circuit, Qubit, Gate
from zquantum.core.evolution import time_evolution, time_evolution_derivatives
from openfermion import QubitOperator
from qeopenfermion import convert_qubitop_to_dict, convert_dict_to_qubitop
from forestopenfermion import qubitop_to_pyquilpauli

import itertools
import networkx as nx

def build_farhi_qaoa_circuit_template(hamiltonian):
    """Constructs a circuit template for a QAOA ansatz.

    Args:
        hamiltonians (list): a list of zquantum.core.qubitoperator.QubitOperator objects

    Returns:
        circuit_template (dict): dictionary describing the ansatz
    """

    n_qubits = count_qubits(hamiltonian)

    diffusion_op = QubitOperator()
    for i in range(n_qubits):
        diffusion_op += QubitOperator((i, 'X'))

    ansatz = {'ansatz_type': 'singlet UCCSD',
             'ansatz_module': 'zquantum.qaoa.ansatz',
             'ansatz_func' : 'build_qaoa_circuit',
            'ansatz_grad_func': 'build_qaoa_circuit_grads',
            'supports_simple_shift_rule': False,
             'ansatz_kwargs' : {
                 'hamiltonians': [
                     convert_qubitop_to_dict(hamiltonian),
                     convert_qubitop_to_dict(diffusion_op)]
                 },
             'n_params': [2]
            }
    
    return(ansatz)

def build_qaoa_circuit(params, hamiltonians):
    """Generates a circuit for QAOA. This is not only for QAOA proposed by Farhi
    et al., but also general ansatz where alternating layers of time evolution under 
    two different Hamiltonians H1 and H2 are considered.

    Args:
        hamiltonians (list):
            A list of dict or zquantum.core.qubitoperator.QubitOperator objects representing Hamiltonians
            H1, H2, ..., Hk which forms one layer of the ansatz
                    exp(-i Hk tk) ... exp(-i H2 t2) exp(-i H1 t1)
            For example, in the case of QAOA proposed by Farhi et al, the list the list is then
            [H1, H2] where
                H1 is the Hamiltonian for which the ground state is sought, and
                H2 is the Hamiltonian for which the time evolution act as a diffuser 
                    in the search space.
        params (numpy.ndarray): 
            A list of sets of parameters. Each parameter in a set specifies the time
            duration of evolution under each of the Hamiltonians H1, H2, ... Hk.
            
    Returns:
        zquantum.core.circuit.Circuit: the ansatz circuit
    """

    if mod(len(params), len(hamiltonians)) != 0:
        raise Warning('There are {} input parameters and {} Hamiltonians. Since {} does not divide {} the last layer will be incomplete.'.\
            format(len(params), len(hamiltonians), len(params), len(hamiltonians)))

    # Convert qubit operators from dicts to QubitOperator objects, if needed
    for index, hamiltonian in enumerate(hamiltonians):
        if isinstance(hamiltonian, dict):
            hamiltonians[index] = convert_dict_to_qubitop(hamiltonian)

    output = Circuit()

    # Start with a layer of Hadarmard gates
    n_qubits = count_qubits(hamiltonians[0])
    qubits = [Qubit(qubit_index) for qubit_index in range(n_qubits)]
    output.qubits = qubits
    for qubit_index in range(n_qubits):
        output.gates.append(Gate('H', (qubits[qubit_index],)))

    # Add time evolution layers
    for i in range(params.shape[0]):
        hamiltonian_index = mod(i, len(hamiltonians))
        current_hamiltonian = qubitop_to_pyquilpauli(hamiltonians[hamiltonian_index])
        output += time_evolution(current_hamiltonian, params[i])

    return output

def build_qaoa_circuit_grads(params, hamiltonians):
    """ Generates gradient circuits and corresponding factors for the QAOA ansatz
        defined in the function build_qaoa_circuit.

    Args:
        hamiltonians (list):
            A list of dict or zquantum.core.qubitoperator.QubitOperator objects representing Hamiltonians
            H1, H2, ..., Hk which forms one layer of the ansatz
                    exp(-i Hk tk) ... exp(-i H2 t2) exp(-i H1 t1)
            For example, in the case of QAOA proposed by Farhi et al, the list the list is then
            [H1, H2] where
                H1 is the Hamiltonian for which the ground state is sought, and
                H2 is the Hamiltonian for which the time evolution act as a diffuser 
                    in the search space.
        params (numpy.ndarray): 
            A list of sets of parameters. Each parameter in a set specifies the time
            duration of evolution under each of the Hamiltonians H1, H2, ... Hk.
            
    Returns:
        gradient_circuits (list of lists of zquantum.core.circuit.Circuit: the circuits)
        circuit_factors (list of lists of floats): combination coefficients for the expectation
            values of the list of circuits.
    """
    if mod(len(params), len(hamiltonians)) != 0:
        raise Warning('There are {} input parameters and {} Hamiltonians. Since {} does not divide {} the last layer will be incomplete.'.\
            format(len(params), len(hamiltonians), len(params), len(hamiltonians)))

    # Convert qubit operators from dicts to QubitOperator objects, if needed
    for index, hamiltonian in enumerate(hamiltonians):
        if isinstance(hamiltonian, dict):
            hamiltonians[index] = convert_dict_to_qubitop(hamiltonian)

    hadamard_layer = Circuit()

    # Start with a layer of Hadarmard gates
    n_qubits = count_qubits(hamiltonians[0])
    qubits = [Qubit(qubit_index) for qubit_index in range(n_qubits)]
    hadamard_layer.qubits = qubits
    for qubit_index in range(n_qubits):
        hadamard_layer.gates.append(Gate('H', (qubits[qubit_index],)))

    # Add time evolution layers
    gradient_circuits = []
    circuit_factors = []
    
    for index1 in range(params.shape[0]):

        hamiltonian_index1 = mod(index1, len(hamiltonians))
        current_hamiltonian = qubitop_to_pyquilpauli(hamiltonians[hamiltonian_index1])
        derivative_circuits_for_index1, factors = time_evolution_derivatives(
            current_hamiltonian,
            params[index1])
        param_circuits = []

        for derivative_circuit in derivative_circuits_for_index1:
            
            output_circuit = Circuit()
            output_circuit.qubits = qubits
            output_circuit += hadamard_layer

            for index2 in range(params.shape[0]):
                hamiltonian_index2 = mod(index2, len(hamiltonians))
                if index2 == index1:
                    output_circuit += derivative_circuit
                else:
                    current_hamiltonian = qubitop_to_pyquilpauli(hamiltonians[hamiltonian_index2])
                    output_circuit += time_evolution(current_hamiltonian, params[index2])
            param_circuits.append(output_circuit)
        
        circuit_factors.append(factors)
        gradient_circuits.append(param_circuits)

    return gradient_circuits, circuit_factors
