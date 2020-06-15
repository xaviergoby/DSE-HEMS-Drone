'''
This code is based on the paper https://www.researchgate.net/publication/314200017_A_Practical_Performance_Evaluation_Method_for_Electric_Multicopters ,
uses all the equations shown in it in order to be able to estimate performance parameters of a multirotor such as
hover time, propeller speed, the current for the ESC, max speed and distance, among other things, using as input
parameters related to the propeller, ESC (electronic speed converter), motor, and battery, which we should be able to
find in the specs for these most of the time. It has a lot of assumptions and uses a lot of constants and coeffecients
at times, which for now are all copied from them but some could potentially be adjusted if we know them more accurately
for our case. This file has all the constants, parameters (what you would want to change to see how it affects results),
and all the governing equations that basically model the main elements (propller, ESC, motor, battery), the other
estimation files then use these to give the results.
'''

import numpy as np

params_names = ['A', 'EPSILON', 'LAMBDA', 'ZETA', 'e', 'C_fd', 'ALPHA_0', 'K_0', 'Temp', 'p', 'g', 'R', 'rho', 'W', 'n_r',
               'B_p', 'D_p', 'H_p', 'est_N', 'est_M', 'a_N', 'b_N', 'a_M', 'b_M', 'thrust_max', 'K_V0', 'I_m_max', 'I_m0',
               'U_m0', 'R_m', 'I_e_max', 'R_e', 'I_c', 'C_b', 'R_b', 'U_b', 'K_b', 'DOD']

A = 5 # Aspect ratio, 'typical' value taken from paper but we can tailor it when applicable to our propeller
EPSILON = 0.85 # Downwash correction factor, also taken from paper
LAMBDA = 0.75 # Correction coefficient of the blade airfoil area, also taken from paper
ZETA = 0.5 # Another correction factor related to the average rotor linear speed
e = 0.83 # Oswald factor, estimation from paper but we can also adjust if known better
C_fd = 0.015 # Zero lift drag coefficient, again can adjust if known better
ALPHA_0 = 0 # Zero-lift angle in rad, same comment as above can be adjusted
K_0 = 6.11 # slope of lift curve, also can be adjusted, paper took something slightly below 2*pi I imagine

# Environment Parameters
Temp = 298.15 # ISA sea-level Temperature in Celsius
p = 101325 # ISA sea-level pressure in Pa
g = 9.81 # Acceleration due to gravity m/s^2
R = 287.05 # Gas constant of air
rho = p/(R*Temp) # ISA sea-level density kg/m^3

# General Parameters
W = 3.5 * g # Total weight in Newtons
n_r = 4

# Propeller parameters
B_p = 2 # Nunmber of blades, optimal is 2 from research
D_p = 15.5 * 0.0254 # Propeller diameter in m (the 0.0254 is conversion from in. to m)
H_p = 5.3 * 0.0254 # Propeller pitch in m

# If these are 1 then it will estimate a lot of stuff related to thrust and RPM using assumed coefficients, if 0 then
# you need to input your own known relationships (from manufacturer data) between RPM and thrust and power
est_N = 0
est_M = 0 #

# These are the parameters for the linear regressions relating first thrust to RPM, in the form of
# RPM = a_N * Thrust + b_N and power to thrust, in the form of Power = a_M * Thrust + b_M, with thrust in grams
# These will only be used if the est_* parameters above are set to 0 (the regressions in the propulsion excel sheet).
a_N = 1.56
b_N = 2381
a_M = 0.264
b_M = -169

thrust_max = 3520 * (g/1000) # Put this number here if it is known, but it is not a required input

# Motor parameters
K_V0 = 475 # Nominal no-load motor constant in r/min/V (RPM/V, revolutions per minute per volt)
I_m_max = 27 # Maximum motor current in Amps
I_m0 = 0.53 # Motor nominal no-load current in Amps
U_m0 = 15 # Motor nominal no-load voltage in Volts
R_m = 0.111 # Motor resistance in Ohms
#G_m = blah # # Weight of Motor, not really relevant for this calculations since we start with total weight

