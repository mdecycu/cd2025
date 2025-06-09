from controller import Robot, Keyboard

# Constants
#TIME_STEP = 32  # Simulation time step in milliseconds
WHEEL_RADIUS = 0.1  # Radius of the wheels in meters (10cm)
L = 0.471  # Half of the robot's length in meters
W = 0.376  # Half of the robot's width in meters
MAX_VELOCITY = 10.0  # Maximum velocity allowed for the wheels

# Initialize the robot
robot = Robot()

# Get simulation time step
timestep = int(robot.getBasicTimeStep())
emitter = robot.getDevice("score_emitter")
score_to_send = 2  # 每次加分2分，可依實際得分修改

# Get the DistanceSensor device
sensor = robot.getDevice('sensor')
sensor.enable(timestep)
score = 0
last_score_time = 0
cooldown = 1.0

# Initialize the keyboard
keyboard = Keyboard()
#keyboard.enable(TIME_STEP)
keyboard.enable(timestep)


# Get motor devices
wheel5 = robot.getDevice("wheel5")  # Front-right wheel
wheel6 = robot.getDevice("wheel6")  # Front-left wheel
wheel7 = robot.getDevice("wheel7")  # Rear-right wheel
wheel8 = robot.getDevice("wheel8")  # Rear-left wheel

# Set motors to velocity control mode
for wheel in [wheel5, wheel6, wheel7, wheel8]:
    wheel.setPosition(float('inf'))  # Enable velocity control
    wheel.setVelocity(0)  # Set initial velocity to 0

def set_wheel_velocity(v1, v2, v3, v4):
    """Set the velocity of all wheels."""
    wheel5.setVelocity(v1)
    wheel6.setVelocity(v2)
    wheel7.setVelocity(v3)
    wheel8.setVelocity(v4)

# lookupTable 轉成程式用的格式
lookup_table = [
    (1000, 0.00),
    (620, 0.12),
    (372, 0.13),
    (248, 0.14),
    (186, 0.15),
    (0, 0.18)
]

def ad_to_distance(ad_value):
    # 假設AD值遞減，距離遞增
    for i in range(len(lookup_table)-1):
        a0, d0 = lookup_table[i]
        a1, d1 = lookup_table[i+1]
        if a1 <= ad_value <= a0:
            # 線性插值
            return d0 + (d1 - d0) * (ad_value - a0) / (a1 - a0)
    # 超出範圍時回傳極值
    if ad_value > lookup_table[0][0]:
        return lookup_table[0][1]
    return lookup_table[-1][1]
    
# Main loop
print("Use 'E', 'X', 'S', 'D' keys to control the robot.")
print("E: Move forward, X: Move backward, S: Turn left, D: Turn right.")
print("Press 'Q' to quit.")

#while robot.step(TIME_STEP) != -1:
while robot.step(timestep) != -1:

    key = keyboard.getKey()  # Read the key pressed
    # Read DistanceSensor value
    sensor_value = sensor.getValue()
    #print(sensor_value)
    distance = ad_to_distance(sensor_value)
    current_time = robot.getTime()
    #print(sensor_value)
    # Check if the ball blocks the sensor (you may need to adjust the threshold based on your sensor's range)
    if key == ord('M') or key == ord('m'):
        print(distance)
    if key == ord('K') or key == ord('k'):
        print(distance)

    if distance < 0.11 and (current_time - last_score_time) > cooldown:
        score +=2
        print("得分")
        print(distance)
        # 假設你偵測到某事件得分時才送出
        emitter.send(str(score_to_send).encode('utf-8'))


    if key == ord('E') or key == ord('e'):
        # Move forward
        velocity = MAX_VELOCITY
        set_wheel_velocity(velocity, velocity, velocity, velocity)
    elif key == ord('X') or key == ord('x'):
        # Move backward
        velocity = -MAX_VELOCITY
        set_wheel_velocity(velocity, velocity, velocity, velocity)
    elif key == ord('D') or key == ord('d'):
        # Turn right
        velocity = MAX_VELOCITY
        set_wheel_velocity(-velocity, velocity, -velocity, velocity)
    elif key == ord('S') or key == ord('s'):
        # Turn left
        velocity = MAX_VELOCITY
        set_wheel_velocity(velocity, -velocity, velocity, -velocity)
    elif key == ord('Q') or key == ord('q'):
        # Quit the program
        print("Exiting...")
        break
    else:
        # Stop the wheels when no key is pressed
        set_wheel_velocity(0, 0, 0, 0)