""" Lab 5 - Exercise 1 """

import matplotlib.pyplot as plt
import numpy as np

import farms_pylog as pylog
from muscle import Muscle
from mass import Mass
from cmcpack import DEFAULT, parse_args
from cmcpack.plot import save_figure
from system_parameters import MuscleParameters, MassParameters
from isometric_muscle_system import IsometricMuscleSystem
from isotonic_muscle_system import IsotonicMuscleSystem

DEFAULT["label"] = [r"$\theta$ [rad]", r"$d\theta/dt$ [rad/s]"]

# Global settings for plotting
# You may change as per your requirement
plt.rc('lines', linewidth=2.0)
plt.rc('font', size=12.0)
plt.rc('axes', titlesize=14.0)     # fontsize of the axes title
plt.rc('axes', labelsize=14.0)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=14.0)    # fontsize of the tick labels
plt.rc('ytick', labelsize=14.0)    # fontsize of the tick labels

DEFAULT["save_figures"] = True


def exercise1a():
    """ Exercise 1a
    The goal of this exercise is to understand the relationship
    between muscle length and tension.
    Here you will re-create the isometric muscle contraction experiment.
    To do so, you will have to keep the muscle at a constant length and
    observe the force while stimulating the muscle at a constant activation."""

    # Defination of muscles
    parameters = MuscleParameters()
    pylog.warning("Loading default muscle parameters")
    pylog.info(parameters.showParameters())
    pylog.info("Use the parameters object to change the muscle parameters")

    # Create muscle object
    muscle = Muscle(parameters)

    pylog.warning("Isometric muscle contraction to be completed")

    # Instatiate isometric muscle system
    sys = IsometricMuscleSystem()

    # Add the muscle to the system
    sys.add_muscle(muscle)

    # You can still access the muscle inside the system by doing
    # >>> sys.muscle.l_opt # To get the muscle optimal length
    #x0 = [0.0, sys.muscle.L_OPT]
    
    

    # Evalute for a single muscle stretch
    muscle_stretch = 0.2

    # Evalute for a single muscle stimulation
    muscle_stimulation = 1.

    # Set the initial condition
    x0 = [0.0, sys.muscle.l_opt]
    # x0[0] --> muscle stimulation intial value
    # x0[1] --> muscle contracticle length initial value

    # Set the time for integration
    t_start = 0.0
    t_stop = 0.2
    time_step = 0.001

    time = np.arange(t_start, t_stop, time_step)
    
    
        # Run the integration
   
    result = sys.integrate(x0=x0,
                           time=time,
                           time_step=time_step,
                           stimulation=muscle_stimulation,
                           muscle_length=muscle_stretch)

    # Plotting
    plt.figure('Isometric muscle experiment')
    plt.plot(result.time, result.l_ce)
    plt.title('Isometric muscle experiment')
    plt.xlabel('Time [s]')
    plt.ylabel('Muscle contracticle length [m]')
    plt.grid()
    
    
    
    
    muscle_stretches = np.arange(0,muscle_stretch,0.001)
    
    
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ### code for 1a
    pylog.info(
        "1a. relationship between forces and contractile element length")
    
    length_start = 0.0
    length_stop = 0.3
    length_step = 0.005
    muscle_lengths = np.arange(length_start, length_stop, length_step)

    active_forces=[]
    passive_forces=[]
    total_forces=[]
    element_lengths=[]
    
    for temp_length in muscle_lengths:
        
        temp_result = sys.integrate(x0=x0,
                       time=time,
                       time_step=time_step,
                       stimulation=muscle_stimulation,
                       muscle_length=temp_length)
        temp_active_force=temp_result.active_force[-1]
        temp_passive_force=temp_result.passive_force[-1]
        tenp_total_force=temp_active_force+temp_passive_force
        temp_element_length=temp_result.l_ce[-1]
        
        active_forces=active_forces+[temp_active_force]
        passive_forces=passive_forces+[temp_passive_force]
        total_forces=total_forces+[tenp_total_force]
        element_lengths=element_lengths+[temp_element_length]
    
    
    plt.figure("1a. Isometric muscle experiment (muscle_stimulation == 1)")
    plt.plot(element_lengths,active_forces)
    plt.plot(element_lengths,passive_forces)
    plt.plot(element_lengths,total_forces)
    plt.title('Isometric Muscle Experiment (muscle_stimulation == 1)')
    plt.xlabel('Muscle contracticle length [m]')
    plt.ylabel('Tension [N]')
    plt.legend(("Active Force","Passive Force","Total force"))
    plt.grid()
    plt.show()
    
    
    
    
    
    
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ### code for 1b
    pylog.info(
        "1b. relationship between forces and contractile element length with different stimulations")
    
    length_start = 0.0
    length_stop = 0.3
    length_step = 0.005
    muscle_lengths = np.arange(length_start, length_stop, length_step)
    
    muscle_stimulations = np.arange(0,muscle_stimulation+0.1,0.1)
    
    all_active_forces=[]
    all_passive_forces=[]
    all_total_forces=[]
    all_element_lengths=[]
    
    
    for temp_muscle_stimulation in muscle_stimulations:
        temp_active_forces=[]
        temp_passive_forces=[]
        temp_total_forces=[]
        temp_element_lengths=[]
        
        for temp_length in muscle_lengths:
            temp_result = sys.integrate(x0=x0,
                           time=time,
                           time_step=time_step,
                           stimulation=temp_muscle_stimulation,
                           muscle_length=temp_length)
            temp_active_force=temp_result.active_force[-1]
            temp_passive_force=temp_result.passive_force[-1]
            tenp_total_force=temp_active_force+temp_passive_force
            temp_element_length=temp_result.l_ce[-1]

            temp_active_forces=temp_active_forces+[temp_active_force]
            temp_passive_forces=temp_passive_forces+[temp_passive_force]
            temp_total_forces=temp_total_forces+[tenp_total_force]
            temp_element_lengths=temp_element_lengths+[temp_element_length]
        
        all_active_forces=all_active_forces+[temp_active_forces]
        all_passive_forces=all_passive_forces+[temp_passive_forces]
        all_total_forces=all_total_forces+[temp_total_forces]
        all_element_lengths=all_element_lengths+[temp_element_lengths]
        
        
    plt.figure('1b. Isometric muscle experiment for active forces with different stimulations')
    for i in range(len(muscle_stimulations)):
        plt.plot(all_element_lengths[i], all_active_forces[i])
    plt.title('Isometric muscle experiment for active forces with different stimulations')
    plt.xlabel('Muscle contracticle length [m]')
    plt.ylabel('Tension [N]')
    temp_legends=['stimulation = '+ format((temp_stimulation),'.1f') for temp_stimulation in muscle_stimulations]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    
    plt.figure('1b. Isometric muscle experiment for passive forces with different stimulations')
    for i in range(len(muscle_stimulations)):
        plt.plot(all_element_lengths[i], all_passive_forces[i])
    plt.title('Isometric muscle experiment for passive forces with different stimulations')
    plt.xlabel('Muscle contracticle length [m]')
    plt.ylabel('Tension [N]')
    temp_legends=['stimulation = '+ format((temp_stimulation),'.1f') for temp_stimulation in muscle_stimulations]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    
    plt.figure('1b. Isometric muscle experiment for total forces with different stimulations')
    for i in range(len(muscle_stimulations)):
        plt.plot(all_element_lengths[i], all_total_forces[i])
    plt.title('Isometric muscle experiment for total forces with different stimulations')
    plt.xlabel('Muscle contracticle length [m]')
    plt.ylabel('Tension [N]')
    temp_legends=['stimulation = '+ format((temp_stimulation),'.1f') for temp_stimulation in muscle_stimulations]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    
    
    
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ### code for 1c
    pylog.info(
        "1c. relationship between forces and contractile element length with different fiber lengths")
    
    short_opt=0.08
    #medium_opt=0.1
    long_opt=0.10
    opt_range=[short_opt,long_opt]
    
    muscle_stimulation=1.
    
    length_start = 0.0
    length_stop = 0.3
    length_step = 0.005
    muscle_lengths = np.arange(length_start, length_stop, length_step)
    
    active_forces=[]
    passive_forces=[]
    total_forces=[]
    element_lengths=[]
    
    for temp_opt in opt_range:
        
        parameters = MuscleParameters(l_opt=temp_opt)
        muscle = Muscle(parameters)
        sys = IsometricMuscleSystem()
        sys.add_muscle(muscle)
        #muscle.L_OPT = temp_opt
        
        temp_active_forces=[]
        temp_passive_forces=[]
        temp_total_forces=[]
        temp_element_lengths=[]
        
        for temp_length in muscle_lengths:
            temp_result = sys.integrate(x0=x0,
                           time=time,
                           time_step=time_step,
                           stimulation=muscle_stimulation,
                           muscle_length=temp_length)
            temp_active_force=temp_result.active_force[-1]
            temp_passive_force=temp_result.passive_force[-1]
            tenp_total_force=temp_active_force+temp_passive_force
            temp_element_length=temp_result.l_ce[-1]

            temp_active_forces=temp_active_forces+[temp_active_force]
            temp_passive_forces=temp_passive_forces+[temp_passive_force]
            temp_total_forces=temp_total_forces+[tenp_total_force]
            temp_element_lengths=temp_element_lengths+[temp_element_length]
            
        active_forces=active_forces+[temp_active_forces]
        passive_forces=passive_forces+[temp_passive_forces]
        total_forces=total_forces+[temp_total_forces]
        element_lengths=element_lengths+[temp_element_lengths]
                  
            
    plt.figure("1c. Isometric muscle experiment with different musle fiber lengths" )  
    for i in range(2):
        plt.plot(element_lengths[i],active_forces[i])
        plt.plot(element_lengths[i],passive_forces[i])
        plt.plot(element_lengths[i],total_forces[i])
    plt.xlabel('Muscle contracticle length [m]')
    plt.ylabel('Tension [N]')
    plt.title("Isometric muscle experiment with different musle fiber lengths") 
    plt.legend(["Active Force: musle fiber lengths=0.08","Passive Force musle: fiber lengths=0.08","Total Force: musle fiber lengths=0.08",
            "Active Force: musle fiber lengths=0.10","Passive Force musle: fiber lengths=0.10","Total Force: musle fiber lengths=0.10" ] )
    plt.grid()
    plt.show()
            



