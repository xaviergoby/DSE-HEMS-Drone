import airsim
import time
import datetime
import pprint
from scipy.spatial.transform import Rotation as R
import sys
import math
import argparse
import numpy as np
<<<<<<< HEAD
from Simulation.subsystems_integration.lidar_sensor_sub_sys import LiDaRSensorSubSystem
from Simulation.subsystems_integration.flight_path_nav_sub_sys import FlightPathNavSubSystem
from Simulation.subsystems_integration.optical_sensor_sub_sys import OpticalSensorSubSystem
=======
from lidar_sensor_sub_sys import LiDaRSensorSubSystem
from flight_path_nav_sub_sys import FlightPathNavSubSystem
from optical_sensor_sub_sys import OpticalSensorSubSystem
>>>>>>> master


class DroneMainSystem(LiDaRSensorSubSystem, FlightPathNavSubSystem, OpticalSensorSubSystem):
	def __init__(self, altitude=None, velocity=None, fog_pct=None, rain_pct=None):
		self.altitude = altitude  # e.g. 30
		self.velocity = velocity  # e.g. 5
		# Instantiate MultirotorClient class obj instance
		self.client = airsim.MultirotorClient()
		# Checks state of connection every 1 sec and reports it in Console so user can see the progress for connection.
		self.client.confirmConnection()
		# The client must make this call to request control via API.
		self.client.enableApiControl(True)
		# Initialize drone NED coords position numpy array
		self.position = np.array([0., 0., 0.])
		self.client.simEnableWeather(True)
		self.fog_pct = fog_pct
		self.rain_pct = rain_pct
		self.client.simSetWeatherParameter(airsim.WeatherParameter.Fog, self.fog_pct)
		self.client.simSetWeatherParameter(airsim.WeatherParameter.Rain, self.rain_pct)
		LiDaRSensorSubSystem.__init__(self, self.client)
		FlightPathNavSubSystem.__init__(self, self.client)
		OpticalSensorSubSystem.__init__(self, self.client)

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

	def end(self, disconnection_time_out_sec=3):
		print("\nEnding API Control Over Drone in {0} seconds".format(disconnection_time_out_sec))
		print("Disconnection Start Time (H:M:S): {0}".format(datetime.datetime.now().strftime("%H-%M-%S")))
		time.sleep(disconnection_time_out_sec)
		self.client.armDisarm(False)
		print("Drone Disarmbed")
		self.client.reset()
		print("Drone State Reset")
		self.client.enableApiControl(False)
		print("API Control Disabled")
		print("Disconnection End Time (H:M:S): {0}".format(datetime.datetime.now().strftime("%H-%M-%S")))
		return


if __name__ == "__main__":
	from matplotlib import cm
	import open3d as o3d
	import datetime
	import cv2

	drone = DroneMainSystem(altitude=10, velocity=5, fog_pct=0.90, rain_pct=0.75)
	drone.start(take_off_time_duration=5)

	path_way_points = [
		(5, 0, -1), (10, 0, -1), (15, 0, -1),
		(15, 5, -1), (15, 10, -1), (15, 15, -1),
		(10, 15, -1), (5, 15, -1), (0, 15, -1),
		(0, 20, -1), (0, 25, -1), (0, 30, -1),
		(5, 30, -1), (10, 30, -1), (15, 30, -1),
		(20, 35, -1), (25, 40, -1), (30, 45, -1),
		(35, 35, -1), (40, 40, -1), (45, 45, -1),
		(50, 35, -1), (55, 40, -1), (60, 45, -1),
		(60, 50, -1), (60, 55, -1), (60, 60, -1),
		(60, 50, -1), (60, 55, -1), (60, 60, -1),
		(65, 50, -1), (70, 55, -1), (75, 60, -1),
		(75, 65, -1), (75, 70, -1), (75, 75, -1),
		(75, 75, -1), (80, 75, -1), (85, 75, -1),
		(85, 80, -1), (85, 85, -1), (85, 90, -1),
		(90, 90, -1), (95, 95, -1), (100, 100, -1),
	]

	shortened_path_way_points = [
		(5, 0, -1), (10, 0, -1), (15, 0, -1),
		(15, 5, -1), (15, 10, -1), (15, 15, -1),
		(10, 15, -1), (5, 15, -1), (0, 15, -1),
		(0, 20, -1), (0, 25, -1), (0, 30, -1),
		(5, 30, -1), (10, 30, -1), (15, 30, -1)
	]

	drone.set_flight_path(path_way_points)
	path_way_points_3d_vectors_list = drone.path_way_points_3d_vectors_list
	tot_flight_distance, tot_flight_time = drone.tot_flight_distance, drone.tot_flight_time
	drone.fly_path()

	#
	# print(path_way_points_3d_vectors_list)
	# print(len(path_way_points_3d_vectors_list))
	# print(type(path_way_points_3d_vectors_list))
	# drone_kinematics_data = drone.client.simGetGroundTruthKinematics()
	# print(f"drone_kinematics_data.position.x_val: {drone_kinematics_data.position.x_val}")
	# print(f"drone_kinematics_data.position.y_val: {drone_kinematics_data.position.y_val}")
	# print(f"drone_kinematics_data.position.z_val: {drone_kinematics_data.position.z_val}")
	# drone_pose_data = drone.client.simGetVehiclePose()
	# print(f"drone_pose_data.position.x_val: {drone_pose_data.position.x_val}")
	# print(f"drone_pose_data.position.y_val: {drone_pose_data.position.y_val}")
	# print(f"drone_pose_data.position.z_val: {drone_pose_data.position.z_val}")
	# time.sleep(3)
	#
	# lookahead = drone.velocity + (drone.velocity / 2)
	# drone.client.moveOnPathAsync(path_way_points_3d_vectors_list, drone.velocity, tot_flight_time,
	#                              airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0),
	#                              lookahead, 1)

	extra_additional_tot_flight_time = 10
	t_start = datetime.datetime.now()
	drone.init_lidar_sensor()
	while tot_flight_time + extra_additional_tot_flight_time >= (datetime.datetime.now() - t_start).seconds:
		drone.run_lidar_data_collection()
		drone.update_o3d_window()

		# bgr_img = drone.get_optical_camera_3d_rgb_img()
		# rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
		# rgb_img_rotated = np.rot90(np.rot90(rgb_img))
		# gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
		# hist_equal_grey_img = cv2.equalizeHist(gray_img)
		# hist_equal_img = cv2.cvtColor(hist_equal_grey_img, cv2.COLOR_GRAY2RGB)
		# hist_equal_img_rotated = np.rot90(np.rot90(hist_equal_img))
		# cv2_window_name = "Histogram Equalization of RGB Image Capture In Fog (fog pct = {0})".format(drone.fog_pct)
		# cv2.namedWindow(cv2_window_name, cv2.WINDOW_NORMAL)
		# combined_hist_equalized_rgb_image_array = np.hstack((bgr_img, hist_equal_img))
		# cv2.imshow(cv2_window_name, combined_hist_equalized_rgb_image_array)

		# if cv2.waitKey(1) & 0xFF == ord('q'):
		# 	cv2.destroyAllWindows()
		# 	break
		# else:
		# 	continue

	drone.end(3)
