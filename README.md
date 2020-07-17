# CDL Quantum Hackathon 2020

# Description

The quantum hackathon will be a competition in which teams of the CDL Quantum program participants intensively develop a quantum software project or application over the course of 24 hours. Participants will utilize one of the quantum platforms provided by CDL’s Technical Partners to produce a set of code that implements a quantum algorithm for a chosen application.

The problem a team decides to tackle will be up to the team. To facilitate problem identification, technical partners will present relevant problems (challenges) which we hope will provide inspiration and insight when the teams are deciding what to work on.  

# Purpose

The hackathon has four objectives:
Synthesis and consolidation of knowledge. Participants will have a chance to put what they have learned into practice and contextualize them within a coding environment.
Team dynamics testing. The hackathon will be a first opportunity for co-founders to work directly with their peers and verify whether or not they work well within a given team.
Test business ideas. We hope that many co-founders will take the hackathon as a chance to test out their business ideas and get some early validation.
Opportunities for corporate partners and early pilots. The hackathon represents an excellent engagement opportunity for our corporate partners interested in getting in on the ground floor of quantum computing.

# Format

Prior to the start of the hackathon, participants will have formed teams of 2-4 people, and will have been provided with a list of example projects which they may choose from if they wish.

The hackathon will begin with a presentation introducing the event, and setting rules and expectations. At 10am on Wednesday, July 22th the teams will begin working on their code and be free to do so until 10am on Thursday, July 23th. At this time we will implement a code freeze, meaning that teams will need to upload their code to a repository under MIT License, and we will not accept projects after the deadline.

After lunch and a break, the teams will give short presentations on their projects, which will be judged by a panel (composition to be decided). 

# Team Deliverables and Judging

The teams should strive to create the most complete and streamlined version of their project as is possible within the time allocated. Their performance will be judged on the following primary criteria:
Technical difficulty
Creativity and originality
Usefulness and business potential
Presentation quality

# Location: 

The event will take place online. You will be responsible for coordinating meetings and video conferences for your team during the coding component. We recommend that you stay in regular contact throughout the hackathon to support group dynamics in a virtual setting. Presentations will be made using a cohort-wide zoom call.

# Partners 

Participants may use any of the quantum platforms provided by the following technical partners:
D-Wave
Xanadu
IBM Q
Zapata Computing

Each partner will have dedicated staff member(s) available on slack or via zoom to support you during the project. Given the variety of timezones we will be operating in, please acknowledge that the technical support will not be available for the entire duration of the coding component of the hackathon.

# Prizes

Prizes will be given for 1st, 2nd, and 3rd place, as well as for the choice team from each of the four technical partners. All values in CAD:
1st - $5000
2nd - $2000
3rd - $1000
Partner choices - $1000 each

# Schedule

The bulk of the time will be spent by the co-founders working on their application.

Wednesday, July 22: 
09:00 - 10:00 | Rules and Expectations
10:00 - Open End | Hackathon!!

Thursday, July 23: 
Open Start - 10:00 | Hackathon!!
10:00 	| Coding Freeze
10:00 - 10:30 | Break
10:30 - 12:30 |Group Presentations
12:30 - 13:15 | Break
13:15 - 14:30 | Winner Announcements and Awards

# Challenges

The following problems were provided by our technical partners. Teams can choose to work on one of the problems or an appropriate generalization thereof. 

D-Wave Challenge:

TBD

Hackathon Contact: Alexander Condello

Xanadu Challenge(s):

Hardware Challenge: Find a set of weighted bipartite graphs that can be encoded into Xanadu’s X8 chip. Assign labels to each, encode them into the device, and use the generated samples to create feature vectors. Finally, use classical machine learning tools to classify the graphs using their feature vector representation.

Machine Learning Challenge: 
Strawberry Fields: Implement an algorithm for graph optimization and improve the performance of the algorithm by training the corresponding variational GBS distribution.
PennyLane: Implement a QGAN and run it on two separate quantum computing backends, using one platform as a generator and the other as a discriminator.
Software Challenges:
The following two hackathon challenges could lead to a pull request to the PennyLane repository:
Provide functionality to convert a PennyLane QNode into a scikit-learn Estimator, giving access to the usual scikit-learn API including fit() and predict() methods.
PennyLane contains the quantum-aware optimizers Rotosolve, QNG, and Rosalin. Rewrite them as PyTorch or TensorFlow native optimizers and provide a tutorial showing how they can be used to train a quantum model.

Heroic Challenge: This is a very tough one, but could lead to an excellent tutorial or even a research paper. The input parameters to the quantum algorithm for vibronic spectra require electronic structure calculations that can also be performed using VQE on a quantum computer. Implement an end-to-end quantum algorithm for vibronic spectra by using a quantum computer to obtain the Doktorov operator for the vibronic transition and encode it into a GBS device to obtain the vibronic spectrum of a molecule. 

Hackathon Contact:

Zapata Computing Challenge:

Working with Variational Quantum Algorithms (VQA) often means trying a lot of different ideas and benchmarking them against each other. In this challenge we would like you to integrate/implement some elements of VQA – optimizer, ansatz, measurement strategy, etc. – into Orquestra and benchmark it using other existing methods.
 
Example of a project could be to use QAOA to solve Maximum Independent Set problem. You could implement the Model Gradient Descent optimizer (described here: https://arxiv.org/abs/2004.04197, appendix D) and compare it to optimizers such as Nelder-Mead, L-BFGS-B and SPSA (all available in Orquestra), using standard cost function as well as CVaR (described here: https://arxiv.org/abs/1907.04769).

IBM Q Challenge:

TBD
