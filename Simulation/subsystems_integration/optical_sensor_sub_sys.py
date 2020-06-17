import airsim
import numpy as np

class OpticalSensorSubSystem:
	
	def __init__(self, client):
		self.client = client

	def get_optical_camera_output_response(self):
		# Get (camera) imaging system responses/outputs
		responses = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
		# type(responses) => list
		response = responses[0]
		# type(response) => airsim.types.ImageResponse
		return response

	def get_optical_camera_3d_rgb_img(self):
		response = self.get_optical_camera_output_response()
		img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
		img_rgb = img1d.reshape(response.height, response.width, 3)
		# img_rgb = np.flipud(img_rgb)
		return img_rgb
