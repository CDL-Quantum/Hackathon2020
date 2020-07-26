from pprint import pprint
from typing import List, Dict
from math import log, ceil
import argparse

import pandas as pd
from dwave.system import LeapHybridSampler
import dimod


def knapsack_bqm(cities, values, weights, total_capacity, value_r=0, weight_r=0):
    """
    build the knapsack binary quadratic model

    See # Q-Alpha comments for original contributions
    added parameters:
        value_r: the proportion of value contributed from the objects outside of
                the knapsack. For the standard knapsack problem this is 0,
                but in the case of GDP we might consider that a closed city
                retains some % of GDP
        weight_r: the proportion of weight contributed from the objects outside
                of the knapsack. For the standard knapsack problem this is 0,
                but in the case of sick people we might consider that a closed city
                retains some % of its sick people over time

    From DWave Knapsack examples
    Originally from Andrew Lucas, NP-hard combinatorial problems as Ising spin glasses
    Workshop on Classical and Quantum Optimization; ETH Zuerich - August 20, 2014
    based on Lucas, Frontiers in Physics _2, 5 (2014)    
    """

    # Initialize BQM - use large-capacity BQM so that the problem can be
    # scaled by the user.
    bqm = dimod.AdjVectorBQM(dimod.Vartype.BINARY)

    # Lagrangian multiplier
    # First guess as suggested in Lucas's paper
    lagrange = max(values)

    # Number of objects
    x_size = len(values)

    # Lucas's algorithm introduces additional slack variables to handle
    # the inequality. max_y_index indicates the maximum index in the y
    # sum; hence the number of slack variables.
    max_y_index = ceil(log(total_capacity))

    # Slack variable list for Lucas's algorithm. The last variable has
    # a special value because it terminates the sequence.
    y = [2**n for n in range(max_y_index - 1)]
    y.append(total_capacity + 1 - 2**(max_y_index - 1))

    # Q-Alpha - calculate the extra constant in second part of problem hamiltonian
    C = sum([weight * weight_r for weight in weights])
    # Q-Alpha - change weights to weight*(1-weight_r)
    weights = [weight*(1-weight_r) for weight in weights]

    # Q-Alpha - change values to value*(1-value_r)
    # values = [value*(1-value_r) for value in values]

    # Hamiltonian xi-xi terms
    for k in range(x_size):
        # Q-Alpha add final term lagrange * C * weights[k]
        bqm.set_linear(
            cities[k],
            lagrange * (weights[k] ** 2) - values[k] + lagrange * C * weights[k])

    # Hamiltonian xi-xj terms
    for i in range(x_size):
        for j in range(i + 1, x_size):
            key = (cities[i], cities[j])
            bqm.quadratic[key] = 2 * lagrange * weights[i] * weights[j]

    # Hamiltonian y-y terms
    for k in range(max_y_index):
        # Q-Alpha add final term -lagrange * C * y[k]
        bqm.set_linear('y' + str(k), lagrange *
                       (y[k]**2) - lagrange * C * y[k])

    # Hamiltonian yi-yj terms
    for i in range(max_y_index):
        for j in range(i + 1, max_y_index):
            key = ('y' + str(i), 'y' + str(j))
            bqm.quadratic[key] = 2 * lagrange * y[i] * y[j]

    # Hamiltonian x-y terms
    for i in range(x_size):
        for j in range(max_y_index):
            key = (cities[i], 'y' + str(j))
            bqm.quadratic[key] = -2 * lagrange * weights[i] * y[j]

    return bqm


def solve_cities(cities: List, gdps: List, sick: List, total_capacity: int,
                 value_r=0, weight_r=0, num_reads=1, verbose=False) -> Dict:
    """
    Solves problem: "Which cities should I should I shut down in order to stay
    within healthcare resources constraints while maximizing overall GDP"
    parameters:
        cities - list of city names
        gdps - corresponding list of GDP per city
        sick - corresponding number of sick people per city
        total_capacity - max capacity for sick people summed over all cities
        num_reads - number of samples to take
        verbose - whether to print out best result
    returns:
        (dict) - list of dictionaries with individual results and selected attributes
                    sorted in order of least energy first
    """
    if sum(sick) < total_capacity:
        print("Warning in solve_cities: Total number of sick people is less "
              + "than total capacity. There's no knapsack problem to solve!")

    bqm = knapsack_bqm(cities, gdps, sick, total_capacity,
                       value_r=value_r, weight_r=weight_r)
    sampler = LeapHybridSampler()
    samplesets = [sampler.sample(bqm) for _ in range(num_reads)]

    df = pd.DataFrame({'city': cities, 'gdp': gdps, 'sick': sick})
    df = df.set_index('city')

    solution_set = []
    for sampleset in samplesets:
        open_cities = []
        closed_cities = []
        for k, v in sampleset.first.sample.items():
            if k in cities:
                if v == 1:
                    open_cities.append(k)
                else:
                    closed_cities.append(k)
        solution_set.append({
            'open_cities': open_cities,
            'closed_cities': closed_cities,
            'energy': sampleset.first.energy,
            'salvaged_gdp': sum(df.loc[open_cities]['gdp']) + sum(df.loc[closed_cities]['gdp']) * value_r,
            'used_capacity': int(round(sum(df.loc[open_cities]['sick'])))
        })

    # do sorting from lowest to highest energy
    if num_reads > 1:
        energies = [solution['energy'] for solution in solution_set]
        solution_set = [x for _, x in sorted(zip(energies, solution_set))]

    if verbose:
        print('BEST SOLUTION')
        print('Open cities')
        print(solution_set[0]['open_cities'])
        print('\n')
        print('Closed cities')
        print(solution_set[0]['closed_cities'])
        print('\n')
        total_gdp = sum(df['gdp'])
        salvaged_gdp = solution_set[0]['salvaged_gdp']
        print(
            f'Salvaged GDP: {salvaged_gdp} ({(100*salvaged_gdp/total_gdp):.1f}%)')
        used_capacity = solution_set[0]['used_capacity']
        print(
            f'Used up hospital capacity: {used_capacity:d} of {total_capacity} ({(100*used_capacity/total_capacity):.1f}%)')

    return solution_set


def solve_cities_from_csv(filepath: str, total_capacity: int, value_r=0, weight_r=0,
                          num_reads=1, verbose=False) -> Dict:
    """
    Bridge to solve_cities given a csv file for the cities, gdps, and sick
    csv file needs to have header: city,gdp,sick
    """
    df = pd.read_csv(filepath)
    assert ','.join(
        df.columns) == 'city,gdp,sick', "Ensure csv header is city,gdp,sick"
    solution_set = solve_cities(list(df['city']), list(
        df['gdp']), list(df['sick']), total_capacity, value_r=value_r,
        weight_r=weight_r, num_reads=num_reads, verbose=verbose)
    return solution_set


def main():
    """ CLI
    """
    description = "Solve the problem: \"Which cities should I should I shut "
    description += "down in order to stay within healthcare resources "
    description += "constraints while maximizing overall GDP\""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--data', '-d',
                        help="path to csv file with columns: city,gdp,sick. Header expected")
    parser.add_argument('--total-capacity', '-t', type=int,
                        help="Maximum capacity for sick people for all cities combined.")
    parser.add_argument('--num-reads', '-n', type=int, default=1,
                        help="Number of samples to return")
    args = parser.parse_args()
    solution_set = solve_cities_from_csv(
        args.data, args.total_capacity, args.num_reads, verbose=True)


if __name__ == '__main__':
    main()
