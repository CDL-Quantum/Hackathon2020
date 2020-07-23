import pennylane as qml
from quantum_aware_optims import *
import torch

n_wires = 2

dev = qml.device("default.qubit", analytic=True, wires=2)

def ansatz(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])


@qml.qnode(dev)
def circuit(params):
    ansatz(params)
    return qml.expval(qml.PauliZ(0)), qml.expval(qml.PauliY(1))


@qml.qnode(dev)
def circuit2(params):
    ansatz(params)
    return qml.expval(qml.PauliX(0))

qcircuits = [circuit, circuit2]
proportions = torch.Tensor([0.5, 0.8, -0.2])
init_params = torch.Tensor([0.3, 0.25])
optim = RotoSolve(init_params,qcircuits,proportions)
for n in range(100):
    loss = optim.step()
    print(loss)