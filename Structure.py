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
3. Thin-walled circular section meaning moment of intertia neglection of higher order terms
'''
import numpy as np

AeroL= 0.10       #{N/m}, Aerodynamic load is assumed uniform pointed towards ground is +
Mmotor=0.25 #[kg] Mass of the motor
Mg= 0.1 # [kg]Mass of the structure including landing gear)
Lbeam=0.3 # meters, the length of the whole beam
LD= 2/3. #The division in thick/small beam
maxT= 40 #N
Wa=9.81*(Mg+Mmotor)
d=0.02 #Diameter of the circular hollow shaft
t=0.001 #m thickkness of the shaft
# the largest load we need to calculate for

Ry=maxT-Wa-AeroL*Lbeam
Rm=-maxT*Lbeam+Wa*Lbeam+AeroL*Lbeam**2/2
Ry=-Ry
Rm=-Rm
print (Ry,Rm)

# area moment of inertia
#For circular shaft
I_x=np.pi*d**3*t/8
#bendingstress
BS=Rm*(d/2)/I_x
BS=BS/10**6
print (BS,"MPa")