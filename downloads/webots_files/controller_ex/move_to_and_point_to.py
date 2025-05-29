from controller import Robot, GPS, InertialUnit
import math

def clamp_angle(angle):
    """將角度包覆到 [-pi, pi] 區間"""
    return (angle + math.pi) % (2 * math.pi) - math.pi

def goto_point(robot, gps, imu, wheels, x_goal, y_goal, speed=0.4, goal_threshold=0.05, K_omega=2.0):
    """
    動態閉環控制讓 youBot 前進到 (x_goal, y_goal)，同時修正heading
    """
    WHEEL_RADIUS = 0.0478
    BOT_L = 0.228
    BOT_W = 0.158
    r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
    timestep = int(robot.getBasicTimeStep())
    while robot.step(timestep) != -1:
        pos = gps.getValues()
        x, y = pos[0], pos[1]
        dx = x_goal - x
        dy = y_goal - y
        dist = math.hypot(dx, dy)
        if dist < goal_threshold:
            break
        yaw = imu.getRollPitchYaw()[2]
        theta_goal = math.atan2(dy, dx)
        heading_error = clamp_angle(theta_goal - yaw)
        omega = K_omega * heading_error
        # 世界座標速度
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

def turn_heading_to_point(robot, imu, wheels, x_now, y_now, x_target, y_target, tolerance=2.0):
    """
    原地旋轉，讓車頭從(x_now, y_now)指向(x_target, y_target)
    """
    WHEEL_RADIUS = 0.0478
    BOT_L = 0.228
    BOT_W = 0.158
    r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
    timestep = int(robot.getBasicTimeStep())
    theta_goal = math.atan2(y_target - y_now, x_target - x_now)
    while robot.step(timestep) != -1:
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
    w.setPosition(float('inf'))  # 無限旋轉模式

# 先讓感測器啟動穩定
for _ in range(10):
    robot.step(timestep)

# 1. 前往 (4,4)
goto_point(robot, gps, imu, wheels, 4.0, 4.0)

# 2. 到達後取得當下位置
pos = gps.getValues()
x_now, y_now = pos[0], pos[1]

# 3. 車頭指向 (0,0)
turn_heading_to_point(robot, imu, wheels, x_now, y_now, 0.0, 0.0)

print("已抵達 (4,4) 並將車頭指向 (0,0)")