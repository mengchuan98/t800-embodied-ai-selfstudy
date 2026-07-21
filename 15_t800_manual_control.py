"""示例 15：手动拖拽滑块控制 T800 关节（最简教学版，直接修改 qpos）。

思路：
  1) 用 tkinter 创建滑条面板，每个滑条对应一个电机/关节
  2) 直接修改 data.qpos[...] 让关节瞬移到目标角度
  3) 固定机器人 base（free joint 的 qpos 保持初始值），防止机器人倒下
  4) 不走 PD、不发 ctrl 力矩，拖动效果最直观稳定
  5) 滑条显示角度为度数 (deg)，内部存为弧度 (rad)
"""

import math
import tkinter as tk
from tkinter import ttk
from pathlib import Path

import mujoco
import mujoco.viewer

XML_PATH = Path(__file__).with_name("t800.xml")


def main():
    model = mujoco.MjModel.from_xml_path(str(XML_PATH))
    data = mujoco.MjData(model)

    qpos0 = data.qpos.copy()

    # ---- 收集所有可控的 actuator -> joint 映射 ----
    act_list = []  # [(aid, jnt_name, qposadr, lo_deg, hi_deg, init_deg), ...]
    for aid in range(model.nu):
        jnt_id = int(model.actuator_trnid[aid, 0])
        if jnt_id < 0 or jnt_id >= model.njnt:
            continue
        jnt_type = int(model.jnt_type[jnt_id])
        if jnt_type not in (mujoco.mjtJoint.mjJNT_HINGE, mujoco.mjtJoint.mjJNT_SLIDE):
            continue

        jnt_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, jnt_id) or f"J{aid:02d}"
        qposadr = int(model.jnt_qposadr[jnt_id])

        if int(model.jnt_limited[jnt_id]):
            lo_deg = math.degrees(float(model.jnt_range[jnt_id, 0]))
            hi_deg = math.degrees(float(model.jnt_range[jnt_id, 1]))
        else:
            lo_deg, hi_deg = -180.0, 180.0

        init_deg = math.degrees(float(data.qpos[qposadr]))
        act_list.append((aid, jnt_name, qposadr, lo_deg, hi_deg, init_deg))

    print(f"可控电机数: {len(act_list)}")

    # ---- tkinter 滑条窗口 ----
    root = tk.Tk()
    root.title("T800 手动关节控制")
    root.geometry("560x760")
    root.resizable(False, True)

    # 标题区
    header = ttk.Frame(root)
    header.pack(fill="x", padx=10, pady=(8, 4))
    ttk.Label(header, text="T800 手动关节控制", font=("Microsoft YaHei", 12, "bold")).pack(side="left")

    # 副标题
    ttk.Label(
        root,
        text="拖动滑条，直接修改各关节 qpos。这个版本是教学演示版，不走 PD，不动力学控制。",
        font=("Microsoft YaHei", 9),
    ).pack(anchor="w", padx=12, pady=(0, 6))

    # 恢复按钮
    def reset_pose():
        for i, (_, _, _, _, _, init_deg) in enumerate(act_list):
            target_vars[i].set(init_deg)

    ttk.Button(root, text="恢复初始姿态", command=reset_pose).pack(anchor="e", padx=12, pady=(0, 6))

    # 滚动区域
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=(0, 0), pady=0)
    scrollbar.pack(side="right", fill="y")

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # 表头
    ttk.Label(scroll_frame, text="[ID]  JOINT", width=22, anchor="w").grid(row=0, column=0, padx=(10, 0), pady=2)
    ttk.Label(scroll_frame, text="目标角度 (deg)", width=10, anchor="w").grid(row=0, column=2, padx=6, pady=2)

    target_vars = []
    for i, (aid, jnt_name, qposadr, lo_deg, hi_deg, init_deg) in enumerate(act_list):
        row = i + 1

        # 左侧标签 [00] J00_HIP_PITCH_L
        ttk.Label(scroll_frame, text=f"[{i:02d}]  {jnt_name}", width=22, anchor="w").grid(
            row=row, column=0, padx=(10, 0), pady=1, sticky="w"
        )

        # 目标角度变量（度数）
        target_var = tk.DoubleVar(value=init_deg)
        target_vars.append(target_var)

        # 滑条（显示值在上方）
        scale = tk.Scale(
            scroll_frame,
            from_=lo_deg, to=hi_deg,
            variable=target_var,
            orient="horizontal",
            length=260,
            showvalue=True,
            resolution=0.1,
            tickinterval=0,
        )
        scale.grid(row=row, column=1, padx=(4, 6), pady=1)

        # 右侧数值显示
        val_label = ttk.Label(scroll_frame, text=f"{init_deg:.1f}", width=8, anchor="w")
        val_label.grid(row=row, column=2, padx=6, pady=1, sticky="w")

        def make_callback(lbl=val_label, var=target_var):
            def cb(*_):
                lbl.config(text=f"{var.get():.1f}")
            return cb

        target_var.trace_add("write", make_callback())

    # ---- mujoco viewer + 仿真循环 ----
    with mujoco.viewer.launch_passive(model, data) as viewer:
        print("已启动 3D 预览。拖动滑条控制关节，关闭窗口结束。")

        def step():
            if not viewer.is_running():
                root.quit()
                return

            # 锁定 base free joint
            data.qpos[:3] = qpos0[:3]
            data.qpos[3:7] = qpos0[3:7]

            # 把滑条角度（deg）转 rad 写进 qpos
            for i, (_, _, qposadr, _, _, _) in enumerate(act_list):
                data.qpos[qposadr] = math.radians(target_vars[i].get())

            # 重新计算正运动学和碰撞等派生量
            mujoco.mj_forward(model, data)
            viewer.sync()

            root.after(10, step)

        root.after(10, step)
        root.mainloop()


if __name__ == "__main__":
    main()
