"""Run network without Pybullet"""

import time
import numpy as np
import matplotlib.pyplot as plt
import farms_pylog as pylog
from network import SalamandraNetwork
from save_figures import save_figures
from parse_args import save_plots
from simulation_parameters import SimulationParameters
import plot_results  


def run_network(duration, update=False, drive=0):
    """Run network without Pybullet and plot results
    Parameters
    ----------
    duration: <float>
        Duration in [s] for which the network should be run
    update: <bool>
        description
    drive: <float/array>
        Central drive to the oscillators
    """
    # Simulation setup
    timestep = 1e-2
    times = np.arange(0, duration, timestep)
    n_iterations = len(times)
    sim_parameters = SimulationParameters(
        drive=drive,
        amplitude_gradient=None,
        phase_lag=None,
        turn=None,
    )
    network = SalamandraNetwork(sim_parameters, n_iterations)
    osc_left = np.arange(10)
    osc_right = np.arange(10, 20)
    osc_legs = np.arange(20, 24)

    # Logs
    phases_log = np.zeros([
        n_iterations,
        len(network.state.phases(iteration=0))
    ])
    phases_log[0, :] = network.state.phases(iteration=0)
    amplitudes_log = np.zeros([
        n_iterations,
        len(network.state.amplitudes(iteration=0))
    ])
    amplitudes_log[0, :] = network.state.amplitudes(iteration=0)
    freqs_log = np.zeros([
        n_iterations,
        len(network.robot_parameters.freqs)
    ])
    freqs_log[0, :] = network.robot_parameters.freqs
    outputs_log = np.zeros([
        n_iterations,
        len(network.get_motor_position_output(iteration=0))
    ])
    outputs_log[0, :] = network.get_motor_position_output(iteration=0)

    # Run network ODE and log data
    tic = time.time()
    for i, time0 in enumerate(times[1:]):
        if update:
            network.robot_parameters.update(
                SimulationParameters(
                    # amplitude_gradient=None,
                    # phase_lag=None
                )
            )
        network.step(i, time0, timestep)
        phases_log[i+1, :] = network.state.phases(iteration=i+1)
        amplitudes_log[i+1, :] = network.state.amplitudes(iteration=i+1)
        outputs_log[i+1, :] = network.get_motor_position_output(iteration=i+1)
        freqs_log[i+1, :] = network.robot_parameters.freqs
    # # Alternative option
    # phases_log[:, :] = network.state.phases()
    # amplitudes_log[:, :] = network.state.amplitudes()
    # outputs_log[:, :] = network.get_motor_position_output()
    toc = time.time()

    # Network performance
    pylog.info("Time to run simulation for {} steps: {} [s]".format(
        n_iterations,
        toc - tic
    ))

    # Implement plots of network results
    pylog.warning("Implement plots")
    
    # **********************************************************
    # **********************************************************
    # **********************************************************
    # **********************************************************
    # **********************************************************
    # **********************************************************
    ###  8a : swimming
    '''
    plt.figure('phases')
    plt.plot(phases_log)
    
    plt.figure('amplitude')
    plt.plot(amplitudes_log)
    
    plt.figure('frequency')
    plt.plot(freqs_log)
    
    plt.figure('out')
    plt.plot(outputs_log)
    '''
    gait='swimming'
    #plot_results.plot_body_joints(times, outputs_log, f'exercise_9a_{gait}_body_joints', gait=gait)
    plot_results.plot_positions(times,outputs_log[:,:10],labels=[1,2,3,4,5,6,7,8,9,10])
    #plot_results.plot_positions(times,outputs_log[:,10:],labels=[1,2,3,4,5,6,7,8,9,10])
    


def main(plot):
    """Main"""

    run_network(duration=10, drive=2)

    

    # Show plots
    if plot:
        plt.show()
    else:
        save_figures()


if __name__ == '__main__':
    main(plot=not save_plots())

