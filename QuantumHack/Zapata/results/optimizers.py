"""Plot the optimization curves for QAOA from a Quantum Engine workflow result JSON."""

import json
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as tck

def process_data_for_colormesh(x):
    x_diff = x[1] - x[0]
    x = np.append(x, x[-1] + x_diff)
    x = x - x_diff/2
    return x

def plot_grid_values(ax, grid_results):
    grid_size = int(np.sqrt(len(grid_results)))
    x = process_data_for_colormesh(grid_results[:,0][::grid_size])
    y = process_data_for_colormesh(grid_results[:,1][:grid_size])
    XX, YY = np.meshgrid(x, y)
    grid_values = grid_results[:,2].reshape(len(x)-1, len(y)-1).T

    ## This is for having ticks in the plot as multiples of pi
    ax.xaxis.set_major_formatter(tck.FuncFormatter(
    lambda val,pos: '{:.2f}$\pi$'.format(val/np.pi) if val !=0 else '0'
    ))
    ax.xaxis.set_major_locator(tck.MultipleLocator(base=np.pi/4))

    ax.yaxis.set_major_formatter(tck.FuncFormatter(
    lambda val,pos: '{:.2f}$\pi$'.format(val/np.pi) if val !=0 else '0'
    ))
    ax.yaxis.set_major_locator(tck.MultipleLocator(base=np.pi/4))
    mesh_plot = ax.pcolormesh(XX, YY, grid_values)
    return mesh_plot, ax

def plot_trajectory(ax, optimizer_results, color, label):
    ax.plot(optimizer_results[0, 0], optimizer_results[0, 1], '*', color=color)
    ax.plot(optimizer_results[:, 0], optimizer_results[:, 1], color=color, label=label)
    return ax

def plot_cost_function(ax, optimizer_results, color, label):
    ax.plot(optimizer_results[:,2], color=color, label=label)
    return ax

# Insert the path to your JSON file here
with open('87ea48ad-1cae-5323-b842-03b219ec8f54.json') as f:
    data = json.load(f)

# Extract parameters and values
bfgs_results = []
cma_es_results = []
nelder_mead_results = []
grid_results = []
initial_params = []

for task in data:
    if data[task]['class'] == 'generate-random-ansatz-params':
        initial_params = data[task]['params']['parameters']['real']

for task in data:
    if data[task]['class'] == 'optimize-variational-circuit':
        results = [[initial_params[0], initial_params[1], np.nan]]
        history = data[task]['optimization-results']['history']
        for epoch in history:
            x = epoch['params']['real'][0]
            y = epoch['params']['real'][1]
            value = epoch['value']
            results.append([x, y, value])

        specs = data[task]['inputParam:optimizer-specs']
        if "L-BFGS-B" in specs:
            bfgs_results = np.array(results)
        if "Nelder-Mead" in specs:
            nelder_mead_results = np.array(results)
        if "CMAESOptimizer" in specs:
            cma_es_results = np.array(results)
        if "GridSearchOptimizer" in specs:
            grid_results = np.array(results)[1:,:]

# Plot trajectories
fig, (ax1, ax2) = plt.subplots(1, 2)
mesh_plot, ax1 = plot_grid_values(ax1, grid_results)
ax1 = plot_trajectory(ax1, cma_es_results, color='g', label="CMA-ES")
ax1 = plot_trajectory(ax1, bfgs_results, color='b', label="L-BFGS-B")
ax1 = plot_trajectory(ax1, nelder_mead_results, color='r', label="Nelder-Mead")

cbar = fig.colorbar(mesh_plot, ax=ax1)
ax1.legend()
ax1.set_xlabel("beta")
ax1.set_ylabel("gamma")

# Plot values history
ax2 = plot_cost_function(ax2, cma_es_results, color='g', label="CMA-ES")
ax2 = plot_cost_function(ax2, bfgs_results, color='b', label="L-BFGS-B")
ax2 = plot_cost_function(ax2, nelder_mead_results, color='r', label="Nelder-Mead")

ax2.set_xlabel("Iterations")
ax2.set_ylabel("Value")
plt.tight_layout()
plt.show()

