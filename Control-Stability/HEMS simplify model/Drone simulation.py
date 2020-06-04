import control as ctr
import numpy as np

import matplotlib.pyplot as plt
import scipy.io
g=9.81
m=10
L1=1
L2=1
Ix=10
Iy=10
Iz=10
c=1

#T1=
#output pitch roll yaw
A=([[0,0,0,1,0,0,0,0,0,0,0,0],
           [0,0,0,0,1,0,0,0,0,0,0,0],
           [0,0,0,0,0,1,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,1,0,0],
           [0,0,0,0,0,0,0,0,0,0,1,0],
           [0,0,0,0,0,0,0,0,0,0,0,1],
           [g,0,0,0,0,0,0,0,0,0,0,0],
           [0,-g,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0]])
B=([[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,L1/Ix,0,0],
            [0,0,L2/Iy,0],
            [0,0,0,c/Iz],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [1/m,0,0,0]])
C=([[1,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0]])
D=([[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]])
##K=np.array([[Kp_pitch,Ki_pitch,Kd_pitch],
##            [Kp_roll,Ki_roll,Kd_roll],
##            [Kp_yaw,Ki_yaw,Kd_yaw]])
eigvalsSym = np.linalg.eig(A)
print("eigenvalues " ,eigvalsSym)
sys2 = ctr.ss(A,B,C,D)

           
