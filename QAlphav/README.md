# Where to look if you are a judge

- `notebook.ipynb` is the main document which walks you through what we have done.
- `knapsack.py` is where all the D-Wave magic happens.

# Setup

1. Make sure you have the Ocean SDK installed and configured.

2. Set up your preferred virtual environment.

3. `pip install -r requirements.txt`

# How to use

## Knapsack solver

### From command line

Use `python solvers/knapsack.py -h` to get a description of the script and its options.

Here's an example for running the solver with the data in `data.csv` and a nationwide capacity of 500000 sick people at once.

```
python solvers/knapsack.py -d data.csv -t 500000
```

### From python code

Following on the example from above:

```
from solvers.knapsack import solve_cities_from_csv

solution_set = solve_cities_from_csv('data.csv', 500000)
```

See the docstrings in `solvers/knapsack.py` for specifications on the `solution_set` object.
