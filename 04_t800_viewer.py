"""加载 t800.xml 并打开 MuJoCo 被动查看器，实时显示机器人模型。"""

from pathlib import Path
import time

import mujoco
import mujoco.viewer


def main():
    xml_path = Path(__file__).with_name("t800.xml")
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    data = mujoco.MjData(model)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        print(f"已加载: {xml_path.name}")
        print("Viewer已打开，按关闭窗口或 Ctrl+C 结束。")

        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(model.opt.timestep)


if __name__ == "__main__":
    main()
