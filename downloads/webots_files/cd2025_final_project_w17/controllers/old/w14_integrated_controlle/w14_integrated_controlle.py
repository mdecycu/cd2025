from controller import Robot, Keyboard

# Constants
TIME_STEP = 32
MAX_VELOCITY = 10.0
ANGLE_STEP = 38 * 3.14159 / 180  # 18 degrees in radians
INITIAL_POSITION = 0.0

# Initialize robot and keyboard
robot = Robot()
timestep = int(robot.getBasicTimeStep())
keyboard = Keyboard()
keyboard.enable(timestep)

# Get devices
try:
    motor = robot.getDevice('motor1')
    sensor = robot.getDevice('motor1_sensor')
    sensor.enable(timestep)
    mechanism_enabled = True
except:
    mechanism_enabled = False

# Wheel setup (if available)
try:
    wheels = [robot.getDevice(f"wheel{i+1}") for i in range(4)]
    for wheel in wheels:
        wheel.setPosition(float('inf'))  # Infinite position to enable velocity control
        wheel.setVelocity(0)  # Start with zero velocity
    platform_enabled = True
except:
    platform_enabled = False

# Key control flags
key_pressed = {
    'k': False,
    'm': False
}

# State machine: which key is allowed to trigger
# Start with M being allowed
current_state = "allow_m"

# Track motor position (relative to the platform)
current_motor_position = INITIAL_POSITION

print("Press M to move to INITIAL +38°, then K to move -38° from current.")
print("Only one action allowed per key until the other key is pressed.")
print("Use arrow keys to control platform movement.")

while robot.step(timestep) != -1:
    key = keyboard.getKey()

    # Platform control
    if platform_enabled:
        # Platform movement controls
        if key == Keyboard.UP:
            # Move platform forward
            for wheel in wheels:
                wheel.setVelocity(MAX_VELOCITY)
        elif key == Keyboard.DOWN:
            # Move platform backward
            for wheel in wheels:
                wheel.setVelocity(-MAX_VELOCITY)
        elif key == Keyboard.LEFT:
            # Rotate platform left (counter-clockwise)
            wheels[0].setVelocity(MAX_VELOCITY)
            wheels[1].setVelocity(-MAX_VELOCITY)
            wheels[2].setVelocity(MAX_VELOCITY)
            wheels[3].setVelocity(-MAX_VELOCITY)
        elif key == Keyboard.RIGHT:
            # Rotate platform right (clockwise)
            wheels[0].setVelocity(-MAX_VELOCITY)
            wheels[1].setVelocity(MAX_VELOCITY)
            wheels[2].setVelocity(-MAX_VELOCITY)
            wheels[3].setVelocity(MAX_VELOCITY)
        elif key == ord('Q') or key == ord('q'):
            print("Exiting...")
            break
        else:
            # Stop all wheels if no key is pressed
            for wheel in wheels:
                wheel.setVelocity(0)

    # Key control for motor
    if mechanism_enabled:
        # Read the current motor position from the sensor
        current_motor_position = sensor.getValue()

        # M key logic
        if key == ord('M') or key == ord('m'):
            if not key_pressed['m'] and current_state == "allow_m":
                # Move motor to +18 degrees relative to current position
                current_motor_position += ANGLE_STEP
                motor.setPosition(current_motor_position)
                print(f"M pressed: Moving to {current_motor_position:.3f} rad (+18°)")
                current_state = "allow_k"  # Now only K is allowed
            key_pressed['m'] = True
        else:
            key_pressed['m'] = False

        # K key logic
        if key == ord('K') or key == ord('k'):
            if not key_pressed['k'] and current_state == "allow_k":
                # Move motor to -18 degrees relative to current position
                current_motor_position -= ANGLE_STEP
                motor.setPosition(current_motor_position)
                print(f"K pressed: Moving to {current_motor_position:.3f} rad (-18°)")
                current_state = "allow_m"  # Now only M is allowed
            key_pressed['k'] = True
        else:
            key_pressed['k'] = False

        # Debug: print current motor position
        print(f"Current motor position: {current_motor_position:.3f} rad")
