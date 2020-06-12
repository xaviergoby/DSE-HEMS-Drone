import numpy as np

from matplotlib import cm
import open3d as o3d

coords = np.loadtxt('coords1.txt')
distances = np.loadtxt('distances.txt')

cmap = cm.get_cmap("Spectral")
colors = cmap(distances.flatten() / np.max(distances))
colors = colors[:, 0:3]

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(coords)
# pcd.colors = o3d.utility.Vector3dVector(colors)

downpcd = pcd.voxel_down_sample(voxel_size=1)
o3d.visualization.draw_geometries([downpcd])