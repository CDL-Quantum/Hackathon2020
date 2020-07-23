from tabu import TabuSampler
from sklearn import cluster, datasets, mixture
import copy
import matplotlib.pyplot as plt


n_samples = 150
noisy_circles = datasets.make_circles(n_samples=n_samples, factor=.5,noise=.05)
print(noisy_circles)

fig, ax = plt.subplots()
ax.scatter(noisy_circles[0])

plt.xlim(-2.5, 2.5)
plt.ylim(-2.5, 2.5)
plt.xticks(())
plt.yticks(())

def bin_cluster(feature_vecs):
    return True
