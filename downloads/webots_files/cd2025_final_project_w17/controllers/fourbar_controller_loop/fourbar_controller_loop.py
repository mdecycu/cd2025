from controller import Robot, Keyboard, Receiver

# Constants
TIME_STEP = 32
MAX_VELOCITY = 10.0
ANGLE_STEP = 40 * 3.14159 / 180  # 40 degrees in radians
POSITION_M = ANGLE_STEP          # +40 deg
POSITION_K = 0.0                 # 0 deg

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
except Exception:
    mechanism_enabled = False

# Wheel setup (if available)
try:
    wheels = [robot.getDevice(f"wheel{i+1}") for i in range(4)]
    for wheel in wheels:
        wheel.setPosition(float('inf'))
        wheel.setVelocity(0)
    platform_enabled = True
except Exception:
    platform_enabled = False

# Add Receiver
try:
    receiver = robot.getDevice('rcv')
    receiver.enable(timestep)
    receiver_enabled = True
except Exception:
    receiver_enabled = False

current_state = "allow_m"
key_pressed = {'k': False, 'm': False}

while robot.step(timestep) != -1:
    # 1. 處理自動訊息
    if receiver_enabled:
        while receiver.getQueueLength() > 0:
            msg = receiver.getString()
            # print(f"收到指令: {msg}")
            if mechanism_enabled:
                if msg == 'm' and current_state == "allow_m":
                    motor.setPosition(POSITION_M)
                    current_state = "allow_k"
                elif msg == 'k' and current_state == "allow_k":
                    motor.setPosition(POSITION_K)
                    current_state = "allow_m"
            receiver.nextPacket()

    # 2. 處理手動鍵盤
    key = keyboard.getKey()

    # Platform control
    if platform_enabled:
        if key == Keyboard.UP:
            for wheel in wheels:
                wheel.setVelocity(MAX_VELOCITY)
        elif key == Keyboard.DOWN:
            for wheel in wheels:
                wheel.setVelocity(-MAX_VELOCITY)
        elif key == Keyboard.LEFT:
            wheels[0].setVelocity(MAX_VELOCITY)
            wheels[1].setVelocity(-MAX_VELOCITY)
            wheels[2].setVelocity(MAX_VELOCITY)
            wheels[3].setVelocity(-MAX_VELOCITY)
        elif key == Keyboard.RIGHT:
            wheels[0].setVelocity(-MAX_VELOCITY)
            wheels[1].setVelocity(MAX_VELOCITY)
            wheels[2].setVelocity(-MAX_VELOCITY)
            wheels[3].setVelocity(MAX_VELOCITY)
        elif key == ord('Q') or key == ord('q'):
            print("Exiting...")
            break
        else:
            for wheel in wheels:
                wheel.setVelocity(0)

    # Motor key control
    if mechanism_enabled:
        _current_motor_position = sensor.getValue()

        # M key: only take action if allowed and not held
        if key == ord('M') or key == ord('m'):
            if not key_pressed['m'] and current_state == "allow_m":
                motor.setPosition(POSITION_M)
                current_state = "allow_k"
            key_pressed['m'] = True
        else:
            key_pressed['m'] = False

        # K key: only take action if allowed and not held
        if key == ord('K') or key == ord('k'):
            if not key_pressed['k'] and current_state == "allow_k":
                motor.setPosition(POSITION_K)
                current_state = "allow_m"
            key_pressed['k'] = True
        else:
            key_pressed['k'] = False