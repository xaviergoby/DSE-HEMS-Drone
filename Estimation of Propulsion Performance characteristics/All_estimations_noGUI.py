import Governing_constants_and_functions as G
import numpy as np
import Hover_estimation as H
import Max_speed_and_range_estimation as Max

T_b, eff, P_req, sigma, N_hover, I_e, U_e, I_b = H.hover_est(G.W, G.n_r, G.I_c, G.U_b)
max_V, max_range, pitch_opt, V_opt, P_req_opt, eff_opt, T_b_opt = Max.speed_range_est(G.n_r, U_b=G.U_b)


FileName = 'hello2' # Edit this to name the output file whatever you want

with open(f'Input_and_Output_text_files/{FileName}.txt', 'w+') as f:
    f.write('Hover estimation results: \n'
            f'Power required is: {P_req} W \n'
            f'Hovering endurance is: {T_b}  minutes \n'
            f'Duty cycle is: {sigma * 100} % \n'
            f'Propeller RPM is: {N_hover} \n'
            f'ESC current is: {I_e} A \n'
            f'ESC voltage is: {U_e} V \n'
            f'Battery current is: {I_b} A \n'
            f'Efficiency is: {eff * 100} % \n \n'

            'Maximum speed and range estimation results: \n'
            f'Maximum speed is: {max_V} m/s \n'
            f'Maximum range is: {max_range}  m \n'
            f'Pitch for max range condition: {pitch_opt} deg \n'
            f'Speed for max range condition: {V_opt} m/s \n'
            f'Power required at max range condition: {P_req_opt} W \n'
            f'Efficiency at max range condition: {eff_opt * 100} % \n'
            f'Flight time at max range condition: {T_b_opt} minutes \n \n \n'
            
            'These are the input parameters that were used (refer to Governing_constants_and_functions.py for meaning '
            'and units): \n'
                )
    for i in range(len(G.params_names)):
        text = str(G.params_names[i]) + ':' + ' '*(15 - len(G.params_names[i])) + repr(G.params_values[i]).ljust(2) + '\n'
        # f.write(f'{G.params_names[i]}: {G.params_values[i]} \n')
        f.write(text)