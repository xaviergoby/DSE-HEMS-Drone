'''
This file uses the governing equations, constants, and parameters from the Governing_constants_and_functions.py file
(model based on a paper referenced in that file) to estimate the hovering endurance and a few other numbers related
to the power and propulsion sub-system.
'''

import numpy as np
import Governing_constants_and_functions as G

T = G.W/G.n_r # Thrust (N) in hover is equal to weight (N) by number of rotors

N = 60 * np.sqrt(T/(G.rho * G.D_p ** 4 * G.f_C_T())) # Motor speed (RPM)
M = G.rho * G.D_p ** 5 * G.f_C_M() * (N/60) ** 2 # Propeller torque in N*m

U_m = G.f_U_m(N=N, M=M)
I_m = G.f_I_m(N=N, M=M)

sigma = G.f_sigma(U_m=U_m, I_m=I_m)
I_e = G.f_I_e(sigma=sigma, I_m=I_m)

I_b = G.n_r * I_e + G.I_c
U_e = G.f_U_e(I_b)

T_b = G.f_T_b(I_b=I_b)
eff = (2 * np.pi * G.n_r * M * N)/(G.U_b * I_b * 60)
print('Hovering endurance is:', T_b, ' minutes')
print('Duty cycle is:', sigma * 100, '%')
print('Propeller RPM is:', N )
print('ESC current is', I_e, 'A')
print('ESC voltage is', U_e, 'V')
print('Battery current is', I_b, 'A')
print('Efficiency is', eff * 100, '%')

