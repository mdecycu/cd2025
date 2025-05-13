# 匯入必要的模組
from controller import Supervisor, Keyboard  # Supervisor 用於控制模擬環境，Keyboard 用於監聽鍵盤輸入
import time  # 用於實現生成球後的延時
import random  # 用於生成隨機顏色

# 初始化 Supervisor 和 Keyboard 物件
supervisor = Supervisor()
keyboard = Keyboard()
keyboard.enable(int(supervisor.getBasicTimeStep()))  # 啟用鍵盤監聽，根據模擬時間步長設定

# 定義球的參數
sphere_radius = 0.1  # 球的半徑
sphere_position = (-0.62, 1.07, -0.25)  # 球的生成位置

# 定義一個函數，用於生成球的唯一 DEF 名稱
def generate_valid_def_name(base_name="Sphere"):
    timestamp = int(supervisor.getTime() * 1000)  # 使用模擬時間生成唯一名稱
    return f"{base_name}_{timestamp}"

# 定義一個函數，用於生成隨機顏色
def generate_random_color():
    r = random.random()  # 生成隨機紅色分量 (0.0 - 1.0)
    g = random.random()  # 生成隨機綠色分量 (0.0 - 1.0)
    b = random.random()  # 生成隨機藍色分量 (0.0 - 1.0)
    return r, g, b

# 定義一個函數，用於創建球的節點
def create_sphere(supervisor, position):
    def_name = generate_valid_def_name()  # 獲取唯一的 DEF 名稱
    r, g, b = generate_random_color()  # 獲取隨機顏色
    sphere_string = f"""
    DEF {def_name} Solid {{
      translation {position[0]} {position[1]} {position[2]}  # 設置球的初始位置
      children [
        Shape {{
          geometry Sphere {{
            radius {sphere_radius}  # 設置球的半徑
          }}
          appearance Appearance {{
            material Material {{
              diffuseColor {r} {g} {b}  # 隨機設置球的顏色
            }}
          }}
        }}
      ]
      physics Physics {{
        mass 0.1  # 設置球的質量
      }}
      boundingObject Sphere {{
        radius {sphere_radius}  # 設置碰撞邊界為球形
      }}
      contactMaterial "ball"  # 設定 contactMaterial 欄位為 "ball"
    }}
    """
    root = supervisor.getRoot()  # 獲取模擬場景的根節點
    children_field = root.getField("children")  # 獲取根節點的子節點字段
    children_field.importMFNodeFromString(-1, sphere_string)  # 將新創建的球節點加入模擬
    print(f"Sphere created at position {position} with DEF name: {def_name} and color: ({r:.2f}, {g:.2f}, {b:.2f})")

# 主模擬迴圈
last_key_time = 0  # 記錄上次按下鍵的時間
debounce_time = 0.5  # 設定按鍵防抖時間為 0.5 秒

while supervisor.step(int(supervisor.getBasicTimeStep())) != -1:  # 模擬主迴圈
    key = keyboard.getKey()  # 獲取目前按下的鍵
    current_time = time.time()  # 獲取當前時間（實時）

    # 如果按下 'a' 且距離上次按鍵超過防抖時間
    if key == ord('A') and (current_time - last_key_time >= debounce_time):
        create_sphere(supervisor, sphere_position)  # 在指定位置創建球
        last_key_time = current_time  # 更新上次按鍵的時間