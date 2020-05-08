"""Oscillator network ODE"""

import numpy as np

from scipy.integrate import ode
from robot_parameters import RobotParameters


def network_ode(_time, state, robot_parameters):
    """Network_ODE

    Parameters
    ----------
    _time: <float>
        Time
    state: <np.array>
        ODE states at time _time
    robot_parameters: <RobotParameters>
        Instance of RobotParameters

    Return
    ------
    :<np.array>
        Returns derivative of state (phases and amplitudes)
    """
    n_oscillators = robot_parameters.n_oscillators
    phases = state[:n_oscillators]
    amplitudes = state[n_oscillators:2*n_oscillators]
    
    theta=phases
    r=amplitudes
    w=robot_parameters.coupling_weights
    f=robot_parameters.freqs
    phi=robot_parameters.phase_bias
    a=robot_parameters.rates
    R=robot_parameters.nominal_amplitudes
    
    theda_dot=np.zeros_like(theta)
    r_dot=np.zeros_like(r)
    
    for i in range(n_oscillators):
        theta[i]=2*np.pi*f[i]
        r_dot[i]=a[i]*(R[i]-r[i])
        for j in range(n_oscillators):
            theda_dot[i]=theda_dot[i]+r[j]*w[i,j]*np.sin(theta[j]-theta[i]-phi[i,j])

    temp_output=np.concatenate([theda_dot,r_dot])
    
    return temp_output


def motor_output(phases, amplitudes, iteration=None):
    """Motor output.

    Parameters
    ----------
    phases: <np.array>
        Phases of the oscillator
    amplitudes: <np.array>
        Amplitudes of the oscillator

    Returns
    -------
    : <np.array>
        Motor outputs for joint in the system.
    """
    theta=phases
    r=amplitudes
    
    q_dot=np.zeros(14)
    for i in range(14):
        if i<10:
            q_dot[i]=r[i]*(1+np.cos(theta[i]))-r[i+10]*(1+np.cos(theta[i+10]))
        else:
            q_dot[i]=-theta[i+10]
  
    return q_dot


class RobotState(np.ndarray):
    """Robot state"""

    def __init__(self, *_0, **_1):
        super(RobotState, self).__init__()
        self[:] = 0.0

    @classmethod
    def salamandra_robotica_2(cls, n_iterations):
        """State of Salamandra robotica 2"""
        shape = (n_iterations, 2*24)
        return cls(
            shape,
            dtype=np.float64,
            buffer=np.zeros(shape)
        )

    def phases(self, iteration=None):
        """Oscillator phases"""
        return self[iteration, :24] if iteration is not None else self[:, :24]

    def set_phases(self, iteration, value):
        """Set phases"""
        self[iteration, :24] = value

    def set_phases_left(self, iteration, value):
        """Set body phases on left side"""
        self[iteration, :10] = value

    def set_phases_right(self, iteration, value):
        """Set body phases on right side"""
        self[iteration, 10:20] = value

    def set_phases_legs(self, iteration, value):
        """Set leg phases"""
        self[iteration, 20:24] = value

    def amplitudes(self, iteration=None):
        """Oscillator amplitudes"""
        return self[iteration, 24:] if iteration is not None else self[:, 24:]

    def set_amplitudes(self, iteration, value):
        """Set amplitudes"""
        self[iteration, 24:] = value


class SalamandraNetwork:
    """Salamandra oscillator network"""

    def __init__(self, sim_parameters, n_iterations):
        super(SalamandraNetwork, self).__init__()
        # States
        self.state = RobotState.salamandra_robotica_2(n_iterations)
        # Parameters
        self.robot_parameters = RobotParameters(sim_parameters)
        # Set initial state
        # Replace your oscillator phases here
        self.state.set_phases(
            iteration=0,
            value=1e-4*np.random.ranf(self.robot_parameters.n_oscillators),
        )
        # Set solver
        self.solver = ode(f=network_ode)
        self.solver.set_integrator('dopri5')
        self.solver.set_initial_value(y=self.state[0], t=0.0)

    def step(self, iteration, time, timestep):
        """Step"""
        self.solver.set_f_params(self.robot_parameters)
        self.state[iteration+1, :] = self.solver.integrate(time+timestep)

    def outputs(self, iteration=None):
        """Oscillator outputs"""
        # Implement equation here
        temp_output=self.state.amplitudes(iteration=iteration)*np.sin(self.state.phases(iteration=iteration))
        return temp_output

    def get_motor_position_output(self, iteration=None):
        """Get motor position"""
        return motor_output(
            self.state.phases(iteration=iteration),
            self.state.amplitudes(iteration=iteration),
            iteration=iteration,
        )

