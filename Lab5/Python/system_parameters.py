""" Lab 5 : System Parameters """

import numpy as np
import farms_pylog as pylog


class SystemParameters(object):
    """Parent class providing main attributes for other sub system parameters.
    """

    def __init__(self, name='System'):
        super(SystemParameters, self).__init__()
        self. name = name

    def showParameters(self):
        raise NotImplementedError()

    def msg(self, parameters, units, endl="\n" + 4 * " "):
        """ Message """
        to_print = ("{} parameters : ".format(self.name)) + endl
        for param in parameters:
            to_print += (
                "{} : {} [{}]".format(
                    param, parameters[param], units[param]
                )
            ) + endl
        return to_print


class MuscleParameters(SystemParameters):
    """ Muscle parameters

    with:
        Muscle Parameters:
            - l_slack : Tendon slack length [m]
            - l_opt : Contracticle element optimal fiber length [m]
            - f_max : Maximum force produced by the muscle [N]
            - v_max : Maximum velocity of the contracticle element [m/s]
            - pennation : Fiber pennation angle

    Examples:

        >>> muscle_parameters = MuscleParameters(l_slack=0.2, l_opt=0.1)

    Note that not giving arguments to instanciate the object will result in the
    following default values:
        # Muscle Parameters
        - l_slack = 0.13
        - l_opt = 0.11
        - f_max = 1500
        - v_max = 1.2
        - pennation = 1.

    These parameter variables can then be called from within the class using
    for example:

        To assign a new value to the object variable from within the class:

        >>> self.l_slack = 0.2 # Reassign tendon slack constant

        To assign to another variable from within the class:

        >>> example_l_slack = self.l_slack

    You can display the parameters using:

    >>> muscle_parameters = MuscleParameters()
    >>> print(muscle_parameters,showParameters())
    Muscle parameters :
            f_max : 1500 [N]
            v_max : 1.2 [m/s]
            pennation : 1 []
            l_slack : 0.13 [m]
            l_opt : 0.11 [m]

    Or using pylog:

    >>> muscle_parameters = MuscleParameters()
    >>> pylog.info(muscle_parameters.showParameters())
    """

    def __init__(self, **kwargs):
        super(MuscleParameters, self).__init__('Muscle')
        self.parameters = {}
        self.units = {}

        self.units['l_slack'] = 'm'
        self.units['l_opt'] = 'm'
        self.units['f_max'] = 'N'
        self.units['v_max'] = 'm/s'
        self.units['pennation'] = ''

        self.parameters['l_slack'] = kwargs.pop('l_slack', 0.13)
        self.parameters['l_opt'] = kwargs.pop('l_opt', 0.11)
        self.parameters['f_max'] = kwargs.pop('f_max', 1500)
        self.parameters['v_max'] = kwargs.pop('v_max', -12)
        self.parameters['pennation'] = kwargs.pop('pennation', 1)

    @property
    def l_slack(self):
        """ Muscle Tendon Slack length [m]  """
        return self.parameters['l_slack']

    @l_slack.setter
    def l_slack(self, value):
        """ Keyword Arguments:
            value -- Muscle Tendon Slack Length [m]"""
        self.parameters['l_slack'] = value

    @property
    def l_opt(self):
        """ Muscle Optimal Fiber Length [m]  """
        return self.parameters['l_opt']

    @l_opt.setter
    def l_opt(self, value):
        """ Keyword Arguments:
        value -- Muscle Optimal Fiber Length [m]"""
        self.parameters['l_opt'] = value

    @property
    def f_max(self):
        """ Maximum tendon force produced by the muscle [N]  """
        return self.parameters['f_max']

    @f_max.setter
    def f_max(self, value):
        """ Keyword Arguments:
        value -- Maximum tendon force produced by the muscle [N]"""
        self.parameters['f_max'] = value

    @property
    def v_max(self):
        """ Maximum velocity of the contractile element [m/s]  """
        return self.parameters['v_max']

    @v_max.setter
    def v_max(self, value):
        """ Keyword Arguments:
        value -- Maximum velocity of the contractile element [m/s] """
        self.parameters['v_max'] = value

    @property
    def pennation(self):
        """ Muscle fiber pennation angle  """
        return self.parameters['pennation']

    @pennation.setter
    def pennation(self, value):
        """ Keyword Arguments:
            value -- Muscle fiber pennation angle """
        self.parameters['pennation'] = value

    def showParameters(self):
        return self.msg(self.parameters, self.units)


class MassParameters(SystemParameters):
    """ Mass parameters

    with:
        Mass Parameters:
            - g : Mass system gravity [m/s**2]
            - mass : Mass of the object [kg]

    Examples:

        >>> mass_parameters = MassParameters(g = 9.81, mass = 9.81)

    Note that not giving arguments to instanciate the object will result in the
    following default values:
        # Mass Parameters
        - g = 9.81
        - mass = 10.

    These parameter variables can then be called from within the class using
    for example:

        To assign a new value to the object variable from within the class:

        >>> self.g = 10.0 # Reassign gravity constant

        To assign to another variable from within the class:

        >>> example_g = self.g

    You can display the parameters using:

    >>> mass_parameters = MassParameters()
    >>> print(mass_parameters,showParameters())
    Mass parameters :
            g : 9.81 [m/s**2]
            mass : 10. [kg]

    Or using pylog:

    >>> mass_parameters = MassParameters()
    >>> pylog.info(mass_parameters.showParameters())
    """

    def __init__(self, **kwargs):
        super(MassParameters, self).__init__('Mass')
        self.parameters = {}
        self.units = {}

        self.units['g'] = 'm/s**2'
        self.units['mass'] = 'kg'

        self.parameters['g'] = kwargs.pop('g', 9.81)
        self.parameters['mass'] = kwargs.pop('mass', 10.)

    @property
    def g(self):
        """ Get the value of gravity in mass   """
        return self.parameters['g']

    @g.setter
    def g(self, value):
        """ Keyword Arguments:
            value --  Set the value of gravity"""
        self.parameters["g"] = value

    @property
    def mass(self):
        """Get the value of mass in the mass system  """
        return self.parameters["mass"]

    @mass.setter
    def mass(self, value):
        """ Keyword Arguments:
            value --  Set the value of mass"""
        if value <= 0.00001:
            pylog.error(
                "Mass you are trying to set is too low!. Setting to 1.")
            value = 1.0
        self.parameters["mass"] = value

    def showParameters(self):
        return self.msg(self.parameters, self.units)


if __name__ == '__main__':
    M = MuscleParameters()
    pylog.debug(M.showParameters())

    Mass = MassParameters()
    pylog.debug(Mass.showParameters())

