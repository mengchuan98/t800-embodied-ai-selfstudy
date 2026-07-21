"""示例 16：使用 MuJoCo 原生查看器的电机控制滑条操控 T800。

思路：
  1) 加载 T800 模型，启动 MuJoCo 原生被动查看器
  2) 每帧 mj_step 推进物理仿真
  3) 在 MuJoCo 查看器右侧面板中，有电机控制滑条可直接拖动
  4) 不引入任何外部 GUI，纯 MuJoCo 原生控件
"""

import time
from pathlib import Path

import mujoco
import mujoco.viewer

XML_PATH = Path(__file__).with_name("t800.xml")


def main():
    model = mujoco.MjModel.from_xml_path(str(XML_PATH))
    data = mujoco.MjData(model)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        print(f"已加载: {XML_PATH.name}")
        print("MuJoCo 原生查看器已打开。")
        print("提示：右侧面板「Control」标签页可以拖动电机滑条控制关节扭矩。")
        print("关闭窗口或 Ctrl+C 结束。")

        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(model.opt.timestep)


if __name__ == "__main__":
    main()
