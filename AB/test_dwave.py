#make sure D-wave API and config works
from dwave.system import EmbeddingComposite, DWaveSampler
from tabu import TabuSampler
# Define the problem as two Python dictionaries:
#   h for linear terms, J for quadratic terms
h = {}
J = {(0,1): 1,
    (1,2): 2,
    (0,2): 2.5}

# Define the sampler that will be used to run the problem
#sampler = EmbeddingComposite(DWaveSampler())
sampler = TabuSampler()
# Run the problem on the sampler and print the results
sampleset = sampler.sample_ising(h, J, num_reads = 10)
print(sampleset)

tree.create_node("Harry", "harry")  # root node
tree.create_node("Jane", "jane", parent="harry")
tree.create_node("Bill", "bill", parent="harry")
tree.create_node("Diane", "diane", parent="jane")
tree.create_node("Mary", "mary", parent="diane")
tree.create_node("Mark", "mark", parent="jane")
tree.show()
