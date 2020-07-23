![CDL Hackaton](img/CDL_logo.png)

## Tackling the IBM Challenge
Our team has tackled the IBM Challenge to classify a large existing dataset of galaxy images using Quantum Machine Learning techniques. Quantum Image Processing(QIMP) is an emerging field in Quantum Information Processing and is set to provide speedup over its classical counterparts [[1]](https://arxiv.org/abs/1801.01465) The datasets are ever-increasing and with limited classical computational resources, it becomes important to explore methods to tackle this challenge.



## Why is it a Challenge 
### Classification of large data requires large computational resources !
The data we want to process is usually made of millions of images issued from high resolution telescopes. This means that the processing of this data induces the ability to store huge amount of data, which is something that can not be ensured using classical computation.
By processing we may talk about classification, clustering, feature recognition, which can all be gathered into the notion of image processing.

For the problem considered here specifically, we focus on a classification problem, which is a branch of supervised learning.



## The Solution we propose
Quantum computing can be useful in its ability to process huge amounts of data provided the ability to perform an efficient mapping of the classical data on quantum bits.

In following steps, we describe the general workflow we employ to tackle the challenge. 

### 1.Getting the data, defining the objective and preprocessing the data using R.
We obtain a numerical dataset that encodes thousands of galaxy images from the [Galaxy Zoo](https://data.galaxyzoo.org/).We use R for the data manipulation. The dataset we used was extracted from the paper [here](https://www.researchgate.net/publication/280534264_Classifying_Galaxy_Images_through_Support_Vector_Machines). The images are brought down to a series of arrays characterizing the colors and intensities of each pixel.
Data compression is used using several methods in order to get data size pluggable onto a quantum computer.

We clean everything up in order to remain with the first two categories of task 1. Our purpose was to use the features according to those categories to classify each galaxy as “smooth” or “features or disk”. 

The techniques used here were filtering, projection and merging using the tidyverse packages in R. The idea could work for any other category of the original dataset and for any different task. The data manipulation is shown in [data_manipulation.ipynb](https://github.com/olgOk/Hackathon2020/blob/master/TBD/data_manipulation.ipynb).


### 2.Normalization and dimensionality reduction (using PCA) 
The methods we decide to implement to deal with those images are Quantum SVM, and Variational Quantum Classifier.
To perform those tasks, we first need to adapt the input to yield a tractable problem for a current machine (or qasm-simulator in our case).
Since the IBMQ allows to do current SVM over 2 or 3 features, we perform a Principal Component Analysis on the preprocessed data to yield the principal components and keep only the most relevant ones. (We go from a 37 features to extract only 2 main features).

Having the dataset preprocessed we used sklearn package to normalize the data using the MinMAxScaler and PCA to reduce the dimensionality of the inputs. We remain with the main two PCA components which were fed to the quantum subroutines. 

### 3.Applying the classical algorithm Support Vector Machine(SVM) and quantum algorithms Quantum Support Vector Machines(QSVM), Variational Quantum Classifier(VQC)
The **Support Vector Machine(SVM)** is a common algorithm used in supervised learning process. Given  labeled training data, it outputs an optimal hyperplane which is able to categorize new examples. It can be generalized to nonlinear hyper-surfaces via kernel methods allowing it perform even in higher dimensions[[2]](https://www.springer.com/gp/book/9780387987804). However, if the dimensions in which data points are projected, it becomes difficult for classical computers to compute through large computations. The quantum counterpart of the SVM- the **Quantum Support Vector Machines(QSVM)**[[3]](https://medium.com/@aliceliu2004/quantum-support-vector-machines-a-new-era-of-ai-1262dd4b2c7e) takes the classical machine learning algorithm and performs the support vector machine on a quantum circuit in order to be efficiently processed on a quantum computer. QSVM is shown to provide an exponential speedup *O(log N)* relative to its classical counterpart.
The figure below shows comparison of resource costs of classical and quantum image processing for an image of N (i.e., n = log2 N) pixel.

![CDL Hackaton](img/qsvm.PNG)

Similarly, we use another quantum algorithm for classification- the **Variational Quantum Classifier**. Similar to QSVM, the VQC algorithm also applies to classification problems. VQC uses the variational method to solve such problems in a quantum processor. Specifically, it optimizes a parameterized quantum circuit to provide a solution that cleanly separates the data.

We apply these three algoriothms to obtain the classification of forementioned dataset and compare the results.

To run the quantum subroutines on the backend, we need to implement following steps:

-Amplitude encoding of the provided input

-Creation of qubit registers necessary to perform training and testing operations

-Sampling and post processing of the data to obtain results of classification

The code for 3 algorithms are shown in [SVM.ipynb](https://github.com/olgOk/Hackathon2020/blob/master/TBD/SVM.ipynb), [qSVM.ipynb](https://github.com/olgOk/Hackathon2020/blob/master/TBD/qSVM.ipynb), [VQC.ipynb](https://github.com/olgOk/Hackathon2020/blob/master/TBD/VQC.ipynb) respectively.




## Analysis of the solution
The comparison for various parameters like time, accuracy for the three algorithms has been shown in [plots.ipynb](https://github.com/olgOk/Hackathon2020/blob/master/TBD/plots.ipynb).

## Potential business applications
The solution we provide addresses an important problem of lack of computational capabilities. We explore the importance of Quantum Machine Learning techniques in the context of Quantum Image Processing and extend its potential applications to several other fields like space exploration, nanotechnology, material design, medical research etc. 


An extensive document detailing potential applications can be found [here](https://github.com/olgOk/Hackathon2020/blob/master/TBD/BusinessCases.md).





## Future work and possibilities  for improvement of results
### Pre-processing the data using quantum sub-routines
We consider the possibility of Use more quantum subroutines for the preprocessing of the data ([Quantum PCA](https://arxiv.org/abs/1307.0401) on the raw images themselves, use of D-Wave annealer to proceed with [feature selection](https://github.com/olgOk/Hackathon2020/blob/master/TBD/feature_selection.ipynb)). 
### Analysis of the circuit optimization for the VQC to look for better performance and faster results
Optimize circuit depth for VQC.





