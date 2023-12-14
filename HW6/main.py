import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.motor import Motor
from viam.components.base import Base
from viam.components.camera import Camera
from viam.components.encoder import Encoder
from viam.components.movement_sensor import MovementSensor
from viam.services.vision import VisionClient


async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='l3juq13kn77tyl8ws6x6ntg4ehvleur9',
      api_key_id='3991039d-2479-43ab-8a6b-ab0a834fdcbf'
    )
    return await RobotClient.at_address('lg-main.uvyuvpfzkq.viam.cloud', opts)

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)
  
    # viam_base
    base = Base.from_robot(robot, "viam_base")
    viam_base_return_value = await base.is_moving()
    print(f"viam_base is_moving return value: {viam_base_return_value}")
  
    # LG_transform_cam
    lg_transform_cam = Camera.from_robot(robot, "LG_transform_cam")
    lg_transform_cam_return_value = await lg_transform_cam.get_image()
    print(f"LG_transform_cam get_image return value: {lg_transform_cam_return_value}")
  
    # Note that the Camera supplied is a placeholder. Please change this to a valid Camera.
    # LG_vision
    lg_vision = VisionClient.from_robot(robot, "LG_vision")
    lg_vision_return_value = await lg_vision.get_classifications_from_camera('LG_transform_cam', 1)
    print(f"LG_vision get_classifications_from_camera return value: {lg_vision_return_value}") 

    ## Class names: 
    # paper_cup
    # water_bottle
    # paper_case
    # paddle
    print(lg_vision_return_value[0])
    print(lg_vision_return_value[0].class_name)

    if lg_vision_return_value[0].class_name == 'paddle':
        for _ in range(3):
            await base.move_straight(velocity=-100, distance=200)

    if lg_vision_return_value[0].class_name == 'water_bottle':
        # async def move_in_circle(base, linear_velocity=100, angular_velocity=0.5):
        #     # Move in a circle for a certain amount of time
        #     await base.set_velocity(linear_velocity, angular_velocity)
        #     await asyncio.sleep(20)  # Adjust this value to control how long the rover moves in a circle
        #     # await base.stop()
        # await move_in_circle(base)
        async def move_in_triangle(base, side_length=100):
            for _ in range(3):
                # Move forward
                await base.move_straight(velocity=100, distance=side_length)
                # Turn 120 degrees
                await base.spin(velocity=100, angle=120)
        await move_in_triangle(base)
        
    if lg_vision_return_value[0].class_name == 'paper_case':
        async def move_in_square(base, side_length=200):
            for _ in range(4):
                # Move forward
                await base.move_straight(velocity=100, distance=side_length)
                # Turn 90 degrees
                await base.spin(velocity=100, angle=90)
        await move_in_square(base)
    
    if lg_vision_return_value[0].class_name == 'paper_cup':
        await base.move_straight(velocity=100, distance=300)

    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
