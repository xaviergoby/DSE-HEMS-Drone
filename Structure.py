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
maxT= 80 #N
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
#%% The V beam
def Vbeam(a,d):
    #Section 1 is defined as the section coming out of the sidewall of the drone
    # Section 2 is defined as the section connecting 1 and the landing gear+rotor
    # Assume negligble aeroloads
    alpha=a #degrees
    Dv= 0.15 #m
    Dh= 0.25 #m
    #Length of the first section
    Ls1= Dv/np.cos(alpha*np.pi/180)
    #Length of section 1 in h direction
    Ls1_h=np.tan(alpha*np.pi/180)*Dv
    Ls2=Dh-Ls1_h
    #The force and momennt translation of Ls2
    Ry_ls2=maxT-Wa
    M_Ls1=Ls2*Ry_ls2
    T_s2= -M_Ls1*np.cos(alpha*np.pi/180)
    M_s2= M_Ls1*np.sin(alpha*np.pi/180)
    #moment at the origin
    M_O=M_s2+Ry_ls2*Ls1
    #Torque at the origin
    T_s2=T_s2
    
    #Now for a test, the original thrust force should also give the last 2 results
    # in the origin
    TT=np.cos(alpha*np.pi/180)*Ls2*Ry_ls2
    if (TT-T_s2)/T_s2<0.05 and (TT-T_s2)/T_s2>-0.05:
        print("Torque test pass")
    else:
        print("problems!!!!!!!!")
    TMoment= Ry_ls2*(Ls1+np.sin(alpha*np.pi/180)*Ls2)
    if ((TMoment-M_O)/M_O)<0.05 and ((TMoment-M_O)/M_O)>-0.05:
        print("Moment test pass")
    else:
          print("problems!!!!!!!!")
    aeroload=(Ls1+Ls2)
    print(M_s2,"N*m max moment on s2(applied at end of s1)")
    print(T_s2,"N*m Torque")
    print ("Total should remain unchanged",(np.sqrt(M_O**2+T_s2**2)))
    print("aerload",aeroload)
    return Ls1,Ls2,Ls1_h,aeroload
    
#%%

for i in range (1,58):
    print ("current i:", i)
    Ls1,Ls2,Ls1_h,aeroload=Vbeam(i,0.02)
    if aeroload<maxingf:
        maxingf=aeroload
        itest=i
# The helicopter attachment