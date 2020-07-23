.
# Problem
​
  The purpose is to minimize the disparity of water allocation per unit of economic benefit in each sub-area (until now economic benefit is unchanged among different sub-areas and different crop types). In this way, the user can control how much initial water has to be allocated among sub-areas to achieve economical water using.
​
# Method
​
  The objective function is the function that depicts how water allocation equity among different sub-areas. When the value of this objective function is 0, meaning that there is the same water allocation per unit of economic benefit among different sub-areas, otherwise, when this objective function's value is greater than 0 means that one sub-area need to be allocated much more water than other sub-areas to get economic benefits.
​
  Using a hybrid approach of a quantum computer and classical computer to handle linear constraints, continuous variables, binary variables. We solved the water allocation optimization problem in two ways: the first is using QAOA in Qiskit, the second way is solving the problem on Gurobi combined with D-Wave QPU. 
​
  - QAOA: Grover + Colyba: Waiting for final results
​
  - Gurobi + D-Wave QPU: First of all, the original problem is divided into two sub-problems, each sub-problem will be handled on each computer separately. The first sub-problem run on classical computer with Gurobi MILP solver to get partial solutions, then, these partial solutions are used in form of QUBO formulation that is run on D-Wave QPU to check whether a feasible solution or not.
​
# Requirements
​
  - Install Gurobi>8.0
​
  - Install D-Wave Ocean Leap SDK 2.0
​
  - Install Qiskit>0.18
​
# Result
​
  - QAOA
  - Gurobi+D-Wave QPU: get the value of objective function greater than 0, which means that there is one sub-area that need to have more water than other sub-areas.
​
# Future plan
​
  - Find ways to not to use Gurobi.
  - Get information about which sub-area needs to be allocated much more water.
