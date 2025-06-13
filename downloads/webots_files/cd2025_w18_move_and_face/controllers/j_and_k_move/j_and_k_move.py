from controller import Robot, Keyboard
import math

deg = math.pi / 180

# 常數設定
TIME_STEP = 16
WHEEL_RADIUS = 0.05
L = 0.56
W = 0.34
MAX_VELOCITY = 10.0

# 初始化機器人實體
robot = Robot()

# 初始化鍵盤控制
keyboard = Keyboard()
keyboard.enable(TIME_STEP)

# 初始化 IMU 裝置
imu = robot.getDevice("imu")
imu.enable(TIME_STEP)

# 初始化 GPS 裝置
gps = robot.getDevice("gps")
gps.enable(TIME_STEP)

# 取得四個輪子的馬達裝置
wheel1 = robot.getDevice("wheel1")  # 右前輪
wheel2 = robot.getDevice("wheel2")  # 左前輪
wheel3 = robot.getDevice("wheel3")  # 右後輪
wheel4 = robot.getDevice("wheel4")  # 左後輪

for wheel in [wheel1, wheel2, wheel3, wheel4]:
    wheel.setPosition(float('inf'))
    wheel.setVelocity(0)


def set_wheel_velocity(v1, v2, v3, v4):
    wheel1.setVelocity(v1)
    wheel2.setVelocity(v2)
    wheel3.setVelocity(v3)
    wheel4.setVelocity(v4)


def get_yaw():
    return imu.getRollPitchYaw()[2]


def angle_diff(a, b):
    d = a - b
    while d > math.pi:
        d -= 2 * math.pi
    while d < -math.pi:
        d += 2 * math.pi
    return d


def get_position():
    pos = gps.getValues()
    return (pos[0], pos[1])  # Webots: x, y


def move_sideways_precise(distance, fast_velocity=MAX_VELOCITY, slow_velocity=1.0, tolerance=0.005):
    """
    精確橫向移動指定距離（沿自身側向，右為正，左為負），快慢速切換，非絕對座標
    """
    start_pos = get_position()
    yaw = get_yaw()
    #print("yaw:", yaw)
    # 側向單位向量（右側）
    side_vec = (math.sin(yaw), math.cos(yaw))
    #print("side_vec:", side_vec)
    #print(f"Start sideways move {distance:+.3f}m, yaw={yaw:.3f}rad, side_vec={side_vec}")
    while True:
        robot.step(TIME_STEP)
        now_pos = get_position()
        # 計算自起點到目前位置的向量
        dx = now_pos[0] - start_pos[0]
        dy = now_pos[1] - start_pos[1]
        # 投影到側向軸（即累積橫向位移）
        side_moved = dx * side_vec[0] + dy * side_vec[1]
        remain = distance - side_moved
        print("remain:", remain)
        if abs(remain) < tolerance:
            break
        # 快慢速切換
        threshold = abs(distance) / 10.0
        v = fast_velocity if abs(remain) > threshold else slow_velocity
        direction = 1 if remain >= 0 else -1
        set_wheel_velocity(direction * v, -direction * v, -direction * v, direction * v)
    set_wheel_velocity(0, 0, 0, 0)
    print("Sideways move finished")


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


def rotate_by_angle(target_angle_deg, fast_velocity=MAX_VELOCITY, slow_velocity=1.0, tolerance_deg=0.05):
    start_yaw = get_yaw()
    target_rad = math.radians(target_angle_deg)
    slow_zone = math.radians(5)
    direction = -1 if target_angle_deg > 0 else 1

    set_wheel_velocity(-direction * fast_velocity, direction * fast_velocity,
                       -direction * fast_velocity, direction * fast_velocity)

    while True:
        robot.step(TIME_STEP)
        now_yaw = get_yaw()
        turned = angle_diff(now_yaw, start_yaw)
        remain = abs(target_rad) - abs(turned)
        if remain < slow_zone:
            set_wheel_velocity(-direction * slow_velocity, direction * slow_velocity,
                               -direction * slow_velocity, direction * slow_velocity)
        if remain < math.radians(tolerance_deg):
            break

    set_wheel_velocity(0, 0, 0, 0)
    print(f"Yaw changed by {math.degrees(turned):.5f} degrees")


