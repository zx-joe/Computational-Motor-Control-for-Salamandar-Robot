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
        self.n_joints = self.n_body_joints + self.n_legs_joints # 14
        self.n_oscillators_body = 2*self.n_body_joints # 20
        self.n_oscillators_legs = self.n_legs_joints # 4
        self.n_oscillators = self.n_oscillators_body + self.n_oscillators_legs # 24
        
        self.duration = 30
        
        self.drive = 2.
        self.turn = 0
        self.pattern = 'swim'
        
        
        self.drive_body_range = np.array([1., 5.]) 
        self.drive_limb_range = np.array([1., 3.]) 
            
        self.cv_body = [0.2, 0.3]
        self.cv_limb = [0.2, 0.]
        
        self.cr_body = [0.065, 0.196]
        self.cr_limb = [0.131, 0.131]
        
        self.freqs = 1
        self.weak_coupling_weight = 10  
        self.strong_coupling_weight = 30  
        self.phase_lag = 0.2*np.pi
        self.phase_offset = np.pi
        self.phase_body_limb = 0
        
        
        self.rate = 20
        self.nominal_amplitudes = 0.3  
        
        
        self.absolute_amplitude=False
        
        
        self.amplitudes = [0.5, 0.5]

        
        
        
        self.__dict__.update(kwargs)
        