### ESC (Electronic speed converter) parameters
I_e_max = 30 # Max ESC current in Amps
R_e = 0.008 # Internal resistance of ESC in Ohms
I_c = 1 # Control current supplied to the flight controller in Amps, usually 1 A (from paper).
#G_e = blah # Weight of ESC, not really relevant for this calculations since we start with total weight

### Battery parameters
C_b = 5400 # Battery capacity in mAh
R_b = 0.0078 # Battery internal resistance in Ohms
U_b = 22.8 # Battery voltage in Volts
K_b = 45 # Maximum discharge rate in Coulombs
DOD = 0.8
C_min = (1-DOD) * C_b # Basically just calculating minimum battery capacity assuming a DoD, in this case assuming 80% DoD
#G_b = blah # Also irrelevant like the others for now

params_values = [A, EPSILON, LAMBDA, ZETA, e, C_fd, ALPHA_0, K_0, Temp, p, g, R, rho, W, n_r,
               B_p, D_p, H_p, est_N, est_M, a_N, b_N, a_M, b_M, thrust_max, K_V0, I_m_max, I_m0,
               U_m0, R_m, I_e_max, R_e, I_c, C_b, R_b, U_b, K_b, DOD]

### Propeller Model equations

# Drag coefficient, estimated from paper and other coefficients/factors
C_d = C_fd + ((np.pi * A * K_0 ** 2) * (EPSILON * np.arctan(H_p/(np.pi * D_p))-ALPHA_0) ** 2)/(e * (np.pi * A + K_0) ** 2)

# Thrust coefficient, uses blade number, propeller diameter and pitch as inputs, plus correction factors/coefficients
def f_C_T (B_p = B_p, D_p = D_p, H_p = H_p):
    return 0.25 * np.pi**3 * LAMBDA * ZETA ** 2 * B_p * K_0 * ((EPSILON * np.arctan(H_p/(np.pi * D_p))-ALPHA_0)/(np.pi * A + K_0))

# Torque coefficient, uses same inputs as thrust coefficient
def f_C_M (B_p = B_p, D_p = D_p, H_p = H_p):
    return  (1/(8 * A)) * np.pi ** 2 * C_d * ZETA ** 2 * LAMBDA * B_p ** 2

# Propeller RPM
def N (T, est=est_N):
    if est==1:
        return 60 * np.sqrt(T/(rho * D_p ** 4 * f_C_T()))
    else:
        return a_N * (1000/g) * T + b_N # Note conversion factor (1000/g) since relationship had thrust in grams

def M(T, N, est=est_M):
    if est==1:
        return rho * D_p ** 5 * f_C_M() * (N/60) ** 2
    else:
        return (a_M * (1000/g) * T + b_M)/(N * (2 * np.pi/60)) # Note conversion factor since relationship had thrust in grams

### Motor Model Equations

# Motor equivalent voltage
def f_U_m (M, N, K_V0 = K_V0, I_m_max = I_m_max, I_m0 = I_m0, U_m0 = U_m0, R_m = R_m):
    return R_m * ( (M * K_V0 * U_m0)/(9.55 * (U_m0 -  I_m0 * R_m) ) + I_m0) + N * (U_m0 - I_m0 * R_m) / (K_V0 * U_m0)

# Motor equivalent current
def f_I_m (M, N, K_V0 = K_V0, I_m_max = I_m_max, I_m0 = I_m0, U_m0 = U_m0, R_m = R_m):
    return (M * K_V0 * U_m0) / (9.55 * (U_m0 - I_m0 * R_m)) + I_m0

### ESC Model Equations

# Duty Cycle
def f_sigma (U_m, I_m, U_b = U_b, I_e_max = I_e_max, R_e = R_e):
    return (U_m + I_m * R_e) / U_b

# ESC current
def f_I_e (sigma, I_m):
    return sigma * I_m

# ESC voltage
def f_U_e (I_b, C_b = C_b, R_b = R_b, U_b = U_b, K_b = K_b):
    return U_b - I_b * R_b

### Battery Model Equations

# Time to discharge the battery, equivalent to endurance basically
def f_T_b (I_b, C_min = C_min, C_b = C_b, R_b = R_b, U_b = U_b, K_b = K_b):
    return (C_b - C_min)/I_b * ((60) / (1000))  # Note conversion factor included to output minutes, assuming C_b in mAh




