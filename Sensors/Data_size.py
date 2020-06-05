resolution = 1.4 # deg
fov = 70 # deg
bits_in_byte = 8 # bits
# 1 object "per resolution
n_pixels = (70 / 1.4) ** 2 # pixels
bits_per_pixel = 11 # bits
sample_rate = 22 # Hz

data_flow = n_pixels * bits_per_pixel * sample_rate# bits per second
print(data_flow)