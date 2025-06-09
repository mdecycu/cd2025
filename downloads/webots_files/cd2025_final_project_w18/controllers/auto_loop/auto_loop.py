from controller import Supervisor, Emitter

supervisor = Supervisor()
emitter = supervisor.getDevice('em')
timestep = int(supervisor.getBasicTimeStep())

BALL_TO_SWING_DELAY = 0.5    # a -> m
SWING_TO_RESET_DELAY = 0.5   # m -> k
RESET_TO_NEXTBALL_DELAY = 0.3  # k -> a

state = 0
timer = 0

while supervisor.step(timestep) != -1:
    timer += timestep / 1000
    if state == 0:
        emitter.send("a".encode('utf-8'))  # 傳送 a 字串
        timer = 0
        state = 1
    elif state == 1 and timer >= BALL_TO_SWING_DELAY:
        emitter.send("m".encode('utf-8'))  # 傳送 m 字串
        timer = 0
        state = 2
    elif state == 2 and timer >= SWING_TO_RESET_DELAY:
        emitter.send("k".encode('utf-8'))  # 傳送 k 字串
        timer = 0
        state = 3
    elif state == 3 and timer >= RESET_TO_NEXTBALL_DELAY:
        timer = 0
        state = 0