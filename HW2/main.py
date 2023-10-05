import asyncio
import time

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.vision import VisionClient
from viam.components.camera import Camera
from viam.components.base import Base


async def connect():
    creds = Credentials(
        type="robot-location-secret",
        payload="h98wjtxlf60jmyt6l4xz30r4o2wcmwkt0vrq7vbh0h4kysz2")
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address("lg-main.uvyuvpfzkq.viam.cloud", opts)


# Get largest detection box and see if it's center is in the left, center, or
# right third
def leftOrRight(detections, midpoint):
    largest_area = 0
    largest = {"x_max": 0, "x_min": 0, "y_max": 0, "y_min": 0}
    if not detections:
        print("nothing detected :(")
        print("begin search")
        return -1
    for d in detections:
        a = (d.x_max - d.x_min) * (d.y_max-d.y_min)
        if a > largest_area:
            largest_area = a
            largest = d
    centerX = (largest.x_min + largest.x_max)/2
    if centerX < midpoint-midpoint/6:
        return 0  # on the left
    if centerX > midpoint+midpoint/6:
        return 2  # on the right
    else:
        return 1  # basically centered


async def main():
    spinNum = 5         # when turning, spin the motor this much
    straightNum = 50    # when going straight, spin motor this much
    numCycles = 500      # run the loop X times
    vel = 100            # go this fast when moving motor

    # Connect to robot client and set up components
    robot = await connect()
    base = Base.from_robot(robot, "viam_base")
    camera_name = "LG_detectionCam"
    camera = Camera.from_robot(robot, camera_name)
    frame = await camera.get_image(mime_type="image/jpeg")

    # Grab the vision service for the detector
    my_detector = VisionClient.from_robot(robot, "LG_color_detector")

    # Main loop. Detect the ball, determine if it's on the left or right, and
    # head that way. Repeat this for numCycles
    for i in range(numCycles):
        detections = await my_detector.get_detections_from_camera(camera_name)
        print(detections)
        # time.sleep(1)
        answer = leftOrRight(detections, frame.size[0]/2)
        if answer == -1:
            print("rotate")
            # Here, since the object is out of frame, we apply a larger spin degree.
            await base.spin(10, vel) 
        if answer == 0:
            print("left")
            await base.spin(spinNum, vel)     # CCW is positive
            await base.move_straight(straightNum, vel)
        if answer == 1:
            print("center")
            await base.move_straight(straightNum, vel)
        if answer == 2:
            print("right")
            await base.spin(-spinNum, vel)
        # If nothing is detected, keep spinning left until found
        # if answer == -1:
            # while True:
                # await base.spin(spinNum, vel) 
                # detections = await my_detector.get_detections_from_camera(camera_name)
                # answer = leftOrRight(detections, frame.size[0]/2)
                # if answer != -1:
                #     break
                # print("still nothing detected :(")


    await robot.close()

if __name__ == "__main__":
    print("Starting up... ")
    asyncio.run(main())
    print("Done.")