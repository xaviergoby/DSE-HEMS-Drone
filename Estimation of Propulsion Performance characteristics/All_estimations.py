
'''
This is not finished but you can run the four individual estimation programs individually already,
just change the constants/parameters in the Governing_constants_and_equations.py file.
'''

import PySimpleGUI as sg

sg.theme('BluePurple')

layout = [[sg.Frame('Estimated parameters related mostly to propeller aerodynamics, \n these are the defaults and '
                    'you probably do not need to change them:', [[
        sg.T('Aspect ratio:'), sg.In('5', key='A', size=(2,2)), sg.T('\u03B5:'), sg.In('0.85', key='epsilon', size=(4,2)),
        sg.T('\u03BB:'), sg.In('0.75', key='lambda', size=(4,2)), sg.T('\u03B6:'), sg.In('0.5', key='zeta', size=(4,2)),
        sg.T('e:'), sg.In('0.83', key='e', size=(4,2)), sg.T('C_fd'), sg.In('0.015', key='C_fd', size=(5,2)),
        sg.T('\u03B1\u2080:'), sg.In('0', key='alpha_0', size=(2, 2)), sg.T('K_0'), sg.In('6.11', key='K_0', size=(5, 2))]] )],

        [sg.Frame('Drone and Environment parameters:', [[
        sg.T('Temperature in Kelvin:'), sg.In('298.15', key='Temp', size=(7,2)),
        sg.T('Mass in kg:'), sg.In('1.5', key='W', size=(4,2)),
        sg.T('Number of rotors'), sg.In('4', key='n_r', size=(3,2)) ]] )],

        [sg.Frame('Propeller Parameters', [[
        sg.T('Blade number:'), sg.In('2', key='B_p', size=(2,2)), sg.T('Diameter in inches:'), sg.In('10', key='D_p', size=(4,2)),
        sg.T('Pitch in inches:'), sg.In('4.5', key='H_p', size=(4,2)) ]] )],

        [sg.Frame('Motor Parameters', [[
        sg.T('Motor constant (K_V0) in RPM/V:'), sg.In(key='K_V0', size=(5,2)), sg.T('Maximum current in A'), sg.In('30', key='I_m_max', size=(4,2))],
        [sg.T('No-load current in A'), sg.In('0.5', key='I_m0', size=(4,2)), sg.T('No-load Voltage in V'), sg.In('10', key='U_m0', size=(4,2)),
        sg.T('Motor resistance in Ohms'), sg.In('0.111', key='R_m', size=(6, 2))
        ]] )],

        [sg.Frame('Propeller Parameters', [[
        sg.T('Max ESC current in A:'), sg.In('30', key='I_e_max', size=(3,2)), sg.T('ESC internal resistance in Ohms:'), sg.In('0.008', key='R_e', size=(4,2)),
        sg.T('Control current in A'), sg.In('1', key='I_c', size=(3,2)) ]] )],


          [sg.Input(key='-IN-')],
          [sg.Button('Show'), sg.Button('Exit')] ]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in  (None, 'Exit'):
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

window.close()