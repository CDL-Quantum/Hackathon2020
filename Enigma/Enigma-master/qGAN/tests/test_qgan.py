import unittest
from qGAN.qGAN import qGAN, train_qGAN
import numpy as np


class testqGAN(unittest.TestCase):

    def test_time_to_adj(self):
        to = np.array([[0,1,0,0],
                       [1, 0, 0, 0],
                       [0,0,0,1],
                       [0,0,1,0]])
        # array([1, 0, 3, 2])
        truth = np.array([[0,0,0,1],
                         [1,0,0,0],
                         [0,0,0,0],
                         [0,0,1,0]])
        test = qGAN.time_ordered_to_adjacency(to)
        np.testing.assert_array_equal(test, truth)

    def test_with_one_mat(self):
        adj_mat = np.array([[0, 5], [1, 2]])
        x_samples = [np.array([[0,1], [0,0]]), np.array([[0,1], [0,0]])]
        train_qGAN(adj_mat, x_samples, 5, gen_dev='qiskit.aer', disc_dev='qiskit.aer')


if __name__ == '__main__':
    unittest.main()
