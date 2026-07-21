"""加载 t800.xml 并打印每个 body 的世界坐标位置 (data.xpos)。"""

import os

import mujoco

XML_PATH = os.path.join(os.path.dirname(__file__), "t800.xml")
model = mujoco.MjModel.from_xml_path(XML_PATH)
data = mujoco.MjData(model)
mujoco.mj_forward(model, data)

SEP = "=" * 70
SEP2 = "-" * 70

print(f"{SEP}")
print(f"  T800 Body xpos  |  文件: {os.path.basename(XML_PATH)}  |  共 {model.nbody} 个 Body")
print(f"{SEP}")
print(f"  {'序号':>4s}  {'Body 名称':<28s}  {'xpos (x, y, z)':>35s}")
print(f"{SEP2}")

for i in range(model.nbody):
    name = model.body(i).name or f"<unnamed_body_{i}>"
    xp = data.xpos[i]
    print(f"  {i:04d}  {name:<28s}  ({xp[0]:.4f}, {xp[1]:.4f}, {xp[2]:.4f})")

print(f"{SEP}")
