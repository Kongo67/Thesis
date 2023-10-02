import time
import setup_path
import airsim
import os
import keyboard

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# Specify the directory for saving images
image_directory = os.path.join(os.getcwd(), 'images')

# Ensure that the directory exists or create it
os.makedirs(image_directory, exist_ok=True)

# Initialize velocity components
vx, vy, vz = 0, 0, 0

# Function to control the drone based on keyboard input
def update_velocity():
    global vx, vy, vz

    if "up" in keys_pressed:
        vx = 15  # Move forward faster
    elif "down" in keys_pressed:
        vx = -15  # Move backward faster
    else:
        vx = 0

    if "left" in keys_pressed:
        vy = -15  # Move left faster
    elif "right" in keys_pressed:
        vy = 15  # Move right faster
    else:
        vy = 0

    if "space" in keys_pressed:
        vz = 0  # Hover (stop moving vertically)
    elif "w" in keys_pressed:
        vz = -30  # Ascend faster
    elif "s" in keys_pressed:
        vz = 30  # Descend faster
    
    if "a" in keys_pressed:
        client.rotateByYawRateAsync(90, 1).join()
    elif "d" in keys_pressed:
        client.rotateByYawRateAsync(-90, 1).join()

try:
    # Main loop to capture images and control the drone
    while True:
        keys_pressed = keyboard.read_event(suppress=True).name.split(' ')
        update_velocity()  # Update velocity based on keyboard input
        client.moveByVelocityZAsync(2 * vx, 2 * vy, vz, 0.5).join()  # Apply velocity commands
        gps_data = client.getGpsData(gps_name = "", vehicle_name = "")# o retrieve the GPS data
        print("GPS data: %s" % gps_data)

        responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.DepthVis),
            airsim.ImageRequest("1", airsim.ImageType.DepthPlanar, True)])
        print('Retrieved images: %d' % len(responses))
        for response in responses:
            if response.pixels_as_float:
                print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
                airsim.write_pfm(os.path.join(image_directory, 'py1.pfm'), airsim.get_pfm_array(response))
            else:
                print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
                airsim.write_file(os.path.join(image_directory, 'py1.png'), response.image_data_uint8)

except KeyboardInterrupt:
    pass

# Clean up and exit
client.armDisarm(False)
client.enableApiControl(False)

# import time
# import setup_path
# import airsim
# import os
# import keyboard

# # Connect to the AirSim simulator
# client = airsim.MultirotorClient()
# client.confirmConnection()
# client.enableApiControl(True)
# client.armDisarm(True)

# # Specify the directory for saving images
# image_directory = os.path.join(os.getcwd(), 'images')

# # Ensure that the directory exists or create it
# os.makedirs(image_directory, exist_ok=True)

# # Initialize velocity components
# vx, vy, vz = 0, 0, 0

# # Function to control the drone based on keyboard input
# def update_velocity():
#     global vx, vy, vz

#     if "up" in keys_pressed:
#         vx = 15  # Move forward faster
#     elif "down" in keys_pressed:
#         vx = -15  # Move backward faster
#     else:
#         vx = 0

#     if "left" in keys_pressed:
#         vy = -15  # Move left
#     elif "right" in keys_pressed:
#         vy = 15  # Move right
#     else:
#         vy = 0

#     if "space" in keys_pressed:
#         vz = 0  # Hover (stop moving vertically)
#     elif "w" in keys_pressed:
#         vz = -30  # Ascend faster
#     elif "s" in keys_pressed:
#         vz = 30  # Descend faster

# try:
#     # Main loop to capture images and control the drone
#     while True:
#         keys_pressed = keyboard.read_event(suppress=True).name.split(' ')
#         update_velocity()  # Update velocity based on keyboard input
#         client.moveByVelocityZAsync(2 * vx, 2 * vy, vz, 0.5).join()  # Apply velocity commands

#         responses = client.simGetImages([
#             airsim.ImageRequest("0", airsim.ImageType.DepthVis),
#             airsim.ImageRequest("1", airsim.ImageType.DepthPlanar, True)])
#         print('Retrieved images: %d' % len(responses))
#         for response in responses:
#             if response.pixels_as_float:
#                 print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
#                 airsim.write_pfm(os.path.join(image_directory, 'py1.pfm'), airsim.get_pfm_array(response))
#             else:
#                 print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
#                 airsim.write_file(os.path.join(image_directory, 'py1.png'), response.image_data_uint8)

# except KeyboardInterrupt:
#     pass

# # Clean up and exit
# client.armDisarm(False)
# client.enableApiControl(False)
