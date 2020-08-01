![CDL Quantum Hackathon 2020](CDL_logo.jpg)
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

1) Technical difficulty

2) Creativity and originality

3) Usefulness and business potential

4) Presentation quality

# Location: 

The event will take place online. You will be responsible for coordinating meetings and video conferences for your team during the coding component. We recommend that you stay in regular contact throughout the hackathon to support group dynamics in a virtual setting. Presentations will be made using a cohort-wide zoom call.

# Partners 

Participants may use any of the quantum platforms provided by the following technical partners:

- D-Wave

- Xanadu

- IBM Q

- Zapata Computing

Each technology partner will have dedicated staff member(s) available on the respective partner's slack channel to support you during the project. Given the variety of timezones we will be operating in, please acknowledge that the technical support will not be available for the entire duration of the coding component of the hackathon.

# Prizes

Prizes will be given for 1st, 2nd, and 3rd place, as well as for the choice team from each of the four technical partners. All values in CAD:

1st - $5000

2nd - $2000

3rd - $1000

Partner choices - $1000 each

# Schedule

The bulk of the time will be spent by the co-founders working on their application.

## Wednesday, July 22: 

09:00 - 10:00 | Rules and Expectations

10:00 - Open End | Hackathon!!

## Thursday, July 23: 

Open Start - 10:00 | Hackathon!!

10:00 	| Coding Freeze

10:00 - 10:30 | Break

10:30 - 12:30 |Group Presentations

12:30 - 13:15 | Break

13:15 - 14:30 | Winner Announcements and Awards

# Challenges
The following problems were provided by our technical partners. Teams can choose to work on one of the problems or an appropriate generalization thereof.

## D-Wave’s Challenge:
Practical applications require domain knowledge and solutions that work at a real world scale. Hybrid development brings the power of quantum to the scale of classical. Users are challenged to select a practical problem and to solve it at scale with Leap's hybrid solver. As a hint, problems with graph structure like maximum independent set, structural imbalance and maximum cut can be translated to a binary quadratic model without additional variables. Check out https://cloud.dwavesys.com/leap/examples/ for ideas, but use your creativity! The best projects will be the ones that solve the most practical problems.

For support, use the D-Wave's slack channel: #d-wave_training

## Xanadu’s Challenge(s):

### Hardware Challenge
Find a set of weighted bipartite graphs that can be encoded into Xanadu’s X8 chip. Assign labels to each, encode them into the device, and use the generated samples to create feature vectors. Finally, use classical machine learning tools to classify the graphs using their feature vector representation.

### Machine Learning Challenge:
Strawberry Fields: Implement an algorithm for graph optimization and improve the performance of the algorithm by training the corresponding variational GBS distribution.
PennyLane: Implement a QGAN and run it on two separate quantum computing backends, using one platform as a generator and the other as a discriminator.

### Software Challenges:
The following two hackathon challenges could lead to a pull request to the PennyLane repository:
Provide functionality to convert a PennyLane QNode into a scikit-learn Estimator, giving access to the usual scikit-learn API including fit() and predict() methods.
PennyLane contains the quantum-aware optimizers Rotosolve, QNG, and Rosalin. Rewrite them as PyTorch or TensorFlow native optimizers and provide a tutorial showing how they can be used to train a quantum model.

### Heroic Challenge
This is a very tough one, but could lead to an excellent tutorial or even a research paper. The input parameters to the quantum algorithm for vibronic spectra require electronic structure calculations that can also be performed using VQE on a quantum computer. Implement an end-to-end quantum algorithm for vibronic spectra by using a quantum computer to obtain the Doktorov operator for the vibronic transition and encode it into a GBS device to obtain the vibronic spectrum of a molecule.

For support, use the Xanadu's slack channel: #xanadu_training

