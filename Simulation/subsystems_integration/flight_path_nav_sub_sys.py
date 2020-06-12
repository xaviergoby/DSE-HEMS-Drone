import airsim
import time
import datetime
import pprint
from scipy.spatial.transform import Rotation as R
import sys
import math
import argparse
import numpy as np


# boxsize	The overall size of the square box to survey
# stripewidth	How far apart to drive the swim lanes, this can depend on the type of camera lens , for example.
# altitude	The height to fly the survey.
# speed	The speed of the survey, can depend on how fast your camera can snap shots.

class FlightPathNavSubSystem:

	def __init__(self, client, altitude=10, velocity=5):
		self.client = client
		self.altitude = altitude  # e.g. 10
		self.velocity = velocity  # e.g. 5
		self.path_way_points_3d_vectors_list = []
		self.tot_flight_distance = 0
		self.tot_flight_time = 0

	def set_flight_path(self, path_way_points):
		self.create_path_way_points_3d_vectors_list(path_way_points)
		self.compute_set_and_get_tot_flight_path_distance_and_time()

	def create_path_way_points_3d_vectors_list(self, path_way_points):
		path_way_points_3d_vectors_list = []
		for path_way_point_i in path_way_points:
			path_way_point_i_x = path_way_point_i[0]
			path_way_point_i_y = path_way_point_i[1]
			path_way_point_i_z = path_way_point_i[2]
			path_way_point_i_3d_vector = airsim.Vector3r(path_way_point_i_x, path_way_point_i_y, path_way_point_i_z)
			path_way_points_3d_vectors_list.append(path_way_point_i_3d_vector)
		self.path_way_points_3d_vectors_list = path_way_points_3d_vectors_list
		# return self.path_way_points_3d_vectors_list

	# @staticmethod
	def compute_set_and_get_tot_flight_path_distance_and_time(self):
		tot_flight_distance = 0
		tot_flight_time = 0
		for path_way_point_i_3d_vector_idx in range(0, len(self.path_way_points_3d_vectors_list) - 1):
			start_point_3d_vect = self.path_way_points_3d_vectors_list[path_way_point_i_3d_vector_idx]
			end_point_3d_vect = self.path_way_points_3d_vectors_list[path_way_point_i_3d_vector_idx + 1]
			current_flight_distance = start_point_3d_vect.distance_to(end_point_3d_vect)
			current_flight_time = current_flight_distance / self.velocity
			tot_flight_distance = tot_flight_distance + current_flight_distance
			tot_flight_time = tot_flight_time + current_flight_time
		self.tot_flight_distance = tot_flight_distance
		self.tot_flight_time = tot_flight_time
		# return tot_flight_distance, tot_flight_time

	def fly_path(self):
		lookahead = self.velocity + (self.velocity / 2)
		self.client.moveOnPathAsync(self.path_way_points_3d_vectors_list, self.velocity,
									self.tot_flight_time, airsim.DrivetrainType.ForwardOnly,
									airsim.YawMode(False, 0), lookahead, 1)



	# def fly_on_path(self):
	# 	drone_init_kinematics_info = self.client.simGetGroundTruthKinematics()
	# 	drone_init_pos_x_coord = drone_init_kinematics_info.position.x_val
	# 	drone_init_pos_y_coord = drone_init_kinematics_info.position.y_val
	# 	drone_init_pos_z_coord = drone_init_kinematics_info.position.z_val
	# 	path_departure_pmt_3d_vect = airsim.Vector3r(drone_init_pos_x_coord, drone_init_pos_y_coord, drone_init_pos_z_coord)
	# 	print("flying on path...")
	# 	for path_3d_vectors_way_point_i_idx in range(len(self.path_way_points_3d_vectors_list)):
	# 		path_3d_vector_way_point_i = self.path_way_points_3d_vectors_list[path_3d_vectors_way_point_i_idx]
	# 		flight_distance = path_3d_vector_way_point_i.distance_to(path_departure_pmt_3d_vect)
	# 		# flight_time =
	# 		print(f"path_3d_vector_way_point_i: {path_3d_vector_way_point_i}")
	# 		result = self.client.moveOnPathAsync([airsim.Vector3r(125, 0, z), airsim.Vector3r(125, -130, z),
	# 											  airsim.Vector3r(0, -130, z),
	# 											  airsim.Vector3r(0, 0, z)],
	# 											 12, 120,
	# 											 airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0), 20,
	# 											 1).join()
	# 		print(f"path_3d_vector_way_point_i: {path_3d_vector_way_point_i}")
	#
	# # drone_pos = self.client.simGetGroundTruthKinematics().position
	# # current_x_pos = drone_pos.x_val
	# # current_y_pos = drone_pos.y_val
	# # current_z_pos = drone_pos.z_val

	def nav_path_way_points(self, path_way_points):
		path_way_point_i_idx = 0
		path_start_way_point_pos = path_way_points[0]
		path_end_way_point_pos = path_way_points[-1]
		# while self.current_x_pos != path_end_way_point_pos[0] and self.current_y_pos != path_end_way_point_pos[1]:
		while path_way_point_i_idx <= len(path_way_points) - 1:
			path_way_point_i = path_way_points[path_way_point_i_idx]
			path_way_point_i_x = path_way_point_i[0]
			path_way_point_i_y = path_way_point_i[1]
			path_way_point_i_z = path_way_point_i[2]
			# x_i_pos = path_way_point_i[0]
			# y_i_pos = path_way_point_i[1]
			# print("\nDrone flying to {0} at {1} [m/s]".format((x_i_pos, y_i_pos, self.current_z_pos), self.velocity))
			# print("Flight To Way Point Start Time (H:M:S): {0}".format(datetime.datetime.now().strftime("%H-%M-%S")))
			self.client.moveToPositionAsync(path_way_point_i_x, path_way_point_i_y, path_way_point_i_z, self.velocity)
			time.sleep(1)
			print("Flight To Way Point End Time (H:M:S): {0}".format(datetime.datetime.now().strftime("%H-%M-%S")))
			path_way_point_i_idx = path_way_point_i_idx + 1
			drone_pos = self.client.simGetGroundTruthKinematics().position
			drone_state = self.client.getMultirotorState()
			drone_imu_data = self.client.getImuData()
			print("Drone IMU Orientation Data: {0}".format(drone_imu_data.orientation))
			print("Collcting LIDAR Data....")
			self.collect_lidar_data()
			print("Collected LIDAR Data!")
			self.current_x_pos = drone_pos.x_val
			self.current_y_pos = drone_pos.y_val
			self.current_z_pos = drone_pos.z_val
			self.current_ned_coords_pos = (self.current_x_pos, self.current_y_pos, self.current_z_pos)
		print("Drone Path Way Points Navigation Complete!")

	def save_lidar_data(self):
		total_scans = self.scans[0]
		for scan in self.scans[1::]:
			total_scans = np.vstack((total_scans, scan))
		np.savetxt('coords.txt', np.transpose(total_scans))

		total_distances = self.distances[0]
		for distances in self.distances[1::]:
			total_distances = np.vstack((total_distances, distances))
		np.savetxt('distances.txt', np.transpose(total_distances))

		np.savetxt('coords.txt', self.scans)
		np.savetxt('distances.txt', self.distances)


