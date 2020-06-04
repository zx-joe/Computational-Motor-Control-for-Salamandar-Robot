"""Exercise 8c"""

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


def exercise_8c(timestep):
    """Exercise 8c"""
    # Use exercise_example.py for reference
    r_head_range=np.linspace(0.1,0.8,6)
    r_tail_range=np.linspace(0.1,0.8,6)
    #r_head_range=np.linspace(0.1,1.,2)
    #r_tail_range=np.linspace(0.1,1.,2)
    parameter_set = [[
        SimulationParameters(
            duration=10,  # Simulation duration in [s]
            timestep=timestep,  # Simulation timestep in [s]
            spawn_position=[0, 0, 0.1], 
            spawn_orientation=[0, 0, 0],  
            drive=3,  # A drive for swimming pattern
            amplitudes = [temp_r_head,temp_r_tail],
            phase_lag=-0.2*np.pi,  # or np.zeros(n_joints) for example
            turn=0,  # Another example
            pattern='swim',

        )
        for temp_r_tail in r_tail_range
        ]
        for temp_r_head in r_head_range
        ]
    
    
    
    
    # Grid search
    
    
    for i in range(len(r_head_range)):
        for j in range(len(r_tail_range)):
            head=r_head_range[i]
            tail=r_tail_range[j]
            filename = './logs_8c/RHead{}RTail{}.{}'
            temp_param=parameter_set[i][j]
            sim, data = simulation (
                sim_parameters=temp_param,  
                arena='water', 
                fast=True
            )
            data.to_file(filename.format(head, tail,'h5'))
            #temp_velocity=np.diff(data["joints"][:,:,0], axis = 0)/timestep
            with open(filename.format(head, tail,'pickle'), 'wb') as param_file:
                pickle.dump(temp_param, param_file)

    #energies = np.zeros_like(parameter_set)
    #velocities=np.zeros_like(parameter_set)
    velocities=[]
    energies=[]
    #velocities=np.zeros((4,3))
     
    #plot_num=0
    for i in range(len(r_head_range)):
        for j in range(len(r_tail_range)):
            head=r_head_range[i]
            tail=r_tail_range[j]
            filename = './logs_8c/RHead{}RTail{}.{}'
            
            data=AnimatData.from_file(filename.format(head, tail,'h5'))
            
            temp_joint_velocities=np.asarray(data.sensors.proprioception.velocities_all())
            temp_joint_torques = np.asarray(data.sensors.proprioception.motor_torques())
            
            links_positions = data.sensors.gps.urdf_positions()
            head_positions = links_positions[:, 0, :]
            final_head_dist=np.linalg.norm(head_positions[-1])

            
            times = data.times
            total_time = times[-1] - times[0] 
            
            temp_velocity = final_head_dist/total_time
            
            temp_energy=np.sum(temp_joint_velocities*temp_joint_torques)
            
            velocities.append([head,tail,temp_velocity])
            energies.append([head,tail,temp_energy])
            #energies.append(temp_energy)
            #velocities[plot_num]=[amp,phi,temp_velocity]
            #energies[i,j]=temp_energy
            
            #plot_num+=1
            
    velocities=np.asarray(velocities)
    energies=np.asarray(energies)
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    vels=velocities[:,2]
    X,Y=np.meshgrid(r_head_range, r_tail_range)
    Z=np.zeros([len(r_tail_range),len(r_head_range)])
    num=0
    for i in range(len(X)):
        for j in range(len(X[0])):
            Z[j][i]=vels[num]
            num+=1
    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    cset = ax.contour(X, Y, Z, zdir='z',  cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='x', cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='y',cmap=cm.coolwarm)
    ax.set_xlabel('RHead amplitude ratio', color='black')
    ax.set_ylabel('RTail amplitude ratio', color='black')
    ax.set_zlabel('velocity', color='black')
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    engs=energies[:,2]
    X,Y=np.meshgrid(r_head_range, r_tail_range)
    Z=np.zeros([len(r_tail_range),len(r_head_range)])
    num=0
    for i in range(len(X)):
        for j in range(len(X[0])):
            Z[j][i]=engs[num]
            num+=1
    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    cset = ax.contour(X, Y, Z, zdir='z',  cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='x', cmap=cm.coolwarm)
    cset = ax.contour(X, Y, Z, zdir='y',cmap=cm.coolwarm)
    ax.set_xlabel('RHead amplitude ratio', color='black')
    ax.set_ylabel('RTail amplitude ratio', color='black')
    ax.set_zlabel('energy', color='black')
    
    plt.figure()
    plot_2d(velocities,['RHead amplitude ratio','RTail amplitude ratio','velocity'])
    
    plt.figure()
    plot_2d(energies,['RHead amplitude ratio','RTail amplitude ratio','energy'])


if __name__ == '__main__':
    exercise_8c(timestep=1e-2)
