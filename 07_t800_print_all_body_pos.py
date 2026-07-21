"""加载 t800.xml 并打印每个 body 的世界坐标位置 (data.xpos)。"""

import os

import mujoco

XML_PATH = os.path.join(os.path.dirname(__file__), "t800.xml")
model = mujoco.MjModel.from_xml_path(XML_PATH)
data = mujoco.MjData(model)

# 前向一步，使 data.xpos 等数据有效
mujoco.mj_forward(model, data)

SEP = "=" * 80
SEP2 = "-" * 80

print(f"{SEP}")
print(f"  T800 Body 世界位置  |  文件: {os.path.basename(XML_PATH)}  |  共 {model.nbody} 个 Body")
print(f"{SEP}")
print(f"  {'序号':>4s}  {'Body 名称':<30s}  {'body_pose (x, y, z)':>40s}")
print(f"{SEP2}")

for i in range(model.nbody):
    name = model.body(i).name or f"<unnamed_body_{i}>"
    pos = data.xpos[i]
    pos_str = f"({pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f})"
    print(f"  {i:04d}  {name:<30s}  {pos_str:>40s}")

print(f"{SEP}")
