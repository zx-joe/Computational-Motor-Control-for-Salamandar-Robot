"""Exercise 8b"""

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


def exercise_8b(timestep):
    """Exercise 8b"""
    amplitude_range=np.linspace(0.1,0.6,6)
    phase_lag_range=np.linspace(np.pi/10,np.pi/2,6)
    #amplitude_range=np.linspace(0.25,2.,2)
    #phase_lag_range=np.linspace(np.pi/10,np.pi/2,2)
    parameter_set = [[
        SimulationParameters(
            duration=10,  # Simulation duration in [s]
            timestep=timestep,  # Simulation timestep in [s]
            spawn_position=[0, 0, 0.1], 
            spawn_orientation=[0, 0, 0],  
            drive=3,  # A drive for swimming pattern
            amplitudes=[temp_amplitude,temp_amplitude],
            phase_lag=temp_phase_lag,  # or np.zeros(n_joints) for example
            turn=0,   # Another example
            pattern='swim',

        )
        for temp_phase_lag in phase_lag_range
        ]
        for temp_amplitude in amplitude_range
        ]
    
    
    
    
    
    # Grid search
    
    for i in range(len(amplitude_range)):
        for j in range(len(phase_lag_range)):
            amp=amplitude_range[i]
            phi=phase_lag_range[j]
            filename = './logs_8b/amplitude{}_phase_lag{}.{}'
            temp_param=parameter_set[i][j]
            sim, data = simulation (
                sim_parameters=temp_param,  
                arena='water', 
                fast=True
            )
            data.to_file(filename.format(amp, phi,'h5'))
            #temp_velocity=np.diff(data["joints"][:,:,0], axis = 0)/timestep
            with open(filename.format(amp, phi,'pickle'), 'wb') as param_file:
                pickle.dump(temp_param, param_file)

    
    
    
    
    #energies = np.zeros_like(parameter_set)
    #velocities=np.zeros_like(parameter_set)
    velocities=[]
    energies=[]
    #velocities=np.zeros((4,3))
     
    #plot_num=0
    for i in range(len(amplitude_range)):
        for j in range(len(phase_lag_range)):
            amp=amplitude_range[i]
            phi=phase_lag_range[j]
            filename = './logs_8b/amplitude{}_phase_lag{}.{}'
            
            data=AnimatData.from_file(filename.format(amp, phi,'h5'))
            
            temp_joint_velocities=np.asarray(data.sensors.proprioception.velocities_all())
            temp_joint_torques = np.asarray(data.sensors.proprioception.motor_torques())
            
            links_positions = data.sensors.gps.urdf_positions()
            head_positions = links_positions[:, 0, :]
            final_head_dist=np.linalg.norm(head_positions[-1])

            
            times = data.times
            total_time = times[-1] - times[0] 
            
            temp_velocity = final_head_dist/total_time
            
            
            temp_energy=np.sum(temp_joint_velocities*temp_joint_torques)
            
            velocities.append([amp,phi,temp_velocity])
            energies.append([amp,phi,temp_energy])
            #energies.append(temp_energy)
            #velocities[plot_num]=[amp,phi,temp_velocity]
            #energies[i,j]=temp_energy
            
            #plot_num+=1
            
    velocities=np.asarray(velocities)
    energies=np.asarray(energies)
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    vels=velocities[:,2]
    X,Y=np.meshgrid(amplitude_range, phase_lag_range)
    Z=np.zeros([len(phase_lag_range),len(amplitude_range)])
    num=0
    for i in range(len(X)):
        for j in range(len(X[0])):
            Z[j][i]=vels[num]
            num+=1
    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    cset = ax.contour(X, Y, Z, zdir='z',  cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='x', cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='y',cmap=cm.coolwarm)
    ax.set_xlabel('amplityde ratio', color='black')
    ax.set_ylabel('phase lag', color='black')
    ax.set_zlabel('velocity', color='black')
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    engs=energies[:,2]
    X,Y=np.meshgrid(amplitude_range, phase_lag_range)
    Z=np.zeros([len(phase_lag_range),len(amplitude_range)])
    num=0
    for i in range(len(X)):
        for j in range(len(X[0])):
            Z[j][i]=engs[num]
            num+=1
    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    cset = ax.contour(X, Y, Z, zdir='z',  cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='x', cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='y',cmap=cm.coolwarm)
    ax.set_xlabel('amplityde ratio', color='black')
    ax.set_ylabel('phase lag', color='black')
    ax.set_zlabel('energy', color='black')
    
    plt.figure()
    plot_2d(velocities,['amplitude ratio','phase_lag','velocity'])
    
    plt.figure()
    plot_2d(energies,['amplitude ratio','phase_lag','energy'])


if __name__ == '__main__':
    exercise_8b(timestep=1e-2)

