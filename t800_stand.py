from pathlib import Path
import time
import mujoco
import mujoco.viewer

def main():
    xml_path = Path(__file__).with_name("t800.xml")
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    # 关闭重力
    model.opt.gravity[:] = [0, 0, 0]
    data = mujoco.MjData(model)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        print(f"已加载: {xml_path.name}")
        print("重力已关闭，机器人将保持初始姿态不动。")
        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(model.opt.timestep)

if __name__ == "__main__":
    main()