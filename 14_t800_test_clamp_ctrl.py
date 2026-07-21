"""示例 14：测试 clamp 函数 —— 输入 10000 的控制值，观察限幅是否生效。

思路：
  1) 遍历每个 actuator，先赋值 data.ctrl[aid] = ±10000
  2) 再用与 12_t800_pd_hold_init_qpos 相同的 clamp 逻辑做限幅
  3) 打印限幅前（输入值）、ctrlrange、限幅后（真实值）
"""

from pathlib import Path

import mujoco

XML_PATH = Path(__file__).with_name("t800.xml")
model = mujoco.MjModel.from_xml_path(str(XML_PATH))
data = mujoco.MjData(model)


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


print(f"电机数量(nu): {model.nu}\n")

# 先用 +10000 测试
test_val = 10000.0

print(f"{'ID':>3s}  {'ACTUATOR':<28s} {'输入值':>12s}  {'CTRL_LO':>12s}  {'CTRL_HI':>12s}  {'真实值':>12s}  {'生效?':>5s}")
print("-" * 105)

for aid in range(model.nu):
    act_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, aid) or f"<unnamed_{aid}>"

    ctrl_lo = float(model.actuator_ctrlrange[aid, 0])
    ctrl_hi = float(model.actuator_ctrlrange[aid, 1])
    limited = bool(int(model.actuator_ctrllimited[aid]))

    # 模拟：输入 10000
    u = test_val
    input_val = u

    # 与 12 号脚本一样的 clamp 逻辑
    if limited:
        u = clamp(u, ctrl_lo, ctrl_hi)

    output_val = u
    clamped = "yes" if output_val != input_val else "no"

    print(f"{aid:3d}  {act_name:<28s} {input_val:>12.1f}  {ctrl_lo:>12.1f}  {ctrl_hi:>12.1f}  {output_val:>12.1f}  {clamped:>5s}")

print()

# 再用 -10000 测试
test_val = -10000.0

print(f"{'ID':>3s}  {'ACTUATOR':<28s} {'输入值':>12s}  {'CTRL_LO':>12s}  {'CTRL_HI':>12s}  {'真实值':>12s}  {'生效?':>5s}")
print("-" * 105)

for aid in range(model.nu):
    act_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, aid) or f"<unnamed_{aid}>"

    ctrl_lo = float(model.actuator_ctrlrange[aid, 0])
    ctrl_hi = float(model.actuator_ctrlrange[aid, 1])
    limited = bool(int(model.actuator_ctrllimited[aid]))

    u = test_val
    input_val = u

    if limited:
        u = clamp(u, ctrl_lo, ctrl_hi)

    output_val = u
    clamped = "yes" if output_val != input_val else "no"

    print(f"{aid:3d}  {act_name:<28s} {input_val:>12.1f}  {ctrl_lo:>12.1f}  {ctrl_hi:>12.1f}  {output_val:>12.1f}  {clamped:>5s}")
