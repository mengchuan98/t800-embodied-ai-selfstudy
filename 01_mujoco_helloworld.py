"""MuJoCo 入门示例：木块自由落体。

在重力作用下模拟一个木块从 1 米高处自由下落，
每隔 200 毫秒（仿真时间）打印一次木块中心的高度。
"""

import time

import mujoco

# 仿真参数
INIT_HEIGHT = 1.0        # 木块初始高度（米），即 body 中心初始 z 坐标
PRINT_INTERVAL = 0.2     # 打印间隔：200 毫秒
SIM_DURATION = 5.0       # 总仿真时长（秒）
DT = 0.002               # 仿真步长（秒），即 500 Hz

# ---------------------------------------------------------------------------
# 用 XML 字符串描述场景：
#   - option: 重力沿 -z 方向 9.81 m/s^2
#   - 地面：一个无限大的平面，用于承接落下的木块
#   - 木块：一个 body，pos 设到初始高度，带 freejoint 可自由运动，
#           用一个 box 几何体表示，质量 1 kg
# ---------------------------------------------------------------------------
XML = """
<mujoco>
  <option gravity="0 0 -9.81" timestep="{dt}"/>
  <worldbody>
    <light name="top_light" pos="1 1 4" directional="true"/>
    <geom type="plane" size="10 10 0.1" rgba="0.9 0.9 0.9 1"/>
    <body name="block" pos="0 0 {height}">
      <freejoint/>
      <geom type="box" size="0.1 0.1 0.1" rgba="0.2 0.5 0.9 1" mass="1"/>
    </body>
  </worldbody>
</mujoco>
""".format(dt=DT, height=INIT_HEIGHT)

# 加载模型并创建数据对象
model = mujoco.MjModel.from_xml_string(XML)
data = mujoco.MjData(model)

print(f"开始模拟：木块从 {INIT_HEIGHT:.1f} 米高处自由下落（重力 -9.81 m/s^2）")
print("-" * 48)

next_print = 0.0          # 下一次打印的仿真时刻
wall_start = time.time()  # 用于实时同步（让 1 秒仿真 ≈ 1 秒真实时间）

while data.time < SIM_DURATION:
    mujoco.mj_step(model, data)

    # 实时同步：避免循环跑得过快，使打印在真实时间上也大致间隔 200 毫秒
    elapsed = time.time() - wall_start
    if data.time > elapsed:
        time.sleep(data.time - elapsed)

    if data.time >= next_print:
        height = data.qpos[2]  # freejoint 的 qpos 前 3 个分量即 body 的位置 (x, y, z)
        print(f"t = {data.time:5.3f} s   高度 = {height:9.6f} m")
        next_print += PRINT_INTERVAL

print("-" * 48)
print("模拟结束。")
