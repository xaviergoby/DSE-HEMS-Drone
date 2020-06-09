import numpy as np
import bpy

coords = np.loadtxt("coords.txt")
dist =  np.loadtxt("distances.txt")

print(coords.shape, dist.shape)
