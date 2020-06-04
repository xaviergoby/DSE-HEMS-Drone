'''
This tries to implement the calculations in https://arxiv.org/abs/1809.02472 to find the optimal parameters for a motor,
using as input an estimation for weight and maximum thrust to weight ratio.
'''

import numpy as np
import Governing_constants_and_functions as G

U_m_max_opt = 30 # Optimal motor equivalent voltage in Volts, from their paper
GW_const = 0.0624 # Constant also from the paper
k_c = 0.82 # Correction factor also from paper
W = 5 * 9.81 # Weight of the drone in N
n_r = 4 # Number of rotors
T_to_W_max = 2.5 # Max thrust to weight ratio, typical numbers for multicopters are 2-3
rho = 1.225

I_m_max_opt = (T_to_W_max * W * 1/n_r) / (GW_const * U_m_max_opt)
K_V_opt = ( (k_c * 255 * rho * G.f_C_T() ** 5) / (np.pi ** 4 * G.f_C_M() ** 4) ) ** (1/2) * \
          (I_m_max_opt ** 2 * U_m_max_opt) / (T_to_W_max * W * (1/n_r)) ** (5/2)

print('Optimal maximum motor voltage (Um_max) is', U_m_max_opt, 'V' )
print('Optimal maximum motor current is (Im_max) is', I_m_max_opt, 'A')
print('Optimal K_V of the motor is', K_V_opt, 'RPM/V')
