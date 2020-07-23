![CDL Hackaton](img/CDL_logo.png)

## Tackling the IBM Challenge
Our team has tackled the IBM Challenge to classify a large existing dataset of galaxy images using Quantum Machine Learning techniques. Quantum Image Processing(QIMP) is an emerging field in Quantum Information Processing and is set to provide speedup over its classical counterparts [[1]](https://arxiv.org/abs/1801.01465) The datasets are ever-increasing and with limited classical computational resources, it becomes important to explore methods to tackle this challenge.



## Why was it a Challenge 
Classification of large data requires large computational resources !





## The Solution we propose
In following steps, we describe the general workflow we employ to tackle the challenge. 

### 1.Getting the data, defining the objective and preprocessing the data using R.
We obtain a numerical dataset that encodes thousands of galaxy images from the [Galaxy Zoo](https://data.galaxyzoo.org/).We use R for the data manipulation. The dataset we used was extracted from the paper [here](https://www.researchgate.net/publication/280534264_Classifying_Galaxy_Images_through_Support_Vector_Machines). We cleaned everything up in order to remain with the first two categories of task 1. Our purpose was to use the features according to those categories to classify each galaxy as “smooth” or “features or disk”. After the cleaning process was finished we got an 11 feature dataset from which one of them was the target. Then, we tackle a binary classification task.
The final dataset has 55k samples.

The techniques used here were filtering, projection and merging using the tidyverse packages in R. The idea could work for any other category of the original dataset and for any different task. The data manipulation is shown in [data_manipulation.ipynb](https://github.com/olgOk/Hackathon2020/blob/master/TBD/data_manipulation.ipynb).


### 2.Normalization and dimensionality reduction (using PCA)  
Having the dataset preprocessed we used sklearn package to normalize the data using the MinMAxScaler and PCA to reduce the dimensionality of the inputs. We remain with the main two PCA components which were fed to the quantum subroutines. 

### 3.Applying the classical algorithm Support Vector Machine(SVM) and quantum algorithms Quantum Support Vector Machines(QSVM), Variational Quantum Classifier(VQC)
The **Support Vector Machine(SVM)** is a common algorithm used in supervised learning process. Given  labeled training data, it outputs an optimal hyperplane which is able to categorize new examples. It can be generalized to nonlinear hyper-surfaces via kernel methods allowing it perform even in higher dimensions[[2]](https://www.springer.com/gp/book/9780387987804). However, if the dimensions in which data points are projected, it becomes difficult for classical computers to compute through large computations. The quantum counterpart of the SVM- the **Quantum Support Vector Machines(QSVM)**[[3]](https://medium.com/@aliceliu2004/quantum-support-vector-machines-a-new-era-of-ai-1262dd4b2c7e) takes the classical machine learning algorithm and performs the support vector machine on a quantum circuit in order to be efficiently processed on a quantum computer. QSVM is shown to provide an exponential speedup *O(log N)* relative to its classical counterpart.
The figure below shows comparison of resource costs of classical and quantum image processing for an image of N (i.e., n = log2 N) pixel.

![CDL Hackaton](img/qsvm.PNG)

Similarly, we use another quantum algorithm for classification- the **Variational Quantum Classifier**. Similar to QSVM, the VQC algorithm also applies to classification problems. VQC uses the variational method to solve such problems in a quantum processor. Specifically, it optimizes a parameterized quantum circuit to provide a solution that cleanly separates the data.

We apply these three algoriothms to obtain the classification of forementioned dataset and compare the results.
The code for 3 algorithms are shown in [SVM.ipynb](https://github.com/olgOk/Hackathon2020/blob/master/TBD/SVM.ipynb), [qSVM.ipynb](https://github.com/olgOk/Hackathon2020/blob/master/TBD/qSVM.ipynb), [VQC.ipynb](https://github.com/olgOk/Hackathon2020/blob/master/TBD/VQC.ipynb) respectively.




## Analysis of the solution

## Potential business applications
The solution we provide addresses an important problem of lack of computational capabilities. We explore the importance of Quantum Machine Learning techniques in the context of Quantum Image Processing and extend its potential applications to several other fields like space exploration, nanotechnology, material design, medical research etc. 


An extensive document detailing potential applications can be found [here](https://github.com/olgOk/Hackathon2020/blob/master/TBD/BusinessCases.md).





## Future work and possibilities 
### Pre-processing the data using QPCA
We consider the possibility of using Quantum Principal Component Analysis[(QPCA)](https://arxiv.org/abs/1307.0401) for pre-processing the data.
### Image processing using D-Wave Platform



