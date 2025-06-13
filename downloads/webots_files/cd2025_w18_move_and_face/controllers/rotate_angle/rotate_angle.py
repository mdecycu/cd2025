from controller import Robot, Keyboard
import math

deg = math.pi/180

# Constants
TIME_STEP = 16  # Simulation time step in milliseconds
WHEEL_RADIUS = 0.05  # Radius of the wheels in meters (10cm)
L = 0.56 
W = 0.34  
MAX_VELOCITY = 10.0  # Maximum velocity allowed for the wheels

# Initialize the robot
robot = Robot()

# Initialize the keyboard
keyboard = Keyboard()
keyboard.enable(TIME_STEP)
imu = robot.getDevice("imu")
imu.enable(TIME_STEP)

# Get motor devices
wheel1 = robot.getDevice("wheel1")  # Front-right wheel
wheel2 = robot.getDevice("wheel2")  # Front-left wheel
wheel3 = robot.getDevice("wheel3")  # Rear-right wheel
wheel4 = robot.getDevice("wheel4")  # Rear-left wheel

# Set motors to velocity control mode
for wheel in [wheel1, wheel2, wheel3, wheel4]:
    wheel.setPosition(float('inf'))  # Enable velocity control
    wheel.setVelocity(0)  # Set initial velocity to 0

def set_wheel_velocity(v1, v2, v3, v4):
    """Set the velocity of all wheels."""
    wheel1.setVelocity(v1)
    wheel2.setVelocity(v2)
    wheel3.setVelocity(v3)
    wheel4.setVelocity(v4)

def get_yaw():
    return imu.getRollPitchYaw()[2]

def angle_diff(a, b):
    """compute shortest diff between two angles, result in [-pi, pi]"""
    d = a - b
    while d > math.pi:
        d -= 2 * math.pi
    while d < -math.pi:
        d += 2 * math.pi
    return d

def rotate_by_angle(target_angle_deg, fast_velocity=MAX_VELOCITY, slow_velocity=1.0, tolerance_deg=0.05):
    start_yaw = get_yaw()
    target_rad = math.radians(target_angle_deg)
    slow_zone = math.radians(5)  # 進入5度內就降速
    direction = 1 if target_angle_deg > 0 else -1
    set_wheel_velocity(-direction*fast_velocity, direction*fast_velocity, -direction*fast_velocity, direction*fast_velocity)
    while True:
        robot.step(TIME_STEP)
        now_yaw = get_yaw()
        turned = angle_diff(now_yaw, start_yaw)
        remain = abs(target_rad) - abs(turned)
        if remain < slow_zone:
            # 降速
            set_wheel_velocity(-direction*slow_velocity, direction*slow_velocity, -direction*slow_velocity, direction*slow_velocity)
        if remain < math.radians(tolerance_deg):
            break
    set_wheel_velocity(0, 0, 0, 0)
    print(f"Yaw changed by {math.degrees(turned):.2f} degrees")

print("Use arrow keys to control youBot.")
print("A: rotate +30 deg, Z: rotate -30 deg, Q: quit.")

# Main loop
print("Use arrow keys to control the robot.")
print("Up: Move forward, Down: Move backward, Left: Turn left, Right: Turn right.")
print("Press 'A' to rotate +30 deg, 'Z' to rotate -30 deg.")
print("Press 'Q' to quit.")

while robot.step(TIME_STEP) != -1:
    key = keyboard.getKey()  # Read the key pressed

    if key == Keyboard.UP:
        # Move forward
        velocity = MAX_VELOCITY
        set_wheel_velocity(velocity, velocity, velocity, velocity)
    elif key == Keyboard.DOWN:
        # Move backward
        velocity = -MAX_VELOCITY
        set_wheel_velocity(velocity, velocity, velocity, velocity)
    elif key == Keyboard.RIGHT:
        # Turn right
        velocity = MAX_VELOCITY
        set_wheel_velocity(-velocity, velocity, -velocity, velocity)
    elif key == Keyboard.LEFT:
        # Turn left
        velocity = MAX_VELOCITY
        set_wheel_velocity(velocity, -velocity, velocity, -velocity)
    elif key == ord('A') or key == ord('a'):
        # Test: Rotate +30 degrees (clockwise)
        print("Rotating +30 degrees (clockwise)")
        # 在按下 a 鍵時
        before_yaw = imu.getRollPitchYaw()[2]
        print(before_yaw)
        rotate_by_angle(30)
        after_yaw = imu.getRollPitchYaw()[2]
        print(after_yaw)
        delta_yaw_deg = (after_yaw - before_yaw)/deg
        print(f"Yaw changed by {delta_yaw_deg:.2f} degrees")
    elif key == ord('Z') or key == ord('z'):
        # Test: Rotate -30 degrees (counterclockwise)
        print("Rotating -30 degrees (counterclockwise)")
        rotate_by_angle(-30)
    elif key == ord('Q') or key == ord('q'):
        # Quit the program
        print("Exiting...")
        break
    else:
        # Stop the wheels when no key is pressed
        set_wheel_velocity(0, 0, 0, 0)