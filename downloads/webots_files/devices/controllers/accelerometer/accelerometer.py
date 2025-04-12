# Copyright 1996-2024 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from controller import Robot

# Initialize the robot
robot = Robot()
time_step = int(robot.getBasicTimeStep())

# Get the accelerometer and enable it
accelerometer = robot.getDevice("accelerometer")
accelerometer.enable(time_step)

# Get the LEDs
front_led = robot.getDevice("front led")
back_led = robot.getDevice("back led")
left_led = robot.getDevice("left led")
right_led = robot.getDevice("right led")

# Get the motors and actuate them in velocity mode to make the robot turn
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.5)
right_motor.setVelocity(-0.5)

# Main loop
while robot.step(time_step) != -1:
    # Get the acceleration vector, which is close to the gravity vector
    acceleration = accelerometer.getValues()

    # Actuate the LEDs according to the acceleration vector
    if abs(acceleration[1]) > abs(acceleration[0]):
        front_led.set(0)
        back_led.set(0)
        left_led.set(1 if acceleration[1] > 0.0 else 0)
        right_led.set(1 if acceleration[1] < 0.0 else 0)
    else:
        front_led.set(1 if acceleration[0] < 0.0 else 0)
        back_led.set(1 if acceleration[0] > 0.0 else 0)
        left_led.set(0)
        right_led.set(0)