def move_to_point_and_face_to(target_point, face_to_point, MAX_VELOCITY=10.0, tolerance_pos=0.01):
    fast_velocity = 10.0
    slow_velocity = 1.0
    # --- 1. 先轉向目標點 ---
    now_pos = get_position()
    yaw = get_yaw()
    head_vec = (math.cos(yaw), math.sin(yaw))
    tar_vec = (target_point[0] - now_pos[0], target_point[1] - now_pos[1])
    rotate_angle = angle_between_vectors(head_vec[0], head_vec[1], tar_vec[0], tar_vec[1])
    print(f"第一段應旋轉 {rotate_angle:.3f} 度")
    rotate_by_angle(rotate_angle)

    # --- 2. 前進到目標點 ---
    while True:
        robot.step(TIME_STEP)
        now_pos = get_position()
        dx = target_point[0] - now_pos[0]
        dz = target_point[1] - now_pos[1]
        dist = math.hypot(dx, dz)
        if dist < tolerance_pos:
            break
        v = fast_velocity if dist > 0.2 else slow_velocity
        set_wheel_velocity(v, v, v, v)
    set_wheel_velocity(0, 0, 0, 0)
    now_pos = get_position()

    # --- 3. 轉向 face_to_point ---
    yaw = get_yaw()
    head_vec = (math.cos(yaw), math.sin(yaw))
    face_vec = (face_to_point[0] - now_pos[0], face_to_point[1] - now_pos[1])
    rotate_angle = angle_between_vectors(head_vec[0], head_vec[1], face_vec[0], face_vec[1])
    print(f"第二段應旋轉 {rotate_angle:.3f} 度")
    rotate_by_angle(rotate_angle)


print("Use arrow keys to control youBot.")
print("A: rotate +30 deg, Z: rotate -30 deg, Q: quit.")
print("M: Move to (3, 3) and face to (0, 0)")
print("J: Move sideways +0.5m, K: Move sideways -0.5m")
print("Up: Move forward, Down: Move backward, Left: Turn left, Right: Turn right.")

while robot.step(TIME_STEP) != -1:
    key = keyboard.getKey()
    if key == Keyboard.UP:
        velocity = MAX_VELOCITY
        set_wheel_velocity(velocity, velocity, velocity, velocity)
    elif key == Keyboard.DOWN:
        velocity = -MAX_VELOCITY
        set_wheel_velocity(velocity, velocity, velocity, velocity)
    elif key == Keyboard.RIGHT:
        velocity = MAX_VELOCITY
        set_wheel_velocity(-velocity, velocity, -velocity, velocity)
    elif key == Keyboard.LEFT:
        velocity = MAX_VELOCITY
        set_wheel_velocity(velocity, -velocity, velocity, -velocity)
    elif key == ord('A') or key == ord('a'):
        print("Rotating +30 degrees (clockwise)")
        before_yaw = imu.getRollPitchYaw()[2]
        print(before_yaw)
        rotate_by_angle(30)
        after_yaw = imu.getRollPitchYaw()[2]
        print(after_yaw)
        delta_yaw_deg = (after_yaw - before_yaw) / deg
        print(f"Yaw changed by {delta_yaw_deg:.5f} degrees")
    elif key == ord('Z') or key == ord('z'):
        print("Rotating -30 degrees (counterclockwise)")
        rotate_by_angle(-30)
    elif key == ord('Q') or key == ord('q'):
        print("Exiting...")
        break
    elif key == ord('M') or key == ord('m'):
        print("Moving to (3,3) and facing to (0,0)")
        move_to_point_and_face_to((3.0, 3.0), (0.0, 0.0))
    elif key == ord('J') or key == ord('j'):
        move_sideways_precise(0.5)
    elif key == ord('K') or key == ord('k'):
        move_sideways_precise(-0.5)
    else:
        set_wheel_velocity(0, 0, 0, 0)