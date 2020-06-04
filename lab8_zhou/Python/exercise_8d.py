"""Exercise 8d"""
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

def exercise_8d1(timestep):
    """Exercise 8d1"""
    parameter_set = SimulationParameters(
                            duration=10,  # Simulation duration in [s]
                            timestep=timestep,  # Simulation timestep in [s]
                            spawn_position=[0, 0, 0.1],  # Robot position in [m]
                            spawn_orientation=[0, 0, 0],  # Orientation in Euler angles [rad]
                            drive=3.,  # An example of parameter part of the grid search
                            amplitudes=[0.3, 0.3], 
                            turn=1,  
                            pattern='swim',
                            phase_lag=0.2*np.pi,
                            #amplitude=1.,
                            # ...
                        )

    filename = './logs_8d/simulation_turn.{}'
    
    
    sim, data = simulation(
        sim_parameters=parameter_set,  # Simulation parameters, see above
        arena='water',  # Can also be 'ground' or 'amphibious'
        fast=True,  # For fast mode (not real-time)
        #record=True,
    )
    data.to_file(filename.format('h5'))  
  
    '''
    sim.interface.video.save(
                filename='8d_turning_right.mp4',
                iteration=sim.iteration,
                writer='ffmpeg',
            )
    '''
    
    
    data=AnimatData.from_file(filename.format('h5'))
    links_positions = data.sensors.gps.urdf_positions()
    head_positions = links_positions[:, 0, :]
    
    osc_phases = data.state.phases_all()
    osc_amplitudes = data.state.amplitudes_all()
    times = data.times

    
    plt.figure()
    plot_results.plot_trajectory(head_positions, title='Head Trajectory of Salmandar Turning Right')
    
    
    plt.figure()
    labels=['Spine Joint '+str(i+1) for i in range(10)]
    
    links_positions = data.sensors.gps.urdf_positions()
    
    plot_results.plot_spine_angles(osc_phases, osc_amplitudes , times,  labels=labels,
                                  title='Spine Angles of Salmandar Turning Right'  )

def exercise_8d2(timestep):
    """Exercise 8d2"""
    parameter_set = SimulationParameters(
                            duration=10,  # Simulation duration in [s]
                            timestep=timestep,  # Simulation timestep in [s]
                            spawn_position=[0, 0, 0.1],  # Robot position in [m]
                            spawn_orientation=[0, 0, 0],  # Orientation in Euler angles [rad]
                            drive=3.,  # An example of parameter part of the grid search
                            amplitudes=[0.3, 0.3], 
                            turn=0,  
                            pattern='swim',
                            phase_lag=-0.2*np.pi,
                            #amplitude=1.,
                            # ...
                        )
    
    filename = './logs_8d/simulation_back.{}'
    
    
   
    sim, data = simulation(
        sim_parameters=parameter_set,  # Simulation parameters, see above
        arena='water',  # Can also be 'ground' or 'amphibious'
        fast=True,  # For fast mode (not real-time)
        #record=True,
    )
    data.to_file(filename.format('h5'))
    
    '''
    sim.interface.video.save(
                filename='8d_backward.mp4',
                iteration=sim.iteration,
                writer='ffmpeg',
            )
    '''
    
    
    
    data=AnimatData.from_file(filename.format('h5'))
    links_positions = data.sensors.gps.urdf_positions()
    head_positions = links_positions[:, 0, :]
    
    osc_phases = data.state.phases_all()
    osc_amplitudes = data.state.amplitudes_all()
    times = data.times
    
    plt.figure()
    plot_results.plot_trajectory(head_positions, title='Head Trajectory of Salmandar Swimming Backward')
    
    plt.figure()
    labels=['Spine Joint '+str(i+1) for i in range(10)]
    
    links_positions = data.sensors.gps.urdf_positions()
    
    plot_results.plot_spine_angles(osc_phases, osc_amplitudes , times,  labels=labels,
                                  title='Spine Angles of Salmandar Swimming Backward'  )

if __name__ == '__main__':
    exercise_8d1(timestep=1e-2)
    exercise_8d2(timestep=1e-2)

