from controller import Supervisor, Keyboard
import time
import random
import math
import numpy as np
import re

# 籃框參數
HOOP_CENTER = [5.9, -0.05, 0.742838]
HOOP_RADIUS = 0.2
BALL_RADIUS = 0.1
EFFECTIVE_RADIUS = HOOP_RADIUS - BALL_RADIUS

BALL_DEF_PATTERN = re.compile(r"Sphere_\d+")

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())
keyboard = Keyboard()
keyboard.enable(timestep)

sphere_radius = 0.1
waiting_ball_def = None
waiting_ball_info = None
last_key_time = 0
debounce_time = 0.5
default_feed_pos = (-0.35, 0.0, 0.9)
Z_FLOOR = 0.1  # 判定球落地的高度
tracked_balls = {}

def axis_angle_to_rotation_matrix(axis, angle):
    x, y, z = axis
    c = np.cos(angle)
    s = np.sin(angle)
    C = 1 - c
    return np.array([
        [x*x*C + c,   x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s, y*y*C + c,   y*z*C - x*s],
        [z*x*C - y*s, z*y*C + x*s, z*z*C + c]
    ])

def generate_valid_def_name(base_name="Sphere"):
    timestamp = int(supervisor.getTime() * 1000)
    return f"{base_name}_{timestamp}"

def generate_random_color():
    return random.random(), random.random(), random.random()

def youbot_local_to_world(local_pos):
    youbot_node = supervisor.getFromDef('youbot')
    if youbot_node is None:
        raise RuntimeError("找不到 DEF 為 youbot 的 Robot 物件")
    youbot_translation = np.array(youbot_node.getField('translation').getSFVec3f())
    youbot_rotation = youbot_node.getField('rotation').getSFRotation()
    youbot_axis = youbot_rotation[:3]
    youbot_angle = youbot_rotation[3]
    youbot_rot_mat = axis_angle_to_rotation_matrix(youbot_axis, youbot_angle)
    rotated = youbot_rot_mat @ np.array(local_pos)
    world_pos = youbot_translation + rotated
    return tuple(world_pos)

def create_static_ball(def_name, world_pos, r, g, b):
    sphere_string = f"""
    DEF {def_name} Solid {{
      translation {world_pos[0]} {world_pos[1]} {world_pos[2]}
      contactMaterial "ball"
      children [
        Shape {{
          geometry Sphere {{
            radius {sphere_radius}
          }}
          appearance Appearance {{
            material Material {{
              diffuseColor {r} {g} {b}
            }}
          }}
        }}
      ]
      boundingObject Sphere {{
        radius {sphere_radius}
      }}
    }}
    """
    root = supervisor.getRoot()
    children_field = root.getField("children")
    children_field.importMFNodeFromString(-1, sphere_string)

def create_dynamic_ball(def_name, world_pos, r, g, b):
    sphere_string = f"""
    DEF {def_name} Solid {{
      translation {world_pos[0]} {world_pos[1]} {world_pos[2]}
      contactMaterial "ball"
      children [
        Shape {{
          geometry Sphere {{
            radius {sphere_radius}
          }}
          appearance Appearance {{
            material Material {{
              diffuseColor {r} {g} {b}
            }}
          }}
        }}
      ]
      boundingObject Sphere {{
        radius {sphere_radius}
      }}
      physics Physics {{
        mass 0.01
        density -1
      }}
    }}
    """
    root = supervisor.getRoot()
    children_field = root.getField("children")
    children_field.importMFNodeFromString(-1, sphere_string)

def create_static_sphere(supervisor, x, y, z):
    global waiting_ball_def, waiting_ball_info
    def_name = generate_valid_def_name()
    waiting_ball_def = def_name
    r, g, b = generate_random_color()
    world_pos = youbot_local_to_world((x, y, z))
    waiting_ball_info = (world_pos, r, g, b)
    create_static_ball(def_name, world_pos, r, g, b)

def activate_dynamic_ball():
    global waiting_ball_def, waiting_ball_info
    if waiting_ball_def is None or waiting_ball_info is None:
        return
    # 刪除靜止球
    ball_node = supervisor.getFromDef(waiting_ball_def)
    if ball_node is not None:
        ball_node.remove()
        supervisor.step(int(supervisor.getBasicTimeStep()))
    # 產生 dynamic 球
    world_pos, r, g, b = waiting_ball_info
    create_dynamic_ball(waiting_ball_def, world_pos, r, g, b)
    waiting_ball_def = None
    waiting_ball_info = None

def get_all_ball_defs():
    ball_defs = []
    root = supervisor.getRoot()
    children = root.getField("children")
    for i in range(children.getCount()):
        node = children.getMFNode(i)
        def_name = node.getDef()
        if def_name and BALL_DEF_PATTERN.fullmatch(def_name):
            ball_defs.append(def_name)
    return ball_defs

print("按 A 產生一顆靜止的球（無 Physics），按 M 讓球變 dynamic 可以被擊出")

while supervisor.step(timestep) != -1:
    key = keyboard.getKey()
    current_time = time.time()
    if key == ord('A') and (current_time - last_key_time >= debounce_time):
        if waiting_ball_def is None:
            create_static_sphere(supervisor, *default_feed_pos)
        else:
            print("還有一顆球等待擊出，請先擊出再產生新球。")
        last_key_time = current_time
    if key == ord('M') and (current_time - last_key_time >= debounce_time):
        activate_dynamic_ball()
        last_key_time = current_time

    # 追蹤每顆球於空中時與籃框中心距離
    for ball_def in get_all_ball_defs():
        ball_node = supervisor.getFromDef(ball_def)
        if ball_node is None:
            continue
        pos = ball_node.getPosition()
        # 只追蹤還沒落地的球
        if pos[2] < Z_FLOOR:
            if ball_def in tracked_balls and not tracked_balls[ball_def]["printed"]:
                # 球落地時印出最接近情況
                best = tracked_balls[ball_def]["best"]
                dx, dy, dz = best["dx"], best["dy"], best["dz"]
                dist = best["dist"]
                print(f"球 {ball_def} 落地！投籃最近點與籃框中心的距離: {dist:.3f} m, 差: dx={dx:.3f}, dy={dy:.3f}, dz={dz:.3f}")
                move_x = dx
                move_y = dy
                print(f"建議籃框往 x: {move_x:+.3f}, y: {move_y:+.3f} 方向調整（即將中心移到 x={HOOP_CENTER[0]+move_x:.3f}, y={HOOP_CENTER[1]+move_y:.3f}）")
                if abs(dx) < 0.02 and abs(dy) < 0.02:
                    print("→ 調整後如果同樣出手，下次進球機率會顯著提升！")
                else:
                    print("→ 調整後下次進球機率會提升，但若拋球有隨機誤差則還要多次校正。")
                tracked_balls[ball_def]["printed"] = True
            continue
        # 持續追蹤球
        dx = pos[0] - HOOP_CENTER[0]
        dy = pos[1] - HOOP_CENTER[1]
        dz = pos[2] - HOOP_CENTER[2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if ball_def not in tracked_balls:
            tracked_balls[ball_def] = {"best": {"dx": dx, "dy": dy, "dz": dz, "dist": dist}, "printed": False}
        else:
            # 若目前距離更近，更新最佳紀錄
            if dist < tracked_balls[ball_def]["best"]["dist"]:
                tracked_balls[ball_def]["best"] = {"dx": dx, "dy": dy, "dz": dz, "dist": dist}