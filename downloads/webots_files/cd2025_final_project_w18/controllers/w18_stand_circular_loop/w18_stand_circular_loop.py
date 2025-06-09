from controller import Robot, Keyboard, GPS, InertialUnit
import math

# ================== 參數初始化 ==================
WHEEL_RADIUS = 0.1
L = 0.471
W = 0.376
MAX_VELOCITY = 10.0

score_to_send = 2
cooldown = 1.0

def clamp_angle(angle):
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
    fast_speed=0.82, slow_speed=0.06, slow_dist=0.09, goal_threshold=0.007,
    K_omega=2.5, min_omega_deg=0.5, min_speed=0.0015
):
    """
    超高精度行進與轉向控制
    """
    r = WHEEL_RADIUS
    timestep = int(robot.getBasicTimeStep())
    prev_dist = 1e6
    in_range_count = 0

    # === 1. 先轉向目標點並前進 ===
    while True:
        ret = robot.step(timestep)
        if ret == -1:
            return
        pos = gps.getValues()
        x, y = pos[0], pos[1]
        dx, dy = x_goal - x, y_goal - y
        dist = math.hypot(dx, dy)
        yaw = imu.getRollPitchYaw()[2]
        # 車頭向量
        head_vec = (math.cos(yaw), math.sin(yaw))
        tar_vec = (dx, dy)
        rotate_angle = angle_between_vectors(head_vec[0], head_vec[1], tar_vec[0], tar_vec[1])
        # == 角速度死區 ==
        if abs(rotate_angle) < min_omega_deg:
            omega = 0.0
        else:
            omega = K_omega * math.radians(rotate_angle)
            omega = max(min(omega, 2.0), -2.0)
        # 動態調整速度
        speed = fast_speed if dist > slow_dist else slow_speed
        # == 線速度死區 ==
        if abs(dist) < min_speed:
            vx_world = 0
            vy_world = 0
        else:
            vx_world = dx / (dist + 1e-9) * speed
            vy_world = dy / (dist + 1e-9) * speed * 0.08  # 側向分量再降權
        v_x = math.cos(yaw) * vx_world + math.sin(yaw) * vy_world
        v_y = -math.sin(yaw) * vx_world + math.cos(yaw) * vy_world
        if abs(v_y) < 0.005:
            v_y = 0.0
        w1 = (1/r) * (v_x - v_y - (L+W)*omega)
        w2 = (1/r) * (v_x + v_y + (L+W)*omega)
        w3 = (1/r) * (v_x + v_y - (L+W)*omega)
        w4 = (1/r) * (v_x - v_y + (L+W)*omega)
        wheels[0].setVelocity(w1)
        wheels[1].setVelocity(w2)
        wheels[2].setVelocity(w3)
        wheels[3].setVelocity(w4)
        # 判斷是否已經非常接近目標且穩定
        if dist < goal_threshold:
            in_range_count += 1
            if in_range_count > 22:  # 連續22個timestep都在範圍內才停
                break
        else:
            in_range_count = 0
        if dist > prev_dist + 0.01 and dist < 0.3:
            print("距離開始增加，強制停車，避免晃動")
            break
        prev_dist = dist
    for w in wheels:
        w.setVelocity(0.0)
    # 靜止等待感測穩定
    for _ in range(20):
        robot.step(timestep)

    # === 2. 強制轉向 face_to 點 ===
    pos = gps.getValues()
    x_now, y_now = pos[0], pos[1]
    yaw = imu.getRollPitchYaw()[2]
    tolerance = 0.4
    steps = 0
    max_steps = 220
    while True:
        if steps > max_steps:
            break
        steps += 1
        ret = robot.step(timestep)
        if ret == -1:
            return
        pos = gps.getValues()
        x_now, y_now = pos[0], pos[1]
        yaw = imu.getRollPitchYaw()[2]
        head_vec = (math.cos(yaw), math.sin(yaw))
        face_vec = (face_to[0] - x_now, face_to[1] - y_now)
        error = angle_between_vectors(head_vec[0], head_vec[1], face_vec[0], face_vec[1])
        if abs(error) < tolerance:
            break
        if abs(error) < min_omega_deg:
            omega = 0.0
        else:
            omega = 1.2 * math.radians(error)
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
    for _ in range(20):
        robot.step(timestep)

