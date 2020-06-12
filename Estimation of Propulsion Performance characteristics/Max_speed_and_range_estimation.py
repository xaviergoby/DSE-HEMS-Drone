
import Governing_constants_and_functions as G
import numpy as np
import sympy as sy
import matplotlib.pyplot as plt

C1 = 3
C2 = 1.5
S = 0.1 # They never say what number they use for area which is really annoying so we'll have to experiment
theta_max = 40 * np.pi/180 # max pitch angle, later we can just take this from the calcuation done in max_load_estimation

def C_D(theta):
    return C1 * (1 - (np.cos(theta)) ** 3) + C2 * (1 - (np.sin(theta)) ** 3)

def V (theta):
    return np.sqrt( (2 * G.W * np.tan(theta)) / (G.rho * S * C_D(theta)) )

def N(theta):
    return G.N(T=G.W/(G.n_r * np.cos(theta)))

def M(theta):
    return G.M(T=G.W/(G.n_r * np.cos(theta)), N=N(theta))

def U_m(theta):
    return G.f_U_m(N=N(theta), M=M(theta))

def I_m(theta):
    return G.f_I_m(N=N(theta), M=M(theta))

def sigma(theta):
    return G.f_sigma(U_m=U_m(theta), I_m=I_m(theta))

def I_e(theta):
    return G.f_I_e(sigma=sigma(theta), I_m=I_m(theta))

def I_b(theta):
    return G.n_r * I_e(theta) + G.I_c

def T_fly(theta):
    return G.f_T_b(I_b(theta))

def range(theta):
    return 60 * V(theta) * T_fly(theta)



theta_values = np.linspace(0, theta_max, 300)

Data_V = V(theta_values)
Data_T_fly = T_fly(theta_values)
Data_range = 60 * V(theta_values) * T_fly(theta_values)
Data_C_D = C_D(theta_values)

#print(Data_V)
#print(Data_T_fly)
#print(Data_range)
print('Max speed is', V(theta_max), 'm/s')
print('Max range is', max(Data_range), 'm')

indx = np.where(Data_range == max(Data_range))[0]
print('Pitch for max range is', theta_values[indx] * 180/np.pi, 'degrees')
print('Velocity for max range is', Data_V[indx], 'm/s')
print('RPM required is', N(theta_values[indx]))
plt.plot(theta_values * 180/np.pi, Data_C_D)
plt.plot()
plt.show()

print(C_D(0*np.pi/180))