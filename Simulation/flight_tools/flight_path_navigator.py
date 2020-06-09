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

class SurveyNavigator:
	def __init__(self, altitude, velocity):
		self.altitude = altitude  # 30
		self.velocity = velocity  # 5
		self.client = airsim.MultirotorClient()
		self.client.confirmConnection()
		self.client.enableApiControl(True)
		self.current_x_pos = None
		self.current_y_pos = None
		self.current_z_pos = None
		self.current_ned_coords_pos = None
		# self.scans = []
		# self.distance_data = []
		
	
	def start(self, take_off_time_duration=None):
		print("Arming the drone...")
		self.client.armDisarm(True)
		print("Drone armed!")
		
		drone_landed_state = self.client.getMultirotorState().landed_state
		if drone_landed_state == airsim.LandedState.Landed:
			print("Drone State: LANDED")
			if take_off_time_duration is None:
				timeout_sec = 20
			else:
				timeout_sec = take_off_time_duration
			print("Drone Taking-Off...\nTake-Off Duration [sec]: {0}".format(timeout_sec))
			take_off_start_time = datetime.datetime.now().strftime("%H-%M-%S")
			print("Take-Off Start Time (H:M:S): {0}".format(take_off_start_time))
			self.client.takeoffAsync(timeout_sec).join()
			take_off_end_time = datetime.datetime.now().strftime("%H-%M-%S")
			print("Drone State: Take-Off Complete")
			print("Take-Off End Time (H:M:S): {0}".format(take_off_end_time))
			drone_pos = self.client.simGetGroundTruthKinematics().position
			drone_ned_coords_pos = (drone_pos.x_val, drone_pos.y_val, drone_pos.z_val)
			self.current_x_pos = drone_pos.x_val
			self.current_y_pos = drone_pos.y_val
			self.current_z_pos = drone_pos.z_val
			self.current_ned_coords_pos = (self.current_x_pos, self.current_y_pos, self.current_z_pos)
			print("Drone Current NED Coord Sys Pos Coords: {0}".format(self.current_ned_coords_pos))
		
		# drone_landed_state = self.client.getMultirotorState().landed_state
		# if drone_landed_state == airsim.LandedState.Landed:
		# 	print("takeoff failed - check Unreal message log for details")
		# 	return
	
	def end(self):
		print("\nEnding API Control Over Drone in 3 seconds")
		print("Disconnection Start Time (H:M:S): {0}".format(datetime.datetime.now().strftime("%H-%M-%S")))
		time.sleep(3)
		self.client.armDisarm(False)
		print("Drone Disarmbed")
		self.client.reset()
		print("Drone State Reset")
		self.client.enableApiControl(False)
		print("API Control Disabled")
		print("Disconnection End Time (H:M:S): {0}".format(datetime.datetime.now().strftime("%H-%M-%S")))
		return
	
	def parse_lidarData(self, data):
		
		# reshape array of floats to array of [X,Y,Z]
		points = np.array(data.point_cloud, dtype=np.dtype('f4'))
		points = np.reshape(points, (int(points.shape[0] / 3), 3))
		
		# transform from local to global reference frame
		position = np.array([data.pose.position.x_val, data.pose.position.y_val, data.pose.position.z_val])
		rotation = R.from_quat([data.pose.orientation.x_val, data.pose.orientation.y_val, data.pose.orientation.z_val,
		                        data.pose.orientation.w_val]).as_matrix()
		
		distances = np.zeros((points.shape[0], 1))
		
		for index in range(len(points)):
			points[index] = np.matmul(rotation, points[index])
			points[index] = np.add(position, points[index])
			
			vector = np.subtract(points[index], position)
			distances[index] = math.sqrt(np.dot(vector, vector))
		
		return points, distances
		
	def collect_lidar_data(self):
		#### LIDAR DATA ####
		lidarData = self.client.getLidarData()
		if (len(lidarData.point_cloud) < 3):
			print("\tNo points received from Lidar data")
		else:
			scan, distance = self.parse_lidarData(lidarData)
			# print("\tReading %d: time_stamp: %d number_of_points: %d" % (i, lidarData.time_stamp, len(scan)))
			print("\t\tlidar position: %s" % (pprint.pformat(lidarData.pose.position)))
			print("\t\tlidar orientation: %s" % (pprint.pformat(lidarData.pose.orientation)))
			
			if not hasattr(self, 'scans'):
				self.scans = scan
			else:
				self.scans = np.vstack((self.scans, scan))
			
			if not hasattr(self, 'distances'):
				self.distances = distance
			else:
				self.distances = np.vstack((self.distances, distance))
		
		
	def nav_path_way_points(self, path_way_points):
		path_way_point_i_idx = 0
		path_start_way_point_pos = path_way_points[0]
		path_end_way_point_pos = path_way_points[-1]
		# while self.current_x_pos != path_end_way_point_pos[0] and self.current_y_pos != path_end_way_point_pos[1]:
		while path_way_point_i_idx <= len(path_way_points)-1:
			path_way_point_i = path_way_points[path_way_point_i_idx]
			x_i_pos = path_way_point_i[0]
			y_i_pos = path_way_point_i[1]
			print("\nDrone flying to {0} at {1} [m/s]".format((x_i_pos, y_i_pos, self.current_z_pos), self.velocity))
			print("Flight To Way Point Start Time (H:M:S): {0}".format(datetime.datetime.now().strftime("%H-%M-%S")))
			self.client.moveToPositionAsync(x_i_pos, y_i_pos, self.current_z_pos, self.velocity)
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
	
	drone_nav = SurveyNavigator(10, 5)
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
	                  (0, 20, -1), (0,  25, -1), (0, 30, -1),
	                  (5, 30, -1), (10,  30, -1), (15, 30, -1),
	                  (20, 35, -1), (25,  40, -1), (30, 45, -1),
	                  (35, 35, -1), (40,  40, -1), (45, 45, -1),
	                  (50, 35, -1), (55,  40, -1), (60, 45, -1)]
	
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
