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

Bp = 2 # Nunmber of blades, optimal is 2 from research
Dp = 0.2794 # Propeller diameter in m
Hp = 0.1194 # Propeller pitch in m
Gp = 0.01502525 * 9.81 # Weight of propeller in N

def f_C_T (Bp = Bp, Dp = Dp, Hp = Hp, Gp = Gp):
    return 0.25 * np.pi**3 * zeta ** 2 * Bp * K_0 * (epsilon * np.arctan(Hp/(np.pi * Dp))-alpha_0)/(np.pi * A + K_0)

