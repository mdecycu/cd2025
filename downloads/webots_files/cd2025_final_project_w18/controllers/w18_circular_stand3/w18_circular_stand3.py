from controller import Robot, GPS, InertialUnit
import math

def clamp_angle(angle):
    """將角度包覆到 [-pi, pi] 區間，避免角度跳躍"""
    return (angle + math.pi) % (2 * math.pi) - math.pi

def angle_between_vectors(ax, ay, bx, by):
    norm_a = math.hypot(ax, ay)
    norm_b = math.hypot(bx, by)
    ax, ay = ax / norm_a, ay / norm_a
    bx, by = bx / norm_b, by / norm_b
    dot = ax * bx + ay * by
    det = ax * by - ay * bx
    angle_rad = math.atan2(det, dot)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def goto_point_and_face_to(
    robot, gps, imu, wheels, x_goal, y_goal, face_to=(0.0, 0.0), 
    fast_speed=1.0, slow_speed=0.22, slow_dist=0.7, goal_threshold=0.22,
    K_omega=1.3, min_omega_deg=2.0, min_speed=0.08
):
    """
    控制 youBot 前進到 (x_goal, y_goal)，到達後車頭朝向 face_to (x, y)。
    前進過程先用較快速度，接近目標時自動減速。加入死區及更平滑的控制。
    角度控制用向量夾角計算。
    """
    WHEEL_RADIUS = 0.0478      # 輪子半徑 (m)
    BOT_L = 0.228              # 機器人長 (m)
    BOT_W = 0.158              # 機器人寬 (m)
    r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
    timestep = int(robot.getBasicTimeStep())

    # === 1. 先轉向目標點並前進 ===
    prev_dist = 1e6
    while True:
        ret = robot.step(timestep)
        if ret == -1:
            print("robot.step 被中止，goto_point_and_face_to 結束")
            return
        pos = gps.getValues()
        x, y = pos[0], pos[1]
        dx, dy = x_goal - x, y_goal - y
        dist = math.hypot(dx, dy)
        if dist < goal_threshold:
            break  # 抵達目標點
        yaw = imu.getRollPitchYaw()[2]  # 車頭方向
        # 車頭向量
        head_vec = (math.cos(yaw), math.sin(yaw))
        # 目標方向向量
        tar_vec = (dx, dy)
        # 計算需轉的角度
        rotate_angle = angle_between_vectors(head_vec[0], head_vec[1], tar_vec[0], tar_vec[1])
        # == 角速度死區 ==
        if abs(rotate_angle) < min_omega_deg:
            omega = 0.0
        else:
            omega = K_omega * math.radians(rotate_angle)
            # 角速度限幅
            omega = max(min(omega, 2.0), -2.0)
        # 動態調整速度
        speed = fast_speed if dist > slow_dist else slow_speed
        # == 線速度死區 ==
        if abs(dist) < min_speed:
            vx_world = 0
            vy_world = 0
        else:
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
        # 若距離已經開始增加，強制停車（避免震盪）
        if dist > prev_dist + 0.01 and dist < 0.3:
            print("距離開始增加，強制停車，避免晃動")
            break
        prev_dist = dist
    # 停車
    for w in wheels:
        w.setVelocity(0.0)
    print(f"[goto_point_and_face_to] 抵達 ({x_goal:.2f},{y_goal:.2f})")

    # === 2. 轉向 face_to 點 ===
    pos = gps.getValues()
    x_now, y_now = pos[0], pos[1]
    yaw = imu.getRollPitchYaw()[2]
    head_vec = (math.cos(yaw), math.sin(yaw))
    face_vec = (face_to[0] - x_now, face_to[1] - y_now)
    rotate_angle = angle_between_vectors(head_vec[0], head_vec[1], face_vec[0], face_vec[1])
    print(f"[goto_point_and_face_to] 車頭需再轉 {rotate_angle:.2f} 度面向 {face_to}")

    # 原地旋轉，帶死區
    tolerance = 7.0  # 容忍誤差角度 (度)
    steps = 0
    max_steps = 200
    while True:
        if steps > max_steps:
            print("[face_to] timeout，強制跳出")
            break
        steps += 1
        ret = robot.step(timestep)
        if ret == -1:
            print("robot.step 被中止，face_to 結束")
            return
        yaw = imu.getRollPitchYaw()[2]
        head_vec = (math.cos(yaw), math.sin(yaw))
        face_vec = (face_to[0] - x_now, face_to[1] - y_now)
        error = angle_between_vectors(head_vec[0], head_vec[1], face_vec[0], face_vec[1])
        # == 角度死區 ==
        if abs(error) < tolerance:
            break
        # == 角速度死區 ==
        if abs(error) < min_omega_deg:
            omega = 0.0
        else:
            omega = 1.0 * math.radians(error)
            omega = max(min(omega, 1.5), -1.5)
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
    print(f"[goto_point_and_face_to] 已面向 {face_to}")

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
wheel_names = ["wheel5", "wheel6", "wheel7", "wheel8"]
wheels = [robot.getDevice(name) for name in wheel_names]
for w in wheels:
    w.setPosition(float('inf'))  # 設定輪子為無限旋轉模式

# 先讓感測器啟動穩定，避免初始值異常
for _ in range(10):
    robot.step(timestep)

# 取得目前位置，作為圓周點生成的基準
pos = gps.getValues()
x0, y0 = pos[0], pos[1]  # 起始位置
radius = 6.23             # 圓半徑 6.23 公尺

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
    # 1. 行進到該點，抵達後車頭朝向(0,0)
    goto_point_and_face_to(robot, gps, imu, wheels, wx, wy, face_to=(0.0, 0.0))
    print(f"已抵達第 {idx+1} 個點: ({wx:.2f}, {wy:.2f})，車頭已指向 (0, 0)")
    # 2. 停留 1 秒
    passive_wait(robot, 1.0)

print("\n已完成圍繞半徑6.23m圓周12點繞行並回到起點，任務結束。")