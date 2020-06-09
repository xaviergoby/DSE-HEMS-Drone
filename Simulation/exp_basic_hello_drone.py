# ready to run example: PythonClient/multirotor/hello_drone.py
import airsim
import os
import time
from datetime import datetime
import threading




# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

def get_drone_pos_data(t):
	for t_i in range(t):
		time.sleep(1)
		current_pose_data = client.simGetVehiclePose()
		current_position_data = current_pose_data.position
		print("\nMESAGE FROM THREAD t1 with target=get_drone_pos_data")
		print(f"current_position_data: {current_position_data}")
		print("Slept for {0} seconds".format(t_i+1))

t1 = threading.Thread(target=get_drone_pos_data, args=(25,))

# t1.start()

take_off_timeout_sec = 20

# Async methods returns Future. Call join() to wait for task to complete.
print("\nMultirotor drone Take-Off task initiated at: {0}".format(datetime.now().strftime('%H:%M:%S')))
# print("Multirotor Drone Take-Off task timeout_sec = {0} [s]".format(take_off_timeout_sec))
# client.takeoffAsync(timeout_sec=take_off_timeout_sec)
# t1.start()
# t1.join()
client.takeoffAsync().join()
t1.start()
# t1.join()
print("\nMultirotor drone Take-Off task completed at: {0}".format(datetime.now().strftime('%H:%M:%S')))
# print(datetime.now().strftime('%H:%M:%S'))

current_state_data = client.getMultirotorState()
imu_data = client.getImuData()
gps_data = client.getGpsData()
current_pose_data = client.simGetVehiclePose()
current_position_data = current_pose_data.position
print(f"\ncurrent_state_data: {current_state_data}")
print(f"\nimu_data: {imu_data}")
print(f"\ngps_data: {gps_data}")
print(f"\ncurrent_pose_data: {current_pose_data}")
print(f"\ncurrent_position_data: {current_position_data}")

client.moveToPositionAsync(0, 0, -30, 5).join()

client.moveToPositionAsync(30, 0, -30, 5)
t1.join()
current_pose_data = client.simGetVehiclePose()
current_position_data = current_pose_data.position
x_val = current_position_data.x_val
while x_val <= 30:
	print(x_val)
	time.sleep(1)
	current_pose_data = client.simGetVehiclePose()
	current_position_data = current_pose_data.position
	x_val = current_position_data.x_val

client.moveToPositionAsync(30, 30, -30, 5)
current_pose_data = client.simGetVehiclePose()
current_position_data = current_pose_data.position
y_val = current_position_data.y_val
while y_val <= 30:
	print(y_val)
	time.sleep(1)
	current_pose_data = client.simGetVehiclePose()
	current_position_data = current_pose_data.position
	y_val = current_position_data.y_val
	


return_home_time_out_sec = 10
print("\nMultirotor drone Return Home task initiated at: {0}".format(datetime.now().strftime('%H:%M:%S')))
print("Multirotor Drone Return Home task timeout_sec = {0} [s]".format(return_home_time_out_sec))
client.goHomeAsync(timeout_sec=return_home_time_out_sec)
print("\nMultirotor drone Return Home task completed at: {0}".format(datetime.now().strftime('%H:%M:%S')))


print("\nReseting multirotor drone client state...")
client.reset()
print("Multirotor drone client state reset!")

# client.moveToPositionAsync(-10, 10, -10, 5).join()
#
# # take images
# responses = client.simGetImages([
#     airsim.ImageRequest("0", airsim.ImageType.DepthVis),
#     airsim.ImageRequest("1", airsim.ImageType.DepthPlanner, True)])
# print('Retrieved images: %d', len(responses))
#
# # do something with the images
# for response in responses:
#     if response.pixels_as_float:
#         print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
#         airsim.write_pfm(os.path.normpath('/temp/py1.pfm'), airsim.get_pfm_array(response))
#     else:
#         print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
#         airsim.write_file(os.path.normpath('/temp/py1.png'), response.image_data_uint8)