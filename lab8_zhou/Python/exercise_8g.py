"""Exercise 8g"""

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


def exercise_8g_land_to_water(timestep):
    """Exercise 8g"""
    # transition from land to water
    
    temp_amplitude=0.3
    parameter_set = SimulationParameters(
                        freqs=1,
                        duration=25,  # Simulation duration in [s]
                        timestep=timestep,  # Simulation timestep in [s]
                        spawn_position=[0, 0, 0.1],  # Robot position in [m]
                        spawn_orientation=[0, 0, np.pi],  # Orientation in Euler angles [rad]
                        drive=2,  # An example of parameter part of the grid search
                        amplitudes=[temp_amplitude, temp_amplitude], 
                        turn=0,  
                        pattern='walk',
                        phase_lag=0.2*np.pi,
                        absolute_amplitude=False,    
                        phase_body_limb=4*np.pi/9 ,
                        transition=['walk','swim'],
                    )
    
  
    filename = './logs_8g/walking_to_swimming.{}'
    
    
    
    sim, data = simulation(
        sim_parameters=parameter_set,  # Simulation parameters, see above
        arena='amphibious',  # Can also be 'ground' or 'amphibious'
        fast=True,  # For fast mode (not real-time)
        # headless=True,  # For headless mode (No GUI, could be faster)
        record=True,  # Record video, see below for saving
        # video_distance=1.5,  # Set distance of camera to robot
        # video_yaw=0,  # Set camera yaw for recording
        # video_pitch=-45,  # Set camera pitch for recording
    )
    # Log robot data
    data.to_file(filename.format('h5'), sim.iteration)
    # Log simulation parameters
    
    
    # Save video
    sim.interface.video.save(
                filename='video_transition_from_walking_to_swimming.mp4',
                iteration=sim.iteration,
                writer='ffmpeg',
            )
    
    
    data=AnimatData.from_file(filename.format('h5'))
    links_positions = data.sensors.gps.urdf_positions()
    head_positions = links_positions[:, 0, :]
    times = data.times
    plt.figure()
    plt.plot(times,head_positions[:,0])
    plt.xlabel("time[s]")
    plt.ylabel("x [m]")
    plt.axis("equal")
    plt.title("X with time for transition from walking to swimming")
    plt.grid(True)
    
    osc_phases = data.state.phases_all()
    osc_amplitudes = data.state.amplitudes_all()
    print(osc_phases.shape)
    print(osc_amplitudes.shape)

    
            
    plt.figure()
    labels=['Spine Joint '+str(i+1) for i in range(10)]        
    plot_results.plot_spine_angles(osc_phases, osc_amplitudes , times,  labels=labels,
                                  title='Spine Angles for transition from walking to swimming'  )
    
    
    plt.figure()
    labels=['Limb Joint '+str(i+1) for i in range(4)]        
    plot_results.plot_limb_angles(osc_phases, temp_amplitude , times,  labels=labels,
                                  title='Limb Angles for transition from walking to swimming'  )

    

def exercise_8g_water_to_land(timestep):
    """Exercise 8g"""
    # transition from water to land
    temp_amplitude=0.3
    parameter_set = SimulationParameters(
                        freqs=1,
                        duration=25,  # Simulation duration in [s]
                        timestep=timestep,  # Simulation timestep in [s]
                        spawn_position=[-6, 0, 0.1],  # Robot position in [m]
                        spawn_orientation=[0, 0, 0],  # Orientation in Euler angles [rad]
                        drive=3.5,  # An example of parameter part of the grid search
                        amplitudes=[temp_amplitude, temp_amplitude], 
                        turn=0,  
                        pattern='walk',
                        phase_lag=0.2*np.pi,
                        absolute_amplitude=False,    
                        phase_body_limb=4*np.pi/9 ,
                        transition=['swim','walk'],
                    )
    
  
    filename = './logs_8g/swimming_to_walking.{}'
    
    
    
    sim, data = simulation(
        sim_parameters=parameter_set,  # Simulation parameters, see above
        arena='amphibious',  # Can also be 'ground' or 'amphibious'
        fast=True,  # For fast mode (not real-time)
        # headless=True,  # For headless mode (No GUI, could be faster)
        record=True,  # Record video, see below for saving
        # video_distance=1.5,  # Set distance of camera to robot
        # video_yaw=0,  # Set camera yaw for recording
        # video_pitch=-45,  # Set camera pitch for recording
    )
    # Log robot data
    data.to_file(filename.format('h5'), sim.iteration)
    # Log simulation parameters
    
    
    # Save video
    sim.interface.video.save(
                filename='video_transition_from_swimming_to_walking.mp4',
                iteration=sim.iteration,
                writer='ffmpeg',
            )
    
    
    data=AnimatData.from_file(filename.format('h5'))
    links_positions = data.sensors.gps.urdf_positions()
    head_positions = links_positions[:, 0, :]
    times = data.times
    plt.figure()
    plt.plot(times,head_positions[:,0])
    plt.xlabel("time[s]")
    plt.ylabel("x [m]")
    plt.axis("equal")
    plt.title("X with time for transition from swimming to walking")
    plt.grid(True)
    
    osc_phases = data.state.phases_all()
    osc_amplitudes = data.state.amplitudes_all()
    
            
    plt.figure()
    labels=['Spine Joint '+str(i+1) for i in range(10)]        
    plot_results.plot_spine_angles(osc_phases, osc_amplitudes , times,  labels=labels,
                                  title='Spine Angles for transition from swimming to walking'  )
    
    
    plt.figure()
    labels=['Limb Joint '+str(i+1) for i in range(4)]        
    plot_results.plot_limb_angles(osc_phases, temp_amplitude , times,  labels=labels,
                                  title='Limb Angles for transition from swimming to walking'  )


if __name__ == '__main__':
    exercise_8g_land_to_water(timestep=1e-2)
    exercise_8g_water_to_land(timestep=1e-2)

