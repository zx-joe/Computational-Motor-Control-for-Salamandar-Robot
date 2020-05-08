"""Simulation parameters"""


class SimulationParameters:
    """Simulation parameters"""

    def __init__(self, **kwargs):
        super(SimulationParameters, self).__init__()
        # Default parameters
        self.n_body_joints = 10
        self.n_legs_joints = 4
        self.duration = 30
        self.phase_lag = None
        self.amplitude_gradient = None
        # Feel free to add more parameters (ex: MLR drive)
        # self.drive_mlr = ...
        # ...
        # Update object with provided keyword arguments
        # NOTE: This overrides the previous declarations
        self.drive=2
        self.__dict__.update(kwargs)

