from controller import Robot, Keyboard

def run_robot():
    # Create the Robot instance
    robot = Robot()

    # Get simulation time step
    timestep = int(robot.getBasicTimeStep())

    # Get the keyboard device
    keyboard = robot.getKeyboard()
    keyboard.enable(timestep)

    # Get motor and sensor devices
    motor = robot.getDevice('motor1')
    sensor = robot.getDevice('sensor')
    sensor.enable(timestep)

    # Set initial motor position
    initial_position = 0.0  # Assuming initial position is 0
    motor.setPosition(initial_position)
    initial = True

    # Main control loop
    while robot.step(timestep) != -1:
        # Read the DistanceSensor value
        sensor_value = sensor.getValue()

        # Read the pressed key
        key = keyboard.getKey()

        if initial:
            motor.setPosition(38 * 3.14159 / 180)  # Set position to desired angle
            initial = False
        
        # Reset joint1 when 'm' is pressed
        if key == ord('M'):
            motor.setPosition(initial_position)  # Reset to initial position
            print("Joint1 reset to initial position")
            
        if key == ord('K'):
            motor.setPosition(38 * 3.14159 / 180)  # Set position to desired angle
            print("Joint1 set to desired angle")

if __name__ == "__main__":
    run_robot()