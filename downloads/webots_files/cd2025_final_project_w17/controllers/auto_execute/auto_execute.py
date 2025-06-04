from controller import Supervisor

# 時間常數 (ms)
BALL_RELEASE_DELAY = 500      # a -> m
LINK_RESET_DELAY = 1000       # m -> k
NEXT_CYCLE_DELAY = 500        # k -> a (下一輪)

# 對應鍵值 (Webots 內部使用 ascii)
KEY_A = ord('A')
KEY_M = ord('M')
KEY_K = ord('K')

state = 0
timer = 0

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

while supervisor.step(timestep) != -1:
    timer += timestep
    if state == 0:
        # 按下 a 鍵產生新球
        supervisor.keyboard.press_key(KEY_A)
        timer = 0
        state = 1
    elif state == 1 and timer > BALL_RELEASE_DELAY:
        # 按下 m 鍵揮動連桿
        supervisor.keyboard.press_key(KEY_M)
        timer = 0
        state = 2
    elif state == 2 and timer > LINK_RESET_DELAY:
        # 按下 k 鍵讓連桿回位
        supervisor.keyboard.press_key(KEY_K)
        timer = 0
        state = 3
    elif state == 3 and timer > NEXT_CYCLE_DELAY:
        # 等待再開始新的一輪
        timer = 0
        state = 0