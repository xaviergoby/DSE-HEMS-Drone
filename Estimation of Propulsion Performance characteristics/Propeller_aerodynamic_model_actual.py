# Aerodynamic Model of the a near ideal Propeller based on [Aerodynamics of Rotor Blades for Quadrotors]
# Takes geometry of propeller as input for power, thrust and drag estimations.

import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
'''
Inputs: 

R_prop                          = Propeller Radius
w_mot                           = Motor Rotation Speed
Cl_0                            = Airfoil 0 angle of attack lift coefficient
Cl_alpha                        = Airfoil angle of attack slope
theta_tip                       = Propeller tip twist
Cd_0                            = Airfoil profile drag
N_b                             = Number of blades
c_tip                           = Tip chord
rho                             = Air density 
K_factor                        = 1/(pi*AR*e)
e_osw                           = Oswald efficiency factor (0.8 for elliptical) 
V_x, V_y, V_z                   = Quadcopter Velocity components
v_ind_x, v_ind_y, v_ind_z       = Horizontal induced velocity 
I_b                             = Blade mass moment of inertia
AR                              = Aspect Ratio 
theta_0                         = Theta at r = 0
'''

def A_disk_calc(R_prop):
    return np.pi*(R_prop**2)

# 'Near Ideal' Propeller Thrust
# Syntax checked
def Thrust_calc(N_b, rho, c_tip, R_prop, w_mot, Cl_0, mu, Cl_alpha, theta_tip, lamb_):
    thrust = (1/4) * N_b * rho * c_tip * (R_prop**3) * (w_mot**2) * (Cl_0*(2 + (mu**2)) + Cl_alpha*(theta_tip*(2+ mu**2) - 2*lamb_))
    return thrust

# Rotor hub/shaft advance ratio mu in direction of V_h
# Syntax checked
def mu_vh(v_ind_h, V_h, w_mot, R_prop):
    mu = (np.linalg.norm(v_ind_h)+np.linalg.norm(V_h))/(w_mot * R_prop)
    return mu

# Induced advance ratio
# Syntax checked
def mu_vh_i(v_ind_h, w_mot, R_prop):
    mu_i = np.linalg.norm(v_ind_h)/(w_mot*R_prop)
    return mu_i

# Non induced advance ratio
# Syntax checked
def mu_vh_h(V_h, w_mot, R_prop):
    mu_h = np.linalg.norm(V_h)/(w_mot*R_prop)
    return mu_h

# Vertical inflow
# Syntax checked
def lamb_calc(v_ind_z, V_z, w_mot, R_prop):
    lamb_inflow = (v_ind_z - V_z)/(w_mot*R_prop)
    return lamb_inflow

def lamb_calc_ind(v_ind_z, w_mot, R_prop):
    lamb_ind = (v_ind_z)/(w_mot*R_prop)
    return lamb_ind

def lamb_calc_z(V_z, w_mot, R_prop):
    lamb_z = V_z/(w_mot*R_prop)
    return lamb_z

# Hub force
# Syntax Checked
def H_force_calc(N_b, rho, c_tip, w_mot, R_prop, mu, zeta, kai):
    H_force = -0.5*(N_b)*rho*c_tip*(w_mot**2)*(R_prop**3)*mu*(zeta + 0.5*kai)
    return H_force

# zeta factor
# Syntax Checked
def zeta_calc(Cd_0, K_factor, Cl_0, Cl_alpha, mu, theta_tip, a1, lamb_):
    zeta = (Cd_0 + K_factor*(Cl_0**2)) + K_factor*Cl_0*Cl_alpha*(8*mu*theta_tip - 4*a1 - 4*lamb_*mu) + K_factor* \
           (Cl_alpha**2)*(4*lamb_*a1 - 4*a1*theta_tip + 4*mu*(theta_tip**2) - 4*mu*theta_tip)
    return zeta

# a1 factor
# Syntax Checked
def a1_calc(theta_0, mu, lamb):
    a1 = (2*mu*((4/3)*theta_0 - lamb))/(1 - (mu**2)/2)
    return a1

# K_factor
# Syntax Checked
def K_factor_calc(AR, e_osw):
    K_factor = 1/(np.pi*e_osw*AR)
    return K_factor

# Kai factor
# Syntax Checked
def Kai_factor_calc(Cl_0, lamb_, Cl_alpha, theta_tip, theta_0):
    Kai_factor = Cl_0*lamb_ + Cl_alpha*(theta_tip*lamb_ - 2*lamb_*((4/3)*theta_0 - lamb_))
    return Kai_factor

# Z Factor
# Syntax Checked
def Z_factor_calc(Cd_0, K_factor, Cl_0, Cl_alpha, theta_tip, lamb_, mu, delta_tau):
    Z_factor = 2*((Cd_0 + K_factor*(Cl_0**2))*(2+ 3*(mu**2)) + 2*K_factor*Cl_0*Cl_alpha*((2*theta_tip - lamb_)*(mu**2) +
                 (theta_tip*(2 + mu**2) - 2*lamb_)) + 2*K_factor*(Cl_alpha**2)*(2*theta_tip*(theta_tip - lamb_)*(mu**2)
                                                                                + 2*(theta_tip**2)*(1 + mu**2) -
                                                                    4*theta_tip*lamb_  + 2*(lamb_**2))) + 2*delta_tau
    return Z_factor

