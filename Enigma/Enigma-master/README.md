# Enigma

### AirLine DataSets
Data sets from the Air line industry with respect to flight routes
![cap5](../figures/)

### Classical GAN
A Classical Generative Adversarial Network designed to output adjacency tables that correlate the flight paths. The model is trained on optimized outputs generated by the Dave machine.
### QGan
The QGAN takes as it's input a sparse matrix describing an adjacency matrix and a solution to the TSP problem as found by the DWave device.
It will then build two shallow quantum circuits. The first will present examples to the second, with the aim of tricking the second into labeling a generated matrix as a real one.
The second attempts to discriminate between generated matrices and real. Each are trained in parallel, and at the end of training we hope to have a generator which can generate good samples of solved TSP problems on our example graph.
The structure of the total circuit differs if the algorithm is to be ran on continuous variable (qumode) or discrete (qubit) systems. But the ability to train for either system is built in.

### Gaussian Boson Sampling
Gaussian Boson Sampling is employed in the continuous mode quantum computer from Xanadu. We use this platform's ability to sample from complex probability distributions to find dense sub-graphs within our total scheduling graph. This allows us to avoid these routes if possible, as the existence of a dense sub graph implies the existence of a congested route / area. This congestion increases operational risk.