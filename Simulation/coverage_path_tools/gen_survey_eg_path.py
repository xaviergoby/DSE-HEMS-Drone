import airsim

boxsize = 50
stripewidth = 10
x = -50
z = -30

path = []
xs = []
distance = 0

while x < boxsize:
	distance += boxsize
	path.append(airsim.Vector3r(x, boxsize, z))
	x += stripewidth
	xs.append(x)
	distance += stripewidth
	path.append(airsim.Vector3r(x, boxsize, z))
	distance += boxsize
	path.append(airsim.Vector3r(x, -boxsize, z))
	x += stripewidth
	xs.append(x)
	distance += stripewidth
	path.append(airsim.Vector3r(x, -boxsize, z))
	distance += boxsize

# print(path)
# path_x_vals = [0, -50]
# path_y_vals = [0, 50]
# path_z_vals = [-30, -30]

path_x_vals = [-50]
path_y_vals = [50]
path_z_vals = [-30]
for p in path:
	x_val = p.x_val
	y_val = p.y_val
	z_val = p.z_val
	path_x_vals.append(x_val)
	path_y_vals.append(y_val)
	path_z_vals.append(z_val)
	print(f"\n{p}")
print(xs)
print(x)

# path_x_vals.append(0)
# path_y_vals.append(0)
# path_z_vals.append(-30)

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot3D([0, path_x_vals[0]], [0, path_y_vals[0]], [path_z_vals[0], path_z_vals[0]], ":k",label="flight to origin point")
ax.scatter3D(path_x_vals, path_y_vals, path_z_vals, color="red", label="rotational maneuvers")
plt.show()