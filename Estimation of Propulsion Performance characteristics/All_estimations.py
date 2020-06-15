
'''
This is not finished but you can run the four individual estimation programs individually already,
just change the constants/parameters in the Governing_constants_and_equations.py file.
'''

import Governing_constants_and_functions as G
import PySimpleGUI as sg
import numpy as np
import Hover_estimation as H

sg.theme('BluePurple')

layout = [[sg.Frame('Estimated parameters related mostly to propeller aerodynamics, \n these are the defaults and '
                    'you probably do not need to change them:', [[
        sg.T('Aspect ratio:'), sg.In('5', key='A', size=(2,2)), sg.T('\u03B5:'), sg.In('0.85', key='epsilon', size=(4,2)),
        sg.T('\u03BB:'), sg.In('0.75', key='lambda', size=(4,2)), sg.T('\u03B6:'), sg.In('0.5', key='zeta', size=(4,2)),
        sg.T('e:'), sg.In('0.83', key='e', size=(4,2)), sg.T('C_fd'), sg.In('0.015', key='C_fd', size=(5,2)),
        sg.T('\u03B1\u2080:'), sg.In('0', key='alpha_0', size=(2, 2)), sg.T('K_0'), sg.In('6.11', key='K_0', size=(5, 2))]] )],

        [sg.Frame('Drone and Environment parameters:', [[
        sg.T('Temperature in Kelvin:'), sg.In('298.15', key='Temp', size=(7,2)),
        sg.T('Pressure in Pa:'), sg.In('101325', key='p', size=(7, 2)),
        sg.T('Mass in kg:'), sg.In('1.5', key='W', size=(4,2)),
        sg.T('Number of rotors'), sg.In('4', key='n_r', size=(3,2)) ]] )],

        [sg.Frame('Propeller Parameters', [[
        sg.T('Blade number:'), sg.In('2', key='B_p', size=(2,2)), sg.T('Diameter in inches:'), sg.In('10', key='D_p', size=(4,2)),
        sg.T('Pitch in inches:'), sg.In('4.5', key='H_p', size=(4,2)), sg.T('Set this to one if you want automatic estimation of propeller coefficients:'), sg.In('0', key='est', size=(3,2)) ]] )],

        [sg.Frame('Motor Parameters', [[
        sg.T('Motor constant (K_V0) in RPM/V:'), sg.In('400', key='K_V0', size=(5,2)), sg.T('Maximum current in A'), sg.In('30', key='I_m_max', size=(4,2))],
        [sg.T('No-load current in A'), sg.In('0.5', key='I_m0', size=(4,2)), sg.T('No-load Voltage in V'), sg.In('10', key='U_m0', size=(4,2)),
        sg.T('Motor resistance in Ohms'), sg.In('0.111', key='R_m', size=(6, 2))
        ]] )],

        [sg.Frame('ESC Parameters', [[
        sg.T('Max ESC current in A:'), sg.In('30', key='I_e_max', size=(3,2)), sg.T('ESC internal resistance in Ohms:'), sg.In('0.008', key='R_e', size=(4,2)),
        sg.T('Control current in A (1 is a standard value)'), sg.In('1', key='I_c', size=(3,2)) ]] )],

        [sg.Frame('Battery Parameters', [[
        sg.T('Battery capacity in mAh:'), sg.In('5000', key='C_b', size=(5,2)), sg.T('Battery internal resistance'), sg.In('0.0078', key='R_b', size=(6,2))],
        [sg.T('Battery voltage in V'), sg.In('22.8', key='U_b', size=(5,2)), sg.T('Batterry Depth of discharge (as a decimal)'), sg.In('0.8', key='DOD', size=(3,2)) ]] )],

        [sg.T('Name for the output file'), sg.In(key='FileName', size=(25,2))],

        [sg.Button('Run'), sg.Button('Exit')] ]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in  (None, 'Exit'):
        break
    if event == 'Run':
        A = float(values['A'])  # Aspect ratio, 'typical' value taken from paper but we can tailor it when applicable to our propeller
        EPSILON = float(values['epsilon'])  # Downwash correction factor, also taken from paper
        LAMBDA = float(values['lambda']) # Correction coefficient of the blade airfoil area, also taken from paper
        ZETA = float(values['zeta'])  # Another correction factor related to the average rotor linear speed
        e = float(values['e'])  # Oswald factor, estimation from paper but we can also adjust if known better
        C_fd = float(values['C_fd'])  # Zero lift drag coefficient, again can adjust if known better
        ALPHA_0 = float(values['alpha_0'])  # Zero-lift angle in rad, same comment as above can be adjusted
        K_0 = float(values['K_0'])  # slope of lift curve, also can be adjusted, paper took something slightly below 2*pi I imagine

        # Environment Parameters
        Temp = float(values['Temp'])  # ISA sea-level Temperature in Celsius
        p = float(values['p'])  # ISA sea-level pressure in Pa
        g = 9.81  # Acceleration due to gravity m/s^2
        R = 287.05  # Gas constant of air
        rho = p / (R * Temp)  # ISA sea-level density kg/m^3

        # General Parameters
        W = float(values['W']) * g  # Total weight in Newtons
        n_r = int(values['n_r'])

        # Propeller parameters
        B_p = int(values['B_p']) # Nunmber of blades, optimal is 2 from research
        D_p = float(values['D_p']) * 0.0254  # Propeller diameter in m (the 0.0254 is conversion from in. to m)
        H_p = float(values['H_p']) * 0.0254  # Propeller pitch in m
        est_N = 0  #
        est_M = 0  #

        # Motor parameters
        K_V0 = int(values['K_V0'])  # Nominal no-load motor constant in r/min/V (RPM/V, revolutions per minute per volt)
        I_m_max = float(values['I_m_max'])  # Maximum motor current in Amps
        I_m0 = float(values['I_m0'])  # Motor nominal no-load current in Amps
        U_m0 = float(values['U_m0'])  # Motor nominal no-load voltage in Volts
        R_m = float(values['R_m'])  # Motor resistance in Ohms
        # G_m = blah # # Weight of Motor, not really relevant for this calculations since we start with total weight

        ### ESC (Electronic speed converter) parameters
        I_e_max = float(values['I_e_max'])  # Max ESC current in Amps
        R_e = float(values['R_e'])  # Internal resistance of ESC in Ohms
        I_c = float(values['I_c'])  # Control current supplied to the flight controller in Amps, usually 1 A (from paper).
        # G_e = blah # Weight of ESC, not really relevant for this calculations since we start with total weight

        ### Battery parameters
        C_b = float(values['C_b'])  # Battery capacity in mAh
        R_b = float(values['R_b'])  # Battery internal resistance in Ohms
        U_b = float(values['U_b'])  # Battery voltage in Volts
        # K_b = float(values['K_b'])  # Maximum discharge rate in Coulombs
        DOD = float(values['DOD'])
        C_min = (1 - float(values['DOD'])) * C_b  # Basically just calculating minimum battery capacity assuming a DoD, in this case assuming 80% DoD
        # G_b = blah # Also irrelevant like the others for now

        ### Propeller Model equations

        # Drag coefficient, estimated from paper and other coefficients/factors
        C_d = C_fd + ((np.pi * A * K_0 ** 2) * (EPSILON * np.arctan(H_p / (np.pi * D_p)) - ALPHA_0) ** 2) / (
                    e * (np.pi * A + K_0) ** 2)

        T_b, eff, P_req, sigma, N, I_e, U_e, I_b = H.hover_est(G.W, G.n_r, G.I_c, G.U_b)

        f = open('Input_and_Output_text_files/' + values['FileName'] + '.txt', 'w+')
        f.write(    'Power required is' + str(P_req) + 'W' +
                    '\n Hovering endurance is:' + str(T_b) + 'minutes' +
                    '\n Duty cycle is:'+ str(sigma * 100) + '%' +
                    'Propeller RPM is:'+ str(N) +
                    'ESC current is'+ str(I_e) + 'A' +
                    'ESC voltage is'+ str(U_e) + 'V' +
                    'Battery current is'+ str(I_b) + 'A' +
                    'Efficiency is'+ str(eff * 100) + '%' )


window.close()