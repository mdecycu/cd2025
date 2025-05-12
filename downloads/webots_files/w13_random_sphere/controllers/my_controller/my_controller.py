# 匯入必要的模組
from controller import Supervisor  # Supervisor 是 Webots 提供的控制器類別，用於監控和控制模擬場景
import random  # 隨機模組，用於生成隨機數
import time  # 時間模組，用於生成唯一時間戳記

# 初始化 Supervisor 物件
supervisor = Supervisor()  # 創建 Supervisor 物件以控制整個模擬
time_step = int(supervisor.getBasicTimeStep())  # 獲取模擬的基本時間步長 (以毫秒為單位)

# 定義 arena 和球生成的參數
arena_size = 5.0  # 定義模擬區域為 5m x 5m 的正方形
sphere_radius = 0.1  # 定義球的半徑為 0.1m
generation_interval = 2.0  # 每次生成球的時間間隔為 2 秒
spheres_per_interval = 10  # 每次生成 10 個球
y_min, y_max = 1.0, 3.0  # 球的初始高度隨機範圍為 1.0m 至 3.0m

# 建立一個列表來追蹤滾動的球
rolling_spheres = []  # 用於儲存生成的球及其生成時間的列表

# 定義一個函數，用於生成球的唯一 DEF 名稱
def generate_valid_def_name(base_name="Sphere"):
    # 使用當前時間戳記（毫秒）與隨機數生成唯一名稱
    timestamp = int(time.time() * 1000)  # 以毫秒為單位獲取當前時間
    random_suffix = random.randint(1000, 9999)  # 生成 1000 至 9999 的隨機數
    return f"{base_name}_{timestamp}_{random_suffix}"  # 返回唯一的 DEF 名稱

# 定義一個函數，用於創建球的節點
def create_sphere(supervisor, position):
    def_name = generate_valid_def_name()  # 獲取唯一的 DEF 名稱
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
              diffuseColor 1 0 0  # 設置球的顏色為紅色
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
    }}
    """
    root = supervisor.getRoot()  # 獲取模擬場景的根節點
    children_field = root.getField("children")  # 獲取根節點的子節點字段
    children_field.importMFNodeFromString(-1, sphere_string)  # 將新創建的球節點加入模擬
    return def_name  # 返回球的 DEF 名稱

# 定義一個函數，用於移除球的節點
def remove_object(node):
    node.remove()  # 調用 Webots 的 remove 方法移除節點

# 主模擬迴圈
last_generation_time = supervisor.getTime()  # 初始化上一輪生成球的時間

while supervisor.step(time_step) != -1:  # 模擬主迴圈，根據時間步長更新
    current_time = supervisor.getTime()  # 獲取當前模擬時間
    
    # 每隔 generation_interval 秒生成一批球
    if current_time - last_generation_time >= generation_interval:
        for _ in range(spheres_per_interval):  # 根據設定的數量生成球
            x = random.uniform(-arena_size / 2, arena_size / 2)  # 隨機生成 x 座標
            z = random.uniform(-arena_size / 2, arena_size / 2)  # 隨機生成 z 座標
            y = random.uniform(y_min, y_max)  # 隨機生成 y 座標
            sphere_def = create_sphere(supervisor, (x, y, z))  # 創建球並獲取其 DEF 名稱
            rolling_spheres.append((sphere_def, current_time))  # 將球的 DEF 名稱與生成時間加入追蹤列表
        last_generation_time = current_time  # 更新上一輪生成球的時間

    # 檢查並移除滾動的球
    root_children = supervisor.getRoot().getField("children")  # 獲取場景的子節點字段
    for sphere_data in rolling_spheres[:]:  # 遍歷滾動球列表（使用副本避免修改列表時出錯）
        sphere_def, creation_time = sphere_data
        node = supervisor.getFromDef(sphere_def)  # 根據 DEF 名稱獲取球的節點
        if not node:  # 如果球的節點已不存在
            rolling_spheres.remove(sphere_data)  # 從追蹤列表中移除
            continue
        
        position = node.getField("translation").getSFVec3f()  # 獲取球的當前位置
        
        # 檢查球是否超出 arena 邊界
        if abs(position[0]) > arena_size / 2 or abs(position[2]) > arena_size / 2:
            # 如果球超出邊界，讓其繼續下落
            continue  # 不對球進行其他操作
        
        # 檢查球是否滾動了 2 秒並移除
        if position[1] <= sphere_radius:  # 如果球觸地
            if current_time - creation_time >= 2.0:  # 如果已經滾動了 2 秒
                rolling_spheres.remove(sphere_data)  # 從追蹤列表中移除
                if random.choice([True, False]):  # 隨機決定是否移除球
                    remove_object(node)  # 移除球的節點