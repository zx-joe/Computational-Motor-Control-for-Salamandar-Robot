"""Exercise example"""

import pickle
import numpy as np
import matplotlib.animation as manimation
from simulation import simulation
from simulation_parameters import SimulationParameters
import farms_pylog as pylog


def exercise_example(timestep):
    """Exercise example"""
    # Parameters
    cv_body = [0.2, 0.3]
    cv_limb = [0.2, 0.]
    
    
    cr_body = [0.056, 0.196]
    cr_limb = [0.131, 0.131]
    

    parameter_set = [
        SimulationParameters(
            freqs=1,
            duration=10,  # Simulation duration in [s]
            timestep=timestep,  # Simulation timestep in [s]
            spawn_position=[-1.3, 0, 0.1],  # Robot position in [m]
            spawn_orientation=[0, 0, 0],  # Orientation in Euler angles [rad]
            drive=4,  # An example of parameter part of the grid search
            amplitudes=[0.3, 0.3], 
            turn=0,  
            pattern='walk',
            phase_lag=0.2*np.pi,
            absolute_amplitude=False,    
            phase_body_limb=4*np.pi/9 ,
            #transition=['walk','swim'],
            #amplitude=1.,
            # ...
        )
        for drive in np.linspace(1, 1, 1)
        # for amplitudes in ...
        # for ...
    ]
    
    

    
    # Grid search
    for simulation_i, sim_parameters in enumerate(parameter_set):
        filename = './logs/example/simulation_{}.{}'
        sim, data = simulation(
            sim_parameters=sim_parameters,  # Simulation parameters, see above
            arena='amphibious',  # Can also be 'ground' or 'amphibious'
            fast=True,  # For fast mode (not real-time)
            # headless=True,  # For headless mode (No GUI, could be faster)
            #record=True,  # Record video, see below for saving
            # video_distance=1.5,  # Set distance of camera to robot
            # video_yaw=0,  # Set camera yaw for recording
            # video_pitch=-45,  # Set camera pitch for recording
        )
        # Log robot data
        data.to_file(filename.format(simulation_i, 'h5'), sim.iteration)
        # Log simulation parameters
        with open(filename.format(simulation_i, 'pickle'), 'wb') as param_file:
            pickle.dump(sim_parameters, param_file)
        # Save video
        if sim.options.record:
            if 'ffmpeg' in manimation.writers.avail:
                sim.interface.video.save(
                    filename='video_transition_from_walking_to_swimming.mp4',
                    iteration=sim.iteration,
                    writer='ffmpeg',
                )
            elif 'html' in manimation.writers.avail:
                # FFmpeg might not be installed, use html instead
                sim.interface.video.save(
                    filename='transition_from_walking_to_swimming.html',
                    iteration=sim.iteration,
                    writer='html',
                )
            else:
                pylog.error('No known writers, maybe you can use: {}'.format(
                    manimation.writers.avail
                ))


if __name__ == '__main__':
    exercise_example(timestep=1e-2)

