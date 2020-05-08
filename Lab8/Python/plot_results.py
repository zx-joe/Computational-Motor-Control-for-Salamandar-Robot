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
    for i, data in enumerate(link_data.T):
        try:
            plt.plot(times, data, label=labels[i])
        except:
            plt.plot(times, data)
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.grid(True)


def plot_trajectory(link_data):
    """Plot positions"""
    plt.plot(link_data[:, 0], link_data[:, 1])
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.axis("equal")
    plt.grid(True)


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
        method='linear'  # nearest, cubic
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
    
    
### 8a
def plot_body_joints(time, joint_angles, file_name='body joint angle', title='Spine angle evolution', offset_mult=1.1,
                     gait='swimming'):
    """ Extracts and plots motor output for body joints"""
    nb_legs = 4
    nb_body = joint_angles.shape[1]-nb_legs
    plt.figure(file_name.replace(" ", "_"))

    offset = joint_angles[:, :nb_body].max()-joint_angles[:, :nb_body].min()

    for body_joint_index in range(nb_body):
        if gait == 'walking':
            offset_add_head = 1.5
            offset_add_upper_bod = 1.5
            if body_joint_index == 0:
                plt.plot(time,
                         joint_angles[:, body_joint_index]
                         + offset_mult * (nb_body-body_joint_index-1) * offset
                         + offset_add_head * offset + offset_add_upper_bod * offset,
                         label=f'head joint {body_joint_index}')
            elif body_joint_index < 6:
                plt.plot(time,
                         joint_angles[:, body_joint_index]
                         + offset_mult * (nb_body - body_joint_index - 1) * offset
                         + offset_add_upper_bod * offset,
                         label=f'upper body joint {body_joint_index}')
            else:
                plt.plot(time,
                         joint_angles[:, body_joint_index]
                         + offset_mult * (nb_body - body_joint_index - 1) * offset,
                         label=f'lower body joint {body_joint_index}')
        else:
            plt.plot(time,
                     joint_angles[:, body_joint_index]
                     + offset_mult * (nb_body - body_joint_index - 1) * offset,
                     label=f'body joint {body_joint_index}')

    plt.grid()
    plt.legend()
    plt.title(title)


def plot_leg_joints(time, joint_angles, file_name='leg joint angle', title='Limb angle evolution', offset_mult=1.1):
    """ Extracts and plots motor output for body joints"""
    nb_legs = 4
    nb_body = joint_angles.shape[1]-nb_legs
    plt.figure(file_name.replace(" ", "_"))

    # Wrap up legs output:
    joint_angles[:, nb_body:] %= 2 * np.pi

    offset = joint_angles[:, nb_body:].max()-joint_angles[:, nb_body:].min()
    if offset == 0:
        offset = 0.5

    for leg_joint_index in range(nb_legs):
        plt.plot(time, joint_angles[:, nb_body+leg_joint_index]+offset_mult*(nb_legs-1-leg_joint_index)*offset,
                 label="leg joint " + str(leg_joint_index))
    plt.grid()
    plt.legend()
    plt.title(title)


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

