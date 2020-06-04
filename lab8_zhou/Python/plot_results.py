"""Plot results"""

import pickle
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from save_figures import save_figures
from parse_args import save_plots
from salamandra_simulation.data import AnimatData

def plot_positions(times, link_data, labels=["x", "y", "z"],ylabel=' '):
    """Plot positions"""
    _ = plt.figure()
    try:
        for i, data in enumerate(link_data.T):
            plt.plot(times, data, label=labels[i])
    except:
        for i, data in enumerate(link_data.T):
            plt.plot(times, data)
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.grid(True)


def plot_trajectory(link_data, title=' '):
    """Plot positions"""
    plt.plot(link_data[:, 0], link_data[:, 1])
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.axis("equal")
    plt.title(title)
    plt.grid(True)
    
    
def plot_spine_angles(phases, amps, times, labels=[], title=' '):
    """Plot spine angles"""
    temp_len=len(times)
    temp_q=np.ones(temp_len)
    
    try:
        for i in range(10):
            temp_q=amps[:,i]*(1+np.cos(phases[:,i]))-amps[:,i+10]*(1+np.cos(phases[:,i+10]))
            plt.plot(times,temp_q, label = labels[i])
            
    
    except:
        for i in range(10):
            temp_q=amps[i]*(1+np.cos(phases[i]))-amps[i+10]*(1+np.cos(phases[i+10]))
            plt.plot(times,temp_q)
        
    plt.legend()
    plt.title(title)
    plt.xlabel('time[s]')
    plt.ylabel('spine angle [rad]')
    
    
def plot_limb_angles(phases, amp, times, labels=[], title=' '):
    """Plot spine angles"""
    temp_len=len(times)
    temp_q=np.ones(temp_len)
    
    try:
        for i in range(20,24):
            temp_q=(1+np.cos(phases[:,i]))*amp
            plt.plot(times,temp_q,label=labels[i-20])
            
    
    except:
        for i in range(20,24):
            temp_q=(1+np.cos(phases[:,i]))*amp
            plt.plot(times,temp_q)
        
    plt.legend()
    plt.title(title)
    plt.xlabel('time[s]')
    plt.ylabel('limb angle [rad]')
    


def plot_2d(results, labels, n_data=300, log=False, cmap=None):
    """Plot result

    results - The results are given as a 2d array of dimensions [N, 3].

    labels - The labels should be a list of three string for the xlabel, the
    ylabel and zlabel (in that order).

    n_data - Represents the number of points used along x and y to draw the plot

    log - Set log to True for logarithmic scale.

    cmap - You can set the color palette with cmap. For example,
    set cmap='nipy_spectral' for high constrast results.

    """
    xnew = np.linspace(min(results[:, 0]), max(results[:, 0]), n_data)
    ynew = np.linspace(min(results[:, 1]), max(results[:, 1]), n_data)
    grid_x, grid_y = np.meshgrid(xnew, ynew)
    results_interp = griddata(
        (results[:, 0], results[:, 1]), results[:, 2],
        (grid_x, grid_y),
        method='nearest'  # nearest, cubic
    )
    extent = (
        min(xnew), max(xnew),
        min(ynew), max(ynew)
    )
    plt.plot(results[:, 0], results[:, 1], "r.")
    imgplot = plt.imshow(
        results_interp,
        extent=extent,
        aspect='auto',
        origin='lower',
        interpolation="none",
        norm=LogNorm() if log else None
    )
    if cmap is not None:
        imgplot.set_cmap(cmap)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    cbar = plt.colorbar()
    cbar.set_label(labels[2])
    
    


def main(plot=True):
    """Main"""
    # Load data
    data = AnimatData.from_file('logs/example/simulation_0.h5', 2*14)
    with open('logs/example/simulation_0.pickle', 'rb') as param_file:
        parameters = pickle.load(param_file)
    times = data.times
    timestep = times[1] - times[0]  # Or parameters.timestep
    amplitudes = parameters.amplitudes
    phase_lag = parameters.phase_lag
    osc_phases = data.state.phases_all()
    osc_amplitudes = data.state.amplitudes_all()
    links_positions = data.sensors.gps.urdf_positions()
    head_positions = links_positions[:, 0, :]
    tail_positions = links_positions[:, 10, :]
    joints_positions = data.sensors.proprioception.positions_all()
    joints_velocities = data.sensors.proprioception.velocities_all()
    joints_torques = data.sensors.proprioception.motor_torques()
    # Notes:
    # For the gps arrays: positions[iteration, link_id, xyz]
    # For the positions arrays: positions[iteration, xyz]
    # For the joints arrays: positions[iteration, joint]

    # Plot data
    plt.figure("Positions")
    plot_positions(times, head_positions)
    plt.figure("Trajectory")
    plot_trajectory(head_positions)

        # Show plots
    if plot:
        plt.show()
    else:
        save_figures()


if __name__ == '__main__':
    main(plot=not save_plots())

