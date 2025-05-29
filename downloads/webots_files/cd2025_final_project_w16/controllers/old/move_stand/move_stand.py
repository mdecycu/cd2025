from controller import Supervisor, Keyboard

MOVE_STEP = 0.01  # 每次平移 0.01 m

supervisor = Supervisor()
keyboard = Keyboard()
timestep = int(supervisor.getBasicTimeStep())
keyboard.enable(timestep)

stand_node = supervisor.getFromDef('stand')
if stand_node is None:
    print("找不到 DEF 為 'stand' 的 Robot，請檢查 world 檔案！")
    exit(1)

translation_field = stand_node.getField('translation')

print("使用上下左右鍵移動 stand：")
print("↑：x 增加 0.01 m，↓：x 減少 0.01 m")
print("→：y 增加 0.01 m，←：y 減少 0.01 m")

while supervisor.step(timestep) != -1:
    key = keyboard.getKey()
    if key == -1:
        continue

    cur_pos = translation_field.getSFVec3f()
    new_pos = list(cur_pos)

    if key == Keyboard.UP:
        new_pos[0] += MOVE_STEP  # x 增加
    elif key == Keyboard.DOWN:
        new_pos[0] -= MOVE_STEP  # x 減少
    elif key == Keyboard.RIGHT:
        new_pos[1] += MOVE_STEP  # y 增加
    elif key == Keyboard.LEFT:
        new_pos[1] -= MOVE_STEP  # y 減少

    if new_pos != cur_pos:
        translation_field.setSFVec3f(new_pos)
        print(f"stand 新位置: x={new_pos[0]:.3f}, y={new_pos[1]:.3f}, z={new_pos[2]:.3f}")