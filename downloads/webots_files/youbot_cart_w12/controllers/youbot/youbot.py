from controller import Robot

# Constants
TIME_STEP = 32  # Simulation time step in milliseconds
WHEEL_RADIUS = 0.1  # Radius of the wheels in meters (10cm)
L = 0.471  # Half of the robot's length in meters
W = 0.376  # Half of the robot's width in meters
MAX_VELOCITY = 10.0  # Maximum velocity allowed for the wheels
TURN_ANGLE = 1.5708  # 90 degrees in radians (π/2)
CORRECTION_FACTOR = 0.95  # Correction factor to fine-tune rotation

# Initialize the robot
robot = Robot()

# Get motor devices
wheel1 = robot.getDevice("wheel1")  # Front-right wheel
wheel2 = robot.getDevice("wheel2")  # Front-left wheel
wheel3 = robot.getDevice("wheel3")  # Rear-right wheel
wheel4 = robot.getDevice("wheel4")  # Rear-left wheel

# Get position sensors for each wheel
wheel1sensor = robot.getDevice("wheel1sensor")
wheel2sensor = robot.getDevice("wheel2sensor")
wheel3sensor = robot.getDevice("wheel3sensor")
wheel4sensor = robot.getDevice("wheel4sensor")

# Enable position sensors
for sensor in [wheel1sensor, wheel2sensor, wheel3sensor, wheel4sensor]:
    sensor.enable(TIME_STEP)

# Set motors to velocity control mode
for wheel in [wheel1, wheel2, wheel3, wheel4]:
    wheel.setPosition(float('inf'))  # Enable velocity control
    wheel.setVelocity(0)  # Set initial velocity to 0

def stop_wheels():
    """Stop all wheels."""
    for wheel in [wheel1, wheel2, wheel3, wheel4]:
        wheel.setVelocity(0)

def turn_right_by_angle(angle, velocity):
    """
    Turn the robot right by a specified angle using position sensors.
    :param angle: The desired turning angle in radians.
    :param velocity: The angular velocity for the turn (rad/s).
    """
    # Adjust the target angle with a correction factor
    adjusted_angle = angle * CORRECTION_FACTOR

    # Calculate the target distance for each wheel
    distance_per_radian = (L + W)  # Distance each wheel travels per radian of rotation
    target_distance = adjusted_angle * distance_per_radian

    # Calculate the target wheel positions
    initial_positions = [
        wheel1sensor.getValue(),
        wheel2sensor.getValue(),
        wheel3sensor.getValue(),
        wheel4sensor.getValue(),
    ]
    target_positions = [
        initial_positions[0] - (target_distance / WHEEL_RADIUS),  # Front-right wheel
        initial_positions[1] + (target_distance / WHEEL_RADIUS),  # Front-left wheel
        initial_positions[2] - (target_distance / WHEEL_RADIUS),  # Rear-right wheel
        initial_positions[3] + (target_distance / WHEEL_RADIUS),  # Rear-left wheel
    ]

    # Set the wheels to turn for a right rotation
    wheel1.setVelocity(-velocity)  # Front-right wheel
    wheel2.setVelocity(velocity)   # Front-left wheel
    wheel3.setVelocity(-velocity)  # Rear-right wheel
    wheel4.setVelocity(velocity)   # Rear-left wheel

    # Monitor the position sensors until the target is reached
    while True:
        current_positions = [
            wheel1sensor.getValue(),
            wheel2sensor.getValue(),
            wheel3sensor.getValue(),
            wheel4sensor.getValue(),
        ]
        # Check if all wheels have reached their target positions
        if (
            current_positions[0] <= target_positions[0] and
            current_positions[1] >= target_positions[1] and
            current_positions[2] <= target_positions[2] and
            current_positions[3] >= target_positions[3]
        ):
            break
        robot.step(TIME_STEP)

    # Stop the wheels
    stop_wheels()

def move_forward(distance, velocity):
    """
    Move the robot forward by a specified distance.
    :param distance: The distance to move in meters.
    :param velocity: The linear velocity for the motion (m/s).
    """
    # Calculate the time required to move the specified distance
    travel_time = distance / velocity

    # Set all wheels to move forward
    wheel1.setVelocity(velocity / WHEEL_RADIUS)
    wheel2.setVelocity(velocity / WHEEL_RADIUS)
    wheel3.setVelocity(velocity / WHEEL_RADIUS)
    wheel4.setVelocity(velocity / WHEEL_RADIUS)

    # Move forward for the calculated time
    start_time = robot.getTime()
    while robot.getTime() - start_time < travel_time:
        robot.step(TIME_STEP)

    # Stop the wheels
    stop_wheels()

# Main execution sequence
try:
    for i in range(10):
        # Step 1: Move forward 4 meters
        move_forward(4.0, 1.0)  # Move forward at 1 m/s
    
        # Step 2: Turn right 90 degrees
        turn_right_by_angle(TURN_ANGLE, 5.0)  # Turning velocity set to 5 rad/s
    
        # Step 3: Move forward another 2 meters
        #move_forward(4.0, 1.0)  # Move forward at 1 m/s

    print("Task completed!")
except Exception as e:
    print(f"An error occurred: {e}")