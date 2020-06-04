"""Exercise 8f"""

import pickle
import numpy as np
from simulation import simulation
from simulation_parameters import SimulationParameters
import math
from plot_results import plot_2d
from salamandra_simulation.data import AnimatData
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import plot_results


def exercise_8f_offet(timestep):
    """search phase offset """
    
    phase_range=np.linspace(0, np.pi, 10)
    
    parameter_set = [  SimulationParameters(
                            duration=10,  # Simulation duration in [s]
                            timestep=timestep,  # Simulation timestep in [s]
                            spawn_position=[0, 0, 0.1],  # Robot position in [m]
                            spawn_orientation=[0, 0, 0],  # Orientation in Euler angles [rad]
                            drive=2.,  # An example of parameter part of the grid search
                            amplitudes=[0.3, 0.3], 
                            turn=0,  
                            pattern='walk',
                            phase_lag=0.2*np.pi,
                            absolute_amplitude=False,    
                            phase_body_limb=temp_phase ,
                        )
                        for temp_phase in phase_range
                            ]
    
    filename = './logs_8f/phase{}.{}'
    
    for i in range(len(phase_range)):
        temp_phase=phase_range[i]
        temp_param=parameter_set[i]
        sim, data = simulation (
                sim_parameters=temp_param,  
                arena='ground', 
                fast=True
            )
        data.to_file(filename.format(temp_phase,'h5'))
        
    velocities=[]
    for i in range(len(phase_range)):
        temp_phase=phase_range[i]
        
        data=AnimatData.from_file(filename.format(temp_phase, 'h5'))

        links_positions = data.sensors.gps.urdf_positions()
        head_positions = links_positions[:, 0, :]
        final_head_dist=np.linalg.norm(head_positions[-1])

        times = data.times
        total_time = times[-1] - times[0] 
        
        temp_velocity = final_head_dist/total_time
        velocities.append(temp_velocity)
        
        
    fig = plt.figure()
    plt.plot(phase_range, velocities)
    plt.legend()
    plt.xlabel("phase")
    plt.ylabel("velocity")
    plt.title("Relationship of Phase Offset and Walking Speed")
    plt.grid(True)
        
          
    
    
def exercise_8f_amplitude(timestep):
    """search oscillation amplitude """
    amplitudes_range=np.linspace(0, 0.6, 10)
    
    parameter_set = [  SimulationParameters(
                            duration=10,  # Simulation duration in [s]
                            timestep=timestep,  # Simulation timestep in [s]
                            spawn_position=[0, 0, 0.1],  # Robot position in [m]
                            spawn_orientation=[0, 0, 0],  # Orientation in Euler angles [rad]
                            drive=2.,  # An example of parameter part of the grid search
                            amplitudes=[temp_amp, temp_amp], 
                            turn=0,  
                            pattern='walk',
                            phase_lag=0.2*np.pi,
                            absolute_amplitude=True,    
                            phase_body_limb=4*np.pi/9 ,
                        )
                        for temp_amp in amplitudes_range
                            ]
    
    filename = './logs_8f/amp{}.{}'
    
    for i in range(len(amplitudes_range)):
        temp_amp=amplitudes_range[i]
        temp_param=parameter_set[i]
        sim, data = simulation (
                sim_parameters=temp_param,  
                arena='ground', 
                fast=True
            )
        data.to_file(filename.format(temp_amp,'h5'))
        
    velocities=[]
    for i in range(len(amplitudes_range)):
        temp_amp=amplitudes_range[i]
        
        data=AnimatData.from_file(filename.format(temp_amp, 'h5'))

        links_positions = data.sensors.gps.urdf_positions()
        head_positions = links_positions[:, 0, :]
        final_head_dist=np.linalg.norm(head_positions[-1])

        times = data.times
        total_time = times[-1] - times[0] 
        
        temp_velocity = final_head_dist/total_time
        velocities.append(temp_velocity)
       
        
    fig = plt.figure()
    plt.plot(amplitudes_range, velocities)
    plt.legend()
    plt.xlabel("amplitude")
    plt.ylabel("velocity")
    plt.title("Relationship of Oscillation Amplitude and Walking Speed")
    plt.grid(True)



if __name__ == '__main__':
    exercise_8f_offet(timestep=1e-2)
    exercise_8f_amplitude(timestep=1e-2)

