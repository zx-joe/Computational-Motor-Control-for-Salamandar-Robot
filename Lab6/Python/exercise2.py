""" Lab 6 Exercise 2

This file implements the pendulum system with two muscles attached

"""

from math import sqrt

import farms_pylog as pylog
import numpy as np
from matplotlib import pyplot as plt

from cmcpack import DEFAULT
from cmcpack.plot import save_figure
from muscle import Muscle
from muscle_system import MuscleSystem
from neural_system import NeuralSystem
from pendulum_system import PendulumSystem
from system import System
from system_animation import SystemAnimation
from system_parameters import (MuscleParameters, NetworkParameters,
                               PendulumParameters)
from system_simulation import SystemSimulation


# Global settings for plotting
# You may change as per your requirement
plt.rc('lines', linewidth=2.0)
plt.rc('font', size=12.0)
plt.rc('axes', titlesize=14.0)     # fontsize of the axes title
plt.rc('axes', labelsize=14.0)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=14.0)    # fontsize of the tick labels
plt.rc('ytick', labelsize=14.0)    # fontsize of the tick labels

DEFAULT["save_figures"] = True


def system_init():
    """Initialize default system."""
    ########## PENDULUM ##########
    # Define and Setup your pendulum model here
    # Check Pendulum.py for more details on Pendulum class
    P_params = PendulumParameters()  # Instantiate pendulum parameters
    P_params.L = 1.0  # To change the default length of the pendulum
    P_params.m = 0.25  # To change the default mass of the pendulum
    pendulum = PendulumSystem(P_params)  # Instantiate Pendulum object
    #### CHECK OUT Pendulum.py to ADD PERTURBATIONS TO THE MODEL #####
    pylog.info('Pendulum model initialized \n {}'.format(
        pendulum.parameters.showParameters()))

    ########## MUSCLES ##########
    # Define and Setup your muscle model here
    # Check MuscleSystem.py for more details on MuscleSystem class
    m1_param = MuscleParameters()  # Instantiate Muscle 1 parameters
    m1_param.f_max = 200.  # To change Muscle 1 max force
    m1_param.l_opt = 0.4
    m1_param.l_slack = 0.45
    m2_param = MuscleParameters()  # Instantiate Muscle 2 parameters
    m2_param.f_max = 200.  # To change Muscle 2 max force
    m2_param.l_opt = 0.4
    m2_param.l_slack = 0.45
    m1 = Muscle('m1', m1_param)  # Instantiate Muscle 1 object
    m2 = Muscle('m2', m2_param)  # Instantiate Muscle 2 object
    # Use the MuscleSystem Class to define your muscles in the system
    # Instantiate Muscle System with two muscles
    muscles = MuscleSystem(m1, m2)
    pylog.info('Muscle system initialized \n {} \n {}'.format(
        m1.parameters.showParameters(),
        m2.parameters.showParameters()))
    # Define Muscle Attachment points
    m1_origin = np.asarray([0.0, 0.9])  # Origin of Muscle 1
    m1_insertion = np.asarray([0.0, 0.15])  # Insertion of Muscle 1

    m2_origin = np.asarray([0.0, 0.8])  # Origin of Muscle 2
    m2_insertion = np.asarray([0.0, -0.3])  # Insertion of Muscle 2
    # Attach the muscles
    muscles.attach(np.asarray([m1_origin, m1_insertion]),
                   np.asarray([m2_origin, m2_insertion]))

    ########## ADD SYSTEMS ##########
    # Create a system with Pendulum and Muscles using the System Class
    # Check System.py for more details on System class
    sys = System()  # Instantiate a new system
    sys.add_pendulum_system(pendulum)  # Add the pendulum model to the system
    sys.add_muscle_system(muscles)  # Add the muscle model to the system

    ########## INITIALIZATION ##########
    t_max = 2  # Maximum simulation time
    time = np.arange(0., t_max, 0.001)  # Time vector
    ##### Model Initial Conditions #####
    x0_P = np.asarray([np.pi/2, 0.0])  # Pendulum initial condition
    # Muscle Model initial condition
    l_ce_0 = sys.muscle_sys.initialize_muscle_length(np.pi/2)
    x0_M = np.asarray([0.05, l_ce_0[0], 0.05, l_ce_0[1]])
    x0 = np.concatenate((x0_P, x0_M))  # System initial conditions

    ########## System Simulation ##########
    sim = SystemSimulation(sys)  # Instantiate Simulation object
    # Simulate the system for given time
    sim.initalize_system(x0, time)  # Initialize the system state
    return sim


