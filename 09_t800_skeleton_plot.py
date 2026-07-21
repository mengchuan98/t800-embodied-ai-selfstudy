"""用 matplotlib 3D 绘制 T800 机器人骨架结构（自动从 body_parentid 构建连线）。"""

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

# ============================================================
# 自动从 body_parentid 构建骨架连线
# ============================================================
edges = []
for b in bodies:
    pid = b["parent"]
    # 跳过父为 -1 或 world(body=0) 自身
    if pid >= 0 and pid != b["id"]:
        edges.append((pid, b["id"]))

# ============================================================
# 关键节点中文标注（精简，避免重叠）
# ============================================================
labels = {
    "LINK_BASE":          "躯干",
    "LINK_HIP_PITCH_L":   "左髋",
    "LINK_KNEE_PITCH_L":  "左膝",
    "LINK_FOOT_L":        "左脚",
    "LINK_HIP_PITCH_R":   "右髋",
    "LINK_KNEE_PITCH_R":  "右膝",
    "LINK_FOOT_R":        "右脚",
    "LINK_WAIST_YAW":     "腰",
    "LINK_SHOULDER_PITCH_L": "左肩",
    "LINK_ELBOW_PITCH_L":    "左肘",
    "LINK_WRIST_END_L":      "左腕",
    "LINK_SHOULDER_PITCH_R": "右肩",
    "LINK_ELBOW_PITCH_R":    "右肘",
    "LINK_WRIST_END_R":      "右腕",
    "LINK_HEAD_YAW":         "头",
}

# ============================================================
# Matplotlib 3D 绘图
# ============================================================
fig = plt.figure(figsize=(14, 11))
ax = fig.add_subplot(111, projection="3d")
ax.set_title("T800 机器人骨架结构（初始姿态）", fontsize=16, pad=20)

# 绘制连线
for p_id, c_id in edges:
    p = bodies[p_id]["pos"]
    c = bodies[c_id]["pos"]
    ax.plot([p[0], c[0]], [p[1], c[1]], [p[2], c[2]],
            color="steelblue", linewidth=2.5, alpha=0.85)

# 绘制关节点
all_pos = np.array([b["pos"] for b in bodies])
ax.scatter(all_pos[:, 0], all_pos[:, 1], all_pos[:, 2],
           c="crimson", s=40, alpha=0.9, edgecolors="white", linewidths=0.5)

# 绘制中文标签，加白色背景框避免重叠时看不清
name_to_id = {b["name"]: b["id"] for b in bodies}
for nm, txt in labels.items():
    if nm not in name_to_id:
        continue
    p = bodies[name_to_id[nm]]["pos"]
    ax.text(p[0], p[1], p[2] + 0.05, txt,
            fontsize=9, color="black",
            ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.25",
                      facecolor="white",
                      edgecolor="gray",
                      alpha=0.85))

# 坐标轴
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")

# 等比例坐标
ax.set_box_aspect([1, 1, 1])
limits = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])
center = np.mean(limits, axis=1)
radius = 0.5 * np.max(limits[:, 1] - limits[:, 0])
ax.set_xlim3d([center[0] - radius, center[0] + radius])
ax.set_ylim3d([center[1] - radius, center[1] + radius])
ax.set_zlim3d([center[2] - radius, center[2] + radius])

ax.view_init(elev=20, azim=-60)

plt.tight_layout()
plt.show()
