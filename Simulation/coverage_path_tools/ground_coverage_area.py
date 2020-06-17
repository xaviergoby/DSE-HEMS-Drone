import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches

TYPE = "Circle"

radius = 100

circ = Circle((0, 100), radius=100, fill=False)
# circ.center == (1,2) #should return True

fig, ax = plt.subplots()
# change default range so that new circles will work
ax.set_xlim((-200, 200))
ax.set_ylim((-100, 300))
ax.set_aspect('equal')

plt.grid(True)

ax.add_artist(circ)

# codes = [Path.MOVETO] + [Path.LINETO]*3 + [Path.CLOSEPOLY]
# vertices = [(0, 0), (-100, 100), (0, 200), (100, 100), (0, 0)]
codes = [Path.MOVETO] + [Path.LINETO]*5 + [Path.CLOSEPOLY]
vertices = [(0, 0), (-87, 50), (-87, 150), (0, 200), (87, 150), (87, 50), (0, 0)]

vertices = np.array(vertices, float)
path = Path(vertices, codes)
# Path = mpath.Path
# fap1 = mpatches.FancyArrowPatch(path=Path([(0, 0), (1, 1), (1, 0)], [Path.MOVETO, Path.CURVE3, Path.CURVE3]),)

pathpatch = PathPatch(path, facecolor='None', edgecolor='green')

# fig, ax = plt.subplots()
ax.add_patch(pathpatch)
ax.set_title('A compound path')

ax.dataLim.update_from_data_xy(vertices)
ax.autoscale_view()

# ax.arrow(0, 0, -100, 100, head_width=0.05, head_length=0.1, fc='k', ec='k')


#########################################################
# HARD CODED WORLD REF FRAME FLIGHT PATH:
# WAYPOINTS IN NED COORDS
point_1 = [0, 0]
point_2 = [-100, 100]
point_3 = [0, 200]
point_4 = [100, 100]
# (3D) DISPLACEMENTS VECTOR IN NED COORDS
vect_1 = [-100, 100] # ds_vect_12
vect_2 = [100, 100] # ds_vect_23
vect_3 = [100, -100] # ds_vect_34
vect_4 = [-100, -100] # ds_vect_41


#########################################################
# COMPUTED WORLD REF FRAME FLIGHT PATH:
# (3D) DISPLACEMENTS VECTOR IN NED COORDS (e.g. ds12 = (x2 - x1, y2 - y1))
ds_vect_12 = [point_2[0] - point_1[0], point_2[1] - point_1[1]]
ds_vect_23 = [point_3[0] - point_2[0], point_3[1] - point_2[1]]
ds_vect_34 = [point_4[0] - point_3[0], point_4[1] - point_3[1]]
ds_vect_41 = [point_1[0] - point_4[0], point_1[1] - point_4[1]]



# ax.arrow(0, 0, -100, 100,
#          head_width=5, head_length=10,
#          fc='k', ec='k',
#          length_includes_head=True)
#
# ax.arrow(-100, 100, 100, 100,
#          head_width=5, head_length=10,
#          fc='k', ec='k',
#          length_includes_head=True)
#
# ax.arrow(0, 200, 100, -100,
#          head_width=5, head_length=10,
#          fc='k', ec='k',
#          length_includes_head=True)
#
# ax.arrow(100, 100, -100, -100,
#          head_width=5, head_length=10,
#          fc='k', ec='k',
#          length_includes_head=True)

plt.show()


# ax.plot()
plt.show()

env_origin_pnt_ned_coords = [0, 0, 0]