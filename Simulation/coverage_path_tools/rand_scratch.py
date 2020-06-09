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

ax.plot3D(path_x_vals, path_y_vals, path_z_vals, 'black', label="scanning flight path")
# ax.plot3D([0], [0], [-30], 'green')
# ax.scatter3D(path_x_vals, path_y_vals, path_z_vals, c=path_z_vals, cmap='Greens')
ax.scatter3D([0], [0], [-30], color="green", label="survey flight path origin point")
ax.plot3D([0, 0], [0, 0], [0, -30], "--k", label="take-off")
ax.plot3D([0, path_x_vals[0]], [0, path_y_vals[0]], [path_z_vals[0], path_z_vals[0]], ":k", label="flight to origin point")
ax.scatter3D(path_x_vals, path_y_vals, path_z_vals, color="red", label="rotational maneuvers")
ax.plot3D([0, path_x_vals[-1]], [0, path_y_vals[-1]], [path_z_vals[-1], path_z_vals[-1]], "-.k", label="return to origin")
# ax.scatter3D([0], [0], [-30], color="green")
ax.axes.set_zlim3d(bottom=0, top=-60)
# plt.plot(path_x_vals, path_y_vals)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.text(0, 0, -30, "O", color='green', fontsize=12)
# ax.text(path_x_vals[0], path_y_vals[0], path_z_vals[0], "P1", color='green', fontsize=12)
ax.text(path_x_vals[1], path_y_vals[1], path_z_vals[1], "P1", color='green', fontsize=12)
ax.text(path_x_vals[2], path_y_vals[2], path_z_vals[2], "P2", color='green', fontsize=12)
ax.text(path_x_vals[3], path_y_vals[3], path_z_vals[3], "P3", color='green', fontsize=12)
ax.text(path_x_vals[4], path_y_vals[4], path_z_vals[4], "P4", color='green', fontsize=12)
# ax.text2D(0, 0, -30, "O (0, 0, -30)", color='green')
plt.legend()
# ax.label()
plt.show()