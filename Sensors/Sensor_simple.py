import numpy as np
import matplotlib.pyplot as plt
rotate_speed = 360 #deg/s
resolution = 1.4 #deg
fov = 90 #deg
pixels = fov / resolution
sizes = [0.01, 0.1, 0.2, 0.5, 1]
velocity = np.linspace(0,10,100) #m/s
size = 0.1 #m
fly_height = 3 #m

def get_distance(size):
    #input is the size of an object and output will be the minimum distance required to sense
    return size / np.sin(np.deg2rad(resolution))

distance_object = get_distance(size)
spacing_measure = np.sqrt(1.5 * 360 / (rotate_speed ) * velocity - fly_height)
plt.plot(velocity, spacing_measure)
plt.show()