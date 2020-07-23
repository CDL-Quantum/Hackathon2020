# CDL Hackathon 2020 QBC - Milan Leonard / Simon Yin 
----
## Chosen problem
Xanadu - PennyLane: 
>PennyLane contains the quantum-aware optimizers Rotosolve, QNG, and Rosalin. Rewrite them as PyTorch or TensorFlow native optimizers and provide a tutorial showing how they can be used to train a quantum model.

## Successfully implemented into pyTorch
1. Rotosolve optimizer. Relies heavily on Python built-ins and is *slow* because of it. However, since it is a non-gradient optimizer it cannot be put further in front of classical layers as gradients can't necessarily flow through it, so this is not a huge deal
2. Quantum Natural Gradient -- utilises the qml.qnn.TorchLayer to create the circuit's representation as a tensor (this is required since it currently accesses the Fubini Metric tensor using the built-in qml circuit one). Then, calculates and updates the gradient in a fully pytorch way


