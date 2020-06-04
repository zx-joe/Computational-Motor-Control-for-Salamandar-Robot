"""Robot parameters"""

import numpy as np
import farms_pylog as pylog
import math


class RobotParameters(dict):
    """Robot parameters"""
    
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def __init__(self, parameters):
        super(RobotParameters, self).__init__()

        # Initialise parameters
        self.n_body_joints = parameters.n_body_joints # 10
        self.n_legs_joints = parameters.n_legs_joints # 4
        self.n_joints = self.n_body_joints + self.n_legs_joints # 14
        self.n_oscillators_body = 2*self.n_body_joints # 20
        self.n_oscillators_legs = self.n_legs_joints # 4
        self.n_oscillators = self.n_oscillators_body + self.n_oscillators_legs # 24
        self.freqs = np.zeros(self.n_oscillators) # 24
        self.coupling_weights = np.zeros([ 
            self.n_oscillators,
            self.n_oscillators
        ])
        self.phase_bias = np.zeros([self.n_oscillators, self.n_oscillators]) 
        self.nominal_amplitudes = np.zeros(self.n_oscillators) 
        self.pattern = parameters.pattern
        self.phase_lag = parameters.phase_lag
        self.turn = parameters.turn
        self.drive = parameters.drive
        self.update(parameters)


    def update(self, parameters):
        """Update network from parameters"""
        self.set_frequencies(parameters) 
        self.set_coupling_weights(parameters)  
        self.set_phase_bias(parameters)  
        self.set_amplitudes_rate(parameters)  
        self.set_nominal_amplitudes(parameters)  
        self.drive = parameters.drive 
        
        


    def set_frequencies(self, parameters):
        """Set frequencies"""

        self.freqs = np.ones(self.n_oscillators) * parameters.freqs
        temp_freq_body=0.
        temp_freq_limb=0.
        
        
        if self.drive>=parameters.drive_body_range[0] and self.drive<=parameters.drive_body_range[1]:
            temp_freq_body=parameters.cv_body[0]*self.drive+parameters.cv_body[1]
            
        if self.drive>=parameters.drive_limb_range[0] and self.drive<=parameters.drive_limb_range[1] and self.pattern=='walk':
            temp_freq_limb=parameters.cv_limb[0]*self.drive+parameters.cv_limb[1]
        
        
        self.freqs[:2*self.n_body_joints] = temp_freq_body*self.freqs[:2*self.n_body_joints]
        self.freqs[2*self.n_body_joints:] = temp_freq_limb*self.freqs[2*self.n_body_joints:]




    def set_coupling_weights(self, parameters):
        """Set coupling weights"""
        wcw = parameters.weak_coupling_weight
        scw = parameters.strong_coupling_weight
        
        temp_range=range(parameters.n_oscillators_body)
        for i in temp_range:
            if i+1 in temp_range:
                self.coupling_weights[i,i+1] = wcw
            if i-1 in temp_range:
                self.coupling_weights[i,i-1] = wcw
            if i+10 in temp_range:
                self.coupling_weights[i,i+10] = wcw
            if i-10 in temp_range:
                self.coupling_weights[i,i-10] = wcw
                
        
        temp_range_2=range(parameters.n_oscillators_body, parameters.n_oscillators)        
        for i in temp_range_2:
            if i+1 in temp_range_2:
                self.coupling_weights[i,i+1] = scw
            if i-1 in temp_range_2:
                self.coupling_weights[i,i-1] = scw
            if i+parameters.n_legs_joints/2 in temp_range_2:
                self.coupling_weights[i,int(i+parameters.n_legs_joints/2)] = scw
            if i-parameters.n_legs_joints/2 in temp_range_2:
                self.coupling_weights[i,int(i-parameters.n_legs_joints/2)] = scw
            

        
        self.coupling_weights[0:6,20] = scw
        self.coupling_weights[6:10,21] = scw
        self.coupling_weights[10:16,22] = scw
        self.coupling_weights[16:20,23] = scw

        if self.drive < 0:
            self.coupling_weights = np.transpose(self.coupling_weights)



    def set_phase_bias(self, parameters):
        """Set phase bias"""
        phase_lag=parameters.phase_lag
        phase_offset=parameters.phase_offset
        phase_body_limb=parameters.phase_body_limb

        temp_range=range(parameters.n_oscillators_body)
        for i in temp_range:
            if i+1 in temp_range:
                self.phase_bias[i][i+1]=-phase_lag
            if i-1 in temp_range:
                self.phase_bias[i][i-1]=phase_lag
            if i+parameters.n_body_joints in temp_range:
                self.phase_bias[i][i+parameters.n_body_joints]=phase_offset
            if i-parameters.n_body_joints in temp_range:
                self.phase_bias[i][i-parameters.n_body_joints]=phase_offset
            
        temp_range_2=range(parameters.n_oscillators_body, parameters.n_oscillators)  
        for i in temp_range_2:
            if i+1 in temp_range_2:
                self.phase_bias[i][i+1] = phase_offset
            if i-1 in temp_range_2:
                self.phase_bias[i][i-1] = phase_offset
            if i+parameters.n_legs_joints/2 in temp_range_2:
                self.phase_bias[i][int(i+parameters.n_legs_joints/2)] = phase_offset
            if i-parameters.n_legs_joints/2 in temp_range_2:
                self.phase_bias[i][int(i-parameters.n_legs_joints/2)] = phase_offset

        self.phase_bias[0:6,20] = phase_body_limb
        self.phase_bias[6:10,21] = phase_body_limb
        self.phase_bias[10:16,22] = phase_body_limb
        self.phase_bias[16:20,23] = phase_body_limb
        

        if self.drive < 0:
            self.phase_bias = np.transpose(self.phase_bias)

    def set_amplitudes_rate(self, parameters):
        """Set amplitude rates"""
        self.rates=np.ones(self.n_oscillators)
        temp_amplitude_rate=parameters.rate
        self.rates = temp_amplitude_rate*self.rates

    def set_nominal_amplitudes(self, parameters):
        """Set nominal amplitudes"""
        self.nominal_amplitudes = np.ones(self.n_oscillators) 
        temp_amp_body=0.
        temp_amp_limb=0.
        
        r_head = parameters.amplitudes[0]
        r_tail = parameters.amplitudes[1]
        
        if self.drive>=parameters.drive_body_range[0] and self.drive<=parameters.drive_body_range[1]:
            temp_amp_body=parameters.cr_body[0]*self.drive+parameters.cr_body[1]
            
        if self.drive>=parameters.drive_limb_range[0] and self.drive<=parameters.drive_limb_range[1] and self.pattern=='walk':
            temp_amp_limb=parameters.cr_limb[0]*self.drive+parameters.cr_limb[1]          
 
        if parameters.absolute_amplitude==False:
            amp_body_1=temp_amp_body*np.ones(self.n_body_joints)*(self.turn+1) 
            amp_body_2=temp_amp_body*np.ones(self.n_body_joints)*(-self.turn+1) 
            amp_limb_1=temp_amp_limb*np.ones(self.n_legs_joints)*(self.turn+1) 
            amp_limb_2=temp_amp_limb*np.ones(self.n_legs_joints)*(-self.turn+1) 
            self.nominal_amplitudes = np.concatenate((amp_body_1,amp_body_2, amp_limb_1, amp_limb_2))            
            
            self.nominal_amplitudes[:self.n_body_joints] *= np.linspace(r_head, r_tail, (self.n_body_joints))
            self.nominal_amplitudes[self.n_body_joints:2*self.n_body_joints] *= np.linspace(r_head, r_tail, (self.n_body_joints))
       
        
        if parameters.absolute_amplitude:
            self.nominal_amplitudes[:self.n_body_joints] = np.linspace(r_head, r_tail, (self.n_body_joints)) * np.ones(self.n_body_joints) 
            self.nominal_amplitudes[self.n_body_joints:2*self.n_body_joints] = np.linspace(r_head, r_tail, (self.n_body_joints)) * np.ones(self.n_body_joints)
        
        
        