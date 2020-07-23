# Problem

  The purpose is to minimize the disparity of water allocation per unit of economic benefit in each sub-area. (Until now, economic benefit is unchanged across different sub-areas and different crop types). In this way, the user can control how much water has to be initially allocated across sub-areas in order to achieve economical water use.

# Method

  The objective function is the function that depicts the water allocation equity across different sub-areas. When the value of this objective function is 0, this means that there is the same water allocation per unit of economic benefit across these sub-areas, otherwise, when this objective function's value is greater than 0, this means that one sub-area needs to be allocated much more water than other sub-areas to have an economic benefit.

  Using a hybrid approach of a quantum computer and classical computer to handle linear constraints, continuous variables, and binary variables, we solved the water allocation optimization problem in two ways: the first is using QAOA in Qiskit, the second way is solving the problem on Gurobi combined with D-Wave QPU. 

  - QAOA: Grover + Colyba: Waiting for final results

  - Gurobi + D-Wave QPU: First of all, the original problem is divided into two sub-problems. Each sub-problem will be handled on each computer separately. The first sub-problem runs on a classical computer with Gurobi MILP solver to get partial solutions, then these partial solutions are used in QUBO formulation that is run on D-Wave QPU to check whether it is a feasible solution or not.

# Requirements

  - Install Gurobi>8.0

  - Install D-Wave Ocean Leap SDK 2.0

  - Install Qiskit>0.18

# Result

  - Colyba + QAOA
  - Gurobi+D-Wave QPU: Able to get optimal water allocation solution for sub-areas in different time. Still need to be benchmarked.

# Future plan

  - Find ways not to use Gurobi.
  - Get information about which sub-area needs to be allocated more water.
  - Add in many more variables that will take advantage of QC:
     - Multiple reservoirs in the same river system
     - Deeper layers of crops types and water utilization types
     - Additional IoT data at higher spatial and temporal resolution
 
