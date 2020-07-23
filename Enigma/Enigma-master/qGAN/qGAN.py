import tensorflow as tf
import pennylane as qml
import numpy as np
import os

from typing import Union, List, Tuple


class qGAN:

    def __init__(self, n_qubits, gen_dev: str = 'default.qubit.tf',  disc_dev: str = 'default.qubit.tf'):
        self.n_qubits = n_qubits
        try:
            self.gen_dev = qml.device(gen_dev, wires=n_qubits)
            self.disc_dev = qml.device(disc_dev, wires=n_qubits)
        except TypeError:
            self.gen_dev = qml.device(gen_dev, wires=n_qubits, cutoff_dim=2)
            self.disc_dev = qml.device(disc_dev, wires=n_qubits, cutoff_dim=2)
        if 'GaussianState' not in self.gen_dev.operations:
            self.create_real, self.generator, self.discriminator = self.create_real_qubit, self.generator_qubit, \
                                                               self.discriminator_qubit
            self.qubit = True
        else:
            self.create_real, self.generator, self.discriminator = self.create_real_qmode, self.generator_qmode,\
                                                                   self.discriminator_qmode
            self.qubit = False


    @staticmethod
    def tsp_cost(adjacency_matrix: np.ndarray, solution_vector: np.ndarray):
        order = np.where(solution_vector == 1)
        norm = np.sum(adjacency_matrix)
        adjacency_matrix = adjacency_matrix / norm
        last = order[0]
        cost = 0
        for next_node in order:
            cost += adjacency_matrix[next_node, last]
            last = next_node
        return cost

    @staticmethod
    def iSWAP(weight: Tuple[float], wires=List[int]):
        c = wires[0]
        t = wires[1]
        rot = weight
        qml.CNOT(wires=[c, t])
        qml.Hadamard(wires=c)
        qml.CNOT(wires=[t, c])
        qml.RZ(rot / 2, wires=c)
        qml.CNOT(wires=[t, c])
        qml.RZ(-rot / 2, wires=c)
        qml.Hadamard(wires=c)
        qml.CNOT(wires=[c, t])

    @staticmethod
    def time_ordered_to_adjacency(time_ordered: Union[np.ndarray, List[int]]):
        """
        Takes a matrix which is defined where each row describes a city and each column a time step, and turns these
        into a directed adjacency matrix - i.e. the row describes the starting node and the column the end node.
        :param time_ordered: A matrix or vector describing the solution to a TSP problem.
        :return: adjacency_matrix: An adjacency matrix of the same
        """
        time_ordered = np.array(time_ordered)
        if len(time_ordered.shape) == 1:
            n = int(np.sqrt(time_ordered.shape[0]))
            # It's a flattened vector, we must convert to a matrix first
            time_ordered = time_ordered.reshape((n, n))
        else:
            n = time_ordered.shape[0]
        order = np.where(time_ordered == 1)[1]
        adjacency = np.zeros((n, n))
        last = None
        for i, index in enumerate(order):
            if i == 0:
                pass
            else:
                adjacency[last, index] = 1
            last = index
        return adjacency

    def create_real_qubit(self, adjacency_matrix: np.ndarray):
        if np.sum(adjacency_matrix.shape) > self.n_qubits:
            raise ValueError('The adjacency matrix provided is too large')
        adj_vec = np.reshape(adjacency_matrix, self.n_qubits)
        for i, connection in enumerate(adj_vec):
            if connection:
                qml.RX((np.pi), wires=i)

    def create_real_qmode(self, adjacency_matrix: np.ndarray):
        if np.sum(adjacency_matrix.shape) > self.n_qubits:
            raise ValueError('The adjacency matrix provided is too large')
        adj_vec = np.reshape(adjacency_matrix, self.n_qubits)
        for i, connection in enumerate(adj_vec):
            if connection:
                qml.FockState(1, wires=i)

    def generator_qubit(self, weights: List[Tuple[float]], **kwargs):
        qb_list = list(range(self.n_qubits))
        for i, l in enumerate(range(int(self.n_qubits / 2), 0, -1)):
            entanglers = qb_list[l:l-i]
            for i, (control, target) in enumerate(zip(entanglers[::-1], entanglers[::-1][1:])):
                #qml.CNOT(wires=[control, target])
                qGAN.iSWAP(weights[self.n_qubits + i], wires=[control, target])
        for qb in range(self.n_qubits):
            qml.RY(weights[qb], wires=qb)

    def generator_qmode(self, weights: List[Tuple[float]], **kwargs):
        qb_list = list(range(self.n_qubits))
        for i, l in enumerate(range(int(self.n_qubits / 2), 0, -1)):
            entanglers = qb_list[l:l-i]
            for i, (control, target) in enumerate(zip(entanglers[::-1], entanglers[::-1][1:])):
                qml.ControlledAddition(weights[self.n_qubits + i], wires=[control, target])
        for qb in range(self.n_qubits):
            qml.SqueezedState(weights[qb], weights[qb + self.n_qubits], wires=qb)

    def discriminator_qubit(self, weights: List[Tuple[float]], **kwargs):
        for qb in range(self.n_qubits):
            qml.RZ(weights[qb], wires=qb)
            qml.RX(weights[qb + self.n_qubits], wires=qb)
        qb_list = list(range(self.n_qubits))
        for i, (control, target) in enumerate(zip(qb_list[::-1], qb_list[::-1][1:])):
            qGAN.iSWAP(weights[2 * self.n_qubits + i], wires=[control, target])

    def discriminator_qmode(self, weights: List[Tuple[float]], **kwargs):
        for qb in range(self.n_qubits):
            qml.SqueezedState(weights[qb], weights[self.n_qubits + qb], wires=qb)
        qb_list = list(range(self.n_qubits))
        for i, (control, target) in enumerate(zip(qb_list[::-1], qb_list[::-1][1:])):
            qml.ControlledAddition(weights[2* self.n_qubits + i], wires=[control, target])


