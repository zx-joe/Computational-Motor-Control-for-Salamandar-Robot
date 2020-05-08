"""Robot parameters"""

import numpy as np
import farms_pylog as pylog


class RobotParameters(dict):
    """Robot parameters"""

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def __init__(self, parameters):
        super(RobotParameters, self).__init__()

        # Initialise parameters
        self.n_body_joints = parameters.n_body_joints
        self.n_legs_joints = parameters.n_legs_joints
        self.n_joints = self.n_body_joints + self.n_legs_joints
        self.n_oscillators_body = 2*self.n_body_joints
        self.n_oscillators_legs = self.n_legs_joints
        self.n_oscillators = self.n_oscillators_body + self.n_oscillators_legs
        self.freqs = np.zeros(self.n_oscillators)
        self.coupling_weights = np.zeros([
            self.n_oscillators,
            self.n_oscillators
        ])
        self.phase_bias = np.zeros([self.n_oscillators, self.n_oscillators])
        self.rates = np.zeros(self.n_oscillators)
        self.nominal_amplitudes = np.zeros(self.n_oscillators)
        self.update(parameters)

    def update(self, parameters):
        """Update network from parameters"""
        self.set_frequencies(parameters)  # f_i
        self.set_coupling_weights(parameters)  # w_ij
        self.set_phase_bias(parameters)  # theta_i
        self.set_amplitudes_rate(parameters)  # a_i
        self.set_nominal_amplitudes(parameters)  # R_i

    def set_frequencies(self, parameters):
        """Set frequencies"""
        #pylog.warning("Coupling weights must be set")
        
        self.freqs = np.zeros(self.n_oscillators)
        
        d_low_body=1.
        d_high_body=5.
        d_low_limb=1.
        d_high_limb=3.
        
        temp_drive=parameters.drive
        if temp_drive >= d_low_body and temp_drive<=d_high_body:
            freq_body=0.2*temp_drive+0.3
        else:
            freq_body=0.
        if temp_drive >= d_low_limb and temp_drive<=d_high_limb:
            freq_limb=0.2*temp_drive
        else:
            freq_limb=0.
        
        self.freqs[:self.n_oscillators_body]=freq_body
        self.freqs[self.n_oscillators_body:]=freq_limb
        

    def set_coupling_weights(self, parameters):
        """Set coupling weights"""
        #pylog.warning("Coupling weights must be set")
        
        self.coupling_weights=np.zeros([self.n_oscillators,self.n_oscillators])
        
        np.fill_diagonal(self.coupling_weights[1:20], 10)
        np.fill_diagonal(self.coupling_weights[10:20], 10)
        np.fill_diagonal(self.coupling_weights[:,1:20], 10)
        np.fill_diagonal(self.coupling_weights[:,10:20], 10)
        
        self.coupling_weights[20,21:23] = 10
        self.coupling_weights[21:23,20] = 10
        self.coupling_weights[23,21:23] = 10
        self.coupling_weights[21:23,23] = 10
        
        self.coupling_weights[0:5,20] = 30
        self.coupling_weights[5:10,21] = 30
        self.coupling_weights[10:15,22] = 30
        self.coupling_weights[15:20,23] = 30
        
        self.coupling_weights[9,10] = 0
        self.coupling_weights[10,9] = 0
        

    def set_phase_bias(self, parameters):
        """Set phase bias"""
        #pylog.warning("Phase bias must be set")
        
        self.phase_bias=np.zeros([self.n_oscillators,self.n_oscillators])
        
        np.fill_diagonal(self.phase_bias[1:20], 0.2*np.pi)
        np.fill_diagonal(self.phase_bias[10:20], np.pi)
        np.fill_diagonal(self.phase_bias[:,1:20], -0.2*np.pi)
        np.fill_diagonal(self.phase_bias[:,10:20], np.pi)
        
        self.phase_bias[20,21:23] = np.pi
        self.phase_bias[21:23,20] = np.pi
        self.phase_bias[23,21:23] = np.pi
        self.phase_bias[21:23,23] = np.pi
        
        self.phase_bias[0:5,20] = np.pi
        self.phase_bias[5:10,21] = np.pi
        self.phase_bias[10:15,22] = np.pi
        self.phase_bias[15:20,23] = np.pi
        
        self.phase_bias[9,10] = 0
        self.phase_bias[10,9] = 0

    def set_amplitudes_rate(self, parameters):
        """Set amplitude rates"""
        #pylog.warning("Convergence rates must be set")
        temp_rates=np.ones(self.n_oscillators)
        self.rates=20*temp_rates

    def set_nominal_amplitudes(self, parameters):
        """Set nominal amplitudes"""
        #pylog.warning("Nominal amplitudes must be set")
        self.nominal_amplitudes = np.zeros(self.n_oscillators)
        
        d_low_body=1.
        d_high_body=5.
        d_low_limb=1.
        d_high_limb=3.
        temp_drive=parameters.drive
        if temp_drive >= d_low_body and temp_drive<=d_high_body:
            nom_amp_body=0.065*temp_drive+0.196
        else:
            nom_amp_body=0.
        if temp_drive >= d_high_limb and temp_drive<=d_high_limb:
            nom_amp_limb=0.131*temp_drive+0.131
        else:
            nom_amp_limb=0.
            
        self.nominal_amplitudes[:self.n_oscillators_body]=nom_amp_body
        self.nominal_amplitudes[self.n_oscillators_body:]=nom_amp_limb
        
        temp_gradient = np.ones(self.n_oscillators)
        
        temp_gradient[:self.n_body_joints] = np.linspace(1,1 ,self.n_body_joints)
        temp_gradient[self.n_body_joints:self.n_oscillators_body] = np.linspace(1,1,self.n_body_joints)      
        self.nominal_amplitudes = temp_gradient * self.nominal_amplitudes

