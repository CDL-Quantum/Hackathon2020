from qiskit.aqua.components.variational_forms import RY
from qiskit.aqua.components.optimizers import COBYLA
from qiskit.aqua.algorithms.adaptive.qaoa.var_form import QAOAVarForm
from qiskit.aqua.algorithms import ExactEigensolver
from qiskit.finance.ising import portfolio
from qiskit import execute, Aer
import numpy as np

from zquantum.core.interfaces.optimizer import Optimizer
from scipy.optimize import OptimizeResult

# set classical optimizer
maxiter = 100
optimizer = COBYLA(maxiter=maxiter)
# set variational ansatz
var_form = RY(n, depth=1)
# var_form = QAOAVarForm(H, 1)  # use this ansatz for CVaR-QAOA
m = var_form.num_parameters
# set backend
backend = Aer.get_backend('statevector_simulator')
# backend = Aer.get_backend('qasm_simulator')  # use this for QASM simulator

def compute_cvar(probabilities, values, alpha):
    """ 
    Auxilliary method to computes CVaR for given probabilities, values, and confidence level.
    
    Attributes:
    - probabilities: list/array of probabilities
    - values: list/array of corresponding values
    - alpha: confidence level
    
    Returns:
    - CVaR
    """
    sorted_indices = np.argsort(values)
    probs = np.array(probabilities)[sorted_indices]
    vals = np.array(values)[sorted_indices]
    cvar = 0
    total_prob = 0
    for i, (p, v) in enumerate(zip(probs, vals)):
        done = False
        if p >= alpha - total_prob:
            p = alpha - total_prob
            done = True
        total_prob += p
        cvar += p * v
    cvar /= total_prob
    return cvar

def eval_bitstring(H, x):
    """
    Auxilliary method to evaluate the objective function for a given bitstring
    
    Attributes:
    - H: cost Hamiltonian
    - x: bitstring
    
    Returns:
    - objective value
    """

    # invert bitstring for convenience and translate to +/-1
    x = x[::-1]    
    spins = np.array([(-1)**(b == '1') for b in x])
    value = 0
    
    # loop over pauli terms and add contribution to objective
    for p in H.paulis:
        weight = np.real(p[0])
        indices = np.where(p[1].z)
        value += weight * np.prod(spins[indices])
    return value

class CVAROptimizer(Optimizer):
    """
    Wrapper for objective function to track the history of evaluations
    """
    
    def __init__(self, var_form, H, offset, alpha, backend, optimal=None):
        self.history = []
        self.var_form = var_form
        self.H = H
        self.offset = offset
        self.alpha = alpha
        self.backend = backend
        self.optimal = optimal
        self.opt_history = []
    
    def evaluate(self, thetas):
    
        # create and run circuit
        qc = self.var_form.construct_circuit(thetas)
        job = execute(qc, self.backend)
        result = job.result()
        counts = result.get_counts()

        # evaluate counts
        probabilities = np.zeros(len(counts))
        values = np.zeros(len(counts))
        for i, (x, p) in enumerate(counts.items()):
            values[i] = eval_bitstring(self.H, x) + self.offset
            probabilities[i] = p
            
        # track optimal probability
        if self.optimal:
            indices = np.where(values <= self.optimal + 1e-8)
            self.opt_history += [sum(probabilities[indices])]
        
        # evaluate cvar
        cvar = compute_cvar(probabilities, values, self.alpha)
        self.history += [cvar]
        return cvar

    optimization_results = {}
    optimization_results['opt_value'] = evaluate
    optimization_results['opt_params'] = opt_history
    optimization_results['history'] = history

    return OptimizeResult(optimization_results)