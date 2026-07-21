"""示例 12：用 PD 控制器让 T800 机器人的每个 actuator 保持到初始 qpos。

思路：
  1) 记录初始 qpos0
  2) 每个仿真步遍历 model.nu 个 actuator：
       - 找到该 actuator 关联的 joint
       - 跳过 FREE / BALL（多自由度），只对 HINGE / SLIDE 做 PD
       - 取出该 joint 的 qposadr / dofadr
       - 计算位置误差 (q_des - q)、速度 qdot
       - 计算原始控制量 u = kp * (q_des - q) - kd * qdot
       - 按 actuator_ctrlrange 限幅后写入 data.ctrl
  3) mj_step 推进物理仿真
"""

import math
import time
from pathlib import Path

import mujoco
import mujoco.viewer


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def main():
    xml_path = Path(__file__).with_name("t800.xml")
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)

    qpos0 = data.qpos.copy()

    kp = 5.0
    kd = 2.0 * math.sqrt(kp)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        print(f"已加载: {xml_path.name}")
        print(f"PD保持初始位置: kp={kp}, kd={kd:.3f}  (基于每个actuator对应的joint)")
        print("关闭窗口或 Ctrl+C 可结束。 ")

        while viewer.is_running():
            for aid in range(model.nu):
                jnt_id = int(model.actuator_trnid[aid, 0])
                if jnt_id < 0 or jnt_id >= model.njnt:
                    continue

                jnt_type = int(model.jnt_type[jnt_id])
                if jnt_type not in (
                    mujoco.mjtJoint.mjJNT_HINGE,
                    mujoco.mjtJoint.mjJNT_SLIDE,
                ):
                    continue

                qposadr = int(model.jnt_qposadr[jnt_id])
                dofadr = int(model.jnt_dofadr[jnt_id])

                q = float(data.qpos[qposadr])
                qd = float(data.qvel[dofadr])
                q_des = float(qpos0[qposadr])

                u = kp * (q_des - q) - kd * qd

                if int(model.actuator_ctrllimited[aid]):
                    lo, hi = float(model.actuator_ctrlrange[aid, 0]), float(model.actuator_ctrlrange[aid, 1])
                    u = clamp(u, lo, hi)

                data.ctrl[aid] = u

            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(model.opt.timestep)


if __name__ == "__main__":
    main()
