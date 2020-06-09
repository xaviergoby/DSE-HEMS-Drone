import os

# Who is "John Doe"?: https://en.wikipedia.org/wiki/John_Doe

ROOT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# returns e.g. C:\Users\JohnDoe\DSE-HEMS-Drone
PROJ_SETTINGS_DIR_PATH = os.path.join(ROOT_DIR_PATH, "proj_settings")
# returns e.g. C:\Users\JohnDoe\DSE-HEMS-Drone\proj_settings
AIRSIM_SETTINGS_DIR_PATH = os.path.join(PROJ_SETTINGS_DIR_PATH, "airsim_settings")
# returns e.g. C:\Users\JohnDoe\DSE-HEMS-Drone\proj_settings\airsim_settings
AIRSIM_VANILLA_SETTINGS_DIR_PATH = os.path.join(AIRSIM_SETTINGS_DIR_PATH, "vanilla_airsim_settings_json")
# returns e.g. C:\Users\JohnDoe\DSE-HEMS-Drone\proj_settings\airsim_settings\vanilla_airsim_settings_json
AIRSIM_LIDAR_SETTINGS_DIR_PATH = os.path.join(AIRSIM_SETTINGS_DIR_PATH, "lidar_airsim_settings_json")
# returns e.g. C:\Users\JohnDoe\DSE-HEMS-Drone\proj_settings\airsim_settings\lidar_airsim_settings_json

AIRSIM_VANILLA_SETTINGS_JSON_PATH = os.path.join(AIRSIM_VANILLA_SETTINGS_DIR_PATH, "settings.json")
# returns e.g. C:\Users\JohnDoe\DSE-HEMS-Drone\proj_settings\airsim_settings\vanilla_airsim_settings_json\settings.json
AIRSIM_LIDAR_SETTINGS_JSON_PATH = os.path.join(AIRSIM_LIDAR_SETTINGS_DIR_PATH, "settings.json")
# returns e.g. C:\Users\JohnDoe\DSE-HEMS-Drone\proj_settings\airsim_settings\lidar_airsim_settings_json\settings.json



if __name__ == "__main__":
	print(f"ROOT_DIR_PATH: {ROOT_DIR_PATH}")
	print(f"PROJ_SETTINGS_DIR_PATH: {PROJ_SETTINGS_DIR_PATH}")
	print(f"AIRSIM_SETTINGS_DIR_PATH: {AIRSIM_SETTINGS_DIR_PATH}")
	print(f"AIRSIM_VANILLA_SETTINGS_DIR_PATH: {AIRSIM_VANILLA_SETTINGS_DIR_PATH}")
	print(f"AIRSIM_LIDAR_SETTINGS_DIR_PATH: {AIRSIM_LIDAR_SETTINGS_DIR_PATH}")
	print(f"AIRSIM_VANILLA_SETTINGS_JSON_PATH: {AIRSIM_VANILLA_SETTINGS_JSON_PATH}")
	print(f"AIRSIM_LIDAR_SETTINGS_JSON_PATH: {AIRSIM_LIDAR_SETTINGS_JSON_PATH}")