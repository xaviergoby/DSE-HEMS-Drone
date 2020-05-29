import numpy as np

rotate_speed = 0 #Rad/s
resolution = 1.4 #deg
fov = 90 #deg
pixels = fov / resolution
sizes = [0.01, 0.1, 0.2, 0.5, 1]

def get_distance(size):
    #input is the size of an object and output will be the minimum distance required to sense
    return size / np.sin(np.deg2rad(resolution))

for size in sizes:
    print(size, "m", get_distance(size), "m")

