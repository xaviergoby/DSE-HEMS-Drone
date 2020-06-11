# ready to run example: PythonClient/car/hello_car.py
import cv2
import os
import airsim
import time
import numpy as np

# connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

while True:
    # get state of the car
    car_state = client.getCarState()
    print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))

    # set the controls for car
    car_controls.throttle = 1
    car_controls.steering = 1
    client.setCarControls(car_controls)

    # let car drive a bit
    time.sleep(1)

    # get camera images from the car
    responses = client.simGetImages([
        airsim.ImageRequest(0, airsim.ImageType.DepthVis),
        airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True),  # depth in perspective projection
        airsim.ImageRequest("1", airsim.ImageType.Scene),  # scene vision image in png format
        airsim.ImageRequest("1", airsim.ImageType.Scene, False, False),  # scene vision image in uncompressed RGBA array
        airsim.ImageRequest(1, airsim.ImageType.DepthPlanner, True)],
        
    )
    print('Retrieved images: %d', len(responses))

    # do something with images
    for response in responses:
        if response.pixels_as_float:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            airsim.write_pfm('py1.pfm', airsim.get_pfm_array(response))
        else:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file('py1.png', response.image_data_uint8)
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)  # get numpy array
            img_rgb = img1d.reshape(response.height, response.width,
                                    3)  # reshape array to 4 channel image array H X W X 3
            cv2.imwrite(os.path.normpath("car_img" + '.png'), img_rgb)  # write to png