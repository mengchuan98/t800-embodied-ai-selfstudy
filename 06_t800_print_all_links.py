"""加载 t800.xml 并打印所有连杆（body）的名称、质量及几何体尺寸信息。"""

import os

import mujoco

XML_PATH = os.path.join(os.path.dirname(__file__), "t800.xml")
model = mujoco.MjModel.from_xml_path(XML_PATH)

GEOM_TYPE = {
    0: "mjGEOM_PLANE",
    1: "mjGEOM_SPHERE",
    2: "mjGEOM_CAPSULE",
    3: "mjGEOM_ELLIPSOID",
    4: "mjGEOM_CYLINDER",
    5: "mjGEOM_BOX",
    6: "mjGEOM_MESH",
    7: "mjGEOM_HFIELD",
}

SEP = "-" * 130

print(f"XML文件: {os.path.basename(XML_PATH)}")
print(f"连杆(body)数量(不含world): {model.nbody - 1}")
print(f"{'ID':>3s}  {'连杆名称':<24s}  {'质量(kg)':>8s}  尺寸")
print(f"{SEP}")

MAX_GEOM_SHOW = 2  # 最多展示前 2 个 geom，超出显示 "+1 more"

for i in range(1, model.nbody):  # 跳过 world
    name = model.body(i).name or f"<unnamed_body_{i}>"
    mass = model.body_mass[i].item()
    geom_num = int(model.body_geomnum[i])
    geom_adr = int(model.body_geomadr[i])

    if geom_num == 0:
        print(f"{i:>3d}  {name:<24s}  {mass:8.4f}  (无)")
        continue

    parts = []
    for k in range(min(geom_num, MAX_GEOM_SHOW)):
        gidx = geom_adr + k
        gtype = GEOM_TYPE.get(model.geom_type[gidx].item(),
                              f"?{model.geom_type[gidx].item()}")
        gsize = model.geom_size[gidx]
        parts.append(f"{gtype}:({gsize[0]:.3f}, {gsize[1]:.3f}, {gsize[2]:.3f})")

    if geom_num > MAX_GEOM_SHOW:
        parts.append(f"+{geom_num - MAX_GEOM_SHOW} more")

    size_str = "; ".join(parts)
    print(f"{i:>3d}  {name:<24s}  {mass:8.4f}  {size_str}")
