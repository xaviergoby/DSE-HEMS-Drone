import numpy as np
import math
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import airsim


def get_cls_instance_properties(cls_instance):
	return [i for i in cls_instance.__dict__.keys() if i[:1] != '_']

class CylindricalSurveillanceAirspace:

	def __init__(self):
		self.radius = 100 # meter
		self.height = 200 # meter


class PolygonalFlightPath:

	def __init__(self, airspace, num_sides=4, alt=-10, mode="sim", clock_wise_nav=True):
		self.airspace = airspace
		for airspace_cls_attr_i_key in self.airspace.__dict__:
			setattr(self, airspace_cls_attr_i_key, self.airspace.__dict__[airspace_cls_attr_i_key])
		self.num_sides = num_sides
		self.alt = alt
		self.init_angular_deg_coord = 270
		self.init_flight_path()
	# self.clock_wise_nav = clock_wise_nav

	def generate_flight_path_way_points(self):
		# deg_coords = list(np.linspace(self.init_angular_deg_coord, 0, self.num_sides))
		deg_coords = list(np.arange(self.init_angular_deg_coord, -90, -360/self.num_sides))
		rad_coords = [np.deg2rad(deg) for deg in deg_coords]
		circumference_way_points = np.round([(math.cos(rad) * self.airspace.radius, math.sin(rad)*self.airspace.radius+100, self.alt) for rad in rad_coords])
		# circumference_way_points_2d = np.array([circumference_way_points[:2] for way_point_i in circumference_way_points])
		circumference_way_points_copy = circumference_way_points.copy()
		circumference_way_points_copy[circumference_way_points_copy == -0.0] = 0
		return circumference_way_points_copy

	def generate_flight_path_ds_vectors(self, return_airsim_ds_vectors=True, return_way_pnts=False):
		path_way_points_3d = self.generate_flight_path_way_points()
		ds_vectors_2d = []
		airsim_ds_vectors = []
		for way_point_i_idx in range(len(path_way_points_3d)):
			ds_vect_i_start_pnt_idx = way_point_i_idx
			if ds_vect_i_start_pnt_idx == len(path_way_points_3d) - 1:
				ds_vect_i_end_pnt_idx = 0
			else:
				ds_vect_i_end_pnt_idx = ds_vect_i_start_pnt_idx + 1
			ds_vect_i_x_cmpt = path_way_points_3d[ds_vect_i_end_pnt_idx][0] - path_way_points_3d[ds_vect_i_start_pnt_idx][0]
			ds_vect_i_y_cmpt = path_way_points_3d[ds_vect_i_end_pnt_idx][1] - path_way_points_3d[ds_vect_i_start_pnt_idx][1]
			ds_vect_i = [ds_vect_i_x_cmpt, ds_vect_i_y_cmpt]
			airsim_ds_vect_i = airsim.Vector3r(ds_vect_i_x_cmpt, ds_vect_i_y_cmpt, self.alt)
			ds_vectors_2d.append(ds_vect_i)
			airsim_ds_vectors.append(airsim_ds_vect_i)
		# path_way_points_2d = path_way_points_3d
		return airsim_ds_vectors, ds_vectors_2d, path_way_points_3d
	# if return_airsim_ds_vectors is False and return_way_pnts is False:
	# 	return ds_vectors_2d
	# elif return_airsim_ds_vectors is False and return_way_pnts is True:
	# 	return ds_vectors_2d, path_way_points
	# elif return_airsim_ds_vectors is True and return_way_pnts is False:
	# 	return airsim_ds_vectors
	# else:
	# 	return airsim_ds_vectors, path_way_points

	# def gen_2d_flight_path(self):
	# 	ds_vectors, way_points = self.generate_flight_path_ds_vectors(return_airsim_ds_vectors=False, return_way_pnts=True)
	# 	return ds_vectors, way_points

	# def gen_3d_flight_path(self):
	# 	airsim_ds_vectors, way_points = self.generate_flight_path_ds_vectors(return_airsim_ds_vectors=True, return_way_pnts=True)
	# 	return airsim_ds_vectors, way_points

	def gen_flight_path(self):
		flight_path_generated = self.generate_flight_path_ds_vectors()
		return flight_path_generated

	def init_flight_path(self):
		self.airsim_ds_vectors, self.ds_vectors_2d, self.way_points = self.gen_flight_path()
		self.flight_path_dict = {"airsim_ds_vectors":self.airsim_ds_vectors, "ds_vectors_2d":self.ds_vectors_2d, "way_points":self.way_points}


# #########################################################
# # HARD CODED WORLD REF FRAME FLIGHT PATH:
# # WAYPOINTS IN NED COORDS
# point_1 = [0, 0]
# point_2 = [-100, 100]
# point_3 = [0, 200]
# point_4 = [100, 100]
# # (3D) DISPLACEMENTS VECTOR IN NED COORDS
# vect_1 = [-100, 100] # ds_vect_12
# vect_2 = [100, 100] # ds_vect_23
# vect_3 = [100, -100] # ds_vect_34
# vect_4 = [-100, -100] # ds_vect_41
#
#
# #########################################################
# # COMPUTED WORLD REF FRAME FLIGHT PATH:
# # (3D) DISPLACEMENTS VECTOR IN NED COORDS (e.g. ds12 = (x2 - x1, y2 - y1))
# ds_vect_12 = [point_2[0] - point_1[0], point_2[1] - point_1[1]]
# ds_vect_23 = [point_3[0] - point_2[0], point_3[1] - point_2[1]]
# ds_vect_34 = [point_4[0] - point_3[0], point_4[1] - point_3[1]]
# ds_vect_41 = [point_1[0] - point_4[0], point_1[1] - point_4[1]]


if __name__ == "__main__":
	# import math
	# n = 4
	# r = 100
	# pi = math.pi
	# # pnts_rounded = [(round(math.cos(2 * pi / n * x) * r, 0), round(math.sin(2 * pi / n * x) * r, 0)) for x in range(0, n + 1)]
	# angular_deg_coords_way_points = list(np.linspace(270, 0, n))
	# angular_rad_coords_way_points = [np.deg2rad(deg) for deg in angular_deg_coords_way_points]
	# my_pnts_rounded = [(round(math.cos(rad) * r, 0), round(math.sin(rad) * r, 0)) for rad in angular_rad_coords_way_points]
	# my_recentred_pnts_rounded = [(round(math.cos(rad) * r, 0), round(math.sin(rad) * r, 0)+100) for rad in angular_rad_coords_way_points]
	# pnts2 = np.round([(math.cos(rad) * r, math.sin(rad) * r + 100) for rad in angular_rad_coords_way_points])


	airspace = CylindricalSurveillanceAirspace()
	flight_path = PolygonalFlightPath(airspace, num_sides=6, alt=-30)
	# airspace_properties = get_cls_instance_properties(airspace)
	# flight_path_properties = get_cls_instance_properties(flight_path)
	print(flight_path.ds_vectors_2d)
	print(flight_path.way_points)
	print(flight_path.airsim_ds_vectors)
	print(flight_path.flight_path_dict)
# print(f"airspace_properties: {airspace_properties}")
# print(f"flight_path_properties: {flight_path_properties}")
# pnts_res = flight_path.generate_flight_path_way_points()
# vectors_res = flight_path.generate_flight_path_ds_vectors()
# print(pnts_res)
# print(vectors_res)


