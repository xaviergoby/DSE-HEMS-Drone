import numpy as np
import math
import matplotlib.pyplot as plt
import cv2


# RCS: Radar Cross-Section


class DroneTestPlatform:


	def __init__(self):
		self.drone_alt = 20 # [m] h
		self.drone_speed = 45 #[m/s] v
		self.max_range = 150 #[m] R_max
		self.radar_cross_section = 10 #[m^2]
		self.FOV = 70 # +/- [degrees]
		self.angular_res = 1.4 #[degrees] beta
		# self.scanning_frq =  #[Hz]

	def compute_sw_distance(self):
		# sw = 2*sqrt(R_max^2 + h^2)
		swath_width = 2 * np.sqrt(self.max_range**2 + self.drone_alt**2)
		return swath_width

	def compute_eff_fov_angle(self):
		# aka horizontal fov
		sw = self.compute_sw_distance()
		# eff_fov_rad = 2*np.arctan(sw/(2*self.drone_alt))
		eff_fov_rad = 2*np.arctan((sw/2)/(self.drone_alt))
		eff_fov_deg = eff_fov_rad * (180/np.pi)
		return eff_fov_deg

drone = DroneTestPlatform()
sw = drone.compute_sw_distance()
eff_sw = drone.compute_eff_fov_angle()
print(sw)
print(eff_sw)