def exercise2():
    """ Main function to run for Exercise 2.

    Parameters
    ----------
        None

    Returns
    -------
        None
        
    """

    '''
    sim = system_init()

    # Add muscle activations to the simulation
    # Here you can define your muscle activation vectors
    # that are time dependent

    act1 = np.ones((len(sim.time), 1)) * 0.05
    act2 = np.ones((len(sim.time), 1)) * 0.05

    activations = np.hstack((act1, act2))

    # Method to add the muscle activations to the simulation

    sim.add_muscle_stimulations(activations)

    #: If you would like to perturb the pedulum model then you could do
    # so by
    sim.sys.pendulum_sys.parameters.PERTURBATION = True
    # The above line sets the state of the pendulum model to zeros between
    # time interval 1.2 < t < 1.25. You can change this and the type of
    # perturbation in
    # pendulum_system.py::pendulum_system function

    # Integrate the system for the above initialized state and time
    sim.simulate()

    # Obtain the states of the system after integration
    # res is np.asarray [time, states]
    # states vector is in the same order as x0
    res = sim.results()

    # In order to obtain internal states of the muscle
    # you can access the results attribute in the muscle class
    muscle_1_results = sim.sys.muscle_sys.muscle_1.results
    muscle_2_results = sim.sys.muscle_sys.muscle_2.results

    # Plotting the results
    plt.figure('Pendulum')
    plt.title('Pendulum Phase')
    plt.plot(res[:, 1], res[:, 2])
    plt.xlabel('Position [rad]')
    plt.ylabel('Velocity [rad.s]')
    plt.grid()
    '''
    
    
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ### code for 2a
    pylog.info("2a")
    
    theta = np.arange(np.pi/4, np.pi*3/4, 0.001)
    
    temp_a1=0.35
    ratios=[0.2, 0.5, 1., 2., 5.,]
    
    L2_s=[]
    h2_s=[]
    
    for temp_ratio in ratios:
        temp_a2=temp_a1*temp_ratio
        temp_L2=np.sqrt(temp_a1*temp_a1+temp_a2*temp_a2+2*temp_a1*temp_a2*np.sin(theta))
        temp_h2=(temp_a1*temp_a2*np.cos(theta))/temp_L2
        
        L2_s=L2_s+[temp_L2]
        h2_s=h2_s+[temp_h2]
    
    


    plt.figure('2a. Relationship between muscle length and pendulum angular position')    
    plt.title('Relationship between  muscle length and pendulum angular position')
    for i in range(len(ratios)):
        plt.plot(theta, L2_s[i])
    plt.xlabel('Angular Position [rad]')
    plt.ylabel('Muscle Length [m]')
    temp_legends=['ratio of a2/a1 = '+ format((temp_ratio),'.2f') for temp_ratio in ratios]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    
    plt.figure('2a. Relationship between moment arm and pendulum angular position')    
    plt.title('Relationship between moment arm and pendulum angular position')
    for i in range(len(ratios)):
        plt.plot(theta, h2_s[i])
    plt.xlabel('Angular Position [rad]')
    plt.ylabel('Moment Arm [m]')
    temp_legends=['ratio of a2/a1 = '+ format((temp_ratio),'.2f') for temp_ratio in ratios]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
 
    
    
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ### code for 2b
    pylog.info("2b")
    
    
    #initialization
    P_params = PendulumParameters()  # Instantiate pendulum parameters
    P_params.L = 1.0  # To change the default length of the pendulum
    P_params.m = 0.25  # To change the default mass of the pendulum
    pendulum = PendulumSystem(P_params)  # Instantiate Pendulum object
    #### CHECK OUT Pendulum.py to ADD PERTURBATIONS TO THE MODEL #####
    pylog.info('Pendulum model initialized \n {}'.format(
        pendulum.parameters.showParameters()))

    ########## MUSCLES ##########
    # Define and Setup your muscle model here
    # Check MuscleSystem.py for more details on MuscleSystem class
    m1_param = MuscleParameters()  # Instantiate Muscle 1 parameters
    m1_param.f_max = 200.  # To change Muscle 1 max force
    m1_param.l_opt = 0.4
    m1_param.l_slack = 0.45
    m2_param = MuscleParameters()  # Instantiate Muscle 2 parameters
    m2_param.f_max = 200.  # To change Muscle 2 max force
    m2_param.l_opt = 0.4
    m2_param.l_slack = 0.45
    m1 = Muscle('m1', m1_param)  # Instantiate Muscle 1 object
    m2 = Muscle('m2', m2_param)  # Instantiate Muscle 2 object
    # Use the MuscleSystem Class to define your muscles in the system
    # Instantiate Muscle System with two muscles
    muscles = MuscleSystem(m1, m2)
    pylog.info('Muscle system initialized \n {} \n {}'.format(
        m1.parameters.showParameters(),
        m2.parameters.showParameters()))
    # Define Muscle Attachment points
    m1_origin = np.asarray([0.0, 0.9])  # Origin of Muscle 1
    m1_insertion = np.asarray([0.0, 0.15])  # Insertion of Muscle 1

    m2_origin = np.asarray([0.0, 0.8])  # Origin of Muscle 2
    m2_insertion = np.asarray([0.0, -0.3])  # Insertion of Muscle 2
    # Attach the muscles
    muscles.attach(np.asarray([m1_origin, m1_insertion]),
                   np.asarray([m2_origin, m2_insertion]))

    ########## ADD SYSTEMS ##########
    # Create a system with Pendulum and Muscles using the System Class
    # Check System.py for more details on System class
    sys = System()  # Instantiate a new system
    sys.add_pendulum_system(pendulum)  # Add the pendulum model to the system
    sys.add_muscle_system(muscles)  # Add the muscle model to the system

    ########## INITIALIZATION ##########
    t_max = 2  # Maximum simulation time
    time = np.arange(0., t_max, 0.001)  # Time vector
    ##### Model Initial Conditions #####
    x0_P = np.asarray([np.pi/2, 0.0])  # Pendulum initial condition
    # Muscle Model initial condition
    l_ce_0 = sys.muscle_sys.initialize_muscle_length(np.pi/2)
    x0_M = np.asarray([0.05, l_ce_0[0], 0.05, l_ce_0[1]])
    x0 = np.concatenate((x0_P, x0_M))  # System initial conditions

    ########## System Simulation ##########
    sim = SystemSimulation(sys)  # Instantiate Simulation object
    # Simulate the system for given time
    sim.initalize_system(x0, time)  # Initialize the system state
    
 
    
    
    omega=1.5
    sin_act_1=np.sin(2*np.pi*omega*time).reshape(len(time),1)
    sin_act_1[sin_act_1<0]=0
    #sin_act_2=np.sin(2*np.pi*omega*time+np.pi/2).reshape(len(time),1)
    sin_act_2=-np.sin(2*np.pi*omega*time).reshape(len(time),1)
    sin_act_2[sin_act_2<0]=0
    activations = np.hstack((sin_act_1,sin_act_2)) 
    
    plt.figure('2b. Activation wave')
    plt.title('Activation wave')
    plt.plot(time, sin_act_1, label='Activation 1')
    plt.plot(time, sin_act_2, label='Activation 2')
    plt.xlabel('Time [s]')
    plt.ylabel('Activation')
    plt.grid()
    plt.legend()
    
    
    # without pertubation
    sim.add_muscle_stimulations(activations)
    sim.initalize_system(x0, time)
    sim.sys.pendulum_sys.parameters.PERTURBATION = False
    sim.simulate()
    res = sim.results()
    muscle1_results = sim.sys.muscle_sys.muscle_1.results
    muscle2_results = sim.sys.muscle_sys.muscle_2.results
    
    
    plt.figure('2b. Limit cycle without pertubation')
    plt.title('Pendulum Phase without pertubation')
    plt.plot(res[:, 1], res[:, 2],)
    plt.xlabel('Position [rad]')
    plt.ylabel('Velocity [rad/s]')
    plt.grid()
    plt.legend()
    
    
    
    # with pertubation
    sim.add_muscle_stimulations(activations)
    sim.initalize_system(x0, time)
    sim.sys.pendulum_sys.parameters.PERTURBATION = True
    sim.simulate()
    res = sim.results()
    muscle1_results = sim.sys.muscle_sys.muscle_1.results
    muscle2_results = sim.sys.muscle_sys.muscle_2.results
    
    
    plt.figure('2b. Limit cycle with pertubation')
    plt.title('Pendulum Phase with pertubation')
    plt.plot(res[:, 1], res[:, 2],)
    plt.xlabel('Position [rad]')
    plt.ylabel('Velocity [rad/s]')
    plt.grid()
    plt.legend()
    
    
    
    
    
    
    
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ### code for 2c
    pylog.info("2c")
    
    # different frequencies
    omegas=1.5*np.array([0.2,0.5,1.,2.,5.])
    
    positions=[]
    vels=[]
    
    for temp_omega in omegas:
        
        sin_act_1=np.sin(2*np.pi*temp_omega*time).reshape(len(time),1)
        sin_act_1[sin_act_1<0]=0
        sin_act_2=-np.sin(2*np.pi*temp_omega*time).reshape(len(time),1)
        sin_act_2[sin_act_2<0]=0
        activations = np.hstack((sin_act_1,sin_act_2)) 
        
        sim.add_muscle_stimulations(activations)
        sim.initalize_system(x0, time)
        sim.sys.pendulum_sys.parameters.PERTURBATION = False
        sim.simulate()
        res = sim.results()
        muscle1_results = sim.sys.muscle_sys.muscle_1.results
        muscle2_results = sim.sys.muscle_sys.muscle_2.results
        
        positions=positions+[res[:, 1]]
        vels=vels+[res[:,2]]
    
    
    plt.figure('2c.Pendulum phase plane with stimulation frequencies')    
    plt.title('Pendulum phase plane with stimulation frequencies')
    for i in range(len(ratios)):
        plt.plot(positions[i], vels[i])
    plt.xlabel('Angular Position [rad]')
    plt.ylabel('Muscle Length [m]')
    temp_legends=['ratio of frequency = '+ format((temp_omega/1.5),'.2f') for temp_omega in omegas]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    
    
    '''
    # different frequencies
    omegas=1.5*np.array([0.2,0.5,1.,2.,5.])
    
    positions=[]
    vels=[]
    
    for temp_omega in omegas:
        
        sin_act_1=np.sin(2*np.pi*temp_omega*time).reshape(len(time),1)
        sin_act_1[sin_act_1<0]=0
        sin_act_2=np.sin(2*np.pi*temp_omega*(np.pi/6+time)).reshape(len(time),1)
        sin_act_2[sin_act_2<0]=0
        activations = np.hstack((sin_act_1,sin_act_2)) 
        
        sim.add_muscle_stimulations(activations)
        sim.initalize_system(x0, time)
        sim.sys.pendulum_sys.parameters.PERTURBATION = False
        sim.simulate()
        res = sim.results()
        muscle1_results = sim.sys.muscle_sys.muscle_1.results
        muscle2_results = sim.sys.muscle_sys.muscle_2.results
        
        positions=positions+[res[:, 1]]
        vels=vels+[res[:,2]]
    
    
    plt.figure('2c.Pendulum phase plane with stimulation frequencies')    
    plt.title('Pendulum phase plane with stimulation frequencies')
    for i in range(len(ratios)):
        plt.plot(positions[i], vels[i])
    plt.xlabel('Angular Position [rad]')
    plt.ylabel('Muscle Length [m]')
    temp_legends=['ratio of frequency = '+ format((temp_omega/1.5),'.2f') for temp_omega in omegas]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    '''
    
    
    
    
    
    
    
    

    # To animate the model, use the SystemAnimation class
    # Pass the res(states) and systems you wish to animate
    simulation = SystemAnimation(
        res, sim.sys.pendulum_sys, sim.sys.muscle_sys
    )
    if not DEFAULT["save_figures"]:
        # To start the animation
        simulation.animate()
        plt.show()
    else:
        figures = plt.get_figlabels()
        pylog.debug("Saving figures:\n{}".format(figures))
        for fig in figures:
            plt.figure(fig)
            save_figure(fig)
            plt.close(fig)


if __name__ == '__main__':
    from cmcpack import parse_args
    parse_args()
    exercise2()

