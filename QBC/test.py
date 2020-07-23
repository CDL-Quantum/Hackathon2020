import pennylane as qml
from quantum_aware_optims import *
import torch
from torch.optim import SGD

n_wires = 2

dev = qml.device("default.qubit", analytic=True, wires=2)

def ansatz(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])

@qml.qnode(dev)
def circuit(inputs, params):
    ansatz(params)
    return qml.expval(qml.PauliZ(0)), qml.expval(qml.PauliY(1))

@qml.qnode(dev)
def circuit2(params):
    ansatz(params)
    return qml.expval(qml.PauliX(0))

qcircuits = [circuit, circuit2]
proportions = torch.Tensor([0.5, 1.2, -0.2])
init_params = torch.Tensor([0.1, 0.25])

qlayer = qml.qnn.TorchLayer(circuit,{"params":2})

expvals = qlayer(init_params)
def loss_func(expvals):
    loss = torch.mul(expvals[0],torch.tensor(0.5)) + torch.mul(expvals[1],torch.tensor(0.2))
    return loss

optim =  SGD([qlayer.params], lr=0.1)
optimQNG = QuantumNaturalGradientOptim([qlayer.params],circuit, lr=0.1)
for i in range(100):
    output = qlayer(qlayer.params)
    loss = loss_func(output)
    print(loss)
    loss.backward()
    optimQNG.step()
    optimQNG.zero_grad()
# optim = RotoSolve(init_params,qcircuits,proportions)
# loss = optim.step()
# print(loss)
# print(optim.param_groups)