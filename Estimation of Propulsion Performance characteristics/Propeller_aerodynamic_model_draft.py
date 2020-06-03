# Aerodynamic Model of the Propeller based on [Aerodynamics of Rotor Blades for Quadrotors]
# Takes geometry of propeller as input for power, thrust and drag estimations.

import numpy as np
'''
Assumptions:

1) The rotor disc has an infinite nubmer of rotor blades such that there is a uniform constant distribution of 
aerodynamic forces over the rotor disc. 

2) The rotor disc is infinitely thin disc of area A_disk which offers no resistance to air passing through.

3) The flow is irrotational an therefore no swirl is imparted to it. 

4) The air outside the streamtube remains undisturbed by the actuator disc. 

Variables:

T           =           Thrust                              [N]
P           =           Power
A_disk      =           Propeller Disk Area                 [m^2]
D_prop      =           Propeller Diameter                  [m]
rho         =           Air density                         [kg/m^3]
R_prop      =           Propeller Maximum Radius            [m]
beta_flap   =           Blade Flapping Angle                [rad]
w_mot       =           Motor speed                         [rad/s]
V_h         =           Horizontal Velocity                 [m/s]
V_z         =           Vertical Velocity                   [m/s]
v_ind_h     =           Induced horizontal velocity         [m/s]
v_ind_z     =           Induced vertical velocity           [m/s]
a0, a1...   =           Blade Flapping Coefficients         [-]
b1          =           Blade Flapping Coefficient          [-]
c           =           Blade Chord Length                  [m]
N_b         =           Number of Blades                    [-]
I_b         =           Blade Mass Moment of Inertia        [kg*m^2]



'''

# Determine disk loading of propeller to see if the model is valid
def disk_loading(T,A):
    dl = T/A
    return dl

# Area of the propeller disk
def disk_area(D_prop):
    A_disk = 0.25 * (D_prop*D_prop) * np.pi
    return A_disk

# Hover power based on momentum theory
def hover_power(T, rho, A):
    P_hover = (T**(3/2)) / np.sqrt(2*rho*A)
    return P_hover

# Transverse scalar velocity at a blade element
def U_h(w_mot, r_loc, V_h, v_ind_h, psi):
    return w_mot*r_loc + (np.linalg.norm(V_h + v_ind_h))*np.sin(psi)

# Advance ratio
def mu_ad(v_ind_h,V_h, w_mot, R_prop):
    return np.linalg.norm(v_ind_h + V_h)/(w_mot*R_prop)

# Vertical inflow ratio
def lamb_in(v_ind_z, V_z, w_mot, R_prop):
    return (v_ind_z - V_z)/(w_mot*R_prop)

# Solidity ratio
def sigma_sol(N_b, c, R_prop):
    return (N_b*c)/(np.pi*R_prop)

# Thrust coefficient
def thrust_coeff(T, w_mot):
    return T/(w_mot*w_mot)

# Power coefficient
def power_coeff(P, w_mot):
    return P/(w_mot**3)

# Lock number for a constant chord blade
def lock_const_chord(rho, A_disk, c, R_prop, I_b):
    return (rho*A_disk*c*(R_prop**4))/I_b

# Blade Flapping Coefficient a0
def a0_calc(lock, theta_0, mu, lamb):
    a0 = (lock/8)*(theta_0*(1+ mu**2) - (4/3)*lamb)
    return a0

# Blade Flapping Coefficient a1
def a1_calc(theta_0, mu, lamb):
    a1 = (2*mu*((4/3)*theta_0 - lamb))/(1 - (mu**2)/2)
    return a1

# Blade Flapping Coefficient b1
def b1_calc(mu, a0):
    b1 = ((4/3)*mu*a0)/(1 - (mu**2)/2)
    return b1

# Blade Flapping Angle as function of Psi
def flap_angle(psi, a0, a1, b1):
    beta_angle = a0 - a1*np.cos(psi) - b1*np.sin(psi)
    return beta_angle

# Blade Flapping Angle Derivative as function of psi
def flap_angle_der(psi, w_mot, a1, b1):
    beta_angle_dot = (a1*np.sin(psi) - b1*np.cos(psi))*w_mot
    return beta_angle_dot





if __name__== '__main__':
    #Verification fro disk_loading, disk_area, hover_power
    D_prop = 2
    T = 200
    rho = 1.225
    A_disk = disk_area(D_prop)
    print(A_disk)
    print(disk_loading(T, A_disk))
    print(hover_power(T,rho, A_disk))

    #Verification for U_h
    r_loc = 0.125

    w_mot = 523 #Rad/s
    V_h = np.array([np.sqrt(12.5), np.sqrt(12.5), 0])
    print(np.linalg.norm(V_h))
    v_ind_h = np.array([0,0,0])
    psi = np.pi/2
    R_prop = D_prop/2

    print(U_h(w_mot, r_loc, V_h, v_ind_h, psi))
    print(mu_ad(v_ind_h, V_h, w_mot, R_prop))

    #Blade flap verification