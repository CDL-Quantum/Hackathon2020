# This file contains the implementation of the FRQI algorithm in Qiskit

import qiskit as qk
from qiskit import Aer,execute
from math import pi, sqrt, acos
from utils import r_num, g_num, b_num

# this function takes the results for the measurements and returns the angles it finds
def probs(results, num_shots):

	prob = {}
	
	# create every possible basis vector and add the estimated prob of that vector being measured
	chars = ["0", "1"]
	for c in chars:
		for d in chars:
			for e in chars:
				state = c + d + e
				if (state in results):
					prob[state] = results[state]/num_shots
				else:
					prob[state] = 0.

	# using the probability of every pixel being 0, estimate the angle stored
	angles = []
	for c in chars:
		for d in chars:
			zero = "0" + c + d
			one = "1" + c + d
			zero_prob = prob[zero]/(prob[zero] + prob[one])
			# prob(|0>) = cos^2(theta), so to solve for theta need to do inverse
			angles.append(acos(sqrt(zero_prob)))
	
	return angles

# this function creates the FRQI state for the image
def run(angles, num_shots):

	qr = qk.QuantumRegister(3)
	cr = qk.ClassicalRegister(3)

	# create a circuit
	qc= qk.QuantumCircuit(qr,cr)

	#Creating the Hadamard State
	qc.h(qr[0])
	qc.h(qr[1])

	i = 0
	# for every angle, add to the circuit the encoding of that angle
	for ang in angles:

		# to make sure we are transforming the correct vector, need to NOT certain qubits
		qc.x(qr[0])

		if(i%2 == 0):
			qc.x(qr[1])

		# The C^2-Ry operation
		qc.cu3(ang,0,0,qr[0],qr[2])
		qc.cx(qr[0],qr[1])
		qc.cu3(-ang,0,0,qr[1],qr[2])
		qc.cx(qr[0],qr[1])
		qc.cu3(ang,0,0,qr[1],qr[2])

		i += 1

	qc.barrier(qr)
	qc.measure(qr,cr)

	# run the circuit
	backend_sim = Aer.get_backend('qasm_simulator')
	job_sim = execute(qc, backend_sim, shots=num_shots)
	result_sim = job_sim.result()

	# get the dictionary that contains number of times each outcome was measured
	counts = result_sim.get_counts(qc)

	new_angles = probs(counts, num_shots)

	return new_angles