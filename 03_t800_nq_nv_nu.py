"""加载 t800.xml 并打印机器人的自由度相关参数。

MuJoCo 中三个关键维度：
  - nq : 广义坐标数量（位形空间维度，即 qpos 的长度）
  - nv : 广义速度数量（速度空间维度，即 qvel 的长度）
  - nu : 执行器 / 电机数量（控制向量维度，即 ctrl 的长度）
"""

import os

import mujoco

XML_PATH = os.path.join(os.path.dirname(__file__), "t800.xml")

# 加载模型（<include> 的相对路径会基于 XML 文件所在目录解析）
model = mujoco.MjModel.from_xml_path(XML_PATH)

print("已加载模型: t800.xml")
print("-" * 40)

print(f"nq (广义坐标数量) : {model.nq}")
print(f"nv (广义速度数量) : {model.nv}")
print(f"nu (电机/执行器数): {model.nu}")

print("-" * 40)
print("说明:")
print("  qpos 长度 = nq，qvel 长度 = nv，ctrl 长度 = nu")
