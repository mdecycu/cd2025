from controller import Robot, GPS, InertialUnit
import math

# 建立 Webots 機器人
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# 取得 GPS 與 IMU 裝置
gps = robot.getDevice("gps")
imu = robot.getDevice("inertial unit")
gps.enable(timestep)
imu.enable(timestep)

# 取得四個輪子的裝置並設為無限轉動模式
wheel_names = ["wheel1", "wheel2", "wheel3", "wheel4"]
wheels = [robot.getDevice(name) for name in wheel_names]
for w in wheels:
    w.setPosition(float('inf'))

def clamp_angle(angle):
    """將角度包覆到 [-pi, pi]"""
    return (angle + math.pi) % (2 * math.pi) - math.pi

def goto_point(robot, gps, imu, wheels, x_goal, y_goal):
    """
    讓 youBot 以動態閉環控制自動前往 (x_goal, y_goal)，
    移動時持續修正 heading 與前進方向
    """
    # youBot 參數
    WHEEL_RADIUS = 0.0478
    BOT_L = 0.228
    BOT_W = 0.158
    r, L, W = WHEEL_RADIUS, BOT_L, BOT_W
    speed = 0.4             # 前進速度 (公尺/秒)
    goal_threshold = 0.05   # 到達目標的閾值 (公尺)
    K_omega = 2.0           # heading 誤差的 P 控制增益

    timestep = int(robot.getBasicTimeStep())
    while robot.step(timestep) != -1:
        # 取得目前位置與方位
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

        # heading 誤差用 P 控制器轉成角速度
        omega = K_omega * heading_error

        # 世界座標速度向量（朝向目標點）
        vx_world = dx / (dist + 1e-9) * speed
        vy_world = dy / (dist + 1e-9) * speed

        # 轉成本體座標速度
        v_x = math.cos(yaw) * vx_world + math.sin(yaw) * vy_world
        v_y = -math.sin(yaw) * vx_world + math.cos(yaw) * vy_world

        # 麥克納姆輪逆運動學，計算四輪速度
        w1 = (1/r) * (v_x - v_y - (L+W)*omega)
        w2 = (1/r) * (v_x + v_y + (L+W)*omega)
        w3 = (1/r) * (v_x + v_y - (L+W)*omega)
        w4 = (1/r) * (v_x - v_y + (L+W)*omega)

        # 設定輪速
        wheels[0].setVelocity(w1)
        wheels[1].setVelocity(w2)
        wheels[2].setVelocity(w3)
        wheels[3].setVelocity(w4)

    # 停車
    for w in wheels:
        w.setVelocity(0.0)

# 讓感測器啟動穩定
for _ in range(10):
    robot.step(timestep)

# 執行：自動前往 (1, 1)
goto_point(robot, gps, imu, wheels, -4.0, -5.0)
print("已抵達目標點 (1, 1)")