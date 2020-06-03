import numpy as np

# I honestly don't know what these constants are at the moment they are from the paper and we will have
# to explain them eventually
A = 5
epsilon = 0.85
lambd = 0.75
zeta = 0.55
e = 0.83
C_fd = 0.015
alpha_0 = 0
K_0 = 6.11

# Environment Parameters
Temp = 288.15 # ISA sea-level Temperature in Celsius
p = 101325 # ISA sea-level pressure in Pa
g = 9.81 # Acceleration due to gravity m/s^2
R = 287.05
rho = p/(R*Temp) # ISA sea-level density kg/m^3

# General Parameters
W = 3.7 * g
n_r = 4

# Propeller parameters
B_p = 2 # Nunmber of blades, optimal is 2 from research
D_p = 0.2794 # Propeller diameter in m
H_p = 0.1194 # Propeller pitch in m
W_p = 0.01502525 * g # Weight of propeller in N, not really relevant since we start with total weight

# Motor parameters
K_V0 = 890 # in r/min/V
I_m_max = 19 # in Amps
I_m0 = 0.5 # in Amps
U_m0 = 10 # in Volts
R_m = 0.101 # in Ohms
#G_m = blah # # Weight of Motor, not really relevant for this calculations since we start with total weight

### ESC (Electronic speed converter) parameters
I_e_max = 30 # Max ESC current in Amps
R_e = 0.008 # Internal resistance of ESC in Ohms
I_c = 1 # Control current supplied to the flight controller in Amps, usually 1 A.
#G_e = blah # Weight of ESC, not really relevant for this calculations since we start with total weight

### Battery parameters
C_b = 5000 # Battery capacity in mAh
R_b = 0.01 # Battery internal resistance in Ohms
U_b = 12 # Battery voltage in Volts
K_b = 45 # Maximum discharge rate in Coulombs
C_min = 0.2 * C_b # Basically just calculating minimum battery capacity assuming a DoD, in this case assuming 80%
#G_b = blah # Also irrelevant like the others for now

### Propeller Model equations

C_d = C_fd + ((np.pi * A * K_0 ** 2) * (epsilon * np.arctan(H_p/(np.pi * D_p))-alpha_0) ** 2)/(e * (np.pi * A + K_0) ** 2)

def f_C_T (B_p = B_p, D_p = D_p, H_p = H_p, W_p = W_p):
    return 0.25 * np.pi**3 * zeta ** 2 * B_p * K_0 * (epsilon * np.arctan(H_p/(np.pi * D_p))-alpha_0)/(np.pi * A + K_0)

def f_C_M (B_p = B_p, D_p = D_p, H_p = H_p, W_p = W_p):
    return (1/(8 * A)) * np.pi ** 2 * C_d * zeta ** 2 * lambd * B_p ** 2

### Motor Model Equations

def f_U_m (M, N, K_V0 = K_V0, I_m_max = I_m_max, I_m0 = I_m0, U_m0 = U_m0, R_m = R_m):
    return R_m * ( (M * K_V0 * U_m0)/(9.55 * (U_m0 -  I_m0 * R_m) ) + I_m0) + N * (U_m0 - I_m0 * R_m) / (K_V0 * U_m0)

def f_I_m (M, N, K_V0 = K_V0, I_m_max = I_m_max, I_m0 = I_m0, U_m0 = U_m0, R_m = R_m):
    return (M * K_V0 * U_m0) / (9.55 * (U_m0 - I_m0 * R_m)) + I_m0

### ESC Model Equations

def f_sigma (U_m, I_m, U_b = U_b, I_e_max = I_e_max, R_e = R_e):
    return (U_m + I_m * R_e) / U_b

def f_I_e (sigma, I_m):
    return sigma * I_m

def f_U_e (I_b, C_b = C_b, R_b = R_b, U_b = U_b, K_b = K_b):
    return U_b - I_b * R_b

### Battery Model Equations

def f_T_b (I_b, C_min = C_min, C_b = C_b, R_b = R_b, U_b = U_b, K_b = K_b):
    return (C_b - C_min)/I_b * ((60) / (1000))  # Note conversion factor included to output minutes, assuming C_b in mAh
