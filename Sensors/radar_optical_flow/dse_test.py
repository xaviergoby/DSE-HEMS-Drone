# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 11:24:21 2020

@author: Tijmen
"""

# Python client example to get Lidar data from a drone
#

import setup_path 
import airsim

import sys
import math
import time
import argparse
import pprint
import numpy as np
from scipy.spatial.transform import Rotation as R

from matplotlib import cm
import open3d as o3d


# Makes the drone fly and get Lidar data
class LidarTest:

    def __init__(self):

        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.movement = np.array([0.,0.,0.])
        
        

    def execute(self):

        print("arming the drone...")
        self.client.armDisarm(True)

        state = self.client.getMultirotorState()
        s = pprint.pformat(state)
        #print("state: %s" % s)

#        airsim.wait_key('Press any key to takeoff')
        self.client.takeoffAsync().join()

        state = self.client.getMultirotorState()
        #print("state: %s" % pprint.pformat(state))


#        self.client.hoverAsync().join()

        self.client.moveToPositionAsync(-20, 140, -30, 5)
        
        
        for i in range(35):
            lidarData = self.client.getLidarData();
            if (len(lidarData.point_cloud) < 3):
                print("\tNo points received from Lidar data")
            else:
                scan = self.parse_lidarData(lidarData)
                print("\tReading %d: time_stamp: %d number_of_points: %d" % (i, lidarData.time_stamp, len(scan)))
                print("\t\tlidar position: %s" % (pprint.pformat(lidarData.pose.position)))
                print("\t\tlidar orientation: %s" % (pprint.pformat(lidarData.pose.orientation)))
                
                if not hasattr(self,'scans'):
                    self.scans = scan
                else:
                    for index,point in enumerate(scan):
                        scan[index] = np.add(point,self.movement)
                        
                    source = o3d.geometry.PointCloud()

                    source.points = o3d.utility.Vector3dVector(scan)
                    source = source.voxel_down_sample(voxel_size=1)
                    source.estimate_normals()
                    
                    target = o3d.geometry.PointCloud()
                    target.points = o3d.utility.Vector3dVector(self.scans)
                    target = target.voxel_down_sample(voxel_size=1)
                    target.estimate_normals()
                    
                    threshold = 10
                    trans_init = np.identity(4)
                    
                    reg_p2p = o3d.registration.registration_icp(
                    source, target, threshold, trans_init,
                    o3d.registration.TransformationEstimationPointToPlane())
                    print(reg_p2p)
                    print("Transformation is:")
                    print(reg_p2p.transformation)
                    translation = reg_p2p.transformation[0:3,3]
                    rotation = reg_p2p.transformation[0:3,0:3]
                    for index,point in enumerate(scan):
                        scan[index] = np.matmul(rotation,point)
                        scan[index] = np.add(point,translation)
                    self.scans = np.vstack((self.scans,scan))
                    self.movement = np.add(self.movement,translation)
                    vis.add_geometry(o3d.utility.Vector3dVector(scan))
                    vis.update_geometry(source)
                    vis.update_renderer()
#                if not hasattr(self,'distances'):
#                    self.distances = distance
#                else:
#                    self.distances = np.vstack((self.distances,distance))
            time.sleep(0.5)
            
            
    def parse_lidarData(self, data):

        # reshape array of floats to array of [X,Y,Z]
        points = np.array(data.point_cloud, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0]/3), 3))
        
    
        # transform from local to global reference frame
#        position = np.array([data.pose.position.x_val,data.pose.position.y_val,data.pose.position.z_val])
        rotation = R.from_quat([data.pose.orientation.x_val,data.pose.orientation.y_val,data.pose.orientation.z_val,data.pose.orientation.w_val]).as_matrix()
        
        distances = np.zeros((points.shape[0],1))
        
        for index in range(len(points)):
            points[index] = points[index]*float(np.random.randint(0,20)+90)/100.
            points[index] = np.matmul(rotation,points[index])
#            points[index] = np.add(position,points[index])
            
#            vector = np.subtract(points[index],position)
#            distances[index] = math.sqrt(np.dot(vector,vector))
        
        return points#,distances

    def write_lidarData_to_disk(self, points):
        # TODO
        print("not yet implemented")

    def stop(self):

        airsim.wait_key('Press any key to reset to original state')

        self.client.armDisarm(False)
        self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")

# main
if __name__ == "__main__":
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    args = sys.argv
    args.pop(0)

    arg_parser = argparse.ArgumentParser("Lidar.py makes drone fly and gets Lidar data")

    arg_parser.add_argument('-save-to-disk', type=bool, help="save Lidar data to disk", default=False)
  
    args = arg_parser.parse_args(args)    
    lidarTest = LidarTest()
    try:
        lidarTest.execute()
    finally:
        lidarTest.stop()
        
    print(lidarTest.movement)
    np.savetxt('coords.txt',lidarTest.scans)
#    np.savetxt('distances.txt',lidarTest.distances)
#    
#    colors = cm.jet(lidarTest.distances.flatten()/np.max(lidarTest.distances))
#    colors = colors[:,0:3]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(lidarTest.scans)
#    pcd.colors = o3d.utility.Vector3dVector(colors)
    
#    downpcd = pcd.voxel_down_sample(voxel_size=1)
    #o3d.visualization.draw_geometries([pcd])
        