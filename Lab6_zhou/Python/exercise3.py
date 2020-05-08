""" Lab 6 Exercise 3
This file implements the pendulum system with two muscles attached driven
by a neural network
"""

import numpy as np
from matplotlib import pyplot as plt
import farms_pylog as pylog
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
plt.rc('axes', labelsize=14.0)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=14.0)    # fontsize of the tick labels
plt.rc('ytick', labelsize=14.0)    # fontsize of the tick labels


def system_init():
    """ Use this function to create a new default system. """
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

    ########## Network ##########
    # The network consists of four neurons
    N_params = NetworkParameters()  # Instantiate default network parameters
    N_params.D = 2.  # To change a network parameter
    # Similarly to change w -> N_params.w = (4x4) array

    # Create a new neural network with above parameters
    neural_network = NeuralSystem(N_params)
    pylog.info('Neural system initialized \n {}'.format(
        N_params.showParameters()))

    ########## ADD SYSTEMS ##########
    # Create system of Pendulum, Muscles and neural network using SystemClass
    # Check System.py for more details on System class
    sys = System()  # Instantiate a new system
    sys.add_pendulum_system(pendulum)  # Add the pendulum model to the system
    sys.add_muscle_system(muscles)  # Add the muscle model to the system
    # Add the neural network to the system
    sys.add_neural_system(neural_network)

    ##### Time #####
    t_max = 6  # Maximum simulation time
    time = np.arange(0., t_max, 0.001)  # Time vector

    ##### Model Initial Conditions #####
    x0_P = np.asarray([np.pi/2, 0.])  # Pendulum initial condition

    # Muscle Model initial condition
    l_ce_0 = sys.muscle_sys.initialize_muscle_length(np.pi/2)
    x0_M = np.asarray([0.05, l_ce_0[0], 0.05, l_ce_0[1]])

    x0_N = np.asarray([-0.5, 1, 0.5, 1])  # Neural Network Initial Conditions

    x0 = np.concatenate((x0_P, x0_M, x0_N))  # System initial conditions

    ##### System Simulation #####
    # For more details on System Simulation check SystemSimulation.py
    # SystemSimulation is used to initialize the system and integrate
    # over time
    sim = SystemSimulation(sys)  # Instantiate Simulation object
    sim.initalize_system(x0, time)  # Initialize the system state
    return sim


