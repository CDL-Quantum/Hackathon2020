#%%
from torch.optim import Optimizer
from torch.autograd import Function
from collections.abc import Iterable
import pennylane as qml
import torch
torch.halfpi = torch.acos(torch.zeros(1)).item() # no built-in torch.pi, this is pi/2
# %%
def evaluate_circuits(params, qcircuits):
    """Evaluates each of the quantum circuits provided to build everything """
    circuit_evals = []
    for qcircuit in qcircuits: # there should be a list comprehension one-liner for this but I can't find it 
        circuit_eval = qcircuit(params)
        if isinstance(circuit_eval,Iterable):
            for i in circuit_eval:
                circuit_evals.append(i)
        else:
            circuit_evals.append(circuit_eval)
    return circuit_evals

def costfunc(circuit_evals, proportions):
    """Takes the expectation values of the circuit evaluations and adds them according to the proportion
    Arguments:
        circuit_evals :[Float]: the expectation values
        proportions :[Float]: the mixing coefficients
    """
    loss = 0
    for circ_eval, prop in zip(circuit_evals,proportions):
        loss += circ_eval * prop
    return loss

def kronecker(matrix1, matrix2):
    """ Torch kronecker product """
    return torch.ger(matrix1.view(-1), matrix2.view(-1)).reshape(*(matrix1.size() + matrix2.size())).permute([0, 2, 1, 3]).reshape(matrix1.size(0) * matrix2.size(0), matrix1.size(1) * matrix2.size(1))

class RotoSolve(Optimizer):
    """Implements the RotoSolve parameter finding algorithm for a given circuit ansatz as given by Ostaszewski et al. (2019) (https://arxiv.org/abs/1905.09692)
    QCircuits can be extended as native pytorch operations, requires QCircuit definition as pennylane QNodes. 
    Arguments:
        params (torch.Tensor): Object of :class: torch.Tensor of parameters to update
    """
    def __init__(self, params, qcircuits, proportions):
        super().__init__([params], defaults = {})
        self.qcircuits = qcircuits
        self.proportions = proportions
        self.final_params = params.tolist()
        init_evals = evaluate_circuits(self.final_params, qcircuits)
        initial_cost = costfunc(init_evals, proportions)
        self.losses = [initial_cost]

        

    def step(self):
        """Iterates over the params and sets equal to the closed-form solution found in the param.grad after loss.backward()"""
        for group in self.param_groups:
            params_ = group['params'][0].tolist()
            for idx in range(len(params_)):
                params_[idx] = 0
                circuit_evals = torch.Tensor(evaluate_circuits(params_, self.qcircuits))
                cost0 = costfunc(circuit_evals, self.proportions)
                
                params_[idx] = torch.halfpi
                circuit_evals = torch.Tensor(evaluate_circuits(params_, self.qcircuits))
                costplus = costfunc(circuit_evals, self.proportions)
                
                params_[idx] = -torch.halfpi
                circuit_evals = torch.Tensor(evaluate_circuits(params_, self.qcircuits))
                costminus = costfunc(circuit_evals, self.proportions)

                a = torch.atan2(
                    2.0 * cost0 - costplus - costminus, costplus - costminus
                    ).item()
                params_[idx] = -torch.halfpi - a 
                if params_[idx] <= -2*torch.halfpi:
                    params_[idx] += 4+torch.halfpi
                group['params'] = [torch.FloatTensor(params_)]
        step_circuit_evals = evaluate_circuits(params_, self.qcircuits)
        cost = costfunc(step_circuit_evals, self.proportions)
        self.losses.append(cost)
        self.final_params = params_
        return cost


class QuantumNaturalGradientOptim(Optimizer):
    """ The quantum natural gradient optimizer -- assume access to TorchLayer"""
    def __init__(self, params, qcircuit, lr):
        self.qcircuit = qcircuit
        super().__init__(params, defaults = {})
        self.lr = lr
    
    def step(self):
        for group in self.param_groups:
            params_tensor = group['params'][0]
            fubinimetric = torch.tensor(self.qcircuit.metric_tensor([[],params_tensor.tolist()])).float() # uses the fubinimetric built in
            for p in group['params']:             
                if p.grad is not None:
                    natural_grad = fubinimetric@p.grad.float()
                    p.data.add_(-natural_grad*self.lr)

    # Basically, the trick is to compute gdagger on the parameter update step.
    


# %%
"""
I want to take in the torch.tensor matrix corresponding to the parameterised quantum circuit and then apply it to the input vector 
"""