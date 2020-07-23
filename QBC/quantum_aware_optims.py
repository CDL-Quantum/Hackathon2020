#%%
from torch.optim import Optimizer
from torch.autograd import Function
from collections.abc import Iterable
import torch
torch.halfpi = torch.acos(torch.zeros(1)).item() # no built-in torch.pi, this is pi/2
# %%
def evaluate_circuits(params, qcircuits):
    """Evaluates quantum circuits as required """
    circuit_evals = []
    for qcircuit in qcircuits: # there should be a list comprehension one-liner for this but I can't find it 
        circuit_eval = qcircuit(params)
        if isinstance(circuit_eval,Iterable):
            for i in circuit_eval:
                circuit_evals.append(i)
        else:
            circuit_evals.append(circuit_eval)
    return circuit_evals

def rotocost(circuit_evals, proportions):
    cost = 0
    for circ_eval, prop in zip(circuit_evals,proportions):
        cost += circ_eval * prop
    return cost

class RotoSolve(Optimizer):
    """Implements the RotoSolve parameter finding algorithm for a given circuit ansatz as given by Ostaszewski et al. (2019) (https://arxiv.org/abs/1905.09692)
    
    Arguments:
        params (torch.Tensor): Object of :class: torch.Tensor of parameters to update
    """
    def __init__(self, params, qcircuits, proportions):
        super().__init__([params], defaults = {})
        self.qcircuits = qcircuits
        self.proportions = proportions
        

    def step(self):
        """Iterates over the params and sets equal to the closed-form solution found in the param.grad after loss.backward()"""
        for group in self.param_groups:
            params_ = group['params'][0].tolist()
            for idx in range(len(params_)):
                params_[idx] = 0
                circuit_evals = torch.Tensor(evaluate_circuits(params_, self.qcircuits))
                cost0 = rotocost(circuit_evals, self.proportions)
                
                params_[idx] = torch.halfpi
                circuit_evals = torch.Tensor(evaluate_circuits(params_, self.qcircuits))
                costplus = rotocost(circuit_evals, self.proportions)
                
                params_[idx] = -torch.halfpi
                circuit_evals = torch.Tensor(evaluate_circuits(params_, self.qcircuits))
                costminus = rotocost(circuit_evals, self.proportions)

                a = torch.atan2(
                    2.0 * cost0 - costplus - costminus, costplus - costminus
                    ).item()
                params_[idx] = -torch.halfpi - a 
                if params_[idx] <= -2*torch.halfpi:
                    params_[idx] += 4+torch.halfpi
                group['params'] = [torch.FloatTensor(params_)]
        step_circuit_evals = evaluate_circuits(params_, self.qcircuits)
        return rotocost(step_circuit_evals, self.proportions)
        



# %%
