"""示例 13：遍历 T800 每个关节电机 (actuator)，打印其 ctrl range（扭矩限幅）。"""

from pathlib import Path

import mujoco

XML_PATH = Path(__file__).with_name("t800.xml")
model = mujoco.MjModel.from_xml_path(str(XML_PATH))

print(f"电机数量(nu): {model.nu}\n")

# 表头
print(f"{'ID':>3s}  {'ACTUATOR':<28s} {'JOINT':<24s} {'LIMIT':<5s} {'CTRL_LO':<12s} {'CTRL_HI':<12s}")
print("-" * 95)

for aid in range(model.nu):
    # actuator 名称
    act_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, aid)
    if not act_name:
        act_name = f"<unnamed_{aid}>"

    # 关联的 joint
    jnt_id = int(model.actuator_trnid[aid, 0])
    if 0 <= jnt_id < model.njnt:
        jnt_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, jnt_id) or f"<unnamed_{jnt_id}>"
    else:
        jnt_name = "N/A"

    # ctrl range（扭矩限幅）
    ctrl_lo = float(model.actuator_ctrlrange[aid, 0])
    ctrl_hi = float(model.actuator_ctrlrange[aid, 1])
    limited = "yes" if int(model.actuator_ctrllimited[aid]) else "no"

    print(f"{aid:3d}  {act_name:<28s} {jnt_name:<24s} {limited:<5s} {ctrl_lo:<12.6f} {ctrl_hi:<12.6f}")