def exercise3():
    """ Main function to run for Exercise 3.

    Parameters
    ----------
        None

    Returns
    -------
        None
    """

    '''
    # Create system
    sim = system_init()

    # Add external inputs to neural network
    sim.add_external_inputs_to_network(np.ones((len(sim.time), 4)))

    # Integrate the system for the above initialized state and time
    sim.simulate()

    # Obtain the states of the system after integration
    # res is np.asarray [time, states]
    # states vector is in the same order as x0
    res = sim.results()

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
       

    

    ######################################################

    #  initialization
    ########## PENDULUM ##########
    P_params = PendulumParameters()  
    P_params.L = 1.0  
    P_params.m = 0.25  
    pendulum = PendulumSystem(P_params)  

    pylog.info('Pendulum model initialized \n {}'.format(
        pendulum.parameters.showParameters()))

    ########## MUSCLES ##########
    m1_param = MuscleParameters() 
    m1_param.f_max = 200. 
    m1_param.l_opt = 0.4
    m1_param.l_slack = 0.45
    m2_param = MuscleParameters()  
    m2_param.f_max = 200.  
    m2_param.l_opt = 0.4
    m2_param.l_slack = 0.45
    m1 = Muscle('m1', m1_param)  
    m2 = Muscle('m2', m2_param)  
    muscles = MuscleSystem(m1, m2)
    
    pylog.info('Muscle system initialized \n {} \n {}'.format(
        m1.parameters.showParameters(),
        m2.parameters.showParameters()))

    

    ######## Define Muscle Attachment points
    m1_origin = np.asarray([0.0, 0.9])  
    m1_insertion = np.asarray([0.0, 0.15])  
    m2_origin = np.asarray([0.0, 0.8])  
    m2_insertion = np.asarray([0.0, -0.3]) 
    muscles.attach(np.asarray([m1_origin, m1_insertion]),
                   np.asarray([m2_origin, m2_insertion]))

    ##### Time #####
    t_max = 6
    time = np.arange(0., t_max, 0.001)  

 
  
    
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ### code for 3a
    
    # without perturbation
    pylog.info("3a")
 
    
    d = 1.
    tau = np.array([0.02, 0.02, 0.1, 0.1])
    b = np.array([3., 3., -3., -3.])
    w=np.zeros((4,4))
    w[0,1]=w[0,3]=w[1,0]=w[1,2]=-5
    w[0,2]=w[1,3]=5
    w[2,0]=w[3,1]=-5
    w=w.T
    
    N_params = NetworkParameters()
    N_params.D = d
    N_params.tau = tau
    N_params.b = b
    N_params.w=w
    neural_network = NeuralSystem(N_params)
    
    sys = System()  
    sys.add_pendulum_system(pendulum)  
    sys.add_muscle_system(muscles)  
    sys.add_neural_system(neural_network)
    
    x0_P = np.asarray([np.pi/2, 0.])
    l_ce_0 = sys.muscle_sys.initialize_muscle_length(np.pi/2)
    x0_M = np.asarray([0.05, l_ce_0[0], 0.05, l_ce_0[1]])
    x0_N = np.asarray([-0.5, 1, 0.5, 1])  
    x0 = np.concatenate((x0_P, x0_M, x0_N))
   
    sim = SystemSimulation(sys)  
    sim.initalize_system(x0, time) 
    sim.simulate()
    res = sim.results()
    
    positions=res[:,1]
    vels=res[:,2]
    
    plt.figure('3a. Activation with time ')
    plt.title('Activation with time')
    plt.plot(res[:, 0], res[:, 3], label="Activation 1")
    plt.plot(res[:, 0], res[:, 5], label="Activation 2")
    plt.xlabel('Time [s]')
    plt.ylabel('Activation')
    plt.legend()
    plt.grid()
    plt.show()

    # Plotting the results
    plt.figure('3a. Pendulum state with time')
    plt.title('Pendulum state with time')
    plt.plot(res[:, 0], positions)
    plt.xlabel('Time [s]')
    plt.ylabel('Position [rad]')
    plt.grid()
    plt.show()

    # Plotting the results
    plt.figure('3a. Pendulum phase plot')
    plt.title('Pendulum phase plot')
    plt.plot(positions, vels)
    plt.xlabel('Position [rad]')
    plt.ylabel('Velocity [rad/s]')
    plt.grid()
    plt.show()
    
    
    
    
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ###########################################################
    ### code for 3b
    pylog.info("3b")
    
    all_positions=[]
    all_vels=[]
    all_time=[]
    all_act_1=[]
    all_act_2=[]
    
    external_drives=np.array([0.5, 1., 2.])
    for temp_drive in external_drives:
        sim = SystemSimulation(sys)  
        sim.initalize_system(x0, time) 
        sim.add_external_inputs_to_network(np.ones((len(sim.time), 4))*temp_drive)
        sim.simulate()
        res = sim.results()
        
        
        all_time=all_time+[res[:,0]]
        all_positions=all_positions+[res[:,1]]
        all_vels=all_vels+[res[:,2]]
        all_act_1=all_act_1+[res[:,3]]
        all_act_2=all_act_2+[res[:,5]]
        
    plt.figure('3a. Activation with time by different external drives')
    plt.title('Activation with time by different external drives')
    for i in range(len(external_drives)):
        plt.plot(all_time[i], all_act_1[i])
        plt.plot(all_time[i], all_act_2[i])
    plt.xlabel('Time [s]')
    plt.ylabel('Activation')
    temp_legends=['Activation 1: external drive: = 0.5' , 'Activation 2: external drive: = 0.5',
                 'Activation 1: external drive: = 1.0' , 'Activation 2: external drive: = 1.0',
                 'Activation 1: external drive: = 2.0' , 'Activation 2: external drive: = 2.0']
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    
        
    plt.figure('3b. Pendulum state with time by different external drives')
    plt.title('Pendulum state with time by different external drives')
    for i in range(len(external_drives)):
        plt.plot(all_time[i], all_positions[i])
    plt.xlabel('Time [s]')
    plt.ylabel('Position [rad]')
    temp_legends=['external drive: '+ format((temp_drive),'.2f') for temp_drive in external_drives]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    
    plt.figure('3a. Pendulum phase plot by different external drives')
    plt.title('Pendulum phase plot by different external drives')
    for i in range(len(external_drives)):
        plt.plot(all_positions[i], all_vels[i])
    plt.xlabel('Position [rad]')
    plt.ylabel('Velocity [rad/s]')
    temp_legends=['external drive: '+ format((temp_drive),'.2f') for temp_drive in external_drives]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    
    
      
    
    

    # To animate the model, use the SystemAnimation class
    # Pass the res(states) and systems you wish to animate
    simulation = SystemAnimation(
        res, sim.sys.pendulum_sys, sim.sys.muscle_sys, sim.sys.neural_sys)

    if DEFAULT["save_figures"] is False:
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
    exercise3()

