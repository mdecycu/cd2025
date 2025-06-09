from controller import Robot, Keyboard, GPS, InertialUnit
import math

# ================== 參數初始化 ==================
# 機器人尺寸參數
WHEEL_RADIUS = 0.1  # 原本設10cm，繞圓部分採用此參數
L = 0.471
W = 0.376
MAX_VELOCITY = 10.0

# 控制用
score_to_send = 2
cooldown = 1.0

# ====== 繞圓與heading輔助函數 ======
def clamp_angle(angle):
    """將角度包覆到 [-pi, pi] 區間，避免角度跳躍"""
    return (angle + math.pi) % (2 * math.pi) - math.pi

def goto_point(robot, gps, imu, wheels, x_goal, y_goal, speed=0.4, goal_threshold=0.15, K_omega=2.0):
    """
    控制 stand 前進到 (x_goal, y_goal)，同時修正 heading，直到距離小於 goal_threshold
    """
    WHEEL_RADIUS = 0.1      # 與鍵盤模式一致
    BOT_L = 0.471
    BOT_W = 0.376
    r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
    timestep = int(robot.getBasicTimeStep())
    while True:
        ret = robot.step(timestep)
        if ret == -1:
            return
        pos = gps.getValues()
        x, y = pos[0], pos[1]
        dx, dy = x_goal - x, y_goal - y
        dist = math.hypot(dx, dy)
        if dist < goal_threshold:
            break
        yaw = imu.getRollPitchYaw()[2]
        theta_goal = math.atan2(dy, dx)
        heading_error = clamp_angle(theta_goal - yaw)
        omega = K_omega * heading_error
        # 目標速度向量 (世界座標)
        vx_world = dx / (dist + 1e-9) * speed
        vy_world = dy / (dist + 1e-9) * speed
        # 轉成本體座標速度
        v_x = math.cos(yaw) * vx_world + math.sin(yaw) * vy_world
        v_y = -math.sin(yaw) * vx_world + math.cos(yaw) * vy_world
        # 麥克納姆輪逆運動學
        w1 = (1/r) * (v_x - v_y - (L+W)*omega)
        w2 = (1/r) * (v_x + v_y + (L+W)*omega)
        w3 = (1/r) * (v_x + v_y - (L+W)*omega)
        w4 = (1/r) * (v_x - v_y + (L+W)*omega)
        wheels[0].setVelocity(w1)
        wheels[1].setVelocity(w2)
        wheels[2].setVelocity(w3)
        wheels[3].setVelocity(w4)
    # 停車
    for w in wheels:
        w.setVelocity(0.0)

def turn_heading_to_point(robot, imu, wheels, x_now, y_now, x_target, y_target, tolerance=8.0, max_steps=200):
    """原地旋轉車頭，讓車頭從(x_now, y_now)指向(x_target, y_target)"""
    WHEEL_RADIUS = 0.1
    BOT_L = 0.471
    BOT_W = 0.376
    r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
    timestep = int(robot.getBasicTimeStep())
    theta_goal = math.atan2(y_target - y_now, x_target - x_now)
    steps = 0
    while True:
        if steps > max_steps:
            break
        steps += 1
        ret = robot.step(timestep)
        if ret == -1:
            return
        yaw = imu.getRollPitchYaw()[2]
        error = clamp_angle(theta_goal - yaw)
        if abs(math.degrees(error)) < tolerance:
            break
        K = 1.0
        omega = K * error
        v_x = v_y = 0
        w1 = (1/r) * (v_x - v_y - (L+W)*omega)
        w2 = (1/r) * (v_x + v_y + (L+W)*omega)
        w3 = (1/r) * (v_x + v_y - (L+W)*omega)
        w4 = (1/r) * (v_x - v_y + (L+W)*omega)
        wheels[0].setVelocity(w1)
        wheels[1].setVelocity(w2)
        wheels[2].setVelocity(w3)
        wheels[3].setVelocity(w4)
    for w in wheels:
        w.setVelocity(0.0)

def passive_wait(robot, sec):
    start_time = robot.getTime()
    while robot.getTime() - start_time < sec:
        if robot.step(int(robot.getBasicTimeStep())) == -1:
            break

# ================== 主程式 ==================
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# 控制裝置
emitter = robot.getDevice("score_emitter")
sensor = robot.getDevice('sensor')
sensor.enable(timestep)
score = 0
last_score_time = 0

keyboard = Keyboard()
keyboard.enable(timestep)

# 馬達
wheel5 = robot.getDevice("wheel5")  # Front-right
wheel6 = robot.getDevice("wheel6")  # Front-left
wheel7 = robot.getDevice("wheel7")  # Rear-right
wheel8 = robot.getDevice("wheel8")  # Rear-left
for wheel in [wheel5, wheel6, wheel7, wheel8]:
    wheel.setPosition(float('inf'))
    wheel.setVelocity(0)

