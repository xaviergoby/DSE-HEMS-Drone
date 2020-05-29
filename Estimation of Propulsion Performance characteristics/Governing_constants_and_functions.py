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
W_p = 0.01502525 * g # Weight of propeller in N

# Motor parameters
K_V0 =

C_d = C_fd + ((np.pi * A * K_0 ** 2) * (epsilon * np.arctan(H_p/(np.pi * D_p))-alpha_0) ** 2)/(e * (np.pi * A + K_0) ** 2)

def f_C_T (B_p = B_p, D_p = D_p, H_p = H_p, W_p = W_p):
    return 0.25 * np.pi**3 * zeta ** 2 * B_p * K_0 * (epsilon * np.arctan(H_p/(np.pi * D_p))-alpha_0)/(np.pi * A + K_0)

def f_C_M (B_p = B_p, D_p = D_p, H_p = H_p, W_p = W_p):
    return (1/8 * A) * np.pi ** 2 * C_d * zeta ** 2 * lambd * B_p ** 2
