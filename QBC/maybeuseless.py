class RotoLoss(Function):
    """ Implements the rotosolve loss algorithm, needs to be it's own class to override .backward() to set the .grad param to not be the gradient
    but the closed form solution for the next step.

    Arguments:
        qcircuit: The fixed quantum circuit you're looking to optimize
        params: the params to feed into the quantum circuit
    """
    @staticmethod
    def forward(ctx,  params, qcircuits, proportions):
        # This is the training loop 
        for idx in range(len(params)):
            params_ = params.tolist()
            params_[idx] = 0
            circuit_evals = evaluate_circuits(params_, qcircuits)
            cost0 = rotocost(circuit_evals, proportions)
            
            params_[idx] = torch.halfpi
            circuit_evals = evaluate_circuits(params_, qcircuits)
            costplus = rotocost(circuit_evals, proportions)
            
            params_[idx] = -torch.halfpi
            circuit_evals = evaluate_circuits(params_, qcircuits)
            costminus = rotocost(circuit_evals, proportions)

            a = torch.atan2(
                2.0 * cost0 - costplus - costminus, costplus - costminus
                ).item()
            params_[idx] = -torch.halfpi - a 
            if params_[idx] <= -2*torch.halfpi:
                params_[idx] += 4+torch.halfpi
        if len(circuit_evals) != len(proportions):
            raise ValueError("There must be the same number of mixing coefficients as expectation value returns")
        cost = 0
        for circuit_eval, proportion in zip(circuit_evals, proportions):
            cost += circuit_eval * proportion
        return torch.Tensor(cost)

    @staticmethod
    def backward(ctx):
        return None, None, None, None