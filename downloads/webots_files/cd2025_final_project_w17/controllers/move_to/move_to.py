from controller import Supervisor
import math

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

BOT_DEF = 'youBot'
BOT_Z = 0.102838
radius = 4.0  # 圓周半徑

bot = supervisor.getFromDef(BOT_DEF)
assert bot is not None, "找不到 youBot (DEF 必須為 youBot)"

start_x = radius
start_y = 0.0
heading = math.atan2(-start_y, -start_x)  # pi

bot.getField("translation").setSFVec3f([start_x, start_y, BOT_Z])
bot.getField("rotation").setSFRotation([0, 0, 1, heading])

supervisor.step(timestep)
print("[Supervisor] youBot 已移動到 (4, 0), 車頭朝向原點 (0,0)")