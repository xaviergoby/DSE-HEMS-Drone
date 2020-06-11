import airsim
from Sensors.radar_optical_flow import setup_path

# boxsize	The overall size of the square box to survey
# stripewidth	How far apart to drive the swim lanes, this can depend on the type of camera lens , for example.
# altitude	The height to fly the survey.
# speed	The speed of the survey, can depend on how fast your camera can snap shots.

class SurveyNavigator:
	def __init__(self, altitude, velocity):
		self.altitude = altitude # 30
		self.velocity = velocity # 5
		self.client = airsim.MultirotorClient()
		self.client.confirmConnection()
		self.client.simEnableWeather(True)
		self.client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.85)
		self.client.enableApiControl(True)
		
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
			self.client.takeoffAsync(timeout_sec).join()
			print("Drone State: Take-Off Complete")
			

		drone_landed_state = self.client.getMultirotorState().landed_state
		if drone_landed_state == airsim.LandedState.Landed:
			print("takeoff failed - check Unreal message log for details")
			return
		
if __name__ == "__main__":
	drone_nav = SurveyNavigator(10, 5)
	drone_nav.start(5)
	