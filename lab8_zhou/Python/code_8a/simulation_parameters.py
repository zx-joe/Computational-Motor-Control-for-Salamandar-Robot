"""Simulation parameters"""
import numpy as np
import math

class SimulationParameters:
    """Simulation parameters"""

    def __init__(self, **kwargs):
        super(SimulationParameters, self).__init__()
        # Default parameters
        self.n_body_joints = 10
        self.n_legs_joints = 4
        self.duration = 30
        self.phase_lag = 0.2*np.pi
        self.amplitude_gradient = [1,1]
        # Feel free to add more parameters (ex: MLR drive)
        # self.drive_mlr = ...
        # ...
        # Update object with provided keyword arguments
        # NOTE: This overrides the previous declarations
        self.drive=2.5
        self.rates=2
        self.__dict__.update(kwargs)

