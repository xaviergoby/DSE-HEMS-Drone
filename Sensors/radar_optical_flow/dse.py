# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 11:24:21 2020

@author: Tijmen
"""

# Python client example to get Lidar data from a drone
#
from Sensors.radar_optical_flow import setup_path
# import setup_path
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
        self.position = np.array([0.,0.,0.])
        
        

    def execute(self):
        vis = o3d.visualization.VisualizerWithEditing()
        vis.create_window()
        
        mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)
        mesh_sphere.paint_uniform_color([0.9, 0.1, 0.1])
        
        
        print("arming the drone...")
        self.client.armDisarm(True)
        self.client.takeoffAsync().join()

#        state = self.client.getMultirotorState()
        self.client.moveToPositionAsync(-20, 140, -30, 5)
        
        i = 0
        prev_millis = int(round(time.time() * 1000))
        while True:
            millis = int(round(time.time() * 1000))
            if millis-prev_millis>500:
                i+=1
                prev_millis = millis
                lidarData = self.client.getLidarData();
                if (len(lidarData.point_cloud) < 3):
                    print("\tNo points received from Lidar data")
                else:
                    scan = self.parse_lidarData(lidarData)
                    
                    if not hasattr(self,'scans'):
                        self.scans = scan
                        self.distances = np.sqrt(np.sum(np.multiply(scan,scan),axis=1))
                    else:
                        scan = np.add(scan,np.tile(self.position,(scan.shape[0],1)))
                            
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
                        
                        translation = reg_p2p.transformation[0:3,3]
                        rotation = reg_p2p.transformation[0:3,0:3]
                        self.position = np.add(self.position,translation)
                       
                        scan = np.transpose(np.matmul(rotation,np.transpose(scan)))
                        scan = np.add(scan,np.tile(translation,(scan.shape[0],1)))
                        self.scans = np.vstack((self.scans,scan))
                        
                        vectors = np.subtract(scan,np.tile(self.position,(scan.shape[0],1)))
                        self.distances = np.hstack((self.distances,np.sqrt(np.sum(np.multiply(vectors,vectors),axis=1))))
                        
                    show = o3d.geometry.PointCloud()
                    show.points = o3d.utility.Vector3dVector(self.scans)
                    colors = cm.jet(self.distances.flatten()/np.max(self.distances))
                    colors = colors[:,0:3]
                    show.colors = o3d.utility.Vector3dVector(colors)
                                  
                    drone = mesh_sphere.sample_points_uniformly()
                    drone_points = np.array(drone.points)
                    drone_points = np.add(drone_points,np.tile(self.position,(drone_points.shape[0],1)))
                    drone.points = o3d.utility.Vector3dVector(drone_points)       
                    
                    param = vis.get_view_control().convert_to_pinhole_camera_parameters()
                    vis.clear_geometries()
                    vis.add_geometry(show+drone)
                    vis.get_view_control().convert_from_pinhole_camera_parameters(param)

                
            vis.poll_events()
            vis.update_renderer()

            
    def parse_lidarData(self, data):
        # reshape array of floats to array of [X,Y,Z]
        points = np.array(data.point_cloud, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0]/3), 3))

        rotation = R.from_quat([data.pose.orientation.x_val,data.pose.orientation.y_val,data.pose.orientation.z_val,data.pose.orientation.w_val]).as_matrix()
        points = np.transpose(np.matmul(rotation,np.transpose(points))) 
        return points

    def write_lidarData_to_disk(self, points):
        # TODO
        print("not yet implemented")

    def stop(self):

        self.client.armDisarm(False)
        self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")

# main
if __name__ == "__main__":
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

#    print(lidarTest.position)
#    np.savetxt('coords.txt',lidarTest.scans)
#    np.savetxt('distances.txt',lidarTest.distances)
#    colors = cm.jet(lidarTest.distances.flatten()/np.max(lidarTest.distances))
#    colors = colors[:,0:3]
#    pcd = o3d.geometry.PointCloud()
#    pcd.points = o3d.utility.Vector3dVector(lidarTest.scans)
#    pcd.colors = o3d.utility.Vector3dVector(colors)
#    
#    downpcd = pcd.voxel_down_sample(voxel_size=1)
#    o3d.visualization.draw_geometries([downpcd])
        