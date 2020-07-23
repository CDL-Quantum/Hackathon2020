import pennylane as qml
import numpy as np
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

# optim =  SGD([qlayer.params], lr=0.1)
# optimQNG = QuantumNaturalGradientOptim([qlayer.params],circuit, lr=0.1)
# for i in range(100):
#     output = qlayer(qlayer.params)
#     loss = loss_func(output)
#     print(loss)
#     loss.backward()
#     optimQNG.step()
#     optimQNG.zero_grad()
# optim = RotoSolve(init_params,qcircuits,proportions)
# loss = optim.step()
# print(loss)
# print(optim.param_groups)


dev = qml.device("default.qubit", wires=3)


@qml.qnode(dev)
def circuit(inputs, params):
    # |psi_0>: state preparation
    qml.RY(np.pi / 4, wires=0)
    qml.RY(np.pi / 3, wires=1)
    qml.RY(np.pi / 7, wires=2)

    # V0(theta0, theta1): Parametrized layer 0
    qml.RZ(params[0], wires=0)
    qml.RZ(params[1], wires=1)

    # W1: non-parametrized gates
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])

    # V_1(theta2, theta3): Parametrized layer 1
    qml.RY(params[2], wires=1)
    qml.RX(params[3], wires=2)

    # W2: non-parametrized gates
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])

    return qml.expval(qml.PauliY(0))

qlayer = qml.qnn.TorchLayer(circuit, {"params": 4})

def loss_func(theta):
    loss = qlayer(theta)
    return loss

params = np.array([0.5, -0.123, 0.543, 0.233])
qlayer.params.data = torch.tensor(params)
optimQNG = QuantumNaturalGradientOptim([qlayer.params], circuit, lr=0.1)
for i in range(100):
    loss = loss_func(qlayer.params)
    print(loss)
    loss.backward()
    optimQNG.step()
    optimQNG.zero_grad()