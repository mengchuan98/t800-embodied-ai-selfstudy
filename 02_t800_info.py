"""加载 t800.xml 并打印模型基本信息。

演示如何用 mujoco 加载一个 XML 模型文件，并读取：
  - 身体（body）部件数量
  - 关节（joint）数量
  - 电机 / 执行器（actuator）数量
"""

import os

import mujoco

XML_PATH = os.path.join(os.path.dirname(__file__), "t800.xml")

# 加载模型（<include> 的相对路径会基于 XML 文件所在目录解析）
model = mujoco.MjModel.from_xml_path(XML_PATH)

print("已加载模型: t800.xml")
print("-" * 40)

# model.nbody  : 身体部件总数（含 worldbody）
# model.njnt   : 关节总数
# model.nu     : 执行器（电机）数量，即控制向量维度
print(f"身体部件数量 (nbody)   : {model.nbody}")
print(f"关节数量   (njnt)    : {model.njnt}")
print(f"电机数量   (nu)      : {model.nu}")

print("-" * 40)

# 补充：列出各身体、关节、电机的名字，方便核对
print("身体列表:")
for i in range(model.nbody):
    print(f"  [{i}] {model.body(i).name}")

print("\n关节列表:")
for i in range(model.njnt):
    print(f"  [{i}] {model.joint(i).name}")

print("\n电机列表:")
for i in range(model.nu):
    print(f"  [{i}] {model.actuator(i).name}")