def exercise1d():
    """ Exercise 1d

    Under isotonic conditions external load is kept constant.
    A constant stimulation is applied and then suddenly the muscle
    is allowed contract. The instantaneous velocity at which the muscle
    contracts is of our interest."""

    # Defination of muscles
    muscle_parameters = MuscleParameters()
    print(muscle_parameters.showParameters())

    mass_parameters = MassParameters()
    print(mass_parameters.showParameters())

    # Create muscle object
    muscle = Muscle(muscle_parameters)

    # Create mass object
    mass = Mass(mass_parameters)

    pylog.warning("Isotonic muscle contraction to be implemented")

    # Instatiate isotonic muscle system
    sys = IsotonicMuscleSystem()

    # Add the muscle to the system
    sys.add_muscle(muscle)

    # Add the mass to the system
    sys.add_mass(mass)

    # You can still access the muscle inside the system by doing
    # >>> sys.muscle.l_opt # To get the muscle optimal length

    # Evalute for a single load
    load = 250/9.81

    # Evalute for a single muscle stimulation
    muscle_stimulation = 1.0

    # Set the initial condition
    x0 = [0.0, sys.muscle.l_opt,
          sys.muscle.l_opt + sys.muscle.l_slack, 0.0]
    # x0[0] - -> activation
    # x0[1] - -> contractile length(l_ce)
    # x0[2] - -> position of the mass/load
    # x0[3] - -> velocity of the mass/load

    # Set the time for integration
    t_start = 0.0
    t_stop = 0.4
    time_step = 0.001
    time_stabilize = 0.2

    time = np.arange(t_start, t_stop, time_step)

    # Run the integration
    result = sys.integrate(x0=x0,
                           time=time,
                           time_step=time_step,
                           time_stabilize=time_stabilize,
                           stimulation=muscle_stimulation,
                           load=load
                           )

    # Plotting
    plt.figure('Isotonic muscle experiment')
    plt.plot(result.time,
             result.v_ce)
    plt.title('Isotonic muscle experiment')
    plt.xlabel('Time [s]')
    plt.ylabel('Muscle contracticle velocity [lopts/s]')
    plt.grid()
    
    
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ### code for 1d
    pylog.info(
        "1d. relationship between muscle contractile velocity and external load")
    
    load_start = 1
    load_stop = 501
    load_step = 10
    load_range=np.arange(load_start, load_stop, load_step)
    
    muscle_stimulation = 1.0
    
    vels=[]
    tendon_forces=[]
    active_forces=[]
    passive_forces=[]
    total_forces=[]
    
    for temp_load in load_range:
        temp_result = sys.integrate(x0=x0,
                           time=time,
                           time_step=time_step,
                           time_stabilize=time_stabilize,
                           stimulation=muscle_stimulation,
                           load=temp_load)     
        
        temp_tendon_force=temp_result.tendon_force[-1]
        temp_active_force=temp_result.active_force[-1]
        temp_passive_force=temp_result.passive_force[-1]
        temp_total_force=temp_active_force+temp_passive_force
        
        tendon_forces=tendon_forces+[temp_tendon_force]
        active_forces=active_forces+[temp_active_force]
        passive_forces=passive_forces+[temp_passive_force]
        total_forces=total_forces+[temp_total_force]
        
        temp_l_mtu=temp_result.l_mtu[-1]
        
        if temp_l_mtu < sys.muscle.l_opt + sys.muscle.l_slack:
            vels=vels+[np.min(temp_result.v_ce)]
        else:
            vels=vels+[np.max(temp_result.v_ce)]
            
            
    plt.figure('1d. Isotonic muscle experiment for tension and contractile velocities')
    plt.plot(vels,tendon_forces)
    plt.plot(vels,load_range)
    plt.plot(vels,active_forces)
    plt.plot(vels,passive_forces)
    plt.plot(vels,total_forces)
    plt.title('Isotonic muscle experiment for tension and contractile velocities')
    plt.xlabel('Muscle contracticle velocity [lopts/s]')
    plt.ylabel('Tension [N]')
    plt.legend(("Tendon Force","Load","Active Force","Passive Force","Total force"))
    plt.grid()
    plt.show()

    
        
        
        
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################    
    ### code for 1f
    
   
   
    
    pylog.info(
        "1f. relationship between muscle contractile velocity and external load with different stimulations")
    
    muscle_stimulations = np.arange(0,muscle_stimulation+0.1,0.1)
    
    load_start = 1
    load_stop = 501
    load_step = 10
    load_range=np.arange(load_start, load_stop, load_step)
    
    all_vels=[]
    all_tendon_forces=[]
    
    for temp_muscle_stimulation in muscle_stimulations:
        
        temp_vels=[]
        temp_tendon_forces=[]
        
        for temp_load in load_range:
            temp_result = sys.integrate(x0=x0,
                               time=time,
                               time_step=time_step,
                               time_stabilize=time_stabilize,
                               stimulation=temp_muscle_stimulation,
                               load=temp_load) 
            
            temp_tendon_force=temp_result.tendon_force[-1]
            temp_tendon_forces=temp_tendon_forces+[temp_tendon_force]
            
            temp_l_mtu=temp_result.l_mtu[-1]

            if temp_l_mtu < sys.muscle.l_opt + sys.muscle.l_slack:
                temp_vels=temp_vels+[np.min(temp_result.v_ce)]
            else:
                temp_vels=temp_vels+[np.max(temp_result.v_ce)]
                
        all_vels=all_vels+[temp_vels]
        all_tendon_forces=all_tendon_forces+[temp_tendon_forces]
    
    plt.figure('1f. Isotonic muscle experiment for loads and contractile velocities with different stimulations')
    for i in range(len(muscle_stimulations)):
        plt.plot( all_vels[i],load_range)
    plt.title('Isotonic muscle experiment for loads and contractile velocities with different stimulations')
    plt.xlabel('Muscle contracticle velocity [lopts/s]')
    plt.ylabel('Tension [N]')
    temp_legends=['stimulation = '+ format((temp_stimulation),'.1f') for temp_stimulation in muscle_stimulations]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
    
    plt.figure('1f. Isotonic muscle experiment for tendon forces and contractile velocities with different stimulations')
    for i in range(len(muscle_stimulations)):
        plt.plot( all_vels[i],all_tendon_forces[i])
    plt.title('Isotonic muscle experiment for tendon forces and contractile velocities with different stimulations')
    plt.xlabel('Muscle contracticle velocity [lopts/s]')
    plt.ylabel('Tension [N]')
    temp_legends=['stimulation = '+ format((temp_stimulation),'.1f') for temp_stimulation in muscle_stimulations]
    plt.legend(temp_legends)
    plt.grid()
    plt.show()
 
 
               
 


def exercise1():
    exercise1a()
    exercise1d()

    if DEFAULT["save_figures"] is False:
        plt.show()
    else:
        figures = plt.get_figlabels()
        print(figures)
        pylog.debug("Saving figures:\n{}".format(figures))
        for fig in figures:
            plt.figure(fig)
            save_figure(fig)
            plt.close(fig)


if __name__ == '__main__':
    from cmcpack import parse_args
    parse_args()
    exercise1()

