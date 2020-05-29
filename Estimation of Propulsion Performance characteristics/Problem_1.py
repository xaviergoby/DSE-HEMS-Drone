import numpy as np
import Governing_constants_and_functions as G

T = G.W/G.n_r # Thrust (N) in hover is equal to weight (N) by number of rotors

N = 60 * np.sqrt(T/(G.rho * G.D_p ** 4 * G.f_C_T())) # Motor speed (RPM)
M = G.rho * G.D_p ** 5 * G.f_C_M * (N/60) ** 2 # Propeller torque in N*m