## Zapata Computing’s Challenge:
Working with Variational Quantum Algorithms (VQA) often means trying a lot of different ideas and benchmarking them against each other. In this challenge we would like you to integrate/implement some elements of VQA – optimizer, ansatz, measurement strategy, etc. – into Orquestra and benchmark it using other existing methods.
Example of a project could be to use QAOA to solve Maximum Independent Set problem. You could implement the Model Gradient Descent optimizer (described here: https://arxiv.org/abs/2004.04197, appendix D) and compare it to optimizers such as Nelder-Mead, L-BFGS-B and SPSA (all available in Orquestra), using standard cost function as well as CVaR (described here: https://arxiv.org/abs/1907.04769).

For support, use the Zapata's slack channel: #zapata-comuting_training

## IBM Q’s Challenge:
Morphological classification is key in our understanding of the large-scale structure of the universe. The use of Machine Learning for analyzing astrophysical datasets is on the rise [1] and it is expected next generation of instruments (LSST, SKA etc …) will generate bigger than ever datasets [2]
Quantum Image Processing (QIMP) is an emerging field of Quantum Information Processing and can provide speedup over their classical counterparts [3] and we have seen progress in the Quantum  Machine Learning field as well.

The challenge is as follow:
Using an existing dataset (for example [4] and one of the known image representation (FRQI [5] or NEQR [6] for example), apply Quantum machine learning algorithms for galaxy classification.
[1] https://arxiv.org/abs/1910.00774
[2] https://doi.org/10.1093/mnras/stz3006
[3] https://arxiv.org/abs/1801.01465
[4] https://data.galaxyzoo.org/
[5] https://pdfs.semanticscholar.org/0a3b/dfb66973144792533d763e9edaec40b2785b.pdf
[6] https://www.researchgate.net/publication/257641933_NEQR_A_novel_enhanced_quantum_representation_of_digital_images

# Winners of the 2020 CDL Quantum Hackathon
## Overall Winners:

### First Place: Q-Alpha
Submission: "Which cities to shut down" as a knapsack problem.

Directory: https://github.com/CDL-Quantum/Hackathon2020/tree/master/QAlpha

### Second Place: QBC
Submission: Successfully implementing into PyTorch:
1) Rotosolve optimizer. Relies heavily on Python built-ins and is slow because of it. However, since it is a non-gradient optimizer it cannot be put further in front of classical layers as gradients can't necessarily flow through it, so this is not a huge deal
2) Quantum Natural Gradient -- utilises the qml.qnn.TorchLayer to create the circuit's representation as a tensor (this is required since it currently accesses the Fubini Metric tensor using the built-in qml circuit one). Then, calculates and updates the gradient in a fully pytorch way

Directory: https://github.com/CDL-Quantum/Hackathon2020/tree/master/QBC

### Third Place: Quantum Hack
Submission: Complete construction of a QGAN using Xanadu's and IBM Q's infrastructure.

Directory: https://github.com/CDL-Quantum/Hackathon2020/tree/master/QuantumHack

## Technology Partner Challenge Winners:

### D-wave: Q-Alpha
Submission: "Which cities to shut down" as a knapsack problem.

Directory: https://github.com/CDL-Quantum/Hackathon2020/tree/master/QAlpha

### IBM Q: Physics in Stream
Submission: Quantum Image Processing (QIMP) to classify a large existing dataset of galaxy images using Quantum Machine Learning techniques.

Directory: https://github.com/CDL-Quantum/Hackathon2020/tree/master/TBD

### Xanadu: QBC
Submission: Submission: Successfully implementing into PyTorch:
1) Rotosolve optimizer. Relies heavily on Python built-ins and is slow because of it. However, since it is a non-gradient optimizer it cannot be put further in front of classical layers as gradients can't necessarily flow through it, so this is not a huge deal
2) Quantum Natural Gradient -- utilises the qml.qnn.TorchLayer to create the circuit's representation as a tensor (this is required since it currently accesses the Fubini Metric tensor using the built-in qml circuit one). Then, calculates and updates the gradient in a fully pytorch way

Directory: https://github.com/CDL-Quantum/Hackathon2020/tree/master/QBC
