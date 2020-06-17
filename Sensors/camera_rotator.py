import numpy as np
import matplotlib.pyplot as plt

def get_mmoi(w, h, m):
    return m * (w**2 + h**2) / 12

def get_moment(mmoi, acceleration):
    return mmoi * acceleration

def get_acceleration(time, angle):
    return angle * 2 / (time*0.5)**2

angle = np.pi/2 # rad
w_rgb, h_rgb, m_rgb = 0.038, 0.038, 0.056
w_ir, h_ir, m_ir = 0.044, 0.057, 0.115
time = 5 # seconds

mmoi = get_mmoi(w_rgb, h_rgb, m_rgb) + get_mmoi(w_ir, h_ir, m_ir)
acceleration = get_acceleration(time, angle)
moment = get_moment(mmoi, acceleration)

print(f"To rotate {angle} radians in {time} seconds, an acceleration of {acceleration} rad/s^2 is needed.\
 With mass moment of inertia of {mmoi}, a moment of {moment} Nm is required from the electromotor.")
print(f"This is {moment*1000} Nmm.")