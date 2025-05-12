from controller import Robot, DistanceSensor

def run_robot():
    # Create the Robot instance
    robot = Robot()

    # Get simulation time step
    timestep = int(robot.getBasicTimeStep())

    # Get the DistanceSensor device
    sensor = robot.getDevice('sensor')
    sensor.enable(timestep)
    score = 0
    last_score_time = 0
    cooldown = 1.0

    # Get motor and keyboard devices
    motor = robot.getDevice('motor1')
    keyboard = robot.getKeyboard()
    keyboard.enable(timestep)

    # Set initial motor position
    initial_position = 0.0  # Assuming initial position is 0

    # Main control loop
    while robot.step(timestep) != -1:
        # Read DistanceSensor value
        sensor_value = sensor.getValue()
        current_time = robot.getTime()
        #print(sensor_value)
        # Check if the ball blocks the sensor (you may need to adjust the threshold based on your sensor's range)
        if sensor_value > 200 and (current_time - last_score_time) > cooldown:
            score +=2
            print("得分")
        # Motor control (existing functionality)
        motor.setPosition(38 * 3.14159 / 180)

if __name__ == "__main__":
    run_robot()