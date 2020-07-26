We have provided a brief explanation of the TSP Algorithm used for the food bank solution below :

## Mapping Traveling Salesman Problem into QUBO (Quadratic Unconstrained Binary Optimization)
In order to find approximately optimal solutions of Traveling Salesman Problem we map the problem into QUBO model.  
A route is represented as a matrix. For example:

<pre>
Visit Order / City  A B C D  
1                   1 0 0 0  
2                   0 0 0 1  
3                   0 1 0 0  
4                   0 0 1 0  
</pre>

There are 4 cities in this example: A, B, C, D. This matrix represents a route where city A is visited first, then D, then B and then C. Optionally, salesman returns to city A at the end. The row number represents the order of a city in a travel route. To make this route valid only one `1` should be allowed in every row and column.

In our case annealing process can be thought as a process that assignes binary values `0` or `1` to the matrix entries in order to find an approximately optimal Traveling Salesman route. Annealing process is going to try all possible routes, thus trying all kind of combinations of `0` and `1` in the matrix.
Without constraints, most paths will not be valid. For example,
<pre>
Visit Order / City  A B C D  
1                   0 1 0 0  
2                   0 1 0 0  
3                   0 0 0 1  
4                   0 1 0 0  
</pre>
is not a valid path, because city B is visited 3 times. Every city must be visited exactly once.
Also, 
<pre>
Visit Order / City  A B C D  
1                   1 1 1 0  
2                   0 0 0 0  
3                   0 0 0 1  
4                   0 0 0 0  
</pre>
is not a valid path, because cities A, B and C are all visited in step one. Only one city can be visited in a single step.

In order to make annealing process to only consider valid paths we are going to apply constraints to our function.

The first constraint is to make every city appear exactly once in a route:
<pre>
A Σ<sub>city</sub>(1 - Σ<sub>step</sub>(x<sub>city,step</sub>))
</pre>
Here **A** is some constant, the first sum runs across columns in the matrix above (ensuring every city gets this constraint applied to it), the second sum runs accross all binary values in a given column (ensuring every city is visited exactly once). Minimum of this function occurres when every city gets included exactly once into a route.

The second constraint is to make exactly one city to be visited in one step of the route:
<pre>
A Σ<sub>step</sub>(1 - Σ<sub>city</sub>(x<sub>city,step</sub>))
</pre>
Here **A** is the same constant as above, the first sum runs across rows in the matrix above (ensuring every step gets this constraint applied to), the second sum runs accross all binary values in a given row (ensuring exactly one city is visited in a given step). Minimum of this function occurres when every step involves visiting exactly one city.

To this point we can generate all valid paths. Now we need to minimize sum of weights of nodes (distances between cities) on possible valid paths. To do that we add this term to our function:
<pre>
B Σ<sub>city_u,city_v</sub>(W<sub>city_u,city_v</sub> Σ<sub>step</sub>(x<sub>city_u,step</sub>x<sub>city_v,step+1</sub>))
</pre>
Here **W<sub>u,v</sub>** is the length between two cities (weight of an edge). **B** must be small enough to ensure path being valid is more important than path being optimal:
<pre>
0 < B max(W<sub>u,v</sub>) < A
</pre>
