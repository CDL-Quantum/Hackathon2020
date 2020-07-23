# Quantum Annealing for Clustering Malicious Software

## Team <A|B>
### Members
* Nick Allgood
* Ajinkya Borle

### Systems and Datasets 

* D-Wave Hybrid Solver
* Endgame Malware BEnchmark for Research (EMBER) 2018 dataset - https://github.com/endgameinc/ember

## Purpose

Clustering malicious software is a very useful and researched topic in the field of malware analysis. Malware clusters are used by malware analysis and cybersecurity experts to find closely related patterns in malicious executables, most noteably PE executable information inside of Windows binaries. Having the ability to cluster allows a malware analyst to easily and quickly identify samples of malicious software that belong to a certain family so they can proceed to write signatures against this data for use in antivirus and antimalware software packages. Malware signatrues are often only written after new malware is detected, as such clustering is also very useful now that machine learning techniques are being applied for both static and dynamic analysis.

## Process

We use the EMBER data set and do a traditional DBSCAN to form a baseline clustering of data classically. We then formulate the data into an Ising hamiltonian and run it through a classical TABU solver to ensure we are on the right path. Once verified, we continue to run the same hamiltonian on the D-Wave hybrid solver.

## Results

### Binary Clustering Random Data

![Alt text](img.jpg?raw=true "Title")

### Binary Clustering 1 pass Ising formulation

![Alt text](img.jpg?raw=true "Title")

### Binary clustering 2 pass Ising formulation

![Alt text](3.jpg?raw=true "Title")

### D-Wave Hybrid Solver 


