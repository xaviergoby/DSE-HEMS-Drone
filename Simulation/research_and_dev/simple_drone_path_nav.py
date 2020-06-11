import sys
import time

import setup_path
import airsim

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
else:
    client.hoverAsync().join()


if client.getMultirotorState().landed_state == airsim.LandedState.Landed:
    print("take off failed, please check message log")
    sys.exit(1)


# AirSim uses NED coordinates so negative axis is up.
# z of -7 is 7 meters above the original launch point.
z = -7

# make sure we are at the start location (previous flight might have missed the landing spot by a bit.)
client.moveToPositionAsync(0,0,z,1).join()

print("flying path...")

# this method is async, but we are calling .join() so the script waits for path to complete.
for i in range(100):
    time.sleep(2)
    pos = client.simGetGroundTruthKinematics().position
    print("{:.3f},{:.3f},{:.3f}".format(pos.x_val, pos.y_val, pos.z_val))
    client.enableApiControl(True)
    imu_data = client.getImuData()
    print("~"*10)
    print(f"IMU Data: {imu_data}")
    print("~" * 10)
    client.moveToPositionAsync(-5,0,z,1).join()
    pos = client.simGetGroundTruthKinematics().position
    print("{:.3f},{:.3f},{:.3f}".format(pos.x_val, pos.y_val, pos.z_val))
    time.sleep(3)
    pos = client.simGetGroundTruthKinematics().position
    print("{:.3f},{:.3f},{:.3f}".format(pos.x_val, pos.y_val, pos.z_val))
    client.enableApiControl(True)
    client.moveToPositionAsync(5,0,z,1).join()
    pos = client.simGetGroundTruthKinematics().position
    print("{:.3f},{:.3f},{:.3f}".format(pos.x_val, pos.y_val, pos.z_val))

client.moveToPositionAsync(0,0,-10,1).join()
print("landing")
client.landAsync().join()
print("disarming drone")
client.armDisarm(False)
client.enableApiControl(False)
print("done!")

print_position(client)