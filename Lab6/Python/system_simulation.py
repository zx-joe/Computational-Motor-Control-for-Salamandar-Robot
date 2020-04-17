import numpy as np
from cmcpack import integrate
import sys


class SystemSimulation(object):
    """System Simulation
    """

    def __init__(self, sys):
        super(SystemSimulation, self).__init__()
        self.sys = sys
        self.muscle_stimulations = None
        self.ext_in = None

    def add_muscle_stimulations(self, act):
        """Function applies the array of muscle stimulations during time
        integration
        Parameters
        ----------
        act: <array>
            2D array of stimulation values for each time instant

        """
        self.muscle_stimulations = act

    def add_external_inputs_to_network(self, ext_in=None):
        """Function to add the external inputs to the neural network

        Parameters
        ----------
        ext_in: np.ndarray
            External inputs to each neuron in the network.
            Range of the inputs is [0, 1]
            The array is np.ndarray containing external inputs to
            each neuron at time t
        """
        self.ext_in = ext_in

    def _get_current_external_input_to_network(self, time):
        """Function to get the current external input to network.

        Parameters
        ----------
        self: type
            description
        time: float
            Current simulation time

        Returns
        -------
        current_ext_in : np.asarray
            Current external input to each neuron at time t
        """

        if self.ext_in is not None:
            index = np.argmin((self.time - time)**2)
            return np.asarray(self.ext_in[index, :])

        return np.zeros(4)

    def _get_current_muscle_stimulation(self, time, state):
        """Function to return the current muscle stimulation
        to be applied during integration.
        """
        if self.sys.systems_list.count('neural') == 1:
            # Apply the stimulation function to the neuron state m
            neural_act = self.sys.neural_sys.n_act(state[6:])
            return np.asarray([neural_act[0], neural_act[1]])
        else:
            if self.muscle_stimulations is not None:
                index = np.argmin((self.time - time)**2)
                return np.asarray(self.muscle_stimulations[index, :])
            else:
                return np.asarray([0.05, 0.05])

    def initalize_system(self, x0, time, *args):
        """Initialize the system to start simulation.

        Parameters
        ----------
        x0: numpy.array
            Initial states of the models on the system
        time: numpy.array
            Time vector for the system to be integrated for
        args: tuple
            external args for the integrator

        """

        self.x0 = x0
        self.time = time
        self.args = args

        # Initialize muscle states
        init_muscle_lce = self.sys.muscle_sys.initialize_muscle_length(
            self.x0[0])

        self.x0[3] = init_muscle_lce[0]
        self.x0[5] = init_muscle_lce[1]

    def derivative(self, state, time, *args):
        """ System derivative
        Parameters
        ----------
        self: type
            description
        state: <array>
            States of the system
        time: <float>
            Current integration time
        args: <list>

        Returns
        -------
        derivative: <np.array>
            Derivative at current integration time
        """
        #: Unwrap the states
        pendulum_states = state[:2]
        muscle_states = state[2:6]
        angle = pendulum_states[0]
        l_ce_1 = muscle_states[1]
        l_ce_2 = muscle_states[3]

        #: Update the muscle system
        self.sys.muscle_sys.update(angle, l_ce_1, l_ce_2)
        #: Get the appropriate muscle stimulations
        muscle_stimulations = self._get_current_muscle_stimulation(
            time, state
        )
        #: Compute muscle system derivative
        m_der = self.sys.muscle_sys.derivative(
            muscle_states, time, muscle_stimulations
        )
        #: Compute pendulum system derivative
        p_der = self.sys.pendulum_sys.pendulum_system(
            time, pendulum_states[0], pendulum_states[1],
            self.sys.muscle_sys.torque
        )

        if (self.sys.systems_list.count('neural') == 1.0):
            self.sys.neural_sys.external_inputs(
                self._get_current_external_input_to_network(time))
            n_der = self.sys.neural_sys.derivative(
                time, state[6:])
            update = np.concatenate((p_der, m_der, n_der), axis=0)
        else:
            update = np.concatenate((p_der, m_der), axis=0)
        return update

    def simulate(self):
        """ Simulate the system. """
        #: Run the integrator fpr specified time
        self.res = integrate(
            self.derivative, self.x0, self.time, args=self.args,
            rk=True, tol=True
        )

    def results(self):
        """Return the state of the system after integration.
        The function adds the time vector to the integrated
        system states."""

        #: Instatiate the muscle results container
        self.sys.muscle_sys.muscle_1.instantiate_result_from_state(
            self.time)
        self.sys.muscle_sys.muscle_2.instantiate_result_from_state(
            self.time)

        angle = self.res[:, 1]
        muscle_1_state = self.res[:, 2:4]
        muscle_2_state = self.res[:, 4:6]

        muscle_1 = self.sys.muscle_sys.muscle_1
        muscle_2 = self.sys.muscle_sys.muscle_2

        for idx, _time in enumerate(self.time):
            #: Compute muscle lengths from angle
            muscle_lengths = self.sys.muscle_sys.update(
                angle[idx], muscle_1_state[idx][0], muscle_2_state[idx][0]
            )
            muscle_1.generate_result_from_state(
                idx, _time, self.sys.muscle_sys.muscle_1_length, muscle_1_state[idx][:])
            muscle_2.generate_result_from_state(
                idx, _time, self.sys.muscle_sys.muscle_2_length, muscle_2_state[idx][:])

        return np.concatenate(
            (np.expand_dims(self.time, axis=1), self.res), axis=1)

