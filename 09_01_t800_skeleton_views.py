"""用 matplotlib 绘制 T800 机器人骨架的三视图（正视图/侧视图/俯视图）。"""

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

import mujoco

# ============================================================
# 解决中文乱码问题
# ============================================================
for name in ["SimHei", "Microsoft YaHei", "WenQuanYi Micro Hei", "Noto Sans CJK SC"]:
    for f in fm.fontManager.ttflist:
        if name in f.name:
            plt.rcParams["font.sans-serif"] = [f.name, "DejaVu Sans", "Arial"]
            plt.rcParams["axes.unicode_minus"] = False
            break
    else:
        continue
    break

# ============================================================
# 加载模型并获取 body 坐标
# ============================================================
XML_PATH = os.path.join(os.path.dirname(__file__), "t800.xml")
model = mujoco.MjModel.from_xml_path(XML_PATH)
data = mujoco.MjData(model)
mujoco.mj_forward(model, data)

bodies = []
for i in range(model.nbody):
    name = model.body(i).name or f"unnamed_{i}"
    bodies.append({
        "id": i,
        "name": name,
        "parent": int(model.body_parentid[i]),
        "pos": data.xpos[i].copy(),
    })

edges = []
for b in bodies:
    pid = b["parent"]
    if pid >= 0 and pid != b["id"]:
        edges.append((pid, b["id"]))

all_pos = np.array([b["pos"] for b in bodies])
center = (all_pos.min(axis=0) + all_pos.max(axis=0)) / 2.0
radius = 0.5 * np.max(all_pos.max(axis=0) - all_pos.min(axis=0)) * 1.2

# ============================================================
# 三个 3D 子图（正视图 / 侧视图 / 俯视图视角）
# ============================================================
views = [
    ("正视图 (Front)",  0,   0),
    ("侧视图 (Side)",   0, -90),
    ("俯视图 (Top)",   90,   0),
]

fig = plt.figure(figsize=(18, 6))
fig.suptitle("T800 机器人骨架 — 三视图", fontsize=18, fontweight="bold")

for idx, (title, elev, azim) in enumerate(views):
    ax = fig.add_subplot(1, 3, idx + 1, projection="3d")
    ax.set_title(title, fontsize=13, pad=10)

    for p_id, c_id in edges:
        p = bodies[p_id]["pos"]
        c = bodies[c_id]["pos"]
        ax.plot([p[0], c[0]], [p[1], c[1]], [p[2], c[2]],
                color="steelblue", linewidth=2.5, alpha=0.85)

    ax.scatter(all_pos[:, 0], all_pos[:, 1], all_pos[:, 2],
               c="crimson", s=35, alpha=0.9, edgecolors="white", linewidths=0.5)

    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(center[0] - radius, center[0] + radius)
    ax.set_ylim(center[1] - radius, center[1] + radius)
    ax.set_zlim(center[2] - radius, center[2] + radius)
    ax.view_init(elev=elev, azim=azim)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()