def set_wheel_velocity(v1, v2, v3, v4):
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
    for i in range(len(lookup_table)-1):
        a0, d0 = lookup_table[i]
        a1, d1 = lookup_table[i+1]
        if a1 <= ad_value <= a0:
            return d0 + (d1 - d0) * (ad_value - a0) / (a1 - a0)
    if ad_value > lookup_table[0][0]:
        return lookup_table[0][1]
    return lookup_table[-1][1]

# ==== 繞圓裝置初始化 ====
gps = robot.getDevice("gps")
imu = robot.getDevice("inertial unit")
gps.enable(timestep)
imu.enable(timestep)
wheel_names = ["wheel5", "wheel6", "wheel7", "wheel8"]
wheels = [robot.getDevice(name) for name in wheel_names]
for w in wheels:
    w.setPosition(float('inf'))

# 讓感測器啟動穩定
for _ in range(10):
    robot.step(timestep)

# ==== 按鍵說明 ====
print("Use 'E', 'X', 'S', 'D' keys to control the robot.")
print("E: Move forward, X: Move backward, S: Turn left, D: Turn right.")
print("Press 'C' to start circle-around mode, 'Q' to quit.")

# ==== 主迴圈 ====
CIRCLE_MODE = False

while robot.step(timestep) != -1:
    key = keyboard.getKey()
    # Read DistanceSensor value
    sensor_value = sensor.getValue()
    distance = ad_to_distance(sensor_value)
    current_time = robot.getTime()

    if key == ord('M') or key == ord('m'):
        print(distance)
    if key == ord('K') or key == ord('k'):
        print(distance)

    if distance < 0.11 and (current_time - last_score_time) > cooldown:
        score += score_to_send
        print("得分")
        print(distance)
        emitter.send(str(score_to_send).encode('utf-8'))
        last_score_time = current_time

    if CIRCLE_MODE:
        # 繞圓模式主控
        # 取得目前位置
        pos = gps.getValues()
        x0, y0 = pos[0], pos[1]
        radius = 6.23  # 圓半徑

        # 計算基準極角
        current_angle = math.atan2(y0, x0)
        if current_angle < 0:
            current_angle += 2 * math.pi

        # 產生 12 等分點
        angles = [((current_angle + (2*math.pi)*i/12) % (2*math.pi)) for i in range(12)]
        waypoints = [(radius * math.cos(a), radius * math.sin(a)) for a in angles]

        # 找最近點為起點
        min_idx = min(range(12), key=lambda i: math.hypot(waypoints[i][0] - x0, waypoints[i][1] - y0))
        ordered_waypoints = waypoints[min_idx:] + waypoints[:min_idx] + [(x0, y0)]

        for idx, (wx, wy) in enumerate(ordered_waypoints):
            print(f"\n=== 準備前往第 {idx+1} 個點: ({wx:.2f}, {wy:.2f}) ===")
            goto_point(robot, gps, imu, wheels, wx, wy)
            pos = gps.getValues()
            x_now, y_now = pos[0], pos[1]
            # 車頭指向圓心 (0,0)
            turn_heading_to_point(robot, imu, wheels, x_now, y_now, 0.0, 0.0)
            print(f"已抵達第 {idx+1} 個點: ({wx:.2f}, {wy:.2f})，車頭已指向 (0, 0)")
            passive_wait(robot, 1.0)
        print("\n已完成圍繞半徑6.23公尺圓周12點繞行並回到起點，任務結束。")
        CIRCLE_MODE = False  # 回到一般模式
        continue  # 跳過下方鍵盤處理，等待下一步
    # === 一般鍵盤控制 ===
    if key == ord('E') or key == ord('e'):
        set_wheel_velocity(MAX_VELOCITY, MAX_VELOCITY, MAX_VELOCITY, MAX_VELOCITY)
    elif key == ord('X') or key == ord('x'):
        set_wheel_velocity(-MAX_VELOCITY, -MAX_VELOCITY, -MAX_VELOCITY, -MAX_VELOCITY)
    elif key == ord('D') or key == ord('d'):
        set_wheel_velocity(-MAX_VELOCITY, MAX_VELOCITY, -MAX_VELOCITY, MAX_VELOCITY)
    elif key == ord('S') or key == ord('s'):
        set_wheel_velocity(MAX_VELOCITY, -MAX_VELOCITY, MAX_VELOCITY, -MAX_VELOCITY)
    elif key == ord('Q') or key == ord('q'):
        print("Exiting...")
        break
    elif key == ord('C') or key == ord('c'):
        print("啟動圓周繞行模式...")
        set_wheel_velocity(0, 0, 0, 0)
        CIRCLE_MODE = True
    else:
        set_wheel_velocity(0, 0, 0, 0)