# Delta tau
# Syntax Checked
def delta_tau_calc(Cd_0, K_factor, Cl_0, Cl_alpha, mu, theta_tip, a1, lamb_):
    delta_tau = (mu**2)*((Cd_0 + K_factor*(Cl_0**2)) + K_factor*Cl_0*Cl_alpha*(8*mu*theta_tip - 4*a1 - 4*lamb_*mu) +
                         K_factor*(Cl_alpha**2)*(4*lamb_*a1 - 4*a1*theta_tip + 4*mu*(theta_tip**2) - 4*mu*theta_tip))
    return delta_tau

# Power formula
# Syntax checked
def power_calc(rho, N_b, c, w_motor, R_prop, Z, thrust, kappa, lamb_i, lamb_z, H_force, mu_ind, mu_h):
    power = (1/8)*rho*N_b*c*(w_motor**3)*(R_prop**4)*Z + (thrust*(kappa*lamb_i - lamb_z) - H_force*(kappa*mu_ind + mu_h))*w_motor*R_prop
    return power

def induced_opt_func(v_i, T, H, A_disk, rho, V_h, V_z):
    return np.array([T-  2*rho*A_disk*v_i[1]*np.sqrt((v_i[0] + V_h)**2 + (v_i[1] - V_z)**2), H - 2*rho*A_disk*v_i[0]*np.sqrt((v_i[0] + V_h)**2 + (v_i[1] - V_z)**2)])

if __name__ == '__main__':
    v_ind_x, v_ind_y, v_ind_z = 1, 1, 1
    v_ind_h = np.linalg.norm(np.array([v_ind_x, v_ind_y, 0]))

    v_i = np.array([np.linalg.norm(v_ind_h), v_ind_z])
    for i in range(0, 100):

        N_b = 2
        rho = 1.225
        c_tip = 0.01
        R_prop = 0.22
        A_disk = A_disk_calc(R_prop)
        w_mot = 700
        Cl_0 = 0.1
        V_x, V_y, V_z = -2, -2, 0
        V_h = np.array([V_x, V_y, 0])
        V_h_norm = np.linalg.norm(V_h)
        AR = 10
        e_osw = 0.7
        Cd_0 = 0.2
        kappa = 1
        c = 0.04
        mu = mu_vh(v_ind_h, V_h, w_mot, R_prop)
        lamb_ = lamb_calc(v_ind_z, V_z, w_mot, R_prop)
        Cl_alpha = 2*np.pi
        theta_tip = np.deg2rad(1)
        theta_0 = np.deg2rad(6)
        a1 = a1_calc(theta_0, mu, lamb_)
        kai = Kai_factor_calc(Cl_0, lamb_, Cl_alpha, theta_tip, theta_0)

        K_factor = K_factor_calc(AR, e_osw)
        zeta = zeta_calc(Cd_0, K_factor, Cl_0, Cl_alpha, mu, theta_tip, a1, lamb_)
        H_force = H_force_calc(N_b, rho, c_tip, w_mot, R_prop, mu, zeta, kai)
        T_force = Thrust_calc(N_b, rho, c_tip, R_prop, w_mot, Cl_0, mu, Cl_alpha, theta_tip, lamb_)
        delta_tau = delta_tau_calc(Cd_0, K_factor, Cl_0, Cl_alpha, mu, theta_tip, a1, lamb_)
        Z_factor = Z_factor_calc(Cd_0, K_factor, Cl_0, Cl_alpha, theta_tip, lamb_, mu, delta_tau)
        mu_ind = mu_vh_i(v_ind_h, w_mot, R_prop)
        mu_h = mu_vh_h(V_h, w_mot, R_prop)
        lamb_z = lamb_calc_z(V_z, w_mot, R_prop)
        lamb_ind = lamb_calc_ind(v_ind_z, w_mot, R_prop)
        power = power_calc(rho, N_b, c, w_mot, R_prop, Z_factor, T_force, kappa, lamb_ind, lamb_z, H_force, mu_ind, mu_h)
        # Converge to the induced velocity using non linear least squares


        least_sol = least_squares(induced_opt_func, v_i, method = 'dogbox', args=(T_force, H_force, A_disk, rho, V_h_norm, V_z)).x
        #print(least_squares(induced_opt_func, v_i, method = 'dogbox', args=(T_force, H_force, A_disk, rho, V_h_norm, V_z)))
        v_ind_h = least_sol[0]
        v_ind_z = least_sol[1]
        v_i = np.array([v_ind_h, v_ind_z])
        print(T_force)
        print(H_force)
        #print(v_i)
        #print(T_force)
        print(v_i)



