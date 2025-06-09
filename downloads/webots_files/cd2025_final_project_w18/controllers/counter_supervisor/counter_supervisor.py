from controller import Supervisor

SEGMENTS = [
    [1,1,1,1,1,1,0], # 0
    [0,1,1,0,0,0,0], # 1
    [1,1,0,1,1,0,1], # 2
    [1,1,1,1,0,0,1], # 3
    [0,1,1,0,0,1,1], # 4
    [1,0,1,1,0,1,1], # 5
    [1,0,1,1,1,1,1], # 6
    [1,1,1,0,0,0,0], # 7
    [1,1,1,1,1,1,1], # 8
    [1,1,1,1,0,1,1], # 9
]
DIGIT_MATERIALS = [
    ['a3mat', 'b3mat', 'c3mat', 'd3mat', 'e3mat', 'f3mat', 'g3mat'], # 百
    ['a2mat', 'b2mat', 'c2mat', 'd2mat', 'e2mat', 'f2mat', 'g2mat'], # 十
    ['a1mat', 'b1mat', 'c1mat', 'd1mat', 'e1mat', 'f1mat', 'g1mat'], # 個
]
ON_COLOR = [0, 1, 0]
OFF_COLOR = [0.05, 0.05, 0.05]

def set_digit(supervisor, digit_index, value):
    segs = SEGMENTS[value]
    for i, seg_on in enumerate(segs):
        mat_node = supervisor.getFromDef(DIGIT_MATERIALS[digit_index][i])
        if mat_node:
            mat_node.getField('diffuseColor').setSFColor(ON_COLOR if seg_on else OFF_COLOR)
        else:
            print(f"找不到 {DIGIT_MATERIALS[digit_index][i]} 這個DEF")

def set_display(supervisor, value):
    value = max(0, min(999, int(value)))
    h = value // 100
    t = (value // 10) % 10
    u = value % 10
    set_digit(supervisor, 0, h)
    set_digit(supervisor, 1, t)
    set_digit(supervisor, 2, u)

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

score = 0
receiver = supervisor.getDevice("score_receiver")
receiver.enable(timestep)

while supervisor.step(timestep) != -1:
    while receiver.getQueueLength() > 0:
        data = receiver.getString()
        if data.isdigit():
            try:
                received_score = int(data)
                score += received_score
                print(f"收到得分訊息: +{received_score}, 總分: {score}")
            except Exception as e:
                print("訊息格式錯誤:", e)
        receiver.nextPacket()
    set_display(supervisor, score)