if __name__ == "__main__":
	from matplotlib import cm
	import open3d as o3d

	drone_nav = FlightPathNavSubSystem(10, 5)
	drone_nav.start(5)
	# drone_nav.end()
	# path_waypoints = [(5, 0, -1), (10, 0, -1), (15, 0, -1),
	#                   (15, 5, -1), (15, 10, -1), (15, 15, -1),
	#                   (10, 15, -1), (5, 15, -1), (0, 15, -1),
	#                   (0, 20, -1), (0,  25, -1), (0, 30, -1),
	#                   (5, 30, -1), (10,  30, -1), (15, 30, -1),
	#                   (20, 35, -1), (25,  40, -1), (30, 45, -1),
	#                   (35, 35, -1), (40,  40, -1), (45, 45, -1),
	#                   (50, 35, -1), (55,  40, -1), (60, 45, -1)]

	path_waypoints = [(5, 0, -1), (10, 0, -1), (15, 0, -1),
					  (15, 5, -1), (15, 10, -1), (15, 15, -1),
					  (10, 15, -1), (5, 15, -1), (0, 15, -1),
					  (0, 20, -1), (0, 25, -1), (0, 30, -1),
					  (5, 30, -1), (10, 30, -1), (15, 30, -1),
					  (20, 35, -1), (25, 40, -1), (30, 45, -1),
					  (35, 35, -1), (40, 40, -1), (45, 45, -1),
					  (50, 35, -1), (55, 40, -1), (60, 45, -1)]

	drone_nav.nav_path_way_points(path_waypoints)
	time.sleep(10)
	drone_nav.save_lidar_data()
	drone_nav.end()

	total_scans = drone_nav.scans[0]
	for scan in drone_nav.scans[1::]:
		total_scans = np.vstack((total_scans, scan))
	np.savetxt('coords.txt', np.transpose(total_scans))

	total_distances = drone_nav.distances[0]
	for distances in drone_nav.distances[1::]:
		total_distances = np.vstack((total_distances, distances))
	np.savetxt('distances.txt', np.transpose(total_distances))

	np.savetxt('coords.txt', drone_nav.scans)
	np.savetxt('distances.txt', drone_nav.distances)

	cmap = cm.get_cmap("Spectral")
	colors = cmap(drone_nav.distances.flatten() / np.max(drone_nav.distances))
	# colors = cm.jet(drone_nav.distances.flatten() / np.max(drone_nav.distances))
	colors = colors[:, 0:3]
	pcd = o3d.geometry.PointCloud()
	pcd.points = o3d.utility.Vector3dVector(drone_nav.scans)
	pcd.colors = o3d.utility.Vector3dVector(colors)

	downpcd = pcd.voxel_down_sample(voxel_size=1)
	o3d.visualization.draw_geometries([downpcd])
