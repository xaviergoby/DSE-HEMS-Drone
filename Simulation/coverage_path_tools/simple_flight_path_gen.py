import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# class SimpleFlightPathGen:
fig = plt.figure()
ax = plt.axes(projection='3d')




# Data for a three-dimensional line
z_line = np.linspace(0, 200, 10000)
x_line = np.sin(z_line)
y_line = np.cos(z_line)
ax.plot3D(x_line, y_line, z_line, 'black')

# Data for three-dimensional scattered points
# z_data = 200 * np.random.random(1000)
# x_data = np.sin(z_data) + 0.1 * np.random.randn(1000)
# y_data = np.cos(z_data) + 0.1 * np.random.randn(1000)
# ax.scatter3D(x_data, y_data, z_data, color="black")
# ax.scatter3D(x_data, y_data, z_data, c=z_data, cmap='Greens')
plt.show()