from controller import Robot, Keyboard, Receiver

import math

# ==== Constants ====
TIME_STEP = 32
MAX_VELOCITY = 20.0
ANGLE_STEP = 40 * math.pi / 180  # 40 deg in radians
POSITION_M = ANGLE_STEP
POSITION_K = 0.0

# 原地旋轉速度設定：每秒 1 度 = 0.01745 rad/s
DEG_PER_SEC = 10.0
OMEGA = DEG_PER_SEC * math.pi / 180.0  # 1deg/s in rad/s

# 麥克納姆參數
WHEEL_RADIUS = 0.1
BOT_L = 0.471
BOT_W = 0.376

robot = Robot()
timestep = int(robot.getBasicTimeStep())
keyboard = Keyboard()
keyboard.enable(timestep)

# Devices
try:
    motor = robot.getDevice('motor1')
    sensor = robot.getDevice('motor1_sensor')
    sensor.enable(timestep)
    mechanism_enabled = True
except Exception:
    mechanism_enabled = False

try:
    wheels = [robot.getDevice(f"wheel{i+1}") for i in range(4)]
    for wheel in wheels:
        wheel.setPosition(float('inf'))
        wheel.setVelocity(0)
    platform_enabled = True
except Exception:
    platform_enabled = False

try:
    receiver = robot.getDevice('rcv')
    receiver.enable(timestep)
    receiver_enabled = True
except Exception:
    receiver_enabled = False

current_state = "allow_m"
key_pressed = {'k': False, 'm': False, 'a': False}

print("平台操作：")
print("  方向鍵：移動/旋轉")
print("  F鍵：原地逆時針旋轉，G鍵：原地順時針旋轉（每秒 1 度）")
print("  (a/m/k 動作自動由 supervisor 指令發送) Q鍵：離開")

while robot.step(timestep) != -1:
    # 1. 處理自動訊息 (來自 Supervisor)
    if receiver_enabled:
        while receiver.getQueueLength() > 0:
            msg = receiver.getString()
            if mechanism_enabled:
                if msg == 'a':
                    # 可以根據需要加特殊動作（通常 a 動作不會動 motor，只是進入 allow_m 狀態）
                    current_state = "allow_m"
                elif msg == 'm' and current_state == "allow_m":
                    motor.setPosition(POSITION_M)
                    current_state = "allow_k"
                elif msg == 'k' and current_state == "allow_k":
                    motor.setPosition(POSITION_K)
                    current_state = "allow_m"
            receiver.nextPacket()

    # 2. 處理手動鍵盤（保留 m/k/a 手動模式，或僅限自動）
    key = keyboard.getKey()

    # Platform manual control
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
        elif key == ord('F') or key == ord('f'):
            print("f pressed")
            # 原地逆時針旋轉
            omega = OMEGA
            r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
            v_x = v_y = 0
            w1 = (1/r) * (v_x - v_y - (L+W)*omega)
            w2 = (1/r) * (v_x + v_y + (L+W)*omega)
            w3 = (1/r) * (v_x + v_y - (L+W)*omega)
            w4 = (1/r) * (v_x - v_y + (L+W)*omega)
            wheels[0].setVelocity(w1)
            wheels[1].setVelocity(w2)
            wheels[2].setVelocity(w3)
            wheels[3].setVelocity(w4)
        elif key == ord('G') or key == ord('g'):
            print("g pressed")
            # 原地順時針旋轉
            omega = -OMEGA
            r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
            v_x = v_y = 0
            w1 = (1/r) * (v_x - v_y - (L+W)*omega)
            w2 = (1/r) * (v_x + v_y + (L+W)*omega)
            w3 = (1/r) * (v_x + v_y - (L+W)*omega)
            w4 = (1/r) * (v_x - v_y + (L+W)*omega)
            wheels[0].setVelocity(w1)
            wheels[1].setVelocity(w2)
            wheels[2].setVelocity(w3)
            wheels[3].setVelocity(w4)
        elif key == ord('Q') or key == ord('q'):
            print("Exiting...")
            break
        else:
            for wheel in wheels:
                wheel.setVelocity(0)

    # (可選) 若還允許平台手動 m/k/a 控制，可保留下方
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

        # A key: 進入 allow_m 狀態（通常在 supervisor 自動循環時才需要，手動可略過）
        if key == ord('A') or key == ord('a'):
            if not key_pressed['a']:
                current_state = "allow_m"
            key_pressed['a'] = True
        else:
            key_pressed['a'] = False