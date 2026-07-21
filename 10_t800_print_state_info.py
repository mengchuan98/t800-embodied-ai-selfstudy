"""加载 t800.xml 并打印关键参数：nq / nv / nu 数量，以及 qpos / qvel / ctrl 初始值。"""

import os

import mujoco

XML_PATH = os.path.join(os.path.dirname(__file__), "t800.xml")
model = mujoco.MjModel.from_xml_path(XML_PATH)
data = mujoco.MjData(model)
mujoco.mj_forward(model, data)

SEP = "--------------------------------------------------"

def fmt_array(arr, per_line=10):
    """把数组每 per_line 个换行，方便长数组的查看。"""
    line = "    "
    out = []
    for i, v in enumerate(arr):
        line += f"{v: 9.6f}, "
        if (i + 1) % per_line == 0:
            out.append(line)
            line = "    "
    if line.strip():
        out.append(line)
    return "\n".join(out)

print(f"XML文件: {os.path.basename(XML_PATH)}")
print(SEP)

print(f"nq   数量: {model.nq}")
print(f"nv   数量: {model.nv}")
print(f"nu   数量: {model.nu}")
print(SEP)

print(f"qpos 长度: {model.nq}")
print(f"qpos 初始值: [\n{fmt_array(data.qpos)}\n]")
print(SEP)

print(f"qvel 长度: {model.nv}")
print(f"qvel 初始值: [\n{fmt_array(data.qvel)}\n]")
print(SEP)

print(f"ctrl 长度: {model.nu}")
print(f"ctrl 初始值: [\n{fmt_array(data.ctrl)}\n]")
print(SEP)
