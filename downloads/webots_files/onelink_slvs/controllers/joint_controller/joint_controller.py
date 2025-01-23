from controller import Robot, Motor
import math

# Create a robot instance
robot = Robot()

# Get the motor device
motor = robot.getDevice('joint_motor')

# Set the motor position to infinity (continuous rotation)
motor.setPosition(float('inf'))

# Time step
timestep = int(robot.getBasicTimeStep())

# Rotation speed (30 degrees per second)
speed = math.pi / 6  # 30 degrees = π/6 radians per second

# Main control loop
while robot.step(timestep) != -1:
    # Set motor velocity
    motor.setVelocity(speed)