import sys
import time

import setup_path
import airsim
import datetime

def print_position(client):
	state = client.getMultirotorState()
	gps = state.gps_location
	print("gps location lat={}, lon={}, alt={}".format(gps.latitude, gps.longitude, gps.altitude))
	pos = state.kinematics_estimated.position
	print("local position x={}, y={}, z={}".format(pos.x_val, pos.y_val, pos.z_val))


client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

print_position(client)

landed = client.getMultirotorState().landed_state
if landed == airsim.LandedState.Landed:
	print("taking off...")
	client.takeoffAsync().join()
	# client.takeoffAsync(timeout_sec=3).join()
	# client.takeoffAsync(timeout_sec=3)
else:
	client.hoverAsync().join()

if client.getMultirotorState().landed_state == airsim.LandedState.Landed:
	print("take off failed, please check message log")
	sys.exit(1)

# AirSim uses NED coordinates so negative axis is up.
# z of -7 is 7 meters above the original launch point.
z = -7

# make sure we are at the start location (previous flight might have missed the landing spot by a bit.)
# client.moveToPositionAsync(0, 0, z, 1).join()
# client.moveToPositionAsync(0, 0, z, 1, timeout_sec=3).join()
client.moveToPositionAsync(0, 0, z, 1, timeout_sec=3)

print("flying path...")
client.enableApiControl(True)
# this method is async, but we are calling .join() so the script waits for path to complete.
for i in range(100):
	x_pos = i + 1
	print("Iteration number: {0}".format(i))
	# time.sleep(1)
	pos = client.simGetGroundTruthKinematics().position
	print("{:.3f},{:.3f},{:.3f}".format(pos.x_val, pos.y_val, pos.z_val))
	# client.enableApiControl(True)
	imu_data = client.getImuData()
	print("~" * 10)
	print(f"IMU Data: {imu_data}")
	print("~" * 10)
	current_pose_data = client.simGetVehiclePose()
	current_position_data = current_pose_data.position
	x_val = current_position_data.x_val
	# client.moveToPositionAsync(5, 0, z, 5).join()
	# client.moveToPositionAsync(5, 0, 0, 5).join()
	# client.moveToPositionAsync(x_pos, 0, 0, 1).join()
	# client.moveToPositionAsync(x_pos, 0, z, 1)
	# client.moveToPositionAsync(x_pos, 0, z, 1).join()
	# client.moveToPositionAsync(x_pos, 0, z, 1)
	client.moveToPositionAsync(x_val+1, 0, z, 1).join()

return_home_time_out_sec = 10
print("\nMultirotor drone Return Home task initiated at: {0}".format(datetime.now().strftime('%H:%M:%S')))
print("Multirotor Drone Return Home task timeout_sec = {0} [s]".format(return_home_time_out_sec))
client.goHomeAsync(timeout_sec=return_home_time_out_sec)
print("\nMultirotor drone Return Home task completed at: {0}".format(datetime.now().strftime('%H:%M:%S')))


print("\nReseting multirotor drone client state...")
client.reset()
print("Multirotor drone client state reset!")

# pos = client.simGetGroundTruthKinematics().position
# print("{:.3f},{:.3f},{:.3f}".format(pos.x_val, pos.y_val, pos.z_val))
# time.sleep(3)
# pos = client.simGetGroundTruthKinematics().position
# print("{:.3f},{:.3f},{:.3f}".format(pos.x_val, pos.y_val, pos.z_val))
# client.enableApiControl(True)
# client.moveToPositionAsync(5,0,z,1).join()
# pos = client.simGetGroundTruthKinematics().position
# print("{:.3f},{:.3f},{:.3f}".format(pos.x_val, pos.y_val, pos.z_val))

# client.moveToPositionAsync(0, 0, -10, 1).join()
# client.moveToPositionAsync(0, 0, -10, 1, timeout_sec=3).join()


client.moveToPositionAsync(0, 0, -10, 1, timeout_sec=3)
print("landing")
client.landAsync().join()
print("disarming drone")
client.armDisarm(False)
client.enableApiControl(False)
print("done!")

print_position(client)
