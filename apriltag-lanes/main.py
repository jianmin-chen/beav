from threading import Thread, Event
from time import sleep
from pid import PID
from video import Video
from bluerov_interface import BlueROV
from pymavlink import mavutil
from move import process_frame
import numpy as np
import cv2
from dt_apriltags import Detector

# Create the Video object
video = Video()

# Create the PID object
pid_vertical = PID(K_p=40, K_i=0.0, K_d=0.01, integral_limit=1)
pid_horizontal = PID(K_p=20, K_i=0.0, K_d=30, integral_limit=1)

# Create the mavlink connection
mav_comn = mavutil.mavlink_connection("udpin:0.0.0.0:14550")

# Create the BlueROV object
bluerov = BlueROV(mav_connection=mav_comn)

frame = None
frame_available = Event()
frame_available.set()

vertical_power = 0
lateral_power = 0

# Create detector
at_detector = Detector(
    families="tag36h11",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0,
)

camera_matrix = np.array(
    [353.571428571, 0, 320, 0, 353.571428571, 180, 0, 0, 1]
).reshape((3, 3))

camera_params = (
    camera_matrix[0, 0],
    camera_matrix[1, 1],
    camera_matrix[0, 2],
    camera_matrix[1, 2],
)


def _get_frame():
    global frame, vertical_power, lateral_power
    while not video.frame_available():
        print("Waiting for frame...")
        sleep(0.01)

    try:
        while True:
            frame = video.frame()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width, _ = frame.shape
            tags = at_detector.detect(frame, True, camera_params, 0.1)
            if len(tags):
                for tag in tags:
                    percentx = (0.5 - tag.center[0] / width) * 2
                    percenty = (0.5 - tag.center[1] / height) * 2
                    outputx = pid_horizontal.update(percentx)
                    outputy = pid_vertical.update(percenty)
                vertical_power = outputy
                lateral_power = outputx
            else:
                vertical_power = 0
                lateral_power = 0
    except KeyboardInterrupt:
        return


def _send_rc():
    global vertical_power, lateral_power
    bluerov.set_rc_channels_to_neutral()
    bluerov.arm()
    bluerov.mav_connection.set_mode(19)
    while True:
        bluerov.arm()
        bluerov.set_vertical_power(int(vertical_power))
        bluerov.set_lateral_power(-int(lateral_power))


# Start the video thread
video_thread = Thread(target=_get_frame)
video_thread.start()

# Start the RC thread
rc_thread = Thread(target=_send_rc)
rc_thread.start()

# Main loop
try:
    while True:
        mav_comn.wait_heartbeat()
except KeyboardInterrupt:
    video_thread.join()
    rc_thread.join()
    bluerov.set_rc_channels_to_neutral()
    bluerov.disarm()
    print("Exiting...")