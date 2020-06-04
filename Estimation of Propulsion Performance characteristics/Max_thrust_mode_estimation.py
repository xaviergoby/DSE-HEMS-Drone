

import Governing_constants_and_functions as G
import numpy as np
import sympy as sy

I_m, U_m, M, N = sy.symbols('I_m U_m M N', positive=True)

# These equalities are the equations to be solved, the stuff inside the brackets is just 'left side' and 'right side'
Eq1 = sy.Equality(G.f_sigma(I_m=I_m, U_m=U_m), 1)  # First term ('left side') is duty cycle, which is 1 for max thrust
Eq2 = sy.Equality(M, G.rho * G.D_p ** 5 * G.f_C_M() * (N/60) ** 2) # The equation for M, the motor torque
Eq3 = sy.Equality(U_m, G.f_U_m(M=M, N=N)) # Equation for U_m, equivalent motor voltage
Eq4 = sy.Equality(I_m, G.f_I_m(M=M, N=N)) # Equation for I_m, equivalent motor current

Eqs = [Eq1, Eq2, Eq3, Eq4]

sol = sy.solve(Eqs, [I_m, U_m, M, N])

I_m = sol[0][0]
U_m = sol[0][1]
M = sol[0][2]
N = sol[0][3]

I_e = G.f_I_e(sigma=1, I_m=I_m)
I_b = G.n_r * I_e + G.I_c
U_e = G.f_U_e(I_b=I_b)
eff = (2 * np.pi * G.n_r * M * N)/(G.U_b * I_b * 60)
T = G.f_C_T() * G.rho * (N/60) ** 2 * G.D_p ** 4
T_b = G.f_T_b(I_b=I_b)

print('Max thrust endurance is:', T_b, ' minutes')
print('Propeller RPM is:', N )
print('ESC current is', I_e, 'A')
print('ESC voltage is', U_e, 'V')
print('Battery current is', I_b, 'A')
print('Efficiency is', eff * 100, '%') 
