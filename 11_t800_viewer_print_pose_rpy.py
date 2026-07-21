"""加载 t800.xml 并在 Viewer 仿真过程中，每 100ms 打印机器人的 pos / rpy，共运行 10 秒。"""

from pathlib import Path
import math
import time

import mujoco
import mujoco.viewer


def quat_to_rpy(q):
    """MuJoCo 四元数 [w, x, y, z] → roll, pitch, yaw (弧度)。"""
    w, x, y, z = q[0], q[1], q[2], q[3]
    # roll (绕 X 轴)
    sinr = 2.0 * (w * x + y * z)
    cosr = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr, cosr)
    # pitch (绕 Y 轴)
    sinp = 2.0 * (w * y - z * x)
    pitch = math.asin(max(-1.0, min(1.0, sinp)))
    # yaw (绕 Z 轴)
    siny = 2.0 * (w * z + x * y)
    cosy = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny, cosy)
    return roll, pitch, yaw


def main():
    xml_path = Path(__file__).with_name("t800.xml")
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)

    base_id = model.body("LINK_BASE").id

    DURATION = 10.0
    LOG_INTERVAL = 0.1

    with mujoco.viewer.launch_passive(model, data) as viewer:
        print(f"已加载: {xml_path.name}")
        print(f"基准 body: id={base_id}, name=LINK_BASE")
        print(f"每隔 {int(LOG_INTERVAL * 1000)}ms 打印一次 pos / rpy， 持续 {int(DURATION)}s， 关掉窗口或 Ctrl+C 可结束")
        print(f"     pos(x,y,z): 前后X, 左右Y, 高度Z (单位: m)")
        print(f"     rpy(rad) : roll绕X滚转角, pitch绕Y俯仰角, yaw绕Z偏航角 (单位: rad)\n")

        last_log_time = -LOG_INTERVAL

        while viewer.is_running() and data.time < DURATION:
            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(model.opt.timestep)

            if data.time - last_log_time >= LOG_INTERVAL:
                pos = data.xpos[base_id]
                quat = data.xquat[base_id]
                r, p, y = quat_to_rpy(quat)
                print(f"t={data.time:6.3f}s  "
                      f"pos=({pos[0]: 7.4f}, {pos[1]: 7.4f}, {pos[2]: 7.4f})  "
                      f"rpy(rad)=({r: 7.4f}, {p: 7.4f}, {y: 7.4f})")
                last_log_time = data.time

        print(f"\n仿真结束，共运行 {data.time:.2f}s")


if __name__ == "__main__":
    main()
