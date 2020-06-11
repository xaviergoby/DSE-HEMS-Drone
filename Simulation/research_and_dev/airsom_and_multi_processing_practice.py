


from multiprocessing import Pool
import time
import datetime


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


# t1.start()

take_off_timeout_sec = 20

pool = Pool(processes=2)
r1 = pool.apply_async(f1, (10,))
r2 = pool.apply_async(f2, (10,))
pool.close()
pool.join()

# Async methods returns Future. Call join() to wait for task to complete.
print("\nMultirotor drone Take-Off task initiated at: {0}".format(datetime.now().strftime('%H:%M:%S')))
# print("Multirotor Drone Take-Off task timeout_sec = {0} [s]".format(take_off_timeout_sec))
# client.takeoffAsync(timeout_sec=take_off_timeout_sec)
client.takeoffAsync().join()
print("\nMultirotor drone Take-Off task completed at: {0}".format(datetime.now().strftime('%H:%M:%S')))
# print(datetime.now().strftime('%H:%M:%S'))

def f1(t1):
	for i in range(t1):
		time.sleep(1)
		# print(datetime.datetime.now())
		print("\nTIMER 1: I have waited for {0}".format(i))
		print(datetime.datetime.now())
	# return


def f2(t2):
	for i in range(t2):
		time.sleep(1)
		print("\nTIMER 2: I have waited for {0}".format(i))
		print(datetime.datetime.now())
	# return


if __name__ == '__main__':
	pool = Pool(processes=2)
	start = time.time()
	r1 = pool.apply_async(f1, (10,))
	r2 = pool.apply_async(f2, (10,))
	pool.close()
	pool.join()
