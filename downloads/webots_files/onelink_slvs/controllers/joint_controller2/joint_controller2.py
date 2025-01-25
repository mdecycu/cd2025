from controller import Robot, Motor
import math

# Create a robot instance
robot = Robot()

# Get the motor device
motor = robot.getDevice('joint_motor')
motor2 = robot.getDevice('joint_motor2')

# Set the motor position to infinity (continuous rotation)
motor.setPosition(float('inf'))
motor2.setPosition(float('inf'))

# Time step
timestep = int(robot.getBasicTimeStep())

# Rotation speed (30 degrees per second)
base_speed = 10*math.pi / 6  # 30 degrees = π/6 radians per second

# Main control loop
while robot.step(timestep) != -1:
    # Get the current velocity of motor
    motor_speed = motor.getVelocity()
    
    # 根据 motor 的速度确定 motor2 的旋转方向和速度
    # 如果 motor 正转，motor2 正转；如果 motor 反转，motor2 反转
    motor2_speed = base_speed * (1 if motor_speed >= 0 else -1)
    
    motor.setVelocity(base_speed*0.1)
    motor2.setVelocity(motor2_speed)
    
    print(f"Motor1 velocity: {motor.getVelocity()}")
    print(f"Motor2 velocity: {motor2.getVelocity()}")
