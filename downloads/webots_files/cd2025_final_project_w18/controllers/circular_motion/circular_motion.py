from controller import Robot, GPS, InertialUnit
import math

def clamp_angle(angle):
    """將角度包覆到 [-pi, pi] 區間，避免角度跳躍"""
    return (angle + math.pi) % (2 * math.pi) - math.pi

def goto_point(robot, gps, imu, wheels, x_goal, y_goal, speed=0.4, goal_threshold=0.15, K_omega=2.0):
    """
    控制 youBot 前進到 (x_goal, y_goal)，同時修正 heading，直到距離小於 goal_threshold
    """
    WHEEL_RADIUS = 0.0478      # 輪子半徑 (m)
    BOT_L = 0.228              # 機器人長 (m)
    BOT_W = 0.158              # 機器人寬 (m)
    r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
    timestep = int(robot.getBasicTimeStep())
    while True:
        ret = robot.step(timestep)
        if ret == -1:
            print("robot.step 被中止，goto_point 結束")
            return
        pos = gps.getValues()
        x, y = pos[0], pos[1]
        dx, dy = x_goal - x, y_goal - y
        dist = math.hypot(dx, dy)
        print(f"[goto_point] 目前({x:.2f},{y:.2f}) → 目標({x_goal:.2f},{y_goal:.2f}), 剩餘距離:{dist:.3f}")
        if dist < goal_threshold:
            break  # 抵達目標點，結束此段
        yaw = imu.getRollPitchYaw()[2]  # 取得當前車頭角度
        theta_goal = math.atan2(dy, dx) # 目標方向角
        heading_error = clamp_angle(theta_goal - yaw)
        omega = K_omega * heading_error # 角速度
        # 目標速度向量 (世界座標)
        vx_world = dx / (dist + 1e-9) * speed
        vy_world = dy / (dist + 1e-9) * speed
        # 轉成本體座標速度
        v_x = math.cos(yaw) * vx_world + math.sin(yaw) * vy_world
        v_y = -math.sin(yaw) * vx_world + math.cos(yaw) * vy_world
        # 麥克納姆輪逆運動學，計算各輪速度
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
    print(f"[goto_point] 抵達 ({x_goal},{y_goal})")

def turn_heading_to_point(robot, imu, wheels, x_now, y_now, x_target, y_target, tolerance=8.0, max_steps=200):
    """
    原地旋轉車頭，讓車頭從(x_now, y_now)指向(x_target, y_target)
    tolerance: 容忍誤差角度 (度)
    max_steps: 最多執行步數，避免死循環
    """
    WHEEL_RADIUS = 0.0478
    BOT_L = 0.228
    BOT_W = 0.158
    r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
    timestep = int(robot.getBasicTimeStep())
    theta_goal = math.atan2(y_target - y_now, x_target - x_now)  # 目標方向角
    steps = 0
    while True:
        if steps > max_steps:
            print("[turn_heading] timeout，強制跳出")
            break  # 避免死循環
        steps += 1
        ret = robot.step(timestep)
        if ret == -1:
            print("robot.step 被中止，turn_heading_to_point 結束")
            return
        yaw = imu.getRollPitchYaw()[2]
        error = clamp_angle(theta_goal - yaw)
        print(f"[turn_heading] 現在朝向 {math.degrees(yaw):.2f}° 目標 {math.degrees(theta_goal):.2f}° 誤差 {math.degrees(error):.2f}°")
        if abs(math.degrees(error)) < tolerance:
            break  # 角度已經接近
        K = 1.0
        omega = K * error  # 角速度
        v_x = v_y = 0
        # 原地旋轉麥克納姆輪速度
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
    print(f"[turn_heading] 已朝向 ({x_target},{y_target})")

def passive_wait(robot, sec):
    """讓機器人被動等待 sec 秒，確保 Webots 控制器不中止"""
    start_time = robot.getTime()
    while robot.getTime() - start_time < sec:
        if robot.step(int(robot.getBasicTimeStep())) == -1:
            break

# ====== Main Program ======
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# 取得感測器與馬達
gps = robot.getDevice("gps")
imu = robot.getDevice("inertial unit")
gps.enable(timestep)
imu.enable(timestep)
wheel_names = ["wheel1", "wheel2", "wheel3", "wheel4"]
wheels = [robot.getDevice(name) for name in wheel_names]
for w in wheels:
    w.setPosition(float('inf'))  # 設定輪子為無限旋轉模式

# 先讓感測器啟動穩定，避免初始值異常
for _ in range(10):
    robot.step(timestep)

# 取得目前位置，作為圓周點生成的基準
pos = gps.getValues()
x0, y0 = pos[0], pos[1]  # 起始位置
radius = 4.0             # 圓半徑 4 公尺

# 計算當下相對原點的極角 (保證在 [0, 2pi) 範圍)
current_angle = math.atan2(y0, x0)
if current_angle < 0:
    current_angle += 2 * math.pi

# 產生 12 個等分點的極角（逆時針方向）
angles = [((current_angle + (2*math.pi)*i/12) % (2*math.pi)) for i in range(12)]
# 產生圓周上的 12 個點座標
waypoints = [(radius * math.cos(a), radius * math.sin(a)) for a in angles]

# 找出離目前位置最近的那個圓周點作為起點
min_idx = min(range(12), key=lambda i: math.hypot(waypoints[i][0] - x0, waypoints[i][1] - y0))
# 依序繞一圈，最後回到原始位置
ordered_waypoints = waypoints[min_idx:] + waypoints[:min_idx] + [(x0, y0)]

for idx, (wx, wy) in enumerate(ordered_waypoints):
    print(f"\n=== 準備前往第 {idx+1} 個點: ({wx:.2f}, {wy:.2f}) ===")
    # 1. 行進到該點
    goto_point(robot, gps, imu, wheels, wx, wy)
    # 2. 到達後取得當下座標
    pos = gps.getValues()
    x_now, y_now = pos[0], pos[1]
    # 3. 車頭指向 (0, 0)
    turn_heading_to_point(robot, imu, wheels, x_now, y_now, 0.0, 0.0)
    print(f"已抵達第 {idx+1} 個點: ({wx:.2f}, {wy:.2f})，車頭已指向 (0, 0)")
    # 4. 停留 1 秒
    passive_wait(robot, 1.0)

print("\n已完成圍繞半徑4m圓周12點繞行並回到起點，任務結束。")