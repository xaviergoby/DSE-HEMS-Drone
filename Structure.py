# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:40:25 2020

@author: Joost
"""
'''This program is calculating the thickness of the beam that you would need 
to carry the aerodynamic load, weight and thrust load at the end of the beam
Assumptions:
1.The beam itself has no weight load(should be very small compared to motor and length is not too large as well)
2.The beam is a cantilever beam it should be sufficiently strong enough mounted to the drone
'''
AeroL= 30       #{N/m}, Aerodynamic load is assumed uniform
Mmotor=1 #[kg] Mass of the motor
Mg= 1 # [kg]Mass of the structure including landing gear)
Lbeam=0.3 # meters, the length of the whole beam
LD= 1/3. #The division in thick/small beam
