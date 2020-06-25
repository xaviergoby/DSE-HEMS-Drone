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
maxT= 35*1.5 #N
Wa=9.81*(Mg+Mmotor)
d=0.02 #Diameter of the circular hollow shaft
t=0.0020 #m thickkness of the shaft
# the largest load we need to calculate for

Ry=maxT-Wa-AeroL*Lbeam
Rm=-maxT*Lbeam+Wa*Lbeam+AeroL*Lbeam**2/2
Ry=-Ry
Rm=-Rm
#print (Ry,Rm)

# area moment of inertia
#For circular shaft
I_x=np.pi*d**3*t/8
#bendingstress
BS=Rm*(d/2)/I_x
BS=BS/10**6
#print (BS,"MPa")
#%% The V beam
def Vbeam(a,d,maxT,Wa):
    #Section 1 is defined as the section coming out of the sidewall of the drone
    # Section 2 is defined as the section connecting 1 and the landing gear+rotor
    # Assume negligble aeroloads
    #This script is a mess, it tries to calculate loads along a V shaped beam
    #It was used as a  first iteration, but it currently serves no purpose
    alpha=a #degrees
    Dv= 0.15 #m
    Dh= 0.25 #m
    t=1/1000.
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
    TT=-np.cos(alpha*np.pi/180)*Ls2*Ry_ls2
    TMoment= Ry_ls2*(Ls1+np.sin(alpha*np.pi/180)*Ls2)
   # if (TT-T_s2)/T_s2<0.05 and (TT-T_s2)/T_s2>-0.05:
      #  print("Torque test pass")
    #else:
     #   print("problems!!!!!!!!")
    #    print (TT,T_s2)
    #if ((TMoment-M_O)/M_O)<0.05 and ((TMoment-M_O)/M_O)>-0.05:
    #    print("Moment test pass")
  # else:
      #    print("problems!!!!!!!!")
          
    aeroload=(Ls1+Ls2)
    #print(M_s2,"N*m max moment on s2(applied at end of s1)")
    #print(T_s2,"N*m Torque")
   # print ("Total should remain unchanged",(np.sqrt(M_O**2+T_s2**2)))
   # print("aerload",aeroload)
    I_x=np.pi*d**3*t/8
    BS=TMoment*(d/2)/I_x
    BS=BS/10**6
   # print (BS,"MPa")
    return Ls1,Ls2,Ls1_h,aeroload,TT,TMoment
    
#%%
#maxingf=100
#for i in range (1,58):
#    print ("current i:", i)
#    Ls1,Ls2,Ls1_h,aeroload,TT,Tmoment=Vbeam(i,0.02,maxT,Wa)
#    if aeroload<maxingf:
#        maxingf=aeroload
#        itest=i
#%% Deflection of the beam calculations
# it is solving the virtual work equation found in the final report
# you can change t, and d the diameter and thickness of the beam.
# you will get a deflection estimate, and a weight estimate
from scipy import integrate
s=1
#Ls1,Ls2,Ls1_h,aeroload,TT,TMoment= Vbeam(35,0.02,31,0)
G=3.5*10**10
J=np.pi*t*d**3*0.25 #m^4
#FL^2/(2EI)
d=25*10**(-3) #m
t=1.8*10**-3 #m
I_x=np.pi*d**3*t/8. #m^4
Density=1500.
F=maxT
Sh=204*10**(-3)
Sv=222*10**(-3)
E=69*10**9
L3=66*10**(-3)
L2=(220+21)*10**(-3)
L1=25*10**(-3)
M23=np.sin(35.*np.pi/180.)*L3*F
T23=np.cos(35.*np.pi/180.)*L3*F
M12=(222-L1)*10**(-3)*F #See sketch
T12=Sh*F
integrate.quad(lambda x: 1, 0, 4.5)[0]
#IL1=(Sv-L1)*F+ s**2*F+2*s*(Sv-L1)*F
#IL1Toruqe=Sh**2F
MaxTorque=Sh*F/(2*np.pi*(d/2)**2*t)/10**6
MaxM=Sv*F*(d/2)/I_x
MaxM=MaxM/10**6

IL2=F*(np.sin(35*np.pi/180))**2*L3**2+F*s**2+2*F*s*L3*np.sin(35*np.pi/180)
IL2Torque=(np.cos(35*np.pi/180))**2*L3*F
IL3=s**2*F

deflectionL1= (1/(E*I_x))*integrate.quad(lambda s: (Sv-L1)*F+ s**2*F+2*s*(Sv-L1)*F, 0, L1)[0]+ (1/(G*J))*integrate.quad(lambda x: Sh**2*F, 0,L1)[0]
deflectionL2= (1/(E*I_x))*integrate.quad(lambda s: IL2, 0, L2)[0]+ (1/(G*J))*integrate.quad(lambda s: IL2Torque, 0, L2)[0]
deflectionL3= (1/(E*I_x))*integrate.quad(lambda s: s**2*F, 0, L3)[0]
# (1/(G*J))    (1/(E*I_x))
print((deflectionL1+deflectionL2+deflectionL3)*1000)
totaldeflection=(deflectionL1+deflectionL2+deflectionL3)
Volume=(L1+L2+L3)*(d/2)**2*np.pi-((L1+L2+L3)*((d-2*t)/2)**2*np.pi)
Weight=Volume*Density
print (Weight)

L=301.5*10**(-3)
angle=np.arcsin(totaldeflection/L)*180/np.pi