def passive_wait(robot, sec):
    start_time = robot.getTime()
    while robot.getTime() - start_time < sec:
        if robot.step(int(robot.getBasicTimeStep())) == -1:
            break

robot = Robot()
timestep = int(robot.getBasicTimeStep())

emitter = robot.getDevice("score_emitter")
sensor = robot.getDevice('sensor')
sensor.enable(timestep)
score = 0
last_score_time = 0

keyboard = Keyboard()
keyboard.enable(timestep)

wheel5 = robot.getDevice("wheel5")
wheel6 = robot.getDevice("wheel6")
wheel7 = robot.getDevice("wheel7")
wheel8 = robot.getDevice("wheel8")
for wheel in [wheel5, wheel6, wheel7, wheel8]:
    wheel.setPosition(float('inf'))
    wheel.setVelocity(0)

def set_wheel_velocity(v1, v2, v3, v4):
    wheel5.setVelocity(v1)
    wheel6.setVelocity(v2)
    wheel7.setVelocity(v3)
    wheel8.setVelocity(v4)

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

gps = robot.getDevice("gps")
imu = robot.getDevice("inertial unit")
gps.enable(timestep)
imu.enable(timestep)
wheel_names = ["wheel5", "wheel6", "wheel7", "wheel8"]
wheels = [robot.getDevice(name) for name in wheel_names]
for w in wheels:
    w.setPosition(float('inf'))

for _ in range(15):
    robot.step(timestep)

print("Use 'E', 'X', 'S', 'D' keys to control the robot.")
print("E: Move forward, X: Move backward, S: Turn left, D: Turn right.")
print("Press 'C' to start circle-around mode, 'Q' to quit.")

CIRCLE_MODE = False

while robot.step(timestep) != -1:
    key = keyboard.getKey()
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
        pos = gps.getValues()
        x0, y0 = pos[0], pos[1]
        radius = 6.23

        # 以當前 xy 為初始圓周點，並計算其角度
        current_angle = math.atan2(y0, x0)
        if current_angle < 0:
            current_angle += 2 * math.pi

        # 產生 12 等分點，逆時針12點
        angles = [((current_angle + (2*math.pi)*i/12) % (2*math.pi)) for i in range(12)]
        waypoints = [(radius * math.cos(a), radius * math.sin(a)) for a in angles]

        # 找最近點作為起點，並將原始起點座標精確作為最後一點
        min_idx = min(range(12), key=lambda i: math.hypot(waypoints[i][0] - x0, waypoints[i][1] - y0))
        ordered_waypoints = waypoints[min_idx:] + waypoints[:min_idx] + [(x0, y0)]

        for idx, (wx, wy) in enumerate(ordered_waypoints):
            print(f"\n=== 準備前往第 {idx+1} 個點: ({wx:.7f}, {wy:.7f}) ===")
            goto_point_and_face_to(robot, gps, imu, wheels, wx, wy, face_to=(0.0, 0.0))
            pos = gps.getValues()
            print(f"已抵達第 {idx+1} 個點: ({pos[0]:.7f}, {pos[1]:.7f})，車頭已指向 (0, 0)")
            passive_wait(robot, 0.22)
        # 最後一點再次強制轉向面對圓心，確保無論位置如何都會轉向
        pos = gps.getValues()
        x_now, y_now = pos[0], pos[1]
        print("\n=== 最後一點再次強制轉向圓心 ===")
        goto_point_and_face_to(robot, gps, imu, wheels, x_now, y_now, face_to=(0.0, 0.0))
        pos = gps.getValues()
        print(f"\n最終定位：({pos[0]:.7f}, {pos[1]:.7f})，車頭已指向 (0, 0)")
        print("\n已完成圍繞半徑6.23公尺圓周12點繞行並回到起點並轉向，任務結束。")
        CIRCLE_MODE = False
        continue
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