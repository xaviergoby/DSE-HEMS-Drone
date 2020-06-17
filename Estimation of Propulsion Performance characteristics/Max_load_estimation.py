

import Governing_constants_and_functions as G
import numpy as np
import sympy as sy
import math

def max_load_est(sigma=0.8, thrust_max=G.thrust_max):
    if thrust_max:
        load_max = thrust_max * 4 - G.g
        pitch_max = np.arccos(float(G.W / (G.n_r * thrust_max)))

    else:
        I_m, U_m, M, N = sy.symbols('I_m U_m M N', positive=True)

        # These equalities are the equations to be solved, the stuff inside the brackets is just 'left side' and 'right side'
        Eq1 = sy.Equality(G.f_sigma(I_m=I_m, U_m=U_m), sigma)  # First term ('left side') is duty cycle, assumed 0.8 here
        Eq2 = sy.Equality(M, G.rho * G.D_p ** 5 * G.f_C_M() * (N/60) ** 2) # The equation for M, the motor torque
        Eq3 = sy.Equality(U_m, G.f_U_m(M=M, N=N)) # Equation for U_m, equivalent motor voltage
        Eq4 = sy.Equality(I_m, G.f_I_m(M=M, N=N)) # Equation for I_m, equivalent motor current

        Eqs = [Eq1, Eq2, Eq3, Eq4]

        sol = sy.solve(Eqs, [I_m, U_m, M, N])

        I_m = sol[0][0]
        U_m = sol[0][1]
        M = sol[0][2]
        N = sol[0][3]

        I_e = G.f_I_e(sigma=sigma, I_m=I_m)
        I_b = G.n_r * I_e + G.I_c
        U_e = G.f_U_e(I_b=I_b)
        eff = (2 * np.pi * G.n_r * M * N)/(G.U_b * I_b * 60)
        T = G.f_C_T() * G.rho * (N/60) ** 2 * G.D_p ** 4
        # print(T)
        T_b = G.f_T_b(I_b=I_b)
        blah = (G.W/(G.n_r * T))
        pitch_max = np.arccos(float(G.W/(G.n_r * T)))
        load_max = G.n_r * T - G.W
    return load_max, pitch_max

if __name__ == '__main__':
    load_max, pitch_max = max_load_est()
    print('Maximum load is', load_max, 'N')
    print('Maximum pitch angle is', pitch_max * 180/np.pi, 'degrees')