def train_qGAN(adjacency_matrix: np.ndarray, x_samples: List[np.ndarray], epochs: int = 15, lr: float = 0.02,
               gen_dev: str = 'qiskit.aer', disc_dev: str = 'qiskit.aer'):
    """
    Given an adjacency matrix and some sampled solved problems, this function will build the correct size qGAN and
     train it to attempt to generate novel data.
    :param adjacency_matrix: The matrix which defines the whole problem, the cost of travelling from node to node
    :param x_samples: Samples of solved TSP instances, in the form of binary directed adjacency matrices
    :param epochs: Number of epochs to train for
    :param lr: Learning rate of the gradient descent optimiser
    :return:
    """
    n_cities = adjacency_matrix.shape[1]
    n_qubits = adjacency_matrix.shape[1] ** 2
    qgan = qGAN(n_qubits, gen_dev, disc_dev)
    observable = qml.PauliZ if qgan.qubit else qml.NumberOperator

    @qml.qnode(qgan.disc_dev, interface='tf')
    def real_disc_circuits(adjaceny_matrix: np.ndarray, disc_weights):
        """Builds the discrimination circuits when given real data.
        Probability of the data being real is given by measurement of first qubit"""
        qgan.create_real(adjacency_matrix=adjaceny_matrix)
        qgan.discriminator(disc_weights)
        return qml.expval(observable(0))

    @qml.qnode(qgan.gen_dev, interface='tf')
    def gen_disc_circuits(gen_weights, disc_weights):
        """Builds the discrimination circuit with generated data."""
        qgan.generator(gen_weights)
        qgan.discriminator(disc_weights)
        return qml.expval(observable(0))

    @qml.qnode(qgan.gen_dev, interface='tf', shots=1)
    def generate_sample(gen_weights):
        """Just samples from the generated circuit"""
        qgan.generator(gen_weights)
        return [qml.expval(observable(x)) for x in range(n_qubits)]

    def real_true(sample_solution, disc_weights):
        """Probability of measuring true when given real data"""
        disc_output = real_disc_circuits(sample_solution, disc_weights)
        return (disc_output + 1) / 2

    def fake_true(gen_weights, disc_weights):
        """Probability of measuring True when given fake data"""
        disc_output = gen_disc_circuits(gen_weights, disc_weights)
        return (disc_output + 1) / 2

    def disc_cost(sample_solution, gen_weights, disc_weight):
        """Cost function for the discriminator. P(M(1)|fake) - P(M(1)|true)"""
        cost = fake_true(gen_weights, disc_weight) - real_true(sample_solution, disc_weight)
        return cost

    def gen_cost(gen_weight, disc_weight):
        """Cost function from the generator - probability of 'tricking' the discriminator"""
        return - fake_true(gen_weight, disc_weight)

    def gen_hamming_one(gen_z_meas):
        """As the adjacency matrix must be of a certain form we can impose these constraints here.
        They are:  that the diagonal contains only zeros, and that each node is visited only once.
        We impose these by measuring all qubits in the Z basis and weighting against a Hamming weight =/= 1 for each
        row and column, and for weighting against all |1> measurements in the diagonal qubts"""
        to_0_1 = tf.divide(tf.add(gen_z_meas, 1), 2)
        indices = np.arange(n_qubits).reshape((n_cities, n_cities))
        cost = 0
        for i in range(n_cities):
            weight_c = tf.reduce_sum(tf.gather(to_0_1, indices[:, i]))
            weight_r = tf.reduce_sum(tf.gather(to_0_1, indices[i, :]))
            weight_diag = tf.reduce_sum(tf.gather(to_0_1, indices[i, i]))
            cost += 0.001 * tf.abs(tf.subtract(1, weight_c))
            cost += 0.001 * tf.abs(tf.subtract(1, weight_r))
            cost += weight_diag
        # weight_total = tf.abs(tf.subtract(n_cities - 1, tf.reduce_sum(to_0_1)))
        # cost += weight_total
        return cost

    def tsp_cost(sample_solution):
        return qGAN.tsp_cost(adjacency_matrix, sample_solution)

    def train_disc_step(x, gen_weights, disc_weights, optimiser):
        with tf.GradientTape() as tape:
            disc_loss = disc_cost(x, gen_weights, disc_weights)
        grads = tape.gradient(disc_loss, [disc_weights])
        optimiser.apply_gradients(zip(grads, [disc_weights]))
        return disc_loss

    def train_gen_step(x, gen_weights, disc_weights, optimiser):
        with tf.GradientTape() as tape:
            gen_loss = gen_cost(gen_weights, disc_weights)
            gen_z = generate_sample(gen_weights)
            gen_pen = gen_hamming_one(gen_z)
            gen_loss += gen_pen
        grads = tape.gradient(gen_loss, [gen_weights])
        optimiser.apply_gradients(zip(grads, [gen_weights]))
        return gen_loss

    def sample(n_samples, gen_weights):
        samples = []
        for _ in range(n_samples):
            s = generate_sample(gen_weights)
            samples.append(s)
            print('Sampled output: {}'.format(s))
        return samples

    def training(x_train):
        init_gen = np.random.normal(size=(2* n_qubits, ))
        init_disc = np.random.normal(size=((3 * n_qubits) - 1, ))
        gen_weights = tf.Variable(init_gen)
        disc_weights = tf.Variable(init_disc)

        checkpoint_dir = './qgan_checkpoints/'
        chkpt_prefix = os.path.join(checkpoint_dir, 'qubit_{}_ckpt'.format(qgan.qubit))

        optimiser = tf.optimizers.SGD(lr)
        chkpt = tf.train.Checkpoint(optimizer=optimiser, disc_weights=disc_weights,
                                    gen_weights=gen_weights)
        for e in range(epochs):
            for x in x_train:
                disc_loss = train_disc_step(x, gen_weights, disc_weights, optimiser)
                gen_loss = train_gen_step(x, gen_weights, disc_weights, optimiser)
            if not e % 5:
                print('Gen cost: {}\nDisc cost: {}'.format(gen_loss, disc_loss))
                sample = (np.round(generate_sample(gen_weights)).reshape((n_cities, n_cities)) + 1) / 2
                print('Generated sample:\n{}'.format(np.round(sample)))
                chkpt.save(file_prefix=chkpt_prefix)
        return gen_weights, disc_weights

    gen_weights, _ = training(x_samples)
    samples = sample(10, gen_weights)
    return samples
