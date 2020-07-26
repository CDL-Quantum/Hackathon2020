![IBM](ibm.png)
# [IBM Q](https://quantum-computing.ibm.com/)

# Quantum Representation of Digital Images Using NEQR

The Novel Enhanced Quantum Representation (NEQR) is an earlier form of quantum image representation. It uses a normalized superposition to store pixels in an image. NEQR was created to improve over Flexible Representation of Quantum Images (FRQI) by leveraging the basis state of a qubit sequence to store the image's grayscale value. NEQR offers the following advantages over FRQI as demonstrated in [[1](https://doi.org/10.1007/s11128-013-0567-z)]:

* Quadradic speedup of the time complexity to prepare the NEQR quantum image
* Optimal image compression ratio of up to 1.5×
* Accurate image retrieval after measurement, as opposed to probabilistic as FRQI
* Complex color and many other operations can be achieved

The NEQR process to represent an image is composed of two parts; preparation and compression and are described as follows. We will first create one quantum circuit for the pixel values, and the other for the pixel positions. 
To define the first circuit, we need to define the range of the grayscale intensity for each pixel, since the most common grayscale range is generally from 0-256, 8 qubits will be needed since 256 = 2^q. 
In our case we wanted to encode images of galaxies but due to the computational cost we reduced them to 8x8 grayscale images and consider this case as a toy model. That is the reason why our second quantum circuit will include the 6 qubits to represent the pixel positions since we will represent an 8x8 image with 64 positions and 2^6 = 64. So the final circuit will have 8+6=14 qubits to represent an 8x8 grayscale image.

We used the Galaxy Zoo dataset and encoded 100 images into qubits. This encoding turned out to be very inefficient, there were needed 3500 gates average and the resulting density matrix is always sparse. We analyzed the output of the quantum circuit, 2^14 = 16384 elements, and using PCA studied how much we could have compressed that state without losing information. The results showed that using approximately 70 elements is enough, this would mean ~6 qubits. This makes sense due to the fact that we have 8x8 images and 64 pixels of information. After, we did some comparison to show that the analysis with the 16384 elements is equivalent to the analysis with 70 elements.

## Possible business applications: 

The need to encode classic data in qubits is one of the main bottlenecks when designing quantum circuits. This method allows a simple encoding that maps images to qubits. While image processing is a field in which quantum computing could potentially have an enhancement over classical computers, this method would also allow mapping of any classical datasets to qubits, as long as we properly preprocess the data.

