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
                    drive=i*6/3000.
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
    pylog.warning("Implement plots of 8a")
    
    # **********************************************************
    # **********************************************************
    # **********************************************************
    # **********************************************************
    # **********************************************************
    # **********************************************************
    ###  8a 

    plt.figure("Body Joints in Walking Pattern")
    body_labels=['body joint '+str(i+1) for i in range(10)]
    plot_results.plot_positions(times,outputs_log[:,:10],labels=body_labels,ylabel=' ')
    plt.figure("Limb Joints in Walking Pattern")
    limb_labels=['limb joint '+str(i+1) for i in range(4)]
    plot_results.plot_positions(times,outputs_log[:,10:],labels=limb_labels,ylabel=' ')

    plt.figure("phase of joints")
    plt.plot(times,phases_log[:,0],label='body joints')
    plt.plot(times,phases_log[:,-1],label='limb joints')
    plt.grid(True)
    plt.xlabel("time [s]")
    plt.ylabel('phase')
    plt.legend() 
    
    plt.figure("amplitude of joints")
    plt.plot(times,amplitudes_log[:,0],label='body joints')
    plt.plot(times,amplitudes_log[:,-1],label='limb joints')
    plt.grid(True)
    plt.xlabel("time [s]")
    plt.ylabel('amplitude')
    plt.legend() 
    
    plt.figure("frequency of joints")
    plt.plot(times,freqs_log[:,0],label='body joints')
    plt.plot(times,freqs_log[:,-1],label='limb joints')
    plt.grid(True)
    plt.xlabel("time [s]")
    plt.ylabel('frequency [Hz]')
    plt.legend() 


def main(plot):
    """Main"""

    run_network(duration=30, drive=5, update=True)

    # Show plots
    if plot:
        plt.show()
    else:
        save_figures()


if __name__ == '__main__':
    main(plot=not save